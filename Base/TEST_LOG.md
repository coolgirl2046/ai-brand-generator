# TEST_LOG.md — Base(CLI) 테스트 기록

작성: 강하연 | 저장 위치: `Base/TEST_LOG.md`

실행할 때마다 아래 표를 채우고, 터미널 캡처는 최종 보고서에 삽입합니다.

---

## 정상 케이스 1 — `brief.json` (K-Beauty 화장품)

- 실행 명령: `python brand_generator.py`
- 입력한 브리프 경로: `brief.json`
- 결과:
  - [ ] 네이밍 3~5개 생성됨
  - [ ] 슬로건 3개 생성됨
  - [ ] 스토리 생성됨
  - [ ] 컬러 팔레트 + `color_palette.png` 생성됨
  - [ ] 로고 3장 생성됨
  - [ ] 경쟁사 분석(보너스) 생성됨
- 소요 시간: ___분 ___초
- 특이사항:

## 정상 케이스 2 — `B_brief.json` (홈카페 원두)

- 실행 명령: `python brand_generator.py`
- 입력한 브리프 경로: `B_brief.json`
- 결과: (위와 동일한 체크리스트)
- 특이사항:

## 예외 케이스 1 — API 키 누락

- 방법: `.env` 파일에서 `GEMINI_API_KEY=` 값을 잠시 지우고 실행
- 기대 동작: "GEMINI_API_KEY가 설정되지 않았습니다" 메시지 출력 후 즉시 종료
- 실제 결과:
- ✅/❌:

## 예외 케이스 2 (선택) — 존재하지 않는 브리프 경로 입력

- 방법: 브리프 파일 경로 입력 시 존재하지 않는 파일명 입력 (예: `없는파일.json`)
- 기대 동작: "브리프 파일을 찾을 수 없습니다" 메시지 출력 후 즉시 종료
- 실제 결과:

## 예외 케이스 3 (선택) — 이미지 생성 쿼터 초과

- 방법: 위 케이스들을 짧은 시간 내에 반복 실행하여 무료 티어 이미지 생성 한도 초과 유도
- 기대 동작: "API 크레딧/할당량 소진" 안내 메시지 출력, 로고 없이도 나머지 결과는 저장됨
- 실제 결과:

---

## 커밋 방법
```
git checkout main
```
```
git pull
```
```
git checkout -b feature/kang-test
```
(테스트 실행 후 TEST_LOG.md 작성)
```
git add Base/TEST_LOG.md
```
```
git commit -m "[강하연] test: Base 정상/예외 케이스 테스트 및 결과 기록"
```
```
git push origin feature/kang-test
```
GitHub에서 PR 생성 → Merge
