# TEST_LOG.md — Base(CLI) 테스트 기록

작성: 강하연 | 저장 위치: `Base/TEST_LOG.md`

실행할 때마다 아래 표를 채우고, 터미널 캡처는 최종 보고서에 삽입합니다.

---

## 정상 케이스 1 — `brief.json` (K-Beauty 화장품)

- 실행 명령: `python brand_generator.py`
- 입력한 브리프 경로: `brief.json`
- 결과:
(.venv) PS C:\ia-codyssey\assignments\Team projec 2\ai-brand-generator\base> python brand_generator.py          

==================================================
   🎨 AI 브랜드 아이덴티티 생성기
==================================================

✅ API 키 로드 완료 (앞 4자리: AQ.A****)

브리프 파일 경로를 입력하세요: brief.json
출력 폴더 경로를 입력하세요 (엔터 시 ./output): 

✅ 브리프 로드 완료
   - 업종: K- Beauty 화장품
   - 타겟: 20-30대 여성
   - 키워드: 자연, 순수, 건강
   - 출력 폴더: ./output

[1/5] 브랜드 네이밍 생성 중...
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.
  - 온비채 (ONBICHAE): 따뜻함(온)과 순수한 비건 성분(비)으로 피부 본연의 건강한 빛(채)을 채운다는 의미를 담은 감성 비건 브랜드입니다.
  - 순숨비 (SUNSOOMBI): 자연 그대로의 순수한 숨결을 담아 피부에 건강한 휴식과 신뢰감을 선물하는 클린 비건 화장품입니다.
  - 비건로 (VEGANRO): 올바른 비건의 길(路)을 제시하며, 100% 식물성 원료로 순수함과 건강함을 전하는 자연주의 스킨케어 브랜드입니다.
  - 이어숲 (EEARSUP): 청정한 숲의 따뜻한 생명력과 피부를 부드럽게 이어주어 유기농 비건 가치를 실현하는 브랜드입니다.
[2/5] 슬로건 생성 중...
  - "가장 순수한 자연으로, 피부 본연의 건강함을 피우다."
  - "자연이 전하는 순수한 온기, 피부 깊은 곳까지 건강하게."
  - "매일 만나는 순수한 자연, 피부에 전하는 가장 건강한 약속."
[3/5] 브랜드 스토리 생성 중...
  - 스토리 생성 완료 (263자)
[4/5] 컬러 팔레트 생성 중...
  - 메인: #8CA391
  - 서브: #F5EBE6, #E3B5A4, #6B5B52
  - 저장: ./output\color_palette.png
[5/5] 로고 시안 생성 중...
  - 저장: ./output\logo_01.png
  - 저장: ./output\logo_02.png
  - 저장: ./output\logo_03.png

[보너스] 경쟁사 분석 중...
  - 차가운 친환경 메시지를 탈피한 '따뜻한 감성의 피부 웰니스 리추얼' 제안
  - 단순 자연 원료 활용을 넘어선 '피부 근본 건강 중심의 순수 바이오 처방'
  - 진정성 있는 원료 투명성과 휴먼 터치(Human Touch) 기반의 밀착형 신뢰 구축

✅ 완료! ./output/ 폴더를 확인하세요.
   - JSON: ./output\brand_result.json
   - Markdown: ./output\brand_result.md
- 특이사항:없음

  - [v] 네이밍 3~5개 생성됨
  - [v] 슬로건 3개 생성됨
  - [v] 스토리 생성됨
  - [v] 컬러 팔레트 + `color_palette.png` 생성됨
  - [v] 로고 3장 생성됨
  - [v] 경쟁사 분석(보너스) 생성됨
- 특이사항: 없음

## 정상 케이스 2 — `B_brief.json` (홈카페 원두)

- 실행 명령: `python brand_generator.py`
- 입력한 브리프 경로: `B_brief.json`
- 결과:
(venv) PS C:\ia-codyssey\assignments\Team projec 2\ai-brand-generator\Base> python brand_generator.py

==================================================
   🎨 AI 브랜드 아이덴티티 생성기
==================================================

✅ API 키 로드 완료 (앞 4자리: AQ.A****)

브리프 파일 경로를 입력하세요: B_brief.json
출력 폴더 경로를 입력하세요 (엔터 시 ./output): 

✅ 브리프 로드 완료
   - 업종: 홈카페 원두
   - 타겟: 재택근무를 하는 20~30대 직장인
   - 키워드: 집중, 여유, 프리미엄
   - 출력 폴더: ./output

