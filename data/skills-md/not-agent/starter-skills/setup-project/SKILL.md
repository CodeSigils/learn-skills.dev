---
name: setup-project
description: 프로젝트마다 Starter Skills가 읽을 로컬 문서 위치, 실행 명령, 접속 방식, AGENTS.md와 CLAUDE.md의 Starter Skills 섹션을 기본값으로 세팅한다. `/setup-project`만 입력하면 바로 기본 설정을 쓰고, `/setup-project <설명>`이면 설명을 반영한다.
disable-model-invocation: true
---

# 프로젝트 설정 (Setup Project)

목표: `/setup-project`만 입력해도 새 프로젝트에 필요한 기본 설정을 바로 만든다.

이 스킬은 앱을 바로 구현하지 않는다. 아이디어를 구체화하거나, PRD/TODO를 만들거나, 앱 형태와 기술 스택을 정하지 않는다. 프로젝트별 실행 환경과 작업 규칙만 탐색하고 `AGENTS.md`, `CLAUDE.md`, `docs/agents/starter-skills.md`에 기록한다.

`PRD.md`, `TODO.md`, `CONTEXT.md`, `DESIGN.md`는 이 단계에서 만들지 않는다. 각각 `/write-prd`, `/write-todo`, 용어가 흔들릴 때, `/apply-design`에서 만든다.

## 입력 형태 (Invocation)

- `/setup-project`: 기본값으로 바로 쓴다. 확인 질문을 하지 않는다.
- `/setup-project <설명>`: 설명에 들어 있는 실행 환경, 명령, 접속 방식을 반영하고 바로 쓴다.
- 추가 질문은 설명이 서로 충돌하거나, 파일을 안전하게 업데이트할 수 없을 때만 한다.

## 진행 절차 (Workflow)

### 1. 빠르게 확인 (Explore)

현재 프로젝트에서 있는 것만 확인한다. 추측하지 않는다.

- 현재 디렉토리가 프로젝트 루트(root)인지
- 현재 OS가 Windows, macOS, Linux/WSL 중 무엇인지
- `AGENTS.md`, `CLAUDE.md`가 있는지, 기존 `Starter Skills` 섹션이 있는지
- `docs/agents/starter-skills.md`가 있는지
- `PRD.md`, `TODO.md`, `CONTEXT.md`, `DESIGN.md`, `README.md`가 있는지
- `package.json`, `Makefile`, `justfile`, `pyproject.toml` 등에서 실행 명령을 알 수 있는지
- 사용자가 사내망, 회사 내부, 여러 명 접속, Windows CMD 같은 실행 환경을 언급했는지

### 2. 기본값 정하기 (Defaults)

묻지 말고 다음 기본값을 쓴다.

- 로컬 문서(Local Documents): `PRD.md`, `TODO.md`, 필요한 경우 `CONTEXT.md`, `DESIGN.md`
- 환경 전제(Environment Assumptions): Node.js, Python, Git
- 추가 서비스(Extra services): 없음
- Shell: Windows는 `CMD`, macOS는 `zsh`, Linux/WSL은 `bash` 중 현재 OS에 맞는 하나
- 실행 명령(Commands): 실제 파일에서 확인한 명령만 기록하고, 없으면 `Unknown`
- 접속 방식(Access Mode): `Network-ready`
- 사용자 주소(User URL): `http://<network IPv4>:3000`
- 로컬 주소(Local URL): `http://localhost:3000`은 같은 PC에서 확인할 때만 쓴다.

`Unknown`은 모른다는 뜻이 아니라 "명령을 지어내지 않았다"는 뜻이다.

### 3. 부가 설명 반영 (Apply User Notes)

사용자가 `/setup-project <설명>` 형태로 준 말은 설정에 반영한다.

- "사내망", "회사 내부", "여러 명 접속"이 있으면 Access Mode는 `Intranet`으로 둔다.
- User URL은 `http://<network IPv4>:3000` 형식으로 둔다. 사내망이면 `http://<사내망 IPv4>:3000`이라고 적어도 된다. `localhost`를 사용자 주소나 공유 주소로 기록하지 않는다.
- "Windows CMD"가 있으면 Shell은 `CMD`로 둔다. PowerShell 전용 명령을 쓰지 않는다고 기록한다.
- macOS가 확인되면 Shell은 `zsh`로 둔다.
- Linux/WSL이 확인되면 Shell은 `bash`로 둔다.
- 사용자가 `npm run dev`, `npm run build`, `npm run start`, `npm test` 같은 명령을 말하면 해당 명령을 기록한다.
- 문서 위치를 말하면 Local Documents에 반영한다.

설명이 앱 아이디어, 앱 형태, 데이터 저장, 라이브러리 선택에 관한 내용이면 여기서 결정하지 않는다. `write-prd`에서 사용할 수 있도록 "제품/기술 전제는 PRD에서 다룬다"고만 보고한다.

### 4. 꼭 필요할 때만 묻기 (Ask Only If Blocked)

기본값으로 안전하게 쓸 수 있으면 묻지 않는다. 질문은 파일 쓰기를 막는 경우에만 한다.

