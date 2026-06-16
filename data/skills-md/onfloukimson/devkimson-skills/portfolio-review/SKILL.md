---
name: portfolio-review
description: Analyzes developer portfolios, resumes, and project showcase pages for technical writing quality, problem-solving narrative, architecture decisions, quantified impact, hiring competitiveness, and design polish. Use when reviewing portfolios, resumes, project introduction pages, or when the user asks for portfolio feedback, resume critique, 채용 경쟁력, or hiring competitiveness assessment.
---

# Portfolio Review

## When to Use This Skill

Use this skill when the user asks to review, audit, critique, or improve a developer portfolio, resume, project introduction page, or case study.

Accept URLs, screenshots, rendered pages, markdown/text content, PDF resumes, or a combination as evidence. Do not rewrite the portfolio by default. Analyze first, then suggest improvements.

## Inputs

Inspect available artifacts and identify:

- target role and seniority (if stated)
- primary tech stack and domain
- portfolio type (personal site, Notion, PDF resume, GitHub README, etc.)
- projects presented and their business context
- visual design evidence (screenshots or live page)
- quantitative claims and supporting metrics

If role or audience context is missing, state minimum assumptions before scoring.

## Core Philosophy

좋은 포트폴리오는 기술을 나열하는 문서가 아니다.

좋은 포트폴리오는 다음을 설명해야 한다.

1. 어떤 문제가 있었는가
2. 왜 해당 방법을 선택했는가
3. 어떻게 해결했는가
4. 어떤 결과를 얻었는가
5. 그 경험이 다음 프로젝트에 어떤 영향을 주었는가

기술 스택 나열보다 문제 해결 능력 전달을 우선한다.

## Review Workflow

1. Read all provided content end-to-end before scoring.
2. For each project section, check: problem → why → how → result → learning.
3. Run Special Detection Rules (below) on every project block.
4. Score each review category independently, then compute Overall Score.
5. Produce output using the exact Output Format section. Do not omit sections.
6. Write Technical Writing Review with concrete Original → Suggested rewrites.
7. Respond in Korean unless the portfolio is entirely in another language.

## Review Categories

### 1. Technical Writing

검토 항목

* 기술 설명 명확성
* 기술 용어 사용 적절성
* 문장 자연스러움
* 인간이 작성한 것 같은 서술 여부
* AI 생성 문체 여부

평가 기준

Bad

"NestJS를 사용하여 API를 개발했습니다."

Good

"기존 중복 비즈니스 로직을 모듈화하여 유지보수 비용을 줄였으며 NestJS 기반 API 구조를 재설계했습니다."

### 2. Problem Solving

검토 항목

* 문제 정의 존재 여부
* 문제 원인 분석 여부
* 해결 과정 설명 여부
* 해결 결과 설명 여부

탐지 규칙

만약

"무엇을 만들었다"

만 존재하고

"왜 만들었는가"

가 없다면 경고 출력

### 3. Architecture Review

검토 항목

* 시스템 구조 설명
* 설계 의사결정
* 트레이드오프 설명
* 기술 선택 이유

탐지 예시

Bad

"Redis 사용"

Good

"조회 빈도가 높은 데이터를 Redis 캐시로 분리하여 DB 부하를 감소시켰다."

### 4. Impact Analysis

검토 항목

* 정량적 성과
* 성능 개선 수치
* 운영 효율성
* 비용 절감 효과

경고 조건

다음이 없는 경우

* %
* ms
* 초
* 건수
* 비용
* 사용자 수

경고 출력

"정량적 성과 수치 부족"

### 5. Recruiter Review

채용 담당자 관점

질문

* 어떤 사람인지 보이는가
* 어떤 업무를 수행할 수 있는가
* 어느 수준의 개발자인가
* 회사에서 바로 활용 가능한가

평가

0 ~ 10

### 6. CTO Review

CTO 관점

질문

* 문제 해결 능력이 보이는가
* 설계 능력이 보이는가
* 운영 경험이 보이는가
* 리스크 대응 경험이 보이는가

평가

0 ~ 10

### 7. Portfolio Design Review

