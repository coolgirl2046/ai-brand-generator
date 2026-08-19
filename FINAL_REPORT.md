


AI 브랜드 아이덴티티 생성기
팀 프로젝트 결과보고서
AI 활용 학습 · Term Project · Project A


문서 상태  GitHub 검증과 팀원별 수행 증빙을 반영한 최종본



구분
내용
팀장
조민경
팀원
서경환 · 오주연 · 강하연
저장소
github.com/coolgirl2046/ai-brand-generator
기준일
2026-08-19
개발환경
Python 3.10 이상 · Gemini API · Flask · Vercel · matplotlib · Pillow


본 보고서는 공식 미션 요구사항, 실제 구현 코드, GitHub 커밋·Pull Request, 테스트 로그와 배포 기록을 상호 대조하여 작성했습니다.
 1. 프로젝트 개요
본 프로젝트는 업종·타겟·키워드·톤앤매너·경쟁사 등의 브랜드 브리프를 입력하면 Google Gemini API를 활용하여 브랜드 네이밍, 슬로건, 브랜드 스토리, 컬러 팔레트와 로고 시안을 자동 생성하는 Python 프로그램입니다. 공식 요구사항인 CLI 결과물에 더해, 브라우저에서 같은 기능을 사용할 수 있도록 Flask 기반 웹 서비스와 Vercel 배포를 확장 구현했습니다.

핵심 성과  텍스트 생성과 이미지 생성을 하나의 파이프라인으로 연결하고, JSON·Markdown·PNG 파일 저장과 웹 화면 응답을 모두 구현했습니다.

 1.1 처리 흐름
1. 	사용자가 JSON 파일 또는 웹 입력 폼으로 브랜드 브리프를 제공합니다.
2. 	필수 필드 industry, target, keywords를 검증하고 선택 필드를 정규화합니다.
3. 	LLM이 네이밍 3~5개, 슬로건 3개, 약 300자의 브랜드 스토리와 HEX 컬러를 생성합니다.
4. 	이미지 생성 모델이 로고 시안 3개를 만들고, matplotlib이 컬러 팔레트를 PNG로 시각화합니다.
5. 	Base는 JSON·Markdown·PNG로 저장하고, Web은 텍스트와 base64 이미지를 화면에 반환합니다.
 1.2 팀 구성과 역할

담당
확정 역할
GitHub 근거
조민경
기획 총괄, 요구사항·구현 일치 검토, 최종 문서 취합
PR #1 · PLAN.md · SERVICE_PLAN.md
서경환
Base CLI와 Web 백엔드, Gemini API, 오류 처리·병렬화 구현
초기 구축 및 PR #4
오주연
웹 UI 디자인, 접근성, 로딩·인쇄/PDF 스타일 개선
PR #2·#3
강하연
Base 테스트, Vercel 배포, 웹 실사용 검증과 로그 작성
PR #5 · TEST_LOG · WEB_TEST_LOG

 2. 공식 요구사항 이행 현황
공식 미션 요구사항과 실제 구현 위치를 다음과 같이 연결했습니다. 웹 서비스는 추가 확장 결과이며, 과제의 핵심 제출물은 Base CLI 프로그램입니다.

요구사항
실제 구현
판정
대화형 입력
main()의 print/input, 출력 기본값 ./output
충족
JSON 브리프 검증
load_brief(): 필수 3개·선택 3개 필드
충족
네이밍 3~5개
generate_naming(), 한글+영문·의미 포함
충족
슬로건 3개
generate_slogans()
충족
브랜드 스토리
generate_story(), 약 300자
충족
컬러 팔레트
메인 1·서브 3 HEX, matplotlib PNG
충족
로고 2~3개
Gemini 이미지 모델, PNG 3장 저장
충족
결과 저장
brand_result.json/.md, color_palette.png, logo_01~03.png
충족
API 오류 대응
describe_api_error() 및 단계별 try/except
충족
API 키 관리
.env, .env.example, .gitignore
충족
보너스 1
경쟁사 분석·차별화 포인트 3개
충족
보너스 2
한글·영문 네이밍 동시 생성
충족


