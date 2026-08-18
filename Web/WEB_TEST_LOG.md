# WEB_TEST_LOG.md — Vercel 배포 및 실사용 테스트 기록

작성: 강하연 | 저장 위치: `Web/WEB_TEST_LOG.md`

---

## 1. Vercel 배포 설정
- Vercel 프로젝트: Import Git Repository → `art-ruby/ai-brand-generator` (원본 `coolgirl2046/ai-brand-generator`를 fork하여 배포)
- Root Directory: `Web`
- Environment Variables: `GEMINI_API_KEY = ****` (Vercel 대시보드에서 직접 입력, 코드에는 넣지 않음)
- 배포 URL(Production): https://ai-brand-generator-rho.vercel.app/
- 배포 URL(Preview, 테스트 수행 시점): https://ai-brand-generator-fx310qr7f-rubys-projects-59348814.vercel.app/
- 배포 상태: [x] 성공 / [ ] 실패

## 2. 헬스체크
- `GET /api/health` 응답:
```json
{"gemini_key_loaded": true, "status": "ok"}
```

## 3. 정상 케이스 테스트
- 입력: 비건 스킨케어 브랜드 — 키워드: 자연, 순수, 건강 / 톤앤매너: 따뜻하고 신뢰감있는 / 경쟁사: 아로마티카, 이니스프리 / 추가 요청사항: 비건인증 강화
- 결과: [x] 네이밍 [x] 슬로건 [x] 스토리 [ ] 컬러 팔레트(확인 필요) [x] 로고 3장 [x] 경쟁사 분석 모두 정상 표시
  - 네이밍 4개: 퓨어리프(PURELEAF), 그린아워(GREENHOUR), 비건테라피(VEGANTHERAPY), 나루에코(NALUECO)
  - 로고 시안 3개, 경쟁사 차별화 포인트(보너스) 3개 정상 생성
  - Markdown 리포트 다운로드 정상 동작 → 결과 원본은 `Web/sample_output.md` 참고
- 총 응답 시간: 약 20초 (60초 이내 충족)
- 전체 생성 결과 원본: [sample_output.md](./sample_output.md) 참고

## 4. 예외 케이스 테스트
| 케이스 | 방법 | 기대 동작 | 실제 결과 |
|---|---|---|---|
| 필수 항목 누락 | 키워드 필드를 비운 채 "브랜드 아이덴티티 생성" 제출 | 400 에러 + 안내 메시지 | API 호출 자체가 발생하지 않고 프론트엔드 단에서 즉시 검증됨. 키워드 입력창 테두리가 빨간색으로 강조되고, 버튼 하단에 "필수 항목을 입력해주세요: 키워드" 안내 문구가 표시됨. 서버 요청 전에 차단되므로 API 할당량 낭비 없이 방어됨 |
| 짧은 시간 내 반복 요청 | 1분 내 여러 번 연속 제출 | 429 관련 안내 또는 일부 결과라도 정상 반환 | (미실시) |
| (선택) 응답 지연 확인 | 로고 3장까지 포함해 전체 응답 시간 측정 | 60초 이내 완료 | 정상 케이스에서 약 20초 소요 확인 (위 3번 항목 참고) |

## 5. 결론 및 트러블슈팅
- **Vercel Import 시 저장소가 목록에 안 보임**: 원본 저장소(`coolgirl2046/ai-brand-generator`)는 소유자 계정이 아니라 Collaborator 권한만 있어 Vercel의 GitHub App 접근 목록에 자동으로 뜨지 않음 → 본인(`art-ruby`) 계정으로 저장소를 Fork한 뒤, 그 Fork를 Import하여 해결
- **Root Directory 설정 실수**: 폴더 트리에서 `Web` 하위의 `api` 서브폴더가 잘못 선택된 적 있었음 → `Web` 폴더 자체(라디오 버튼)를 다시 선택하여 해결
- **배포 URL의 `/api/health` 접속 시 Vercel 로그인 페이지로 리다이렉트**: 프리뷰 배포 URL에 Vercel Authentication(팀원 로그인 필요) 보호가 걸려있어 로그아웃 상태 접근 시 로그인 화면이 뜸 → 본인 계정으로 로그인한 상태에서 재접속하여 정상 JSON 응답 확인
- 전체적으로 배포 및 실사용 테스트는 정상 완료됨

---

## 커밋 방법
(아래 명령은 저장소 루트인 `ai-brand-generator` 폴더 기준입니다)

```
git checkout main
```
```
git pull origin main
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
