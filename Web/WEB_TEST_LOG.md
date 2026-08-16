# WEB_TEST_LOG.md — Vercel 배포 및 실사용 테스트 기록

작성: 강하연 | 저장 위치: `Web/WEB_TEST_LOG.md`

---

## 1. Vercel 배포 설정
- Vercel 프로젝트: Import Git Repository → `coolgirl2046/ai-brand-generator`
- Root Directory: `Web`
- Environment Variables: `GEMINI_API_KEY = ****` (Vercel 대시보드에서 직접 입력, 절대 코드에 넣지 않음)
- 배포 URL: `https://______________.vercel.app`
- 배포 상태: [ ] 성공 / [ ] 실패

## 2. 헬스체크
- `GET /api/health` 응답:
```json

```

## 3. 정상 케이스 테스트
- 입력: (실제 웹 화면에서 입력한 브리프 내용 요약)
- 결과: [ ] 네이밍 [ ] 슬로건 [ ] 스토리 [ ] 컬러 팔레트 [ ] 로고 3장 [ ] 경쟁사 분석 모두 정상 표시
- 총 응답 시간: ___초 (60초 이내인지 확인)

## 4. 예외 케이스 테스트
| 케이스 | 방법 | 기대 동작 | 실제 결과 |
|---|---|---|---|
| 필수 항목 누락 | 업종/타겟/키워드 중 하나를 비운 채 제출 | 400 에러 + 안내 메시지 | |
| 짧은 시간 내 반복 요청 | 1분 내 여러 번 연속 제출 | 429 관련 안내 또는 일부 결과라도 정상 반환 | |
| (선택) 응답 지연 확인 | 로고 3장까지 포함해 전체 응답 시간 측정 | 60초 이내 완료 | |

## 5. 결론 및 트러블슈팅
- (실제 겪은 문제 → 원인 → 해결 과정을 여기에 기록. 이게 최종보고서 트러블슈팅 섹션의 핵심 자료가 됩니다)

---

## 커밋 방법
```
git checkout main
```
```
git pull
```
(Vercel 배포 및 테스트 진행 후 WEB_TEST_LOG.md 작성)
```
git add Web/WEB_TEST_LOG.md
```
```
git commit -m "[강하연] test: Vercel 배포 및 실사용 테스트 결과 기록"
```
```
git push origin main
```
