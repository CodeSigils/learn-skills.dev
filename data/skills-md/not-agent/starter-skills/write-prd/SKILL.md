---
name: write-prd
description: 현재 대화에서 결정된 제품 방향, 앱 형태, 데이터 필요, 사용 환경을 로컬 `PRD.md`로 작성하거나 업데이트한다. GitHub 이슈(issue)를 만들지 않는다. 사용자가 "PRD 만들어줘", "문서로 정리해줘", "지금까지 정리해줘"라고 할 때 사용한다.
---

# PRD 작성 (Write PRD)

목표: 이미 결정된 내용을 `PRD.md`에 쓴다. 새 인터뷰를 시작하지 않는다.

필수 정보가 없으면 한 번에 하나만 물어본다. 많이 비어 있으면 PRD를 바로 쓰지 말고, 질문 하나를 하거나 `/clarify-idea`를 제안한다.

## 진행 절차 (Workflow)

1. 기존 `PRD.md`가 있으면 읽는다.
2. `docs/agents/starter-skills.md`가 있으면 실행 환경과 접속 방식을 확인한다.
3. 기존 `CONTEXT.md`가 있으면 용어를 따른다.
4. 현재 대화에서 결정된 내용만 `PRD.md`에 반영한다.
5. 같은 개념을 여러 이름으로 부르면 하나를 고르고, 필요하면 `CONTEXT.md`를 만들거나 업데이트한다.
6. 구현 세부 파일명, 코드 조각(code snippet)은 PRD에 넣지 않는다. 단, 앱 형태, 데이터 저장 방식, 사내망 접속, Next.js/SQLite 같은 기술 전제가 제품 사용 방식과 실행 방식에 영향을 주면 기록한다.
7. 끝나면 다음 단계로 `/write-todo`를 제안한다.

## 앱 형태와 기술 전제 (App Shape and Technical Baseline)

앱 형태, 데이터 필요, 기술 전제는 `setup-project`에서 만들지 않는다. `clarify-idea` 대화나 사용자의 직접 요청으로 충분히 결정된 뒤 이 스킬에서 PRD에 기록한다.

기술 전제가 이미 정해졌거나 사용자가 추천을 요청하면 [references/LIBRARY_MAP.md](./references/LIBRARY_MAP.md)에서 관련 카테고리만 참고한다. 전체 문서를 한 번에 읽지 않는다. 이 문서는 SaaS나 외부 서비스 후보표가 아니라 앱 기능과 화면 완성도를 높이는 라이브러리 후보표다.

흔한 앱 형태가 명확하면 [mvp-library-stack.md](./mvp-library-stack.md)를 읽고, 필요한 경우 하나의 preset만 참고한다.

- 저장 없는 UI: [preset-local-ui.md](./preset-local-ui.md)
- 사내 대시보드: [preset-intranet-dashboard.md](./preset-intranet-dashboard.md)
- 사내 CRUD + SQLite: [preset-intranet-crud-sqlite.md](./preset-intranet-crud-sqlite.md)
- 백엔드/API: [preset-backend-api.md](./preset-backend-api.md)
- 데이터 리포트: [preset-data-report.md](./preset-data-report.md)

선택할 근거가 부족하면 preset을 고르지 않는다. 멋있어 보인다는 이유만으로 DB, ORM, 상태관리(state management), 데이터 패칭(data fetching), 인증/결제/메일 발송 같은 서비스 연동을 넣지 않는다.

라이브러리를 PRD에 기록할 때는 "왜 필요한지"와 "이번에 넣지 않는 것"을 함께 적는다. 최신 API나 설치 명령은 구현 직전에 공식 문서로 확인한다.

## PRD.md 형식 (PRD.md Format)

```markdown
# PRD

## 목표 (Goal)

무엇을 만들기로 했는가?

## 사용자 (User)

누구를 위한 것인가?

## 문제 (Problem)

사용자는 어떤 문제를 겪는가?

## 첫 버전 (First Version)

첫 번째로 사용할 수 있는 버전은 무엇을 해야 하는가?

## 사용자 흐름 (User Flow)

1. 사용자가 ...
2. 사용자가 ...
3. 사용자는 ...를 본다

## 성공 확인 (Success Check)

동작한다고 어떻게 확인할 것인가?

## 사용 환경 (Usage Environment)

어디서 누가 접속하는가? 앱 형태, 데이터 필요, 접속 방식을 기록한다. 예: 개인 로컬, 사내망, 대시보드, SQLite 필요.

## 기술 전제 (Technical Baseline)

이미 결정된 실행 방식이나 라이브러리 전제만 기록한다. 정해진 것이 없으면 `미정`으로 둔다.

## 이번에 하지 않을 것 (Not Doing Yet)

- ...

## 열린 질문 (Open Questions)

- ...
```

## CONTEXT.md 규칙 (CONTEXT.md Rule)

안정된 도메인 용어(stable domain term)가 있을 때만 `CONTEXT.md`를 만들거나 업데이트한다. 짧게 유지한다.

```markdown
# 프로젝트 맥락 (Project Context)

## 용어 (Language)

**용어(Term)**:
한두 문장으로 정의한다.
_피할 표현(Avoid)_: 애매한 동의어(synonym)

## 관계 (Relationships)

- **용어(Term)** 하나는 여러 **다른 용어(Other Terms)**를 가진다.

## 애매한 표현 (Flagged Ambiguities)

- "예전 표현"이 X와 Y를 모두 뜻하는 데 쓰였다. 결정: X에는 **용어(Term)**를 쓴다.
```

`CONTEXT.md`는 PRD도 아니고 구현 계획(implementation plan)도 아니다.

## 완료 후

마지막에 다음 한 줄을 덧붙인다.

> 다음 단계는 `/write-todo`입니다. `PRD.md`를 작은 구현 순서로 나눕니다.
