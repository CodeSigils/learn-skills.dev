---
name: morning-briefing
description: Use when producing a daily KPA work briefing that must reconcile schedules, reminders, active tasks, daily logs, and project records before prioritizing work by execution type.
---

# Purpose

Produce a complete daily work briefing that reduces cognitive load without omitting dated deployments, deadlines, verification, or follow-up work.

# Required Knowledge

- `AGENTS.md` sections `0.4.1`, `0.7.1`, `0.13.1`, and `0.14`
- Target-date schedule under `ai-workspace/41-personal-schedule/daily/`
- Relevant recurring reminders under `ai-workspace/42-notification-reminders/entries/`
- `ai-workspace/40-tasks/checklist.md`
- Active task records directly under `ai-workspace/40-tasks/`
- Relevant raw daily logs under `ai-workspace/40-tasks/daily/raw/`
- Relevant project metadata under `ai-workspace/95-projects/active/`
- Relevant project rules and history under `ai-workspace/70-knowledge/domains/`

# Inputs

- Date or relative date for the briefing.
- Optional project focus such as Cardtalk, Daldal English, SLP, or Nuvia.
- Optional human-provided constraints such as meetings, deadlines, deployment windows, or blocked items.

# Mandatory Source Lookup

Use the DB-backed `agent_mcp` virtual filesystem first for ordinary workspace records. Use local files only for runtime files or when MCP is unavailable, and disclose that fallback.

For every briefing, perform this lookup in order:

1. Resolve the requested date to an absolute `YYYY-MM-DD` date.
2. Look for the exact target-date schedule path:
   - `ai-workspace/41-personal-schedule/daily/YYYY-MM-DD.md`
3. Read active recurring reminders whose recurrence applies to the target date.
4. Read `ai-workspace/40-tasks/checklist.md`.
5. List and inspect active task records directly under `ai-workspace/40-tasks/`, excluding templates, indexes, `done.md`, and `daily/`.
6. Select every task whose body contains any of the following:
   - target date, deployment date, deadline, verification date, or follow-up date equal to the briefing date
   - status indicating implementation complete but deployment, QA, verification, approval, or reporting remains
   - overdue or date-unknown follow-up that still has an open completion criterion
7. Read the target-date raw log when present. Also read the latest prior raw log when it contains unfinished work carried into the target date.
8. For selected project tasks, read project metadata first, then project `rules.md`, then only the linked knowledge records needed to verify status and scope.

The absence of an exact daily schedule file does not permit an empty or partial briefing. Continue the task reverse lookup and report the schedule-file gap.

# Workflow

1. Build a source inventory with `found`, `missing`, or `not applicable` for:
   - exact daily schedule
   - recurring reminders
   - central checklist
   - active task records
   - raw logs
   - linked project records
2. Build one candidate item list from all sources before prioritizing.
3. Deduplicate the same work across schedule, checklist, task, raw log, and project history.
4. Split each item into exactly one execution group:
   - `직접 구현`: code, publishing, frontend, API, DB, BO, configuration, or script changes the human or Nova must actively perform.
   - `검증/배포`: staging, production, QA, merge, release, smoke test, Dooray state follow-up, or post-deploy confirmation.
   - `외부 대기`: assignee reply, policy decision, design/spec confirmation, access/account, client/team response, or date-dependent external confirmation.
   - `보고/정리`: daily report, briefing, Dooray comment draft, task/checklist update, raw log, knowledge entry, or stakeholder summary.
5. Evaluate every candidate against the briefing date:
   - documented status and evidence date
   - target, deployment, deadline, or follow-up date
   - remaining prerequisite or completion criterion
   - next concrete action and owner
   - risk of waiting until the next work window
6. Include all items explicitly dated for the briefing date. The one-or-two-item focus limit applies only to `직접 구현`; it must never hide same-day deployments, verification, deadlines, meetings, or required reports.
7. Choose at most two `직접 구현` focus items unless the human asks for more.
8. List follow-up checks separately with owner, next action, and aging risk.
9. Mark items intentionally excluded from focus and explain why.
10. Run the completeness gate before answering.

