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