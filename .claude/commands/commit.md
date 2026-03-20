---
description: "팀 표준에 따라 Conventional Commits 메시지, Claude 기여도 및 자동 서명을 생성합니다."
allowed-tools: [ "Bash(git diff --staged)", "Bash(git commit*)" ]
---
# 커밋 명령어 규칙 (자동 서명 포함)

## 🎯 최종 목표
- **일관성**: 누가 실행하든 동일한 형식의 고품질 커밋 메시지를 생성한다.
- **명확성**: 커밋의 목적과 AI의 기여도를 명확히 기록한다.
- **자동화**: AI 생성 및 공동 저자 정보를 자동으로 포함한다.

## ⚙️ 실행 프로세스 (반드시 순서대로 수행할 것)

1.  **컨텍스트 분석 (가장 중요)**:
    - 현재까지의 **대화 전체 내용**을 검토하여 내가(Claude) 어떤 코드, 로직, 해결책을 제안했는지 파악한다.
    - `git diff --staged` 명령을 실행하여 **최종적으로 반영된 코드 변경사항**을 확인한다.

2.  **기여도 추론**:
    - 위 1단계에서 파악한 '내가 제안한 내용'과 '최종 변경된 코드'를 **비교 분석**한다.
    - 단순 코드 라인 수가 아닌, **로직, 구조, 문제 해결 아이디어**의 기여도를 중심으로 **전체 변경사항 대비 나의 기여도를 백분율(%)로 추론**한다.

3.  **커밋 메시지 생성**:
    - `git diff --staged` 내용을 기반으로 변경사항의 핵심 내용을 요약한다.
    - 아래 **"커밋 메시지 형식"** 규칙을 **반드시** 준수하여 메시지 전체를 작성한다.

4.  **최종 확인**:
    - 생성된 `git commit` 명령어를 사용자에게 보여주고 실행 여부를 확인한다.

## ✍️ 커밋 메시지 형식

### **프로젝트 표준 커밋 메시지 형식**
```
<issue-key> <summary>

<body>
AI-Contribution: <percentage>%

Co-Authored-By: Claude <noreply@anthropic.com>
```
### **규칙**
- **`<issue-key>`**: Jira 이슈 키 (예: `CLM-2463`)
    - 현재 브랜치명에서 추출하거나, 관련 이슈가 있는 경우 명시
    - 브랜치명 예시: `feature/CLM-2555-db-failover` → `CLM-2555`
- **`<summary>`**:
    - 50자 이내의 한글 요약
    - 명령문으로 작성 (예: `추가` not `추가함`)
    - 변경사항의 핵심을 간결하게 표현
- **`<body>`** (선택사항):
    - `-`로 시작하는 주요 변경사항 나열
    - 어떻게(How)보다는 **무엇을(What), 왜(Why)** 변경했는지 설명
    - 마지막 줄에 AI-Contribution 표시
- **`AI-Contribution`**:
    - 2단계에서 추론한 AI 기여도를 백분율로 표시
    - 형식: `AI-Contribution: 85%`
        - 로직, 구조, 문제 해결 아이디어 기준으로 판단
    - body의 마지막 줄에 위치 (Co-Authored-By 앞에 빈 줄 필요)
- **`Co-Authored-By`**:
    - AI가 코드 작성에 기여한 경우 항상 추가
    - 형식: `Co-Authored-By: Claude <noreply@anthropic.com>`
        - Git trailer 규칙에 따라 AI-Contribution과 빈 줄로 구분

### **키워드 (참고용)**
- `feature`: 기능 추가
- `bugsfix`: 버그 수정
- `refactor`: 리팩토링
- `test`: 테스트
- `docs`: 문서

### **예시**
```
CLM-2555 DB failover 안정성 개선을 위한 타임아웃 설정 조정

- connection-timeout 9초에서 30초로 증가
- socket-timeout 30초 추가 설정
- max-lifetime 10분에서 30분으로 증가
- 장애 감지 시간 1초에서 3초로 조정
- failoverTimeoutMs 30초 추가
- JVM DNS 캐시 TTL 설정 추가 (positive: 60초, negative: 10초)
AI-Contribution: 85%

Co-Authored-By: Claude <noreply@anthropic.com>
```