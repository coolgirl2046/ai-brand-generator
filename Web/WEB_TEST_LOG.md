# WEB_TEST_LOG.md — Vercel 배포 및 실사용 테스트 기록

작성: 강하연 | 저장 위치: `Web/WEB_TEST_LOG.md`

---

## 1. Vercel 배포 설정
- Vercel 프로젝트: Import Git Repository → `art-ruby/ai-brand-generator` (원본 `coolgirl2046/ai-brand-generator`를 fork하여 배포)
- Root Directory: `Web`
- Environment Variables: `GEMINI_API_KEY = ****` (Vercel 대시보드에서 직접 입력, 코드에는 넣지 않음)
- 배포 URL: https://ai-brand-generator-fx310qr7f-rubys-projects-59348814.vercel.app/
- 배포 상태: [x] 성공 / [ ] 실패

## 2. 헬스체크
- `GET /api/health` 응답:
```json
{"gemini_key_loaded": true, "status": "ok"}