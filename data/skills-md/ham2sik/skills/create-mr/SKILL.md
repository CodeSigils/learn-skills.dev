---
name: create-mr
description: >-
  create Merge Request 워크플로를 수행한다. 현재 브랜치로 GitLab Merge Request 생성에 필요한 정보를 수집·실행한다.
---

# Merge Request 워크플로

현재 브랜치에 대해 GitLab Merge Request(MR)를 생성한다.

## 변수·설정

### {{PROJECT_NAME}} (선택)

| PROJECT_NAME | PROJECT_PATH          |
| ------------ | --------------------- |
| senior       | ~/service/apps/senior |
| komate       | ~/service/apps/komate |
| career-feed  | ~/career-feed         |
| begins       | ~/begins              |

### {{BRANCH_NAME}} (선택)

default: `develop`

## 사용법

- `/create-mr` — 감지된 프로젝트에서 현재 브랜치로 MR 생성
- `/create-mr {{PROJECT_NAME}}` — 특정 프로젝트에서 MR 생성 (예: `/create-mr career-feed`)
- `/create-mr --target-branch {{BRANCH_NAME}}` — 대상 브랜치 지정 (기본값: `develop`)
- `/create-mr {{PROJECT_NAME}} --target-branch {{BRANCH_NAME}}` — 프로젝트와 대상 브랜치를 함께 지정

## 워크플로 단계

### 1. 대상 프로젝트 결정 및 Git 정보 수집

#### 프로젝트명이 주어진 경우

- `{{PROJECT_NAME}}`에서 경로를 찾는다.
- 해당 디렉터리가 존재하고 `.git` 폴더를 포함하는지 확인한다.

#### 프로젝트명이 없는 경우

- 현재 작업 디렉터리에 `.git`이 있으면 그 디렉터리를 프로젝트로 사용
- 모든 **워크스페이스 폴더**들 각각(또는 하위)에서 `.git` 존재 여부를 확인한다.
- `.git`이 있는 각 저장소에서 **미푸시 커밋** 여부 확인
- 미푸시가 여러 저장소에 있으면 사용자에게 어느 프로젝트로 MR을 만들지 질문
- 하나뿐이면 그 프로젝트로 진행
- 모두 없으면 안내 후 종료

### 2. Git 저장소 정보

- 프로젝트 경로로 이동: `cd {{PROJECT_PATH}}`
- **현재 브랜치 이름** 확인:

  ```bash
  git rev-parse --abbrev-ref HEAD
  ```

- 원격 저장소 URL 확인:

  ```bash
  git remote get-url origin
  ```

- 현재 브랜치에 푸시되지 않은 커밋이 있는지 확인:

  ```bash
  git log origin/<현재 브랜치 이름>..HEAD --oneline
  ```

- 미푸시 커밋이 없으면, **이미 원격에 올라간 브랜치만으로 MR을 만들지** 사용자에게 묻는다.

- **MR 설명에 넣을 최근 커밋** 목록:

  ```bash
  git log origin/<대상브랜치>..HEAD --oneline --no-merges
  ```

- **`service` 저장소**일 경우:
  - 변경 파일 경로로 **서브프로젝트(komate, senior)** 를 판별한다
  - 경로에 `apps/komate/` → `komate`, `apps/senior/` → `senior`, `common/design-system` → `design-system`
  - 둘 다 있으면 변경량이 많은 쪽 또는 사용자에게 확인
  - 감지한 서브프로젝트는 이후 **라벨·미리보기 URL 등(5단계)** 에 쓰기 위해 보관한다.

### 3. 대상 브랜치

- `--target-branch`가 있으면 그 브랜치 사용
- 없으면 `git branch -r | grep origin/develop`로 `develop` 존재 시 `develop`
- 없으면 사용자에게 대상 브랜치 요청

### 4. 원격 URL에서 GitLab 프로젝트 정보 추출

- 원격 URL을 파싱하여 다음을 추출합니다:
  - GitLab 호스트 
  - 프로젝트 경로
  - 프로젝트 ID 또는 네임스페이스/프로젝트 경로
- URL에 자격 증명이 포함되어 있으면 API 인증을 위해 이를 추출합니다.
- URL에 자격 증명이 없으면 `GITLAB_TOKEN` 환경 변수를 확인합니다.

### 5. MR 제목, 설명 생성

#### 제목

브랜치명에서 `feature/` 접두어를 제거한 식별자를 제목으로 사용 (예: `feature/car-49` → `car-49`). `feature/`로 시작하지 않으면 브랜치명 전체 사용