검토 기준  기능 존재 여부뿐 아니라 입력 형식, 결과 개수, 저장 파일명, API 키 보안과 실패 시 진행 정책까지 함께 확인했습니다.

 3. Base CLI 프로그램 구현
 3.1 입력과 검증
브리프 파일 경로를 필수로 입력받고, 출력 폴더는 Enter 입력 시 ./output을 사용합니다. load_brief()는 파일 존재 여부와 JSON 형식을 확인한 뒤 industry, target, keywords 누락 여부를 검사합니다. tone, competitors, notes가 없으면 빈 값으로 보완합니다.

그림 1. 조민경의 Base 입력 스키마 및 load_brief() 구현 검토
 3.2 생성 단계와 저장 결과
네이밍→슬로건→스토리→컬러→로고의 5단계를 순차 실행하고, 보너스 경쟁사 분석을 추가합니다. 각 텍스트 생성 결과를 brand_result.json과 brand_result.md에 저장하며, 팔레트와 로고는 개별 PNG로 저장합니다.

그림 2. Base 정상 케이스 1 실행 결과

그림 3. output 폴더에 생성된 최종 결과물
 3.3 컬러 및 로고 결과
컬러 팔레트는 메인 컬러 1개와 서브 컬러 3개의 HEX 값을 시각화합니다. 로고는 이미지 모델이 생성한 아이콘에 실제 폰트로 브랜드명을 합성하여 AI 이미지의 글자 왜곡 문제를 줄였다.

그림 4. matplotlib으로 저장한 컬러 팔레트

그림 5. 생성된 로고 시안 3종
 3.4 API 오류 처리
API 호출 실패가 전체 파이프라인 중단으로 이어지지 않도록 각 단계에서 예외를 처리하고 다음 단계로 진행합니다. 401·429·503 등 주요 오류를 사용자가 이해할 수 있는 한국어 메시지로 변환합니다. 단, 환경 변수 자체가 없는 경우에는 안내 후 종료합니다.

그림 6. API 키 확인 및 오류 메시지 정책 검토
 4. Web 서비스 확장
Base의 생성 로직을 Flask API와 HTML/CSS/Vanilla JavaScript로 확장했습니다. 사용자는 브라우저 입력 폼에서 브리프를 제출하고, 네이밍·슬로건·스토리·컬러·로고·경쟁사 차별화 포인트를 한 화면에서 확인할 수 있습니다.
 4.1 화면 및 API

메서드
경로
기능
GET
/api/health
배포 상태와 Gemini API 키 로드 여부 확인
POST
/api/generate
브리프 검증 후 텍스트·이미지·리포트 통합 반환


그림 7. Web 입력 폼과 SERVICE_PLAN 화면 흐름 검토

그림 8. /api/generate 명세와 실제 백엔드 구현 검토
 4.2 성능과 안정성
서로 독립적인 네이밍·슬로건·스토리·컬러 호출을 ThreadPoolExecutor로 병렬 실행하고, 로고와 경쟁사 분석도 별도 병렬 처리했습니다. vercel.json에는 maxDuration 60초를 명시하여 서버리스 실행 시간을 확보했습니다.

그림 9. 병렬 처리와 Vercel maxDuration 60 설정 검토
 4.3 웹 UI 개선 결과
오주연은 기능 중심의 초기 화면을 사용자 피드백·접근성·출력 편의성을 갖춘 화면으로 단계적으로 개선했습니다. 실제 변경은 PR #2와 PR #3의 총 5개 커밋과 17장의 GitHub 증빙에서 확인했습니다.
 4.3.1 1차 개선 — 상태 표시·접근성·인쇄
제출 버튼에 is-loading 상태와 스피너를 적용하여 생성 중임을 즉시 알 수 있게 했습니다. 키보드 사용자를 위한 focus-visible 아웃라인을 추가하고, @media print에서 입력 폼과 로딩 요소를 숨기며 팔레트 색상은 유지하도록 구성했습니다.

그림 10. 초기 화면·로딩 스피너·키보드 포커스·인쇄 미리보기 증빙

