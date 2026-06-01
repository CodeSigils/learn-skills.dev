---
name: refactor
description: 새 기능을 추가하지 않고 현재 동작을 유지한 채 코드 구조, 중복, 이름, 파일 책임을 정리한다. 사용자가 "정리해줘", "리팩터링해줘", "코드가 지저분해졌어", "기능 추가 없이 구조만 개선해줘"라고 할 때 사용한다.
---

# 리팩터링 (Refactor)

목표: 동작을 바꾸지 않고 코드를 정리한다.

리팩터링(refactor)은 새 기능 구현으로 번지기 쉽다. 이 스킬(skill)에서는 새 기능을 추가하지 않는다.

## 변경 전 (Before Changing)

먼저 짧게 선언한다.

```markdown
## 리팩터링 범위 (Refactor Scope)

**유지할 동작(Keep behavior):** ...
**바꿀 것(Will change):** ...
**바꾸지 않을 것(Will not change):** ...
**변경 전 확인(Baseline check):** ...
**변경 후 확인(Check after):** ...
```

가능하면 변경 전에 현재 앱 실행, 테스트, 타입 검사, 또는 가장 가까운 사용자 흐름으로 기준 동작(baseline behavior)을 확인한다. 확인하지 못하면 `변경 전 확인(Baseline check)`에 못 했다고 적는다.

사용자가 볼 수 있는 동작(user-visible behavior)이 바뀔 가능성이 있으면 먼저 확인한다.

## 허용되는 변경

- 중복 제거
- 파일/함수 이름 명확화
- 너무 긴 파일 나누기
- 같은 역할의 코드 모으기
- 미사용 코드(dead code) 제거
- `CONTEXT.md` 용어와 맞지 않는 이름 정리

## 금지

- 새 기능 추가
- TODO 새 항목 구현
- UI 흐름(UI flow) 변경
- 데이터 모델(data model) 변경
- 의존성(dependency) 추가
- 디자인 변경

필요하면 리팩터링(refactor)을 멈추고 별도 TODO로 제안한다.

## 변경 후 (After Changing)

변경 전 적은 `변경 후 확인(Check after)`을 실제로 실행한다. 가능하면 `변경 전 확인(Baseline check)`과 같은 방식으로 비교한다. 확인하지 못하면 못 했다고 말한다.

## 완료 형식

```markdown
## 리팩터링 완료 (Refactored)

**바꾼 것(Changed):** ...
**유지한 동작(Behavior kept):** ...
**변경 전 확인(Baseline checked):** ...
**확인한 것(Checked):** ...
**확인하지 못한 것(Not checked):** ...
**후속 TODO(Follow-up TODO):** ...
```