#### 설명

- `URL` 섹션
  - <project-url>은 {{PROJECT_NAME}}과 동일, `career-feed`만 `career`로 사용
  - `https://feature-<브랜치ID>.dev.<project-url>.s.co.kr`
- `변경 사항` 섹션: 2단계에서 모은 커밋 메시지를 목록으로 포함
- `체크리스트` 섹션: 형식은 하단 마크다운 예시와 동일
- 포맷 예시

  ```markdown
  ## Preview URL

  https://feature-<branch-id>.dev.<project-url>.s.co.kr

  ## 변경 사항

  - [commit message 1]
  - [commit message 2]

  ## 체크리스트

  - [ ] 코드 리뷰 완료
  - [ ] 테스트 완료
  ```

#### 라벨

기본 `[]`. `service`이고 서브프로젝트가 있으면 `komate` 또는 `senior` 문자열을 배열에 추가

### 6. GitLab API로 MR 생성

- **API Endpoint**: `https://<gitlab-host>/api/v4/projects/<project-id>/merge_requests`
- **Method**: POST
- **Headers**:

  - `Content-Type: application/json`
  - `PRIVATE-TOKEN: <gitlab-token>`

- **Request Body**:

  ```json
  {
    "source_branch": "<current-branch>",
    "target_branch": "<target-branch>",
    "title": "<mr-title>",
    "description": "<mr-description>",
    "labels": ["<detected-project>"],
    "remove_source_branch": true
  }
  ```

- **중요**: `remove_source_branch: true`는 MR이 수락될 때 소스 브랜치를 삭제하는 옵션을 켭니다.
- **라벨**: `service` 프로젝트이고 서브프로젝트가 감지된 경우, 감지된 프로젝트 라벨(`komate` 또는 `senior`)을 포함합니다.
- 서브프로젝트가 없거나 `service`가 아니면 `labels` 배열은 비우거나 생략해도 됩니다.

### 7. 결과 표시

- API call 성공 시 MR URL, 번호, 제목, 적용 라벨 표시
- API call 실패 시 안내 문구 표시

### 8. Slack 알림 전송 (MR 생성 성공 시에만)

- 6단계에서 API로 MR 생성이 **성공한 경우에만** 실행
- `SLACK_WEBHOOK_URL`(또는 MR용 웹훅 환경 변수)이 없으면 **실패만 알리고 워크플로는 성공으로 종료**
- **실행**: 아래 페이로드로 POST 요청

  - **Endpoint**: `SLACK_WEBHOOK_URL`
  - **Method**: POST
  - **Headers**: `Content-Type: application/json`
  - **Request Body** :

    ```json
    {
      "text": "새 MR이 생성되었습니다",
      "blocks": [
        {
          "type": "header",
          "text": {
            "type": "plain_text",
            "text": "🔀 Merge Request 생성",
            "emoji": true
          }
        },
        {
          "type": "section",
          "fields": [
            { "type": "mrkdwn", "text": "*프로젝트:*\n<project-name>" },
            { "type": "mrkdwn", "text": "*MR #:*\n<mr-iid>" },
            {
              "type": "mrkdwn",
              "text": "*브랜치:*\n<source-branch> → <target-branch>"
            },
            { "type": "mrkdwn", "text": "*제목:*\n<mr-title>" }
          ]
        },
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "<https://<gitlab-host>/<project-path>/-/merge_requests/<mr-iid>|MR 링크 열기>"
          }
        }
      ]
    }
    ```

    - `<project-name>`: 워크스페이스 프로젝트명 (service, career-feed 등)
    - `<mr-iid>`, `<source-branch>`, `<target-branch>`, `<mr-title>`, `<gitlab-host>`, `<project-path>`: Step 2~6에서 확보한 값

- **POST 요청 실패 시**: Slack 전송 실패해도 MR 생성 결과는 이미 표시했으므로, 슬랙 전송 실패만 로그/메시지로 알리고 워크플로우는 성공으로 종료

## 주의사항

- **현재 브랜치는 원격에 푸시되어 있어야 함**: MR을 생성하기 전에 현재 체크아웃된 브랜치가 원격 저장소에 푸시되어 있는지 반드시 확인합니다.
- **GitLab 토큰**: GitLab API 호출에 필요합니다. Git 원격 저장소 URL의 자격 증명에 포함하거나, `GITLAB_TOKEN` 환경 변수로 설정할 수 있습니다.