# Completeness Gate

Do not publish the briefing until all checks pass:

- Every exact-date schedule item appears in the briefing or in `오늘 제외` with a reason.
- Every active task whose deployment, deadline, verification, or follow-up date equals the briefing date appears in the briefing.
- `IMPLEMENTATION_DONE_WAITING_DEPLOYMENT` and equivalent states are treated as open `검증/배포`, not completed work.
- Schedule and task records are cross-checked. If a dated task is absent from the daily schedule, include the task and report `일정 원장 누락`.
- Conflicting status or dates are shown as a discrepancy; do not silently choose one source.
- Missing source files are disclosed.
- Every included item has a source path.
- Every Dooray/Cardtalk work item includes `#number` and the **documented ticket title** (or `(제목 미기록 — 확인 필요)`).

# Briefing-Date Judgment

- Use the requested briefing date as the temporal baseline.
- Consider deadline proximity, remaining work, dependencies, verification windows, and waiting time together.
- A `진행 중` item may still need a same-day decision or verification.
- A `미착수` item with a distant deadline may be intentionally excluded from focus.
- A `완료` implementation may still require deployment, post-deploy verification, Dooray status follow-up, or reporting.
- An overdue or deadline-unknown item must surface the missing evidence needed to assess it.
- Clearly label documented facts and inference. Never invent a deadline, completion state, owner, or dependency.

# Verification Deploy Status Wording

When describing deployment or verification items in briefings, always separate:

1. **Scheduled verification deploy date** — `검증 배포 예정일 YYYY-MM-DD` (sprint, bundle, or ticket schedule)
2. **Current environment state as of briefing date** — `현재(YYYY-MM-DD) 기준 …`

Rules:

- If verification environment already has the deployment before the official schedule date, state both explicitly.
- Do not say only `검증 배포 완료` when a separate scheduled date exists in sources.
- Do not say only `검증 배포 예정` when verification environment already reflects the deployment before that date.
- Apply to Cardtalk bundle deploys, sprint verification deploys, and individual ticket staging work alike.
- For completed verification work, do not surface the item in `외부 대기`, `후속 확인`, or open `검증/배포` unless a new dated obligation exists in sources.

Examples:

- `#135 · 검증 배포 예정일 2026-06-17 14:00 · 현재(2026-06-16) 기준 개발계·FE 연동 완료, 검증계는 내일 예정`
- `CT-23 · 1차 묶음 검증 배포 예정일(로드맵) 별도 · 현재(2026-06-16) 기준 검증계 배포 완료(2026-06-15), 운영 배포 대기`
- `#498/#505 · 별도 예정일 없음 · 현재(2026-06-16) 기준 검증계 배포(2026-05-28)·검증 완료 — 브리핑 제외`

# Ticket Label Format

Humans cannot identify work from ticket numbers alone. Every briefing line that references Dooray or Cardtalk work MUST include the **full ticket title** from source records, not just `#N` or `CT-N`.

## Required pattern

Use this order:

```txt
#<number> `<Dooray title as recorded>`
```

When both CT alias and Dooray number exist:

```txt
CT-<n> / #<number> `<Dooray title as recorded>`
```

Optional project prefix when it reduces ambiguity:

```txt
[Cardtalk] CT-23 / #23 `[06/01] OX퀴즈판 정/오답 최소 문항 개수 정책 제외 건`
[Daldal] #135 `(05/28) 달달영어 공통_서비스 점검 페이지_시크릿 게이트 작업 요청`
```

## Rules

- Never publish a briefing bullet that is only `#135`, `#23`, or `CT-17`.
- Prefer the exact Dooray title string from task/knowledge metadata (`Title`, `Dooray Metadata`, checklist task name).
- If title is missing in sources, write `#N (제목 미기록 — 확인 필요)` and do not invent a title.
- Bundle or sprint lines must still list **each ticket with its title**, or one bundle line plus an indented sub-list with `#N + title` per item.
- Tables (`후속 확인`, `실행 유형별`) must have a **제목** column or embed title in the label cell.

