---
name: reporting
description: Use when generating, cleaning up, or verifying daily business reports from raw daily logs and task records.
---

# Purpose

Generate, clean up, and verify daily business reports from raw daily logs and task records.

# Required Knowledge

- `AGENTS.md` section `0.10 Reporting Rules`
- `README.md`
- `report-rules.md`
- `daily-reporting.md`
- `highworks-reporting.md`

# Inputs

- Raw daily logs under `ai-workspace/40-tasks/daily/raw/`
- Task checklist entries under `ai-workspace/40-tasks/checklist.md`
- Human-provided reporting context, when available

# Workflow

1. Read the reporting rules and the relevant daily raw logs.
2. Group raw work records into business-readable completed work.
3. Separate completed work from next-day plans.
4. Remove unnecessary implementation detail; **`금일`·`명일`** 모두 `highworks-reporting.md` **대표 등 비개발자 독자 기준** 에 맞춰 내부 기술어로만 채워진 줄을 두지 않음. **`명일` 줄은 카테고리 접두 없이** 계획 문장 단일 블록으로 작성(`highworks-reporting.md`).
5. Produce a concise copy-paste friendly report draft.
6. Save reports under `ai-workspace/40-tasks/daily/reports/` or the requested artifact location.
7. Require human review before external submission.

# Output

- Daily report draft.
- Verification summary.
- Related source files.

# Safety Rules

- Do not include personal schedule notes unless the human explicitly requests conversion.
- Do not submit reports externally.
- Preserve raw logs.
- Keep reports concise and business-readable.

# Incident References

- none

# Verification

- Completed work and next-day plans are separated.
- Report avoids unnecessary implementation details.
- `금일`·`명일` 항목이 비개발자 경영층에게 말처럼 읽히는지(코드명·패키지만 있는 줄 없음) 확인 가능.
- `명일` 줄에 **`… ─  …` 접두** 없이 본문만 있는지 확인 가능 (`highworks-reporting.md` 명일 접두 금지).
- Source raw logs or task records are traceable.
- Human review is clearly required before submission.
