"""
AI 브랜드 아이덴티티 생성기
Codyssey 팀미션 2-2-1 [Project A]
"""

import json
import os
import sys
from io import BytesIO

from dotenv import load_dotenv
from google import genai
from google.genai import types

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def print_banner():
    print()
    print("=" * 50)
    print("   🎨 AI 브랜드 아이덴티티 생성기")
    print("=" * 50)
    print()


def load_brief(brief_path: str) -> dict:
    """브리프 JSON 파일을 읽고 필수 필드를 검증한다."""
    if not os.path.exists(brief_path):
        print(f"❌ 오류: 브리프 파일을 찾을 수 없습니다 -> {brief_path}")
        sys.exit(1)

    try:
        with open(brief_path, "r", encoding="utf-8") as f:
            brief = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ 오류: JSON 형식이 올바르지 않습니다 -> {e}")
        sys.exit(1)

    required_fields = ["industry", "target", "keywords"]
    missing = [field for field in required_fields if field not in brief]
    if missing:
        print(f"❌ 오류: 필수 필드가 누락되었습니다 -> {missing}")
        sys.exit(1)

    # 선택 필드는 없으면 빈 값으로 채워둔다.
    brief.setdefault("tone", "")
    brief.setdefault("competitors", [])
    brief.setdefault("notes", "")

    return brief


def prepare_output_folder(output_path: str) -> str:
    """출력 폴더가 없으면 생성한다."""
    os.makedirs(output_path, exist_ok=True)
    return output_path


def check_api_key():
    """환경 변수에서 API 키를 로드하고 없으면 명확히 안내 후 종료한다."""
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ 오류: GEMINI_API_KEY가 설정되지 않았습니다.")
        print("   -> 프로젝트 루트에 .env 파일을 만들고 아래처럼 입력하세요:")
        print("      GEMINI_API_KEY=발급받은_키")
        sys.exit(1)
    return api_key


def describe_api_error(error: Exception) -> str:
    """Gemini API 에러 메시지를 사용자가 바로 이해할 수 있는 한국어 문구로 변환한다.
    (텍스트 생성/이미지 생성 API 호출 모두에서 공통으로 사용한다.)"""
    msg = str(error)
    upper_msg = msg.upper()

    if "RESOURCE_EXHAUSTED" in upper_msg or "429" in msg:
        return "API 크레딧/할당량 소진 (Google AI Studio에서 결제 정보 또는 일일 무료 한도를 확인하세요)"
    if "402" in msg or "PAYMENT" in upper_msg or "BILLING" in upper_msg:
        return "API 결제 정보 확인 필요 (Google AI Studio에서 결제 계정 연결 상태를 확인하세요)"
    if "401" in msg or "UNAUTHENTICATED" in upper_msg or "API KEY" in upper_msg or "API_KEY_INVALID" in upper_msg:
        return "API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)"
    if "UNAVAILABLE" in upper_msg or "503" in msg:
        return "API 서버 일시적 과부하 (잠시 후 다시 시도하세요)"

    return f"알 수 없는 오류 ({msg[:120]})"


