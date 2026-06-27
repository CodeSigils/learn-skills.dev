---
name: resume-optimizer
description: "AI-powered resume optimization for Chinese tech/internet industry, especially AI Product Manager roles. Use this skill whenever the user wants to optimize a resume, rewrite resume bullet points, tailor a resume to a specific JD or company, improve ATS compatibility, add bold annotations for changes, or generate a modified resume with tracked changes. Also use when the user mentions 简历优化, 简历修改, 简历改写, JD匹配, ATS评分, or resume tailoring — even if they don't explicitly say 'resume optimizer.'"
---

# Resume Optimizer — AI产品经理简历优化技能

This skill optimizes Chinese-language resumes (especially for AI Product Manager roles) by applying a 21-dimension modification framework, tracking all changes with bold annotations, and validating output through an AI review loop.

## When to Use

- User wants to optimize/tailor a resume for a specific JD or company
- User wants to improve ATS compatibility scores
- User wants bold-annotated change tracking on a modified resume
- User mentions 简历优化/修改/改写/JD匹配/ATS评分

## Core Workflow

### Step 1: Understand the Context

Determine which mode applies:

| Mode | Condition | Focus |
|------|-----------|-------|
| JD + Company Profile | Has JD text + company hiring profile | Full 21-dimension optimization |
| Company Profile Only | Has profile but no JD | P1画像融入 + P2/P3 |
| Generic | No JD, no profile | AI PM general standards, ATS + quality |

### Step 2: Apply the 21-Dimension Modification Framework

Execute dimensions **in priority order** — P0 → P1 → P2 → P3. For each dimension, apply to **every bullet point** in the resume, not just glance and skip.

#### P0: JD Skill Semantic Alignment (jd-keyword-align)

**The core logic is NOT "extract keywords and stuff them in" — it's "understand skill meaning → find matching experience → adjust description angle to naturally embody the skill."**

Three-step process for each JD skill requirement:

1. **Semantic Decomposition**: Break down what the skill actually means
   - "具备良好的产品思维和用户洞察力" → 产品思维(需求抽象+优先级判断+MVP验证) + 用户洞察力(用户调研+痛点挖掘+需求验证) + 技术可用性(技术→产品功能转化)

2. **Find Matching Experience**: Scan resume for actions/outcomes that embody the decomposed skill
   - "打了3000个用户电话" → embodies 用户洞察力
   - "识别伪需求并砍掉" → embodies 产品思维

3. **Natural Integration**: Adjust description angle so the skill naturally emerges — NOT by slapping on a label
   - ❌ "具备产品思维" (label stuffing)
   - ✅ "通过3000+用户电话访谈挖掘核心痛点，识别3个伪需求并砍掉，聚焦2个高价值方向，上线后转化率提升25%" (reader naturally senses 产品思维)

**Core Skills Section Rule**: Every skill from JD MUST appear in the 核心技能/专业技能 section:
- Already in resume and precise → keep (deduplicate)
- Already in resume but vague → rewrite to be precise (bold the rewritten part)
- Not in resume but required by JD → add new entry (entire entry in **bold**)

#### P1: Company Profile Integration

| Dimension | ID | Logic |
|-----------|----|-------|
| Hard Skills | profile-hard-skill | Same semantic alignment as P0 — understand meaning, find matching experience, adjust description angle |
| Soft Skills | profile-soft-skill | Demonstrate through narrative events, never write "具备XX能力" directly. "协调3个团队推进项目上线" demonstrates 沟通力 |
| Tone Adapt | profile-tone-adapt | Data-driven company → more quantification; methodology company → more framework language |
| Not-Care | profile-not-care | De-emphasize but don't delete |

**Core Skills Section Rule**: Every core_skill and soft_skill from the profile MUST appear in the 核心技能 section, same add/deduplicate/rewrite rules as P0.

#### P2: Core Expression Optimization

| Dimension | ID | What to Do |
|-----------|----|-----------|
| STAR Method | star-method | Restructure as Situation→Task→Action→Result. Must show product decision-making: why do this → how to decide → what business impact |
| XYZ Formula | xyz-formula | Compress to: solved [problem X], by [decision Z], achieved [impact Y] |
| Quantify | quantify | Add metrics WITH baselines: "accuracy from 68% to 92%, complaints down 40%" not just "accuracy 92%" |
| Achievement-Oriented | achievement-oriented | Transform "负责XX" → "identified pain point → made decision → delivered impact" |
| Strong Verbs | strong-verbs | 负责→主导, 参与→推动, 协助→独立承担, 优化→迭代优化, 设计→设计并验证 |
| Remove Fluff | remove-fluff | "工作认真负责" → "independently managed 3 product lines, 0 delayed deliveries, Q OKR 110%" |
| Reorder Experience | reorder-experience | Most relevant to JD/profile goes first |
| Summary Line | summary-line | Generate a one-line positioning tailored to JD/profile: "> AI产品经理，擅长数据驱动的大模型应用落地与商业化" |
| ATS Optimization | ats-optimization | Based on ATS analysis results, fix any dimension scoring < 80 (keyword gaps, format issues, structure completeness, quantification) |