[1/5] 브랜드 네이밍 생성 중...
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.
  - 디아워스 (D'HOURS): 재택근무자의 하루 중 가장 깊은 집중과 여유가 필요한 '그 시간(Hours)'을 맞춰 정기적으로 배송해 주는 프리미엄 홈카페 브랜드입니다.
  - 빈루틴 (BEAN ROUTINE): 매월/매주 정기적으로 전달되는 원두를 통해 일상에 차분한 집중력과 세련된 휴식의 루틴을 선사하는 브랜드입니다.
  - 스테디모먼트 (STEADY MOMENT): '변함없이 찾아오는 순간'을 의미하며, 구독을 통해 업무의 몰입과 고급스러운 여유를 지속해서 공급하는 고품격 원두 브랜드입니다.
  - 포커스드롭 (FOCUS DROP): 한 방울의 커피로 완성되는 깊은 몰입감을 뜻하며, 재택근무자의 홈카페로 신선하게 정기 배송되는 맞춤형 커피 서비스입니다.
[2/5] 슬로건 생성 중...
  - "완벽한 몰입, 깊어지는 여유."
  - "일과 휴식의 경계에서 만나는 프리미엄."
  - "집중을 깨우는 향, 여유를 채우는 한 잔."
[3/5] 브랜드 스토리 생성 중...
  - 스토리 생성 완료 (291자)
[4/5] 컬러 팔레트 생성 중...
  - 메인: #2C221E
  - 서브: #E5DDD0, #5B6E60, #B88B5C
  - 저장: ./output\color_palette.png
[5/5] 로고 시안 생성 중...
  - 저장: ./output\logo_01.png
  - 저장: ./output\logo_02.png
  - 저장: ./output\logo_03.png

[보너스] 경쟁사 분석 중...
  - 시간대별 일의 흐름을 고려한 루틴 큐레이션: 오프라인 공간 중심의 경쟁사와 달리, 몰입이 필요한 오전에 높은 카페인과 깔끔한 목넘김을 주는 'Focus Blend'와 업무 후 리프레시를 위한 낮고 부드러운 'Leisure Blend'로 일상의 리듬을 세밀하게 제안합니다.
  - 재택근무자의 데스크테리어를 고려한 세련된 미니멀 패키징: 책상 위에 두어도 시각적 소음이 되지 않는 차분하고 감각적인 디자인과, 업무 중 밀폐와 보관이 용이한 기능성 프리미엄 용기를 채택하여 홈오피스의 품격을 높입니다.
  - 디지털 워크 라이프스타일 융합 서비스: 원두에 어울리는 최적의 몰입용 앰비언트 사운드트랙과 뽀모도로 타이머 디지털 콘텐츠를 QR코드로 제공하여 단순한 원두 판매를 넘어 '완벽한 재택근무 환경'을 솔루션으로 제공합니다.

✅ 완료! ./output/ 폴더를 확인하세요.
   - JSON: ./output\brand_result.json
   - Markdown: ./output\brand_result.md

## 예외 케이스 1 — API 키 누락

- 방법: `.env` 파일에서 `GEMINI_API_KEY=` 값을 잠시 지우고 실행
- 기대 동작: "GEMINI_API_KEY가 설정되지 않았습니다" 메시지 출력 후 즉시 종료
- 실제 결과:
(.venv) PS C:\ia-codyssey\assignments\Team projec 2\ai-brand-generator\base> python brand_generator.py

==================================================
   🎨 AI 브랜드 아이덴티티 생성기
==================================================

✅ API 키 로드 완료 (앞 4자리: AQ.A****)

브리프 파일 경로를 입력하세요: brief.json
출력 폴더 경로를 입력하세요 (엔터 시 ./output): 

✅ 브리프 로드 완료
   - 업종: K- Beauty 화장품
   - 타겟: 20-30대 여성
   - 키워드: 자연, 순수, 건강
   - 출력 폴더: ./output

[1/5] 브랜드 네이밍 생성 중...
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.
   ❌ API 호출 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
  (네이밍 생성 실패 - 다음 단계로 계속 진행합니다)
[2/5] 슬로건 생성 중...
   ❌ API 호출 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
  (슬로건 생성 실패 - 다음 단계로 계속 진행합니다)
[3/5] 브랜드 스토리 생성 중...
   ❌ API 호출 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
  (스토리 생성 실패 - 다음 단계로 계속 진행합니다)
[4/5] 컬러 팔레트 생성 중...
   ❌ API 호출 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
  (컬러 팔레트 생성 실패 - 다음 단계로 계속 진행합니다)
[5/5] 로고 시안 생성 중...
   ❌ API 호출 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
   ❌ 로고 시안 1 생성 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
   ❌ 로고 시안 2 생성 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
   ❌ 로고 시안 3 생성 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
  (로고 시안 생성 실패 - output 폴더에 텍스트 결과만 저장됩니다)

[보너스] 경쟁사 분석 중...
   ❌ API 호출 실패: API 키 인증 실패 (.env의 GEMINI_API_KEY 값을 확인하세요)
  (경쟁사 정보가 없거나 분석에 실패했습니다 - 건너뜁니다)

✅ 완료! ./output/ 폴더를 확인하세요.
   - JSON: ./output\brand_result.json
   - Markdown: ./output\brand_result.md
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
