# README

# AI 브랜드 아이덴티티 생성기

브랜드 브리프(업종·타겟·키워드·톤앤매너·경쟁사) 하나만 입력하면, AI가 브랜드 네이밍부터 슬로건·스토리·컬러 팔레트·로고 시안까지 원스톱으로 생성해주는 브랜드 아이덴티티 자동화 도구입니다.

> 2026 경남 코디세이(Gyeongnam Codyssey) 팀미션 2-2-1 [Project A]
> 

**🔗 Web URL**: [https://ai-brand-generator-rho.vercel.app/](https://ai-brand-generator-rho.vercel.app/)

---

## 📸 실행 예시

브리프 입력 → AI가 자동 생성한 실제 결과 예시입니다.

**입력**
| 항목 | 값 |
|—|—|
| 업종 | 친환경 화장품 |
| 타겟 | 20-30대 여성 |
| 키워드 | 자연, 순수, 건강 |
| 톤앤매너 | 따뜻하고 신뢰감 있는 |
| 경쟁사 | 이니스프리, 아로마티카 |

**출력 (일부)**
- 브랜드 네이밍 4종: 퓨어가든(PureGarden), 톤오브가이아(Tone of Gaia), 그린아워(Green Hour), 나탈리프(NataLeaf) — 각 이름의 의미·유래까지 함께 생성
- 슬로건 3개, 브랜드 스토리, 컬러 팔레트(메인 1 + 서브 3, HEX 코드 포함)
- AI 생성 로고 시안 3개
- 경쟁사 차별화 포인트 3가지 (보너스)
- 결과를 Markdown 리포트로 다운로드 가능

> 실행 결과 화면(Base)
> 

![실행 결과 화면](Local_Result_.png)

> <output (Pallet,Logo)>
> 

![image.png](image.png)

> 실행 결과 화면(Web)
> 

![Web Result.png](Web_Result.png)

---

## 👥 팀 구성

| 담당 | 역할 |
| --- | --- |
| 조민경 (팀장) | 기획 총괄, 문서 검토, 최종 결과보고서 작성 |
| 서경환 | 전체 파이프라인 설계·구현 (Base + Web), 성능 최적화 |
| 오주연 | 웹 UI/UX 디자인 및 스타일 개선 |
| 강하연 | 테스트 검증, Vercel 배포, 실사용 테스트 |

---

## 🧠 핵심 파이프라인

```
브랜드 브리프 입력 (JSON)
        ↓
AI 브랜드 전략 생성 (네이밍 · 슬로건 · 스토리 · 컬러)
        ↓
경쟁사 분석 및 차별화 포인트 도출 (보너스)
        ↓
AI 이미지 생성 (로고 시안) + 컬러 팔레트 시각화
        ↓
결과 통합 및 저장 (Base: 파일 저장 / Web: 화면 응답 + Markdown 다운로드)
```

---

## 🛠 기술 스택

- **언어**: Python 3.14
- **AI**: Google Gemini API — `google-genai` SDK (`gemini-3.6-flash` 텍스트 생성, `gemini-2.5-flash-image` 이미지 생성)
- **백엔드(Web)**: Flask, Vercel Serverless Functions
- **프론트엔드(Web)**: HTML / CSS / JavaScript
- **시각화**: matplotlib (컬러 팔레트), Pillow (로고 텍스트 합성)
- **배포**: Vercel

---

## 📁 폴더 구조

```
ai-brand-generator/
├── Base/                     # CLI 버전
│   ├── brand_generator.py    # 전체 파이프라인 메인 프로그램
│   ├── brief.json            # 예시 브리프 (K-Beauty 화장품)
│   ├── B_brief.json          # 예시 브리프 (홈카페 원두)
│   ├── PLAN.md                # 기획 문서 (조민경 검토 완료)
│   ├── TEST_LOG.md            # 테스트 기록 (강하연)
│   ├── README.md              # Base 실행 가이드
│   ├── requirements.txt
│   └── .env.example
├── Web/                       # 웹 서비스 버전
│   ├── api/index.py           # Flask 백엔드 (병렬 처리 적용)
│   ├── public/                # 프론트엔드 (index.html, style.css, script.js)
│   ├── assets/fonts/          # 로고 텍스트 합성용 한글 폰트
│   ├── vercel.json            # Vercel 배포 설정 (maxDuration: 60)
│   ├── SERVICE_PLAN.md        # 서비스 기획 문서 (조민경 검토 완료)
│   ├── WEB_TEST_LOG.md        # 배포·실사용 테스트 기록 (강하연)
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   └── screenshot_result.png  # 실행 결과 캡처
├── SETUP_HISTORY.md            # 협업 진행 배경 문서
└── README.md                   # 본 문서
```

---

## 🚀 로컬 실행 방법

### Base (CLI)

```powershell
cd Base
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

`.env` 파일에 발급받은 API 키 입력:

```
GEMINI_API_KEY=발급받은_API_키
```

```powershell
python brand_generator.py
```

브리프 파일 경로(`brief.json` 또는 `B_brief.json`)를 입력하면 `output/` 폴더에 결과(JSON, Markdown, 로고 PNG, 컬러 팔레트 PNG)가 저장됩니다.

### Web (로컬 서버)

```powershell
cd Web
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

`.env`에 API 키 입력 후, `assets/fonts/`에 `NanumGothic-Bold.ttf` 폰트 파일이 있는지 확인:

```powershell
python api/index.py
```

브라우저에서 `http://127.0.0.1:5000` 접속.

---

## ☁️ 배포 (Vercel)

1. [Vercel](https://vercel.com/) 로그인 → **Add New → Project** → 이 저장소 Import
2. **Root Directory**: `Web`
3. **Environment Variables**에 `GEMINI_API_KEY` 등록 (Vercel 대시보드에서 직접 입력, 코드에는 절대 포함하지 않음)
4. **Deploy**

> Gemini 이미지 생성 API는 무료 티어 쿼터가 매우 제한적입니다. 실사용 배포 시 유료 결제 계정 연결을 권장합니다.
> 

---

## 📡 API 명세 (Web)

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| GET | `/api/health` | 배포 확인용 헬스체크 |
| POST | `/api/generate` | 브리프 입력 → 네이밍·슬로건·스토리·컬러·로고·경쟁사분석 통합 응답 |

---

## ✅ 구현 기능

- [x]  CLI 대화형 브리프 입력 및 검증
- [x]  브랜드 네이밍 자동 생성 (의미/유래 포함)
- [x]  슬로건 3개 생성
- [x]  브랜드 스토리 생성
- [x]  컬러 팔레트(HEX) 생성 및 PNG 시각화
- [x]  AI 로고 시안 생성 (텍스트 합성 포함)
- [x]  **보너스** — 경쟁사 분석 및 차별화 포인트 도출
- [x]  Markdown 리포트 생성 및 다운로드
- [x]  API 오류 단계별 처리 (키 누락/쿼터 초과/네트워크 오류)
- [x]  CLI → 웹 서비스 확장 (Flask + Vercel)
- [x]  서버리스 타임아웃 대응을 위한 병렬 처리
- [x]  Vercel 실배포 및 실사용 검증

---

## 🔒 보안

- `.env` 파일은 `.gitignore`로 제외되어 저장소에 커밋되지 않습니다.
- API 키는 `.env.example`처럼 값 없이 키 이름만 저장소에 공유합니다.
- Vercel 배포 시 API 키는 대시보드의 Environment Variables에서만 관리합니다.

---

## 🧩 트러블슈팅

개발 과정에서 겪은 주요 이슈와 해결 과정은 다음 문서에 기록되어 있습니다.

- [`Base/TEST_LOG.md`](Base/TEST_LOG.md) — CLI 정상/예외 케이스 테스트 기록
- [`Web/WEB_TEST_LOG.md`](Web/WEB_TEST_LOG.md) — 배포 및 웹 실사용 테스트 기록
- [`SETUP_HISTORY.md`](SETUP_HISTORY.md) — 팀 협업 진행 배경

대표적인 이슈: Gemini SDK deprecation(`google-generativeai` → `google-genai`) 대응, Vercel 서버리스 타임아웃 대응(병렬 처리 + `maxDuration` 설정), 이미지 생성 무료 쿼터 소진 → 결제 계정 연결로 해결.