질문해도 되는 경우:

- 현재 디렉토리가 프로젝트 루트인지 판단할 수 없고 다른 후보가 명확할 때
- 기존 `Starter Skills` 섹션이 손상되어 자동 업데이트가 위험할 때
- 사용자가 한 설명 안에서 접속 방식이나 명령이 서로 충돌할 때

질문은 한 번에 하나만 한다. 단순히 명령을 찾지 못했다는 이유로 묻지 말고 `Unknown`으로 둔다.

### 5. 쓰기 (Write)

확인받지 말고 바로 쓴다. 사용자가 "미리 보여줘", "쓰기 전에 확인해줘"라고 했을 때만 쓰기 전에 보여준다.

`AGENTS.md`와 `CLAUDE.md`를 둘 다 만든다. 이미 있으면 사용자 내용을 보존하고 `<!-- starter-skills:agents:start -->`부터 `<!-- starter-skills:agents:end -->`까지의 `Starter Skills` 섹션만 추가하거나 업데이트한다.

두 파일의 `Starter Skills` 섹션은 같은 내용이어야 한다.

`docs/agents/starter-skills.md`를 만들거나 업데이트한다. 이 파일은 다른 Starter Skills가 프로젝트 설정을 확인할 때 읽는 파일이다.

## AGENTS.md와 CLAUDE.md Starter Skills 섹션

```markdown
<!-- starter-skills:agents:start -->
# AGENTS

이 문서는 AI 코딩 에이전트가 이 프로젝트에서 작업할 때 따라야 할 공통 지침이다.

## Starter Skills

이 프로젝트는 Starter Skills 흐름을 사용한다. 프로젝트별 설정은 `docs/agents/starter-skills.md`를 먼저 확인한다. 여기에는 로컬 문서 위치, 실행 명령, OS별 Shell, 사용자 URL, 환경 전제가 기록된다.

## 작업 흐름 (Workflow)

기본 순서: `setup-project -> 바로 사용자 요청 처리`

필요한 경우에만 별도 스킬을 사용한다.

- 제품 결정을 문서로 남기려면 `write-prd`
- PRD를 구현 순서로 나누려면 `write-todo`
- 디자인 기준이 필요하면 `apply-design`
- 문서와 실제 구현이 어긋나면 `sync-docs`
- 버그나 이상 동작은 `diagnose`
- 새 기능 없이 코드만 정리할 때는 `refactor`

## 작업 방식 (Working Rules)

- 제품 동작을 바꾸기 전에 `PRD.md`가 있으면 먼저 읽는다.
- 구현 요청을 처리하기 전에 `TODO.md`가 있으면 먼저 읽는다.
- 사용자가 TODO 번호를 지정하면 해당 TODO만 구현한다.
- 요청하지 않은 기능을 덧붙이지 않는다.
- 기존 파일 구조와 코드 스타일을 우선 따른다.
- `CONTEXT.md`가 있으면 그 용어를 사용하고 동의어(synonym)를 새로 만들지 않는다.
- UI나 스타일을 바꾸기 전에 `DESIGN.md`가 있으면 먼저 읽는다.
- 사용자에게 안내하는 URL은 `localhost`가 아니라 `http://<network IPv4>:3000` 형식의 네트워크 주소를 기본으로 사용한다.
- `localhost`는 같은 PC에서 확인할 때만 쓴다.

## 검증 (Validation)

- TODO는 `TODO.md`의 완료 기준(Done Rule)을 만족하기 전까지 완료가 아니다.
- 재현하지 못한 문제는 수정했다고 말하지 않는다.
- 확인하지 못한 것은 명확히 적는다.

<!-- starter-skills:agents:end -->
```

## docs/agents/starter-skills.md 형식

```markdown
# Starter Skills Project Setup

## 로컬 문서 (Local Documents)

- PRD: `PRD.md`
- TODO: `TODO.md`
- Context: `CONTEXT.md` when needed
- Design: `DESIGN.md` when needed

## 실행 명령 (Commands)

- Install: Unknown
- Dev: Unknown
- Build: Unknown
- Start: Unknown
- Test: Unknown
- Typecheck: Unknown

Unknown은 명령을 지어내지 않았다는 뜻이다.

## 환경 전제 (Environment Assumptions)

- 시스템 도구(System tools): Node.js, Python, Git
- Shell: `<Windows CMD | macOS zsh | Linux/WSL bash>`
- 추가 서비스(Extra services): 없음

## 접속 방식 (Access Mode)

- Mode: Network-ready
- User URL: `http://<network IPv4>:3000`
- Local URL: `http://localhost:3000` (same machine only)

User URL은 사용자가 접속하거나 다른 사람에게 안내할 주소다. `localhost`를 User URL로 기록하지 않는다.
```

명령, Shell, 네트워크 IPv4가 확인되면 `Unknown`이나 placeholder를 실제 값으로 바꾼다.

## 완료 (Done)

사용자에게 이렇게 말한다.

```markdown
프로젝트 설정을 기록했습니다.

이제 바로 만들 작업을 요청하면 됩니다.
```
