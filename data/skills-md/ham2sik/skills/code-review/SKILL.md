---
name: code-review
description: >-
  커밋 없이 스테이징된 변경에 대해 AI 코드 리뷰를 수행한다.
---

# 코드 리뷰 워크플로

커밋 없이 스테이징된 변경에 대해 AI 코드 리뷰를 수행한다.

## 변수·설정

### `{{PROJECT_NAME}}` (선택)

특정 프로젝트의 스테이징된 변경만 리뷰한다.

```markdown
| PROJECT_NAME | PROJECT_PATH          |
| ------------ | --------------------- |
| senior       | ~/service/apps/senior |
| komate       | ~/service/apps/komate |
| career-feed  | ~/career-feed         |
| begins       | ~/begins              |
```

### `LOG_PATH` (선택)

아래 **순서대로** 하나만 쓴다.

1. **환경 변수 `LOG_PATH`** (비어 있지 않으면 사용). Cursor **`settings.json`**의 `terminal.integrated.env.linux`(또는 macOS는 `osx`, Windows는 `windows`)에 넣어 두면 통합 터미널 등에서 주입된다.
2. 없으면 **`~/.config/Cursor/User/settings.json`** 을 Read 도구로 연 뒤 JSON을 파싱한다. 경로는 환경에 따라 다를 수 있으니, 없으면 `Cursor/User/settings.json`을 탐색한다.
   - `terminal.integrated.env.linux.LOG_PATH` (Linux)
   - Linux가 아니면 같은 파일의 `terminal.integrated.env.osx` / `terminal.integrated.env.windows` 안의 `LOG_PATH`
3. 위까지 없거나 빈 문자열이면 로그를 생략하고, 5단계에서 채팅에 한 줄로만 안내한다.

## 워크플로 단계

### 1. 대상 저장소·스테이징 확인

**프로젝트명이 주어진 경우**

- `{{PROJECT_NAME}}`에서 경로를 찾는다.
- 해당 디렉터리가 존재하고 `.git` 폴더를 포함하는지 확인한다.
- 해당 디렉터리에서 실행:

  ```bash
     cd <project-path> && git status && echo "=== STAGED CHANGES ===" && git diff --cached
  ```

**프로젝트명이 주어지지 않은 경우**

- **`commit` SKILL**에서 실행한 경우 **1. 대상 저장소·스테이징 확인**이 이미 되어 있으므로, 바로 2번으로 실행한다.
- 모든 **워크스페이스 폴더**들 각각(또는 하위)에서 `.git` 존재 여부를 확인한다.
- 스테이징이 있는 저장소만 나열하고 `git diff --cached --stat`(또는 전체 diff)로 맥락을 수집한다.
- **스테이징이 둘 이상 저장소에 있으면** 사용자에게 어느 저장소(들)를 리뷰할지 묻는다.
- 스테이징이 없으면 안내하고 **종료**한다.

### 2. 리뷰할 스테이징 파일을 읽는다.

- 스테이징 파일에 대해 아래 기준으로 구분하여 내용을 읽는다.
  - **읽을 파일**: 소스 코드 (`.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.scss`, `.json`, `.md` 등)
  - **건너뛸 파일**: 바이너리(이미지·폰트 등), 매우 큰 파일(100KB 초과), 리뷰가 불필요한 생성물

### 3. AI 코드 리뷰를 수행한다.

#### React 성능 리뷰 (React/Next.js 파일)

- **`react-best-practices` SKILL**을 찾아서 실행한다.

#### 일반 코드 리뷰 (모든 파일)

- **`context7` MCP** 도구를 사용하여 최신 문서와 모범 사례(Best Practice)를 먼저 조회한다.
- 코드 품질·잠재 버그·모범 사례를 분석한다.
- 다음을 점검한다:

  - **ESLint 위반**: 스테이징 코드가 프로젝트 ESLint 설정과 맞는지
  - **Prettier 포맷**: Prettier 설정과 포맷이 일치하는지
  - **TypeScript**: `tsconfig.json` 기준 타입 안전성(오류·누락 타입 등)
  - 보안 취약점 (XSS, SQL injection, 민감 데이터 노출)
  - 도구 설정에 따른 코드 스타일 일관성(네이밍·포맷)
  - 누락된 오류 처리 (try-catch, null 검사)
  - 접근성 (aria-label, 키보드 내비게이션 등)
  - React 모범 사례 (훅 의존성, 컴포넌트 구조)
  - Next.js 패턴 (서버/클라이언트 컴포넌트 적절성)

- 발견 사항은 간결한 형식으로 제시한다:

  - **🔴 CRITICAL**: 성능 이슈(Waterfall, 번들 크기) — 커밋 전 수정 권장
  - **🟡 HIGH**: 서버 측 성능 — 수정 권장
  - **🟢 MEDIUM**: 리렌더·렌더링 최적화 — 검토 후 수정
  - **⚪ LOW**: JS 미세 최적화 — 여유 시

- 각 이슈마다 다음을 제시한다:
  - 파일·줄 번호
  - 이슈 설명
  - (성능 이슈의 경우) 수정 전/후가 담긴 수정 제안
  - (성능 이슈의 경우) 기대 영향

### 4. 코드 리뷰 요약을 제시한다.

- 리뷰한 모든 프로젝트의 발견 사항을 요약한다.
- 반드시 다뤄야 할 치명적 이슈를 강조한다.
- 실행 가능한 권고를 제시한다.
- **커밋으로 진행하지 않는다** — 이 커맨드는 리뷰 전용이다.

### 5. 코드 리뷰 요약을 로그 파일에 남긴다.

- **LOG_PATH**는 `변수·설정`의 `LOG_PATH` 규칙대로 구한다. 값이 없으면 로그를 생략하고 채팅에 한 줄로만 안내한다.
- 있으면 `mkdir -p "{{LOG_PATH}}/{{PROJECT_NAME}}"` 후 `"{{LOG_PATH}}/{{PROJECT_NAME}}/code-review.md"`에 **4단계까지 채팅에 제시한 리뷰 본문**을 마크다운으로 **append**한다. `{{PROJECT_NAME}}`이 없으면 1단계 Git 저장소 루트의 디렉터리명을 쓴다. 새 기록 위에 날짜·시간(ISO 8601 권장)과 리뷰 대상 저장소 경로를 짧게 붙인다.

## 중요 사항

- **이 커맨드는 코드 리뷰만 수행한다** — 변경을 커밋하지 않는다.
- **코드 분석 도구**: 리뷰 전에 항상 프로젝트의 ESLint, Prettier, TypeScript 등 설정을 확인·반영한다.
- 리뷰 결과는 실행 가능하고 구체적이어야 한다.
