"""
AI 브랜드 아이덴티티 생성기 - 웹 백엔드 (Vercel Serverless + Flask)
Codyssey 팀미션 2-2-1 [Project A] 웹 배포 전환

기존 CLI(brand_generator.py)의 로직을 그대로 재사용하되,
파일 저장 대신 base64 인코딩으로 이미지를 응답에 직접 포함한다.
"""

import base64
import json
import os
import time
from io import BytesIO

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from google import genai
from google.genai import types

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

load_dotenv()

app = Flask(__name__)

# 로컬 개발 편의용: public 폴더를 Flask가 직접 서빙한다.
# (Vercel 배포 시에는 vercel.json의 builds/routes가 public/*을 먼저 가로채므로
#  이 라우트는 실제로 호출되지 않는다 - 로컬 테스트 전용)
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "..", "public")

# 프로젝트에 동봉한 한글 폰트 (Vercel Linux 환경에는 한글 폰트가 없으므로 반드시 직접 포함)
FONT_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "NanumGothic-Bold.ttf")


# ---------------------------------------------------------------------------
# 공통 유틸 (CLI에서 그대로 이식)
# ---------------------------------------------------------------------------

def describe_api_error(error: Exception) -> str:
    """Gemini API 에러 메시지를 사용자가 바로 이해할 수 있는 한국어 문구로 변환한다."""
    msg = str(error)
    upper_msg = msg.upper()

    if "RESOURCE_EXHAUSTED" in upper_msg or "429" in msg:
        return f"API 크레딧/할당량 소진 (Google AI Studio에서 결제 정보 또는 일일 무료 한도를 확인하세요) | 상세: {msg[:300]}"
    if "402" in msg or "PAYMENT" in upper_msg or "BILLING" in upper_msg:
        return "API 결제 정보 확인 필요 (Google AI Studio에서 결제 계정 연결 상태를 확인하세요)"
    if "401" in msg or "UNAUTHENTICATED" in upper_msg or "API KEY" in upper_msg or "API_KEY_INVALID" in upper_msg:
        return "API 키 인증 실패 (서버 환경변수 GEMINI_API_KEY 값을 확인하세요)"
    if "UNAVAILABLE" in upper_msg or "503" in msg:
        return "API 서버 일시적 과부하 (잠시 후 다시 시도하세요)"

    return f"알 수 없는 오류 ({msg[:120]})"


def validate_brief(brief: dict) -> str | None:
    """브리프 JSON 필수 필드를 검증한다. 문제가 있으면 에러 메시지를, 없으면 None을 반환한다."""
    if not isinstance(brief, dict):
        return "브리프 형식이 올바르지 않습니다."

    required_fields = ["industry", "target", "keywords"]
    missing = [field for field in required_fields if not brief.get(field)]
    if missing:
        return f"필수 항목이 누락되었습니다 -> {', '.join(missing)}"

    if not isinstance(brief.get("keywords"), list) or len(brief["keywords"]) == 0:
        return "keywords는 최소 1개 이상 포함된 배열이어야 합니다."

    brief.setdefault("tone", "")
    brief.setdefault("competitors", [])
    brief.setdefault("notes", "")
    return None