def compose_logo_with_wordmark(icon_image, brand_name: str, main_color: str = ""):
    """AI가 생성한 아이콘 아래에 실제 폰트로 브랜드명을 렌더링하여 합성한다.
    (AI는 이미지 안의 글자를 정확히 그리지 못하므로, 텍스트는 실제 폰트로 별도 렌더링한다.)"""
    from PIL import Image, ImageDraw, ImageFont

    icon_size = icon_image.width
    text_area_height = int(icon_size * 0.22)
    canvas = Image.new("RGB", (icon_size, icon_size + text_area_height), "white")
    canvas.paste(icon_image.convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(canvas)

    font_size = int(text_area_height * 0.42)
    font_candidates = [
        "C:/Windows/Fonts/malgun.ttf",   # Windows 맑은 고딕 (한글 지원)
        "malgun.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Linux (Noto Sans CJK)
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
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
        pass  # 색상 코드가 유효하지 않은 등 극히 예외적인 경우, 텍스트 없이 아이콘만 남긴다.

    return canvas


def call_gemini_json(client: "genai.Client", prompt: str, model: str = "gemini-3.6-flash") -> dict | None:
    """Gemini API를 호출해 JSON 형식 응답을 받아 파싱한다. 실패 시 None을 반환하고 에러를 출력한다."""
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return json.loads(response.text)
    except Exception as e:
        reason = describe_api_error(e)
        print(f"   ❌ API 호출 실패: {reason}")
        return None


def generate_naming(client: "genai.Client", brief: dict) -> list:
    """브랜드 네이밍 후보 3~5개를 한글명+영문명+의미와 함께 생성한다. (보너스: 다국어 네이밍 지원)"""
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


def generate_slogans(client: "genai.Client", brief: dict) -> list:
    """슬로건/태그라인 3개를 생성한다."""
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


def generate_story(client: "genai.Client", brief: dict) -> str:
    """브랜드 스토리(300자 내외)를 생성한다."""
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


def generate_color_palette(client: "genai.Client", brief: dict) -> dict:
    """브랜드에 어울리는 메인 컬러 1개, 서브 컬러 2~3개를 HEX 코드로 추천받는다."""
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


def generate_logo_concept(client: "genai.Client", brief: dict) -> str:
    """이미지 생성 AI에게 전달할 구체적인 로고 심볼 컨셉을 영어 한 문장으로 뽑아낸다.
    (이미지 생성 모델은 부정문 지시("텍스트 넣지 마세요")를 잘 못 알아듣기 때문에,
    처음부터 구체적인 시각 요소를 긍정문으로 지정해주는 것이 훨씬 효과적이다.)"""
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


def save_color_palette_image(colors: dict, output_path: str) -> str | None:
    """컬러 팔레트를 matplotlib으로 시각화하여 PNG로 저장한다."""
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

    palette_path = os.path.join(output_path, "color_palette.png")
    plt.savefig(palette_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return palette_path


def generate_logo_images(
    client: "genai.Client",
    brief: dict,
    names: list,
    colors: dict,
    output_path: str,
    count: int = 3,
) -> list:
    """Gemini 이미지 생성 API(gemini-2.5-flash-image, Nano Banana)로 로고 시안을 PNG로 저장한다."""
    from PIL import Image

    brand_name = names[0]["name"] if names else brief["industry"]
    main_color = colors.get("main", "") if colors else ""

    concept = generate_logo_concept(client, brief)
    if not concept:
        # 컨셉 생성 실패 시 대체용 기본 컨셉 (여전히 텍스트 없는 긍정문 형태 유지)
        concept = f"A single simple abstract geometric shape inspired by {brief['keywords'][0]}"

    color_phrase = f"solid flat {main_color} color fill" if main_color else "solid flat single color fill"
    prompt = (
        f"{concept}. Minimalist flat vector app-icon illustration, {color_phrase}, "
        "thick clean outlines, one simple shape only, centered, plenty of white space "
        "around it, isolated on a plain white background, modern tech startup icon style."
    )

    saved_paths = []
    for i in range(1, count + 1):
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
                print(f"   ⚠️  로고 시안 {i}: 응답에 이미지 데이터가 없습니다.")
                continue

            final_image = compose_logo_with_wordmark(icon_image, brand_name, main_color)
            img_path = os.path.join(output_path, f"logo_{i:02d}.png")
            final_image.save(img_path)
            saved_paths.append(img_path)
        except Exception as e:
            reason = describe_api_error(e)
            print(f"   ❌ 로고 시안 {i} 생성 실패: {reason}")

    return saved_paths


def generate_competitor_analysis(client: "genai.Client", brief: dict) -> list:
    """입력된 경쟁사 브랜드를 분석하여 차별화 포인트를 제안한다. (보너스: 경쟁사 분석)"""
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


def generate_markdown_report(brand_data: dict, output_path: str) -> str:
    """brand_result.json과 동일한 내용을 사람이 읽기 좋은 Markdown 파일로 저장한다. (개인 추가 기능)"""
    brief = brand_data.get("brief", {})
    names = brand_data.get("names", [])
    slogans = brand_data.get("slogans", [])
    story = brand_data.get("story", "")
    colors = brand_data.get("colors", {})
    logos = brand_data.get("logos", [])
    differentiators = brand_data.get("competitor_differentiators", [])

    lines = []
    lines.append(f"# 🎨 브랜드 아이덴티티 리포트")
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
        lines.append("")
        lines.append("![컬러 팔레트](./color_palette.png)")
    else:
        lines.append("_생성된 컬러 팔레트가 없습니다._")
    lines.append("")

    lines.append("## 로고 시안")
    lines.append("")
    if logos:
        for logo_path in logos:
            logo_filename = os.path.basename(logo_path)
            lines.append(f"![로고]({logo_filename})")
    else:
        lines.append("_생성된 로고 시안이 없습니다._")
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

    md_content = "\n".join(lines)
    md_path = os.path.join(output_path, "brand_result.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return md_path


def main():
    print_banner()

    # 0. API 키 확인 (없으면 여기서 종료)
    api_key = check_api_key()
    print("✅ API 키 로드 완료 (앞 4자리: " + api_key[:4] + "****)")
    print()

    # 1. 브리프 파일 경로 입력 (필수)
    brief_path = input("브리프 파일 경로를 입력하세요: ").strip()
    if not brief_path:
        print("❌ 오류: 브리프 파일 경로는 필수입니다.")
        sys.exit(1)

    # 2. 출력 폴더 경로 입력 (선택, 기본값 ./output)
    output_input = input("출력 폴더 경로를 입력하세요 (엔터 시 ./output): ").strip()
    output_path = output_input if output_input else "./output"

    # 3. 브리프 로드 및 검증
    brief = load_brief(brief_path)
    output_path = prepare_output_folder(output_path)

    print()
    print("✅ 브리프 로드 완료")
    print(f"   - 업종: {brief['industry']}")
    print(f"   - 타겟: {brief['target']}")
    print(f"   - 키워드: {', '.join(brief['keywords'])}")
    print(f"   - 출력 폴더: {output_path}")
    print()

    client = genai.Client(api_key=api_key)

    # 4. 브랜드 네이밍 생성
    print("[1/5] 브랜드 네이밍 생성 중...")
    names = generate_naming(client, brief)
    if names:
        for item in names:
            name_kr = item.get("name", "?")
            name_en = item.get("name_en", "")
            suffix = f" ({name_en})" if name_en else ""
            print(f"  - {name_kr}{suffix}: {item.get('meaning', '')}")
    else:
        print("  (네이밍 생성 실패 - 다음 단계로 계속 진행합니다)")

    # 5. 슬로건 생성
    print("[2/5] 슬로건 생성 중...")
    slogans = generate_slogans(client, brief)
    if slogans:
        for s in slogans:
            print(f'  - "{s}"')
    else:
        print("  (슬로건 생성 실패 - 다음 단계로 계속 진행합니다)")

    # 6. 브랜드 스토리 생성
    print("[3/5] 브랜드 스토리 생성 중...")
    story = generate_story(client, brief)
    if story:
        print(f"  - 스토리 생성 완료 ({len(story)}자)")
    else:
        print("  (스토리 생성 실패 - 다음 단계로 계속 진행합니다)")

    # 7. 컬러 팔레트 생성
    print("[4/5] 컬러 팔레트 생성 중...")
    colors = generate_color_palette(client, brief)
    if colors and colors.get("main"):
        print(f"  - 메인: {colors['main']}")
        if colors.get("subs"):
            print(f"  - 서브: {', '.join(colors['subs'])}")
        palette_path = save_color_palette_image(colors, output_path)
        if palette_path:
            print(f"  - 저장: {palette_path}")
    else:
        print("  (컬러 팔레트 생성 실패 - 다음 단계로 계속 진행합니다)")

    # 8. 로고 시안 생성
    print("[5/5] 로고 시안 생성 중...")
    logo_paths = generate_logo_images(client, brief, names, colors, output_path, count=3)
    if logo_paths:
        for p in logo_paths:
            print(f"  - 저장: {p}")
    else:
        print("  (로고 시안 생성 실패 - output 폴더에 텍스트 결과만 저장됩니다)")

    # 10. (보너스) 경쟁사 분석
    print()
    print("[보너스] 경쟁사 분석 중...")
    differentiators = generate_competitor_analysis(client, brief)
    if differentiators:
        for d in differentiators:
            print(f"  - {d}")
    else:
        print("  (경쟁사 정보가 없거나 분석에 실패했습니다 - 건너뜁니다)")

    # 9. 최종 결과 저장
    brand_data = {
        "brief": brief,
        "names": names,
        "slogans": slogans,
        "story": story,
        "colors": colors,
        "logos": logo_paths,
        "competitor_differentiators": differentiators,
    }
    result_path = os.path.join(output_path, "brand_result.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(brand_data, f, ensure_ascii=False, indent=2)

    # 9-1. (개인 추가 기능) Markdown 리포트 저장
    md_path = generate_markdown_report(brand_data, output_path)

    print()
    print(f"✅ 완료! {output_path}/ 폴더를 확인하세요.")
    print(f"   - JSON: {result_path}")
    print(f"   - Markdown: {md_path}")


if __name__ == "__main__":
    main()