검토 항목

#### 감점 요소

* 과도한 애니메이션
* 과도한 그라데이션
* 네온 스타일
* 과도한 그림자
* 과도한 기술 뱃지
* Progress Bar 남발
* GitHub Stats 남발
* 카드 높이 불균형
* 정보 밀도 과다

#### 가산 요소

* 충분한 여백
* 일관된 디자인 시스템
* Before / After 비교
* 실제 서비스 캡처
* 아키텍처 다이어그램
* 프로젝트별 핵심 수치
* 문제 → 해결 → 결과 구조

## Special Detection Rules

다음 문장을 발견하면 개선 제안

"개발"
"구축"
"구현"
"적용"

만 존재하고

문제 정의가 없을 경우

출력

"행위 중심 서술입니다. 문제와 해결 과정을 추가하세요."

추가 탐지 규칙:

- 기술 스택만 나열하고 맥락이 없으면 → "기술 나열 중심입니다. 각 기술이 해결한 문제를 연결하세요."
- 모든 프로젝트 설명 길이가 동일하고 톤이 균일하면 → AI 생성 문체 의심을 Technical Writing Review에 명시
- 성과 수치가 있으나 기준·측정 방법이 없으면 → 신뢰도 경고를 Impact Analysis에 포함

## Scoring Guide

### Overall Score (총점 /100)

| 영역 | 배점 |
|------|------|
| Technical Writing | 15 |
| Problem Solving | 20 |
| Architecture Review | 15 |
| Impact Analysis | 15 |
| Recruiter Review | 10 |
| CTO Review | 10 |
| Portfolio Design Review | 15 |

Recruiter Review와 CTO Review는 각 0~10 점수를 그대로 Overall Score에 반영한다.

### Final Verdict Sub-scores

각 항목 0~10. Overall Score와 독립적으로 평가하되 일관성을 유지한다.

- 스토리텔링: Problem Solving + Technical Writing 종합
- 기술 전달력: Technical Writing + Architecture
- 설계 역량: Architecture Review + CTO Review
- 문제 해결력: Problem Solving + CTO Review
- 디자인 완성도: Portfolio Design Review
- 채용 경쟁력: Recruiter Review + Impact Analysis

## Output Format

아래 형식을 **정확히** 따른다. 섹션을 생략하지 않는다.

## Overall Score

총점: X/100

---

## Strengths

* ...
* ...
* ...

---

## Weaknesses

* ...
* ...
* ...

---

## Technical Writing Review

### Original

...

### Suggested

...

---

## Problem Solving Review

...

---

## Architecture Review

...

---

## Design Review

...

---

## Recruiter Review

...

---

## CTO Review

...

---

## Improvement Priority

### High

...

### Medium

...

### Low

...

---

## Final Verdict

포트폴리오 경쟁력 점수

스토리텔링: X/10
기술 전달력: X/10
설계 역량: X/10
문제 해결력: X/10
디자인 완성도: X/10
채용 경쟁력: X/10

## Decision Rules

1. Judge against hiring competitiveness and problem-solving clarity, not personal aesthetic preference alone.
2. Cite specific sections, projects, or sentences as evidence for every major finding.
3. Distinguish observed facts from assumptions. State when live URL or code access was unavailable.
4. Prefer actionable rewrites over generic advice such as "더 구체적으로 작성하세요."
5. When metrics are missing, suggest realistic metric types the author could add—not fabricated numbers.
6. Flag AI-generated tone only when multiple signals align (uniform structure, hollow adjectives, action verbs without context).
7. Design Review requires visual evidence. If only text was provided, note the limitation and score conservatively.
8. Improvement Priority must map directly to Weaknesses. High items should be fixable within one focused revision session.

## Anti-Patterns to Avoid

- Scoring without reading all project sections.
- Praising tech stack breadth while ignoring missing problem statements.
- Suggesting full redesign when narrative structure is the core issue.
- Inventing metrics or outcomes not present in the source material.
- Equating visual polish with portfolio quality when storytelling is weak.
- Omitting Recruiter or CTO perspective because the user only asked for "design review."