def compose_logo_with_wordmark(icon_image, brand_name: str, main_color: str = ""):
    """AI가 생성한 아이콘 아래에 실제 폰트로 브랜드명을 렌더링하여 합성한다."""
    from PIL import Image, ImageDraw, ImageFont

    icon_size = icon_image.width
    text_area_height = int(icon_size * 0.22)
    canvas = Image.new("RGB", (icon_size, icon_size + text_area_height), "white")
    canvas.paste(icon_image.convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(canvas)

    font_size = int(text_area_height * 0.42)
    font_candidates = [
        FONT_PATH,                        # 프로젝트 동봉 폰트 (Vercel 배포 환경 - 최우선)
        "C:/Windows/Fonts/malgun.ttf",     # Windows 로컬 실행 시
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS 로컬 실행 시
    ]
    font = None
    for path in font_candidates:
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    text_color = main_color if main_color else "#222222"
    bbox = draw.textbbox((0, 0), brand_name, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (icon_size - text_w) / 2
    y = icon_size + (text_area_height - text_h) / 2 - bbox[1]

    try:
        draw.text((x, y), brand_name, fill=text_color, font=font)
    except Exception:
        pass

    return canvas


def is_rate_limit_error(error: Exception) -> bool:
    """RESOURCE_EXHAUSTED(429) - 분당 요청 한도 초과 여부를 판별한다.
    (일일 할당량 완전 소진이 아니라 '잠시 후 재시도하면 풀리는' 종류의 오류인지 확인용)"""
    msg = str(error)
    return "RESOURCE_EXHAUSTED" in msg.upper() or "429" in msg


def call_gemini_json(client: "genai.Client", prompt: str, model: str = "gemini-3.5-flash-lite", max_retries: int = 2) -> dict | None:
    """Gemini API를 호출해 JSON 형식 응답을 받아 파싱한다.
    무료 티어의 분당 요청 한도(429)에 걸리면 10초 대기 후 1회만 재시도한다."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            return json.loads(response.text)
        except Exception as e:
            if is_rate_limit_error(e) and attempt < max_retries - 1:
                print(f"   [대기] 분당 요청 한도 초과 - 10초 후 재시도 ({attempt + 1}/{max_retries})")
                time.sleep(10)
                continue
            print(f"   [API 오류] {describe_api_error(e)}")
            return None
    return None


# ---------------------------------------------------------------------------
# 생성 로직 (CLI에서 그대로 이식 - client, brief만 받는 순수 함수)
# ---------------------------------------------------------------------------

def generate_naming(client, brief: dict) -> list:
    prompt = f"""당신은 전문 브랜드 네이밍 컨설턴트입니다.
아래 브리프를 참고하여 브랜드명 후보 3~5개를 제안하세요.
각 후보는 한글 브랜드명과 그에 대응하는 영문 브랜드명을 함께 제시하세요.

업종: {brief['industry']}
타겟: {brief['target']}
키워드: {', '.join(brief['keywords'])}
톤앤매너: {brief['tone']}
경쟁사: {', '.join(brief['competitors'])}
추가 요청사항: {brief['notes']}

다음 JSON 형식으로만 응답하세요. 다른 설명 텍스트는 포함하지 마세요.
{{
  "names": [
    {{"name": "한글 브랜드명", "name_en": "English Brand Name", "meaning": "의미/유래 설명 (1~2문장)"}}
  ]
}}"""
    result = call_gemini_json(client, prompt)
    if not result or "names" not in result:
        return []
    return result["names"]


def generate_slogans(client, brief: dict) -> list:
    prompt = f"""당신은 전문 카피라이터입니다.
아래 브리프를 참고하여 브랜드 슬로건(태그라인) 3개를 한국어로 제안하세요.
브랜드의 톤앤매너에 맞는 짧고 임팩트 있는 문구여야 합니다.

업종: {brief['industry']}
타겟: {brief['target']}
키워드: {', '.join(brief['keywords'])}
톤앤매너: {brief['tone']}

다음 JSON 형식으로만 응답하세요. 다른 설명 텍스트는 포함하지 마세요.
{{
  "slogans": ["슬로건1", "슬로건2", "슬로건3"]
}}"""
    result = call_gemini_json(client, prompt)
    if not result or "slogans" not in result:
        return []
    return result["slogans"]


def generate_story(client, brief: dict) -> str:
    prompt = f"""당신은 전문 브랜드 스토리텔러입니다.
아래 브리프를 참고하여 브랜드 스토리를 한국어로 작성하세요.
브랜드의 탄생 배경, 철학, 비전을 포함하고, 전체 길이는 300자 내외로 작성하세요.

업종: {brief['industry']}
타겟: {brief['target']}
키워드: {', '.join(brief['keywords'])}
톤앤매너: {brief['tone']}
추가 요청사항: {brief['notes']}

다음 JSON 형식으로만 응답하세요. 다른 설명 텍스트는 포함하지 마세요.
{{
  "story": "브랜드 스토리 본문"
}}"""
    result = call_gemini_json(client, prompt)
    if not result or "story" not in result:
        return ""
    return result["story"]


def generate_color_palette(client, brief: dict) -> dict:
    prompt = f"""당신은 전문 브랜드 컬러 컨설턴트입니다.
아래 브리프를 참고하여 브랜드에 어울리는 컬러 팔레트를 추천하세요.
메인 컬러 1개와 서브 컬러 2~3개를 HEX 코드(#RRGGBB 형식)로 제안하세요.

업종: {brief['industry']}
타겟: {brief['target']}
키워드: {', '.join(brief['keywords'])}
톤앤매너: {brief['tone']}

다음 JSON 형식으로만 응답하세요. 다른 설명 텍스트는 포함하지 마세요.
{{
  "main": "#RRGGBB",
  "subs": ["#RRGGBB", "#RRGGBB"]
}}"""
    result = call_gemini_json(client, prompt)
    if not result or "main" not in result:
        return {}
    return {
        "main": result.get("main", ""),
        "subs": result.get("subs", []),
    }


def generate_logo_concept(client, brief: dict) -> str:
    prompt = f"""당신은 전문 로고 디자이너입니다.
아래 브랜드에 어울리는 심볼/아이콘 로고 컨셉을 영어로 딱 한 문장 설명하세요.
반드시 구체적인 시각 요소 1~2개를 명시하세요 (예: a single leaf, a water droplet merging with a spiral, an upward arrow inside a circle).
글자나 문자, 도장, 인장 느낌의 표현은 절대 언급하지 마세요. 순수한 기하학적/자연 모티프만 사용하세요.

업종: {brief['industry']}
키워드: {', '.join(brief['keywords'])}
톤앤매너: {brief['tone']}

다음 JSON 형식으로만 응답하세요.
{{
  "concept": "영어 한 문장 (예: A single minimalist leaf shape curving into a droplet)"
}}"""
    result = call_gemini_json(client, prompt)
    if not result or "concept" not in result:
        return ""
    return result["concept"]


def generate_competitor_analysis(client, brief: dict) -> list:
    competitors = brief.get("competitors", [])
    if not competitors:
        return []

    prompt = f"""당신은 전문 브랜드 전략 컨설턴트입니다.
아래 브랜드가 경쟁사 대비 어떻게 차별화될 수 있을지 분석하세요.

업종: {brief['industry']}
타겟: {brief['target']}
키워드: {', '.join(brief['keywords'])}
톤앤매너: {brief['tone']}
경쟁사: {', '.join(competitors)}

각 경쟁사의 특징을 간략히 고려하여, 이 브랜드만의 차별화 포인트 3개를 한국어로 제안하세요.

다음 JSON 형식으로만 응답하세요. 다른 설명 텍스트는 포함하지 마세요.
{{
  "differentiators": ["차별화 포인트1", "차별화 포인트2", "차별화 포인트3"]
}}"""
    result = call_gemini_json(client, prompt)
    if not result or "differentiators" not in result:
        return []
    return result["differentiators"]


# ---------------------------------------------------------------------------
# 이미지 생성 (CLI와 차이점: 파일 저장 대신 base64 문자열 반환)
# ---------------------------------------------------------------------------

def build_color_palette_base64(colors: dict) -> str | None:
    """컬러 팔레트를 matplotlib으로 시각화하여 base64 PNG 문자열로 반환한다."""
    main_color = colors.get("main")
    sub_colors = colors.get("subs", [])
    if not main_color:
        return None

    all_colors = [main_color] + sub_colors
    fig, ax = plt.subplots(figsize=(2.2 * len(all_colors), 3))

    for i, hex_code in enumerate(all_colors):
        ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=hex_code, edgecolor="#333333"))
        label = "MAIN" if i == 0 else f"SUB {i}"
        ax.text(i + 0.5, 1.08, label, ha="center", va="bottom", fontsize=10, fontweight="bold")
        ax.text(i + 0.5, -0.12, hex_code, ha="center", va="top", fontsize=10)

    ax.set_xlim(0, len(all_colors))
    ax.set_ylim(-0.3, 1.3)
    ax.axis("off")

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def build_logo_images_base64(client, brief: dict, names: list, colors: dict, count: int = 3) -> list:
    """Gemini 이미지 생성 API(gemini-2.5-flash-image, Nano Banana)로 로고 시안을 base64 PNG로 반환한다."""
    from PIL import Image

    brand_name = names[0]["name"] if names else brief["industry"]
    main_color = colors.get("main", "") if colors else ""

    concept = generate_logo_concept(client, brief)
    if not concept:
        concept = f"A single simple abstract geometric shape inspired by {brief['keywords'][0]}"

    color_phrase = f"solid flat {main_color} color fill" if main_color else "solid flat single color fill"
    prompt = (
        f"{concept}. Minimalist flat vector app-icon illustration, {color_phrase}, "
        "thick clean outlines, one simple shape only, centered, plenty of white space "
        "around it, isolated on a plain white background, modern tech startup icon style."
    )

    logos_base64 = []
    for i in range(1, count + 1):
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=prompt,
                    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
                )
                icon_image = None
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        icon_image = Image.open(BytesIO(part.inline_data.data))
                        break

                if icon_image is None:
                    print(f"   [경고] 로고 시안 {i}: 응답에 이미지 데이터가 없습니다.")
                    break

                final_image = compose_logo_with_wordmark(icon_image, brand_name, main_color)
                out_buf = BytesIO()
                final_image.save(out_buf, format="PNG")
                out_buf.seek(0)
                logos_base64.append(base64.b64encode(out_buf.read()).decode("utf-8"))
                break
            except Exception as e:
                if is_rate_limit_error(e) and attempt < 1:
                    print(f"   [대기] 로고 시안 {i}: 분당 요청 한도 초과 - 10초 후 재시도")
                    time.sleep(10)
                    continue
                print(f"   [오류] 로고 시안 {i} 생성 실패: {describe_api_error(e)}")
                break

        if i < count:
            time.sleep(3)

    return logos_base64


# ---------------------------------------------------------------------------
# Markdown 리포트 (개인 추가 기능 - 다운로드용 텍스트로 유지)
# ---------------------------------------------------------------------------

def build_markdown_report(brand_data: dict) -> str:
    brief = brand_data.get("brief", {})
    names = brand_data.get("names", [])
    slogans = brand_data.get("slogans", [])
    story = brand_data.get("story", "")
    colors = brand_data.get("colors", {})
    differentiators = brand_data.get("competitor_differentiators", [])

    lines = []
    lines.append("# 🎨 브랜드 아이덴티티 리포트")
    lines.append("")
    lines.append(f"- **업종**: {brief.get('industry', '-')}")
    lines.append(f"- **타겟**: {brief.get('target', '-')}")
    lines.append(f"- **키워드**: {', '.join(brief.get('keywords', []))}")
    if brief.get("tone"):
        lines.append(f"- **톤앤매너**: {brief['tone']}")
    if brief.get("competitors"):
        lines.append(f"- **경쟁사**: {', '.join(brief['competitors'])}")
    if brief.get("notes"):
        lines.append(f"- **추가 요청사항**: {brief['notes']}")
    lines.append("")

    lines.append("## 브랜드 네이밍")
    lines.append("")
    if names:
        for item in names:
            name_kr = item.get("name", "?")
            name_en = item.get("name_en", "")
            suffix = f" ({name_en})" if name_en else ""
            lines.append(f"- **{name_kr}{suffix}**: {item.get('meaning', '')}")
    else:
        lines.append("_생성된 네이밍이 없습니다._")
    lines.append("")

    lines.append("## 슬로건")
    lines.append("")
    if slogans:
        for s in slogans:
            lines.append(f'- "{s}"')
    else:
        lines.append("_생성된 슬로건이 없습니다._")
    lines.append("")

    lines.append("## 브랜드 스토리")
    lines.append("")
    lines.append(story if story else "_생성된 스토리가 없습니다._")
    lines.append("")

    lines.append("## 컬러 팔레트")
    lines.append("")
    if colors and colors.get("main"):
        lines.append(f"- **메인**: `{colors['main']}`")
        if colors.get("subs"):
            subs_str = ", ".join(f"`{c}`" for c in colors["subs"])
            lines.append(f"- **서브**: {subs_str}")
    else:
        lines.append("_생성된 컬러 팔레트가 없습니다._")
    lines.append("")

    if brief.get("competitors"):
        lines.append("## 경쟁사 차별화 포인트 (보너스)")
        lines.append("")
        if differentiators:
            for d in differentiators:
                lines.append(f"- {d}")
        else:
            lines.append("_분석에 실패했거나 아직 생성되지 않았습니다._")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Flask 라우트
# ---------------------------------------------------------------------------

@app.route("/")
def serve_index():
    """로컬 개발 서버 전용: public/index.html 서빙"""
    return send_from_directory(PUBLIC_DIR, "index.html")


@app.route("/<path:filename>")
def serve_public(filename):
    """로컬 개발 서버 전용: public/style.css, public/script.js 등 정적 파일 서빙"""
    return send_from_directory(PUBLIC_DIR, filename)


@app.route("/api/health", methods=["GET"])
def health():
    """배포 확인용 헬스체크 (API 키 존재 여부까지 확인)"""
    has_key = bool(os.environ.get("GEMINI_API_KEY"))
    return jsonify({"status": "ok", "gemini_key_loaded": has_key})


@app.route("/api/generate", methods=["POST"])
def generate():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({
            "error": "GEMINI_API_KEY가 서버에 설정되지 않았습니다. Vercel 프로젝트 환경변수를 확인하세요."
        }), 500

    brief = request.get_json(silent=True)
    error_msg = validate_brief(brief)
    if error_msg:
        return jsonify({"error": error_msg}), 400

    client = genai.Client(api_key=api_key)

    names = generate_naming(client, brief)
    time.sleep(3)
    slogans = generate_slogans(client, brief)
    time.sleep(3)
    story = generate_story(client, brief)
    time.sleep(3)
    colors = generate_color_palette(client, brief)

    palette_image_base64 = None
    if colors and colors.get("main"):
        palette_image_base64 = build_color_palette_base64(colors)

    time.sleep(3)
    logos_base64 = build_logo_images_base64(client, brief, names, colors, count=3)

    time.sleep(3)
    differentiators = generate_competitor_analysis(client, brief)

    brand_data = {
        "brief": brief,
        "names": names,
        "slogans": slogans,
        "story": story,
        "colors": colors,
        "competitor_differentiators": differentiators,
    }
    markdown_report = build_markdown_report(brand_data)

    return jsonify({
        "names": names,
        "slogans": slogans,
        "story": story,
        "colors": colors,
        "palette_image_base64": palette_image_base64,
        "logos_base64": logos_base64,
        "competitor_differentiators": differentiators,
        "markdown_report": markdown_report,
    })


# 로컬 개발 서버 실행용 (Vercel 배포 시에는 사용되지 않음)
if __name__ == "__main__":
    app.run(debug=True, port=5000)