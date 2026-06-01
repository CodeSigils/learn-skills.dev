---
name: sync-docs
description: 프로젝트 중간에 `PRD.md`, `TODO.md`, `CONTEXT.md`, `DESIGN.md`, `README.md`, `AGENTS.md`, `CLAUDE.md` 같은 문서가 현재 구현 상태와 어긋났는지 확인하고 맞춘다. 사용자가 "문서 정리해줘", "현재 상태 반영해줘", "TODO 업데이트해줘", "중간 점검하자"라고 할 때 사용한다.
---

# 문서 동기화 (Sync Docs)

목표: 문서와 실제 프로젝트 상태를 다시 맞춘다.

새 기능을 구현하지 않는다. 코드 변경은 문서와 명백히 충돌하는 이름/설명 정리처럼 아주 작은 경우에만 한다.

## 읽을 것

있는 것만 읽는다.

- `PRD.md`
- `TODO.md`
- `CONTEXT.md`
- `DESIGN.md`
- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/agents/starter-skills.md`
- 현재 앱을 이해하는 데 필요한 주요 파일

없다고 바로 만들지 않는다. 필요한 이유가 있을 때만 만든다.

## 확인할 것

- `PRD.md`의 목표가 아직 현재 목표인가?
- `TODO.md`의 `지금 할 일(Now)`, `다음 할 일(Next)`, `나중에 할 일(Later)`이 현재 구현 상태와 맞는가?
- 완료된 TODO가 아직 미체크(unchecked) 상태인가?
- 구현하면서 새로 생긴 사용자가 볼 수 있는 동작(user-visible behavior)이 TODO/PRD에 빠졌는가?
- `CONTEXT.md`의 용어와 UI/문서/코드 용어가 충돌하는가?
- `DESIGN.md`의 색, 폰트, 컴포넌트 규칙과 현재 UI가 크게 어긋나는가? 실제 디자인 변경은 `apply-design`에서 처리해야 하는가?
- `README.md`, `AGENTS.md`, `CLAUDE.md`가 현재 실행 방법, 프로젝트 설명, 에이전트 작업 규칙과 충돌하는가?
- 사내망 앱인데 README, TODO, 보고 문구가 다른 사람의 접속 주소를 `localhost`로 안내하고 있지 않은가?
- `AGENTS.md`와 `CLAUDE.md`의 `Starter Skills` 섹션이 같은 내용인가?

## 업데이트 규칙

- 완료된 TODO는 체크한다.
- 더 이상 맞지 않는 TODO는 지우지 말고 수정하거나 `나중에 할 일(Later)`로 옮긴다.
- 새 아이디어는 바로 구현하지 말고 `나중에 할 일(Later)`에 둔다.
- `CONTEXT.md`에는 안정된 도메인 용어(stable domain term)만 넣는다. 구현 세부사항(detail)은 넣지 않는다.
- `DESIGN.md`는 사실 오류나 파일 경로 같은 작은 정정만 한다. 색, 폰트, 컴포넌트 기준 변경이나 UI 적용은 `apply-design`으로 넘긴다.
- README는 실행/사용 방법이 틀렸을 때만 고친다.
- `AGENTS.md`와 `CLAUDE.md`의 `Starter Skills` 섹션은 같은 내용으로 맞춘다.
- 둘 중 하나에만 `Starter Skills` 섹션이 있으면 다른 파일에도 같은 섹션을 추가한다.

## 완료 형식

```markdown
## 동기화 완료 (Synced)

**업데이트한 것(Updated):** ...
**해결한 충돌(Conflicts fixed):** ...
**아직 불명확한 것(Still unclear):** ...
**다음 TODO(Next TODO):** ...
```
