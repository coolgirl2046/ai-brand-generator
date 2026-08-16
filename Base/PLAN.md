# PLAN.md — AI 브랜드 아이덴티티 생성기 (Base, CLI)

작성: 조민경 (팀장) | 저장 위치: `Base/PLAN.md`

---

## 1. 프로젝트 목표
브랜드 브리프(업종·타겟·키워드 등)를 입력하면 AI가 브랜드 네이밍, 슬로건, 스토리, 컬러 팔레트, 로고 시안까지 자동 생성하는 CLI 프로그램.

## 2. 시스템 아키텍처
```
brief.json (입력)
      │  load_brief()
      ▼
brand_generator.py
      │  generate_naming / generate_slogans / generate_story
      │  generate_color_palette / generate_logo_images
      │  generate_competitor_analysis (보너스)
      ▼
output/
  ├── brand_result.json
  ├── brand_result.md
  ├── color_palette.png
  └── logo_01~03.png
```

## 3. 입력 스키마 — `brief.json`
```json
{
  "industry": "string (필수)",
  "target": "string (필수)",
  "keywords": ["string", "..."],
  "tone": "string (선택)",
  "competitors": ["string", "..."],
  "notes": "string (선택)"
}
```

## 4. 함수 구성 (담당: 서경환)
| 함수 | 역할 |
|---|---|
| `load_brief()` | 브리프 JSON 로드 및 필수 필드 검증 |
| `check_api_key()` | `.env`에서 API 키 로드, 없으면 즉시 종료 |
| `generate_naming()` | 브랜드명 후보 3~5개 (한글+영문) |
| `generate_slogans()` | 슬로건 3개 |
| `generate_story()` | 브랜드 스토리 (300자 내외) |
| `generate_color_palette()` | 메인 1 + 서브 2~3 컬러 (HEX) |
| `generate_logo_concept()` | 로고 컨셉 문장 (긍정문 프롬프팅) |
| `generate_logo_images()` | 로고 시안 3개 생성 (아이콘 + 실제 폰트로 브랜드명 합성) |
| `generate_competitor_analysis()` | 경쟁사 대비 차별화 포인트 (보너스) |
| `generate_markdown_report()` | 결과를 Markdown 리포트로 저장 |

## 5. 에러 처리 정책
- API 키 미설정 → 안내 메시지 출력 후 즉시 종료
- API 호출 실패(401/402/429/503 등) → `describe_api_error()`가 원인별로 한국어 안내 문구 반환, 해당 단계만 건너뛰고 **전체 파이프라인은 계속 진행**
- 브리프 파일 누락/형식 오류 → 즉시 종료 + 안내

## 6. 사용 모델
- 텍스트: `gemini-3.6-flash`
- 이미지: `gemini-2.5-flash-image`
- SDK: `google-genai` (구 SDK `google-generativeai`는 deprecated 되어 사용하지 않음)

## 7. 테스트 케이스
| 케이스 | 브리프 |
|---|---|
| 정상 1 | `brief.json` — K-Beauty 화장품 |
| 정상 2 | `B_brief.json` — 홈카페 원두 |
| 예외 | `.env`에서 `GEMINI_API_KEY` 제거 후 실행 |

## 8. 완료 기준
- [x] `brief.json` 스키마에 맞춰 브리프 2종 이상 작성
- [x] `brand_generator.py` 실행 시 5단계(네이밍~로고) + 보너스(경쟁사분석) 정상 생성
- [x] `.env`가 git에 커밋되지 않음 확인
- [ ] `results`/`output` 폴더에 실행 결과(정상 2건 + 예외 1건) 증빙 커밋 (강하연 담당)
