# SERVICE_PLAN.md — AI 브랜드 아이덴티티 생성기 (Web)

작성: 조민경 (팀장) | 저장 위치: `Web/SERVICE_PLAN.md`

---

## 1. 서비스 목표
Base(CLI)의 로직을 웹으로 전환해, 브라우저에서 브리프를 입력하면 결과(네이밍/슬로건/스토리/컬러/로고/경쟁사분석)를 바로 확인할 수 있는 서비스.

## 2. 화면 흐름
```
1) 입력 폼 (업종/타겟/키워드/톤/경쟁사/요청사항)
        │  제출
        ▼
2) 로딩 상태 표시 (생성 중)
        │
        ▼
3) 결과 화면 (네이밍 · 슬로건 · 스토리 · 컬러 팔레트 이미지 · 로고 3장 · 경쟁사 분석 · Markdown 다운로드)
```

## 3. API 명세
| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/api/health` | 배포 확인용 헬스체크 (API 키 로드 여부 포함) |
| POST | `/api/generate` | 브리프(JSON) 입력 → 브랜드 결과 전체 반환 |

**`/api/generate` 응답 형식**
```json
{
  "names": [...],
  "slogans": [...],
  "story": "string",
  "colors": {"main": "#RRGGBB", "subs": ["#RRGGBB"]},
  "palette_image_base64": "string",
  "logos_base64": ["string", "string", "string"],
  "competitor_differentiators": [...],
  "markdown_report": "string"
}
```

## 4. 기술 스택
- 백엔드: Flask (Vercel Serverless Python Function)
- 프론트: HTML/CSS/Vanilla JS (`public/`)
- 배포: Vercel — Root Directory `Web`, `functions.maxDuration=60`

## 5. 성능/안정성 설계
- CLI와 달리 웹은 응답 시간이 사용자 경험에 직결되므로, 서로 의존관계 없는 API 호출(네이밍/슬로건/스토리/컬러, 로고/경쟁사분석)은 **병렬 실행**으로 처리해 전체 대기 시간을 단축
- 무료 티어 분당 요청 한도(429) 대응: 10초 대기 후 1회 재시도
- 로고 이미지 생성 실패해도 나머지 결과(텍스트 등)는 정상 반환 (부분 실패 허용)

## 6. 담당자 및 커밋
| 담당 | 산출물 |
|---|---|
| 서경환 | `Web/api/index.py` (백엔드 로직 + 병렬화 개선) |
| 오주연 | `Web/public/style.css` (디자인, 접근성/로딩 상태 개선) |
| 강하연 | Vercel 배포 설정 및 실사용 테스트, `WEB_TEST_LOG.md` |

## 7. 완료 기준
- [x] `/api/generate` 로컬 실행 시 정상 응답
- [x] `vercel.json`에 `maxDuration` 명시 (타임아웃 대응)
- [ ] Vercel 실제 배포 성공 및 정상/예외 케이스 테스트 완료 (강하연)


## 8. 팀장 검토 및 확정 (조민경)

- 검토일: 2026-08-17
- 확인 사항:
  - [x] 화면 흐름(2번)이 실제 UI(`Web/public/index.html`)와 일치하는지 확인
  - [x] API 명세(3번)가 백엔드(`Web/api/index.py`)와 일치하는지 확인
  - [x] 성능/안정성 설계(5번)의 병렬 처리와 `vercel.json`의 `maxDuration: 60` 설정이 실제 구현에 반영되어 있는지 확인
- 특이사항: Vercel 실제 배포 및 실사용 테스트는 강하연 담당으로 추후 진행 예정

> ✅ 조민경 검토 완료 — 2026-08-17