그림 11. 로딩, focus-visible, 인쇄/PDF 스타일 구현 코드
 4.3.2 2차 개선 — Violet Nova 최종 디자인
Pretendard와 Space Grotesk 폰트를 적용하고 레이블 정렬을 보정한 뒤, 입력·로딩·결과 화면을 Violet Nova 콘셉트로 통합했습니다. 단순한 시각 변경이 아니라 상태 표시와 출력 가독성을 함께 개선한 작업으로 평가했습니다.

그림 12. PR #2·#3의 코드 차이와 main 병합 증빙

그림 13. Contributors·Pulse에서 확인한 팀 협업 이력

오주연 기여 요약  UI 관련 5개 커밋, PR #2·#3 병합, 로딩·포커스·인쇄/PDF·최종 시각 설계 증빙 17장을 최종본에 반영했습니다.

 5. 테스트 및 Vercel 배포
 5.1 Base 테스트 결과
강하연은 Base 정상 케이스 2건과 잘못된 API 키에 따른 인증 실패 케이스를 실행하고 TEST_LOG.md에 결과를 기록했습니다. 존재하지 않는 파일 경로와 이미지 쿼터 초과는 선택 테스트로 계획했으나 실제 결과가 기록되지 않았으므로 미실시로 분류했습니다.

케이스
입력 또는 조건
실제 결과
판정
정상 1
brief.json · K-Beauty
전체 텍스트, 팔레트, 로고 3장, 경쟁사 분석 생성
통과
정상 2
B_brief.json · 홈카페 원두
다른 업종의 전체 결과 생성
통과
예외 1
잘못된 API 키
각 단계에서 인증 실패 안내 후 다음 단계 진행
통과
예외 2
존재하지 않는 경로
실제 결과 미작성
미실시
예외 3
이미지 쿼터 초과
실제 결과 미작성
미실시


표현 정정  기존 문서의 “API 키 누락”은 실제 로그상 API 키가 로드된 뒤 인증에 실패한 사례이므로 “잘못된 API 키에 따른 인증 실패”로 정정했습니다.


그림 14. Base 테스트 계획과 TEST_LOG 연계 검토
 5.2 Vercel 배포 및 웹 실사용 테스트
강하연은 팀 공식 저장소를 개인 계정 art-ruby로 Fork한 뒤 Vercel에 연결했습니다. Collaborator 권한만 가진 원본 저장소가 Vercel Import 목록에 표시되지 않았기 때문에 Fork를 사용했으며, 배포·테스트 기록은 팀 공식 저장소에 반영했습니다.

항목
확인 결과
Production URL
https://ai-brand-generator-rho.vercel.app/
Root Directory
Web
환경 변수
GEMINI_API_KEY를 Vercel 대시보드에서 설정
헬스체크
{"gemini_key_loaded": true, "status": "ok"}
정상 생성
네이밍 4개, 슬로건, 스토리, 로고 3장, 경쟁사 분석
응답 시간
약 20초 · 60초 이내
필수 입력 누락
프론트엔드에서 차단하고 안내 메시지 표시
반복 요청 429
미실시
컬러 팔레트
저장소 테스트 로그에는 확인 필요로 기록


그림 15. Vercel 빌드 성공 로그

그림 16. Vercel Production 배포 완료 화면
 6. GitHub 협업 기록
주요 역할별 작업은 feature 브랜치와 Pull Request를 통해 main에 병합했습니다. 이후 Vercel 테스트 기록과 Production URL 등 일부 문서 보완은 main 브랜치에 직접 반영되었습니다. 따라서 모든 커밋이 PR을 거쳤다고 표현하지 않고 실제 이력에 맞게 구분했습니다.

PR
담당
주요 변경
결과
#1
조민경
Base/PLAN.md, Web/SERVICE_PLAN.md 검토·확정
병합
#2
오주연
로딩·접근성·인쇄/PDF 스타일
병합
#3
오주연
Violet Nova 최종 UI 디자인
병합
#4
서경환
Markdown 리포트 이미지 삽입 누락 수정
병합
#5
강하연
Base 정상·예외 테스트 및 TEST_LOG 기록
병합

 6.1 조민경 기획 검토