## Bad vs good

Bad:

```txt
- CT-23 검증계 배포 완료
- #135 내일 검증 배포
- #4, #5, #12 1차 완료
```

Good:

```txt
- CT-23 / #23 `[06/01] OX퀴즈판 정/오답 최소 문항 개수 정책 제외 건` — 검증계 배포 완료, 운영 대기
- #135 `(05/28) 달달영어 공통_서비스 점검 페이지_시크릿 게이트 작업 요청` — 검증 배포 예정일 2026-06-17 14:00
- 1차 개발 묶음:
  - #4 `[04/14] 메인 검색 영역 개선`
  - #5 `[04/20] 이용 안내 버튼 변경`
  - #12 `[05/12] 보너스 카드 툴팁 추가 건`
  - #23 `[06/01] OX퀴즈판 정/오답 최소 문항 개수 정책 제외 건`
```

# Output

- `오늘 필수 일정`: all same-day deployments, deadlines, meetings, verification, and reporting obligations.
- `오늘 집중`: one or two direct implementation focus items.
- `실행 유형별 목록`: `직접 구현`, `검증/배포`, `외부 대기`, `보고/정리`.
- `후속 확인 누적 방지`: open checks with owner, next action, and aging risk.
- `KPA가 맡을 것`: tracking, reminders, report drafting, and status reconciliation.
- `사람이 직접 할 것`: implementation, approval, business judgment, external communication requiring human voice, and risky operations.
- `오늘 제외`: intentionally deferred items and reasons.
- `일정·태스크 정합성`: missing schedule records, conflicting statuses, and missing evidence.
- `출처`: paths used for the briefing.

# Safety Rules

- Do not claim completion from missing evidence.
- Do not convert external waiting into a human implementation task.
- Do not include private personal schedule details unless needed for workload planning.
- Do not create new tasks or update status unless the user requested state changes.
- Keep project facts separate from inference.
- Do not judge urgency from status labels alone.
- Do not treat the briefing date as the deadline unless a source explicitly says so.
- Prefer fewer direct focus items, but never omit same-day mandatory work.

# KPA Ownership Defaults

KPA should proactively own:

- daily priority briefing
- mandatory schedule and active-task reconciliation
- grouping work by execution type
- follow-up check aging and resurfacing
- distinguishing direct work from waiting states
- report draft generation from raw logs
- status diffs across schedule, checklist, tasks, daily logs, and project history

The human should retain:

- final priority override
- architecture and product judgment
- code implementation when not delegated
- external stakeholder replies unless explicitly drafted for review
- destructive, production, credential, or migration approval

# Incident References

- 2026-06-11: Cardtalk CT-24 revision-year removal production deployment was omitted because no exact-date schedule file existed and the previous workflow did not require reverse lookup of active task records by deployment date.
- 2026-06-16: Cardtalk June 1st bundle (#4/#5/#12/#23) was under-represented in briefing because deployment history named only CT-23 explicitly and lines used ticket numbers without titles, reducing scanability and causing completed bundle work to look like only the OX ticket mattered.

# Verification

- Exact-date schedule lookup was attempted and its presence or absence is disclosed.
- Active task records were inspected, not only the central checklist.
- Every same-day deployment, deadline, verification, meeting, and reporting obligation is included.
- Every listed item belongs to exactly one execution group.
- Focus contains no more than two direct implementation items by default.
- Follow-up checks include a concrete next action or are explicitly marked unclear.
- Waiting items are not presented as urgent direct implementation unless evidence supports it.
- Inferred urgency, risk, or relationship is clearly distinguished from documented facts.
- Source paths are included.
- Every Dooray/Cardtalk item shows ticket number **and** documented title (not number-only bullets).