#### P3: Polish

| Dimension | ID | What to Do |
|-----------|----|-----------|
| Format Unify | format-unify | Consistent punctuation, indentation, list format |
| Style Unify | style-unify | Consistent tone strength, sentence rhythm |
| Length Unify | length-unify | Balanced section lengths |
| Dedup | dedup | Remove repeated descriptions, vary angles |
| Red Flag | red-flag | Fix typos, timeline gaps, vague dates |
| 3C Principle | 3c-principle | Clear, Concise, Compelling |
| ATS Friendly | ats-friendly | No tables/images/special chars, standard terminology, consistent date format YYYY.MM |

#### Special: Template Insights (template-insights)

When resume-writing methodology analysis is available, apply those insights (writing techniques, keyword strategies, common mistake corrections). Changes from this source are tagged differently from rule-based changes.

### Step 3: Apply Change Annotations

**Every modification must be marked — this is non-negotiable.**

| Operation | Bold Annotation | changes_summary |
|-----------|----------------|-----------------|
| Added (new word/phrase not in original) | ✅ **bold** | before="", after="new content" |
| Modified (rewritten phrasing) | ✅ rewritten part in **bold** | before="original", after="new" |
| Replaced (swapped A for B) | ✅ new word B in **bold** | before="A", after="B" |
| Deleted (original content removed) | ❌ can't bold what's gone | before="deleted content", after="(已删除)" |
| Unchanged | ❌ no annotation | ❌ no record |

**Bold color coding** (added in post-processing):
- **紫:text** (purple bold) → rule-based changes (P0-P3, 20 dimensions)
- **红:text** (red bold) → template-insights-based changes

### Step 4: Anti-AI-Flavor Rules

The resume must read like a real person wrote it, not ChatGPT:

- ❌ Forbidden buzzwords: "赋能", "助力", "深耕", "全方位", "一站式", "全链路", "闭环" (unless already in original resume)
- ❌ No adjective stacking: "卓越的", "出色的", "高效的", "创新的" — let facts speak
- ❌ No empty parallelism: "从0到1，从无到有，从小到大" — say what you actually did
- ❌ No AI-style summaries: "综上所述", "总而言之"
- ✅ Write like talking to an interviewer: "发现用户口语化提问检索不准，设计混合检索策略，意图识别准确率从68%提到92%"

### Step 5: Validation Loop

After generating, validate the output:

1. **Bold annotation completeness**: Line-by-line comparison, check every change is marked
2. **Core skills section completeness**: Every JD/profile skill must appear in 核心技能 section
3. **changes_summary completeness**: All 21 dimensions must have entries; every modification (add/modify/replace/delete) must be recorded
4. **Content preservation**: No sections or bullet points deleted
5. **ATS score improvements**: Low-scoring ATS dimensions must be addressed

If validation fails, retry with feedback (up to 5 attempts total).

## Output Format

Strict JSON:
```json
{
  "modified_resume": "Full resume in Markdown with **bold** annotations",
  "changes_summary": {
    "jd-keyword-align": {"changed": true/false, "items": [{"location": "...", "before": "...", "after": "...", "reason": "..."}]},
    "profile-hard-skill": {"changed": true/false, "items": [...]},
    "...": "...",
    "ats-optimization": {"changed": true/false, "items": [{"location": "...", "before": "...", "after": "...", "reason": "修复ATS分析中XX维度得分低的问题"}]},
    "template-insights": {"changed": true/false, "items": [{"location": "...", "before": "...", "after": "...", "reason": "参考简历模板分析方法论：[specific technique]"}]}
  }
}
```

## Self-Check Before Output

For every bullet point in the output, verify:
1. Does it have at least 1-2 changes marked in **bold**? If not, you didn't optimize enough.
2. Does it naturally embody a JD/profile skill through description angle (not label stuffing)?
3. Does it include quantified metrics with baselines?
4. Does it use strong verbs (主导/推动/驱动) not weak ones (负责/参与/协助)?
5. Does it read like a real person wrote it, not AI?

## AI Experience Highlighting

For any experience involving AI (LLM, RAG, Agent, recommendations, NLP, etc.), emphasize:
1. **Why AI for this scenario** — what pain point/opportunity made AI better than traditional approach
2. **How the opportunity was found** — data analysis, user research, competitive analysis
3. **How model performance was optimized post-launch** — evaluation system → badcase analysis → iteration → improvement
4. **Before/after comparison** — with AI vs. without AI metrics
5. **Product decision thinking** — not "used X model" but "why X over Y → product design → business impact"