그림 17. 조민경 기획 문서 검토 커밋

그림 18. PR #1 생성 및 검토 내용

그림 19. PR #1 main 병합 완료

그림 20. main 동기화·작업 브랜치 삭제·clean 상태 확인
 6.2 강하연 테스트 PR

그림 21. 강하연 테스트 브랜치 작업 및 Git 기록

그림 22. 강하연 PR #5 병합 결과
 6.3 실제 커밋 반영 기준
· 	조민경: 기획 문서 2개에 23줄 추가 후 PR #1 병합
· 	오주연: UI 관련 5개 커밋, PR #2·#3 병합과 수행 증빙 17장 반영
· 	서경환: 프로젝트 초기 구현, 성능 개선, README 및 PR #4 반영
· 	강하연: PR #5 이후 WEB_TEST_LOG, sample_output.md, Production URL 문서를 main에 추가 반영
 7. 주요 문제와 해결 과정

문제
원인
해결
Gemini SDK 변경
구 SDK google-generativeai 사용 정보
신규 google-genai Client 방식으로 전환
Vercel 응답 지연
다수 API 호출의 순차 실행
ThreadPoolExecutor 병렬화와 maxDuration 60 적용
Vercel 저장소 미노출
원본 저장소 Collaborator 권한
개인 계정으로 Fork 후 Import
Root Directory 오류
Web/api 폴더를 잘못 선택
Web 폴더 자체로 재설정
Preview 로그인 리다이렉트
Vercel Authentication 보호
로그인 상태 확인 및 Production URL 보완
AI 로고 글자 왜곡
이미지 모델의 문자 표현 한계
아이콘과 실제 폰트 wordmark 합성
API 인증 실패
잘못된 키 또는 인증 문제
한국어 오류 안내 후 가능한 단계 계속 진행

 8. 학습 목표 달성 및 결론

학습 목표
달성 근거
브랜드 생성 파이프라인 설명
JSON 입력→검증→LLM/이미지 생성→파일·웹 결과 흐름 구현
텍스트+이미지 API 조합
Gemini 텍스트 모델과 이미지 모델을 한 프로그램에서 사용
컬러 시각화
HEX 컬러를 matplotlib으로 PNG 저장
오류 상황 대응
키 누락·인증·할당량·서버 오류 메시지와 부분 실패 정책 구현
협업 과정 이해
역할별 브랜치, PR, Merge, 테스트·배포 기록 작성
서비스 확장 경험
CLI 기능을 Flask와 Vercel 환경으로 확장

본 프로젝트는 공식 미션의 CLI 요구사항을 충족하면서 경쟁사 분석과 한글·영문 네이밍을 추가하고, 동일한 생성 로직을 웹 서비스로 확장했습니다. 서경환의 전체 구현, 오주연의 UI 개선, 강하연의 테스트·배포 검증, 조민경의 요구사항 분석과 기획 검토가 GitHub 이력으로 구분되어 있습니다.
또한 API 호출은 항상 성공하지 않는다는 전제에서 오류를 사용자 친화적으로 안내하고, 가능한 결과는 계속 반환하도록 설계했습니다. 이를 통해 생성형 AI API 활용뿐 아니라 입력 검증, 파일 저장, 이미지 시각화, 서버리스 배포, 테스트와 Git 협업까지 하나의 개발 과정으로 경험했습니다.

종합 결론  공식 CLI 요구사항, 웹 확장, UI 개선, 테스트·배포, GitHub 협업 기록을 팀원별 증빙과 교차 검증하여 최종 결과보고서에 통합했습니다.

 9. 최종 제출 전 확인표

확인 항목
현재 상태
공식 요구사항과 구현 위치 대조
완료
팀원별 역할과 GitHub 이력 대조
완료
API 키 누락·인증 실패 표현 구분
완료
미실시 테스트의 과장 표현 제거
완료
Vercel Fork 배포 이유와 Production URL 반영
완료
조민경·강하연 증빙 배치
완료
오주연 UI 개선·리디자인·협업 증빙
완료
문서 상태
최종본
