# 🎨 AI 브랜드 아이덴티티 생성기

브랜드 브리프(업종, 타겟, 키워드 등)를 입력하면 AI가 브랜드 네이밍, 슬로건, 스토리, 컬러 팔레트, 로고 시안까지 자동으로 생성해주는 CLI 프로그램입니다.

Codyssey 팀미션 2-2-1 [Project A] 결과물입니다.

---

## ✨ 주요 기능

- **브랜드 네이밍**: 한글명 + 영문명 3~5개 후보와 의미/유래 (다국어 지원)
- **슬로건**: 브랜드 톤앤매너에 맞는 태그라인 3개
- **브랜드 스토리**: 탄생 배경/철학/비전이 담긴 300자 내외 스토리
- **컬러 팔레트**: 메인 1개 + 서브 2~3개 HEX 컬러 추천 및 시각화(PNG)
- **로고 시안**: AI 이미지 생성으로 아이콘 로고 시안 3개(PNG)
- **경쟁사 분석**: 입력한 경쟁사 대비 차별화 포인트 3가지 제안

## 🛠 기술 스택

- Python 3.10+
- LLM: Google Gemini API (`gemini-3.6-flash`)
- 이미지 생성: Google Gemini 이미지 생성 API (`gemini-2.5-flash-image`, Nano Banana)
- 시각화: matplotlib, Pillow

## 📁 프로젝트 구조
Project_A_BrandGenerator/
├── brand_generator.py # 메인 프로그램
├── brief.json # 브랜드 브리프 예시
├── .env # API 키 (Git에 커밋되지 않음)
├── .env.example # API 키 형식 예시
├── .gitignore
├── requirements.txt
└── output/ # 결과물 저장 폴더
├── brand_result.json
├── color_palette.png
├── logo_01.png
├── logo_02.png
└── logo_03.png

## 🚀 실행 방법

### 1. 가상환경 설정 및 패키지 설치

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. API 키 설정

`.env.example`을 참고하여 프로젝트 루트에 `.env` 파일을 만들고 아래 내용을 입력하세요.

```
GEMINI_API_KEY=발급받은_API_키
```

> API 키는 [Google AI Studio](https://aistudio.google.com/apikey)에서 발급받을 수 있습니다.
> `.env`는 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다.

### 3. 실행

```powershell
python brand_generator.py
```

실행하면 순서대로 아래를 입력하라는 안내가 나옵니다.

1. 브리프 파일 경로 (예: `brief.json` 또는 `B_brief.json`)
2. 출력 폴더 경로 (엔터 시 기본값 `./output`)

### 4. 결과 확인

`output/` 폴더(또는 직접 지정한 폴더)에 아래 파일들이 생성됩니다.

| 파일 | 내용 |
|---|---|
| `brand_result.json` | 네이밍/슬로건/스토리/컬러/로고 경로/경쟁사 분석 전체 결과 (구조화 데이터) |
| `brand_result.md` | 같은 내용을 사람이 읽기 좋은 Markdown으로 정리한 리포트 |
| `color_palette.png` | 추천 컬러 팔레트 시각화 이미지 |
| `logo_01.png` ~ `logo_03.png` | AI가 생성한 로고 시안 3개 (아이콘 + 브랜드명 합성) |

## 🧪 테스트 케이스

`brief.json`(K-Beauty 화장품)과 `B_brief.json`(홈카페 원두) 두 가지 업종으로 정상 동작을 확인했습니다. 예외 케이스는 아래 트러블슈팅 섹션을 참고하세요.

## 🐛 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `GEMINI_API_KEY가 설정되지 않았습니다` 출력 후 즉시 종료 | `.env` 파일이 없거나 키 값이 비어있음 | 프로젝트 루트에 `.env` 생성 후 `GEMINI_API_KEY=` 뒤에 실제 키 입력 |
| `API 크레딧/할당량 소진` 메시지 | Gemini 무료 티어 일일/분당 한도 초과 (특히 이미지 생성 모델) | Google AI Studio에서 결제 정보 또는 한도 확인 후 재시도 |
| `API 키 인증 실패` 메시지 | 키 값이 잘못되었거나 만료됨 | Google AI Studio에서 키를 재발급받아 `.env`에 다시 입력 |
| 로고 이미지에 브랜드명이 깨져 보임 | 실행 환경에 한글 폰트가 없음 | Windows는 자동으로 맑은 고딕을 찾음. 다른 OS라면 나눔고딕 등 한글 폰트 경로를 `font_candidates`에 추가 |

## 🔒 보안 주의사항

- `.env` 파일에는 실제 API 키가 들어가므로 **절대 Git에 커밋하지 않습니다** (`.gitignore`로 차단됨)
- 저장소에는 `.env.example`처럼 값이 비어있는 형식만 공유합니다
- API 키가 실수로 노출되었다면 Google AI Studio에서 즉시 재발급(폐기+재발급)하세요