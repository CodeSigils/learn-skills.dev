---
name: speckit-baseline
description: Generate feature specifications by analyzing existing source code.
---

# Spec Kit Baseline Skill

## When to Use

- You need a spec for existing or legacy code.
- You want to document a feature before refactoring.
- You inherited a codebase without written requirements.

## Inputs

- A target path, file list, or glob pattern describing the code to analyze.
- Repo context with `.specify/` scripts and templates.

If the target is missing or ambiguous, ask a focused question before continuing.

## Goal

Generate a technology-agnostic spec for existing code, then create the feature branch/spec file using the standard Spec Kit templates.

## Workflow

1. **Parse target input**: Identify files, directories, or patterns to analyze.
   - Accept file paths, glob patterns, or directory paths.
   - If empty: stop and ask for a concrete target.

2. **Discover and read source files**:
   - Expand globs to a file list.
   - Read file contents for analysis.
   - Identify primary language(s) and frameworks.
   - Map key file relationships and dependencies.

3. **Analyze code structure**:
   - Identify entry points and public interfaces.
   - Extract function/method signatures and behaviors.
   - Find data models and entities.
   - Detect API endpoints and routes.
   - Identify user-facing functionality.

4. **Generate a short name** (2-4 words) from the analyzed code:
   - Use action-noun format (e.g., "user-auth", "payment-processing").
   - Base on primary functionality discovered.
   - Preserve technical terms where meaningful.

5. **Create the feature branch and spec file**:
   - Find the highest existing feature number for this short name (branches/specs).
   - Run `.specify/scripts/bash/create-new-feature.sh --json` with the calculated number and short name.
   - Read BRANCH_NAME, FEATURE_DIR, and SPEC_FILE paths from the script JSON output.
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

6. **Load the spec template** from `.specify/templates/spec-template.md`.

7. **Draft the specification** using the template structure:
   - **User Stories**: Infer from user-facing code paths and interactions.
   - **Acceptance Scenarios**: Derive from validation logic, error handling, and tests.
   - **Functional Requirements**: Extract from business rules and constraints.
   - **Key Entities**: Identify from data models and schemas.
   - **Success Criteria**: Infer from metrics, logging, or performance-related code.
   - **Assumptions**: Document inferences made during analysis.

8. **Abstract implementation details**:
   - Convert technical patterns to user-focused requirements.
   - Remove framework-specific terminology.
   - Focus on WHAT the code does, not HOW it does it.

9. **Create spec quality checklist** at `FEATURE_DIR/checklists/requirements.md`.

10. **Report completion** with:
    - Branch name and spec file path.
    - Summary of analyzed files.
    - Key features discovered.
    - Areas needing clarification or review.

## Outputs

- `specs/<feature>/spec.md`
- `specs/<feature>/checklists/requirements.md`

## Key rules

- Focus on extracting WHAT and WHY from HOW.
- Abstract away implementation details in the generated spec.
- Document assumptions made during code analysis.
- Flag areas where code behavior is unclear.
- Preserve discovered business rules and constraints.
- Use `[NEEDS CLARIFICATION]` for ambiguous code sections (max 3).
- Generated specs should be validated by someone who knows the feature.

## Examples

**Code Pattern → Spec Requirement**:

- `if (user.role === 'admin')` → "System MUST restrict action to administrator users"
- `password.length >= 8` → "Passwords MUST be at least 8 characters"
- `cache.set(key, value, 3600)` → "System MUST cache results for improved performance"
- `try { ... } catch (e) { notify(e) }` → "System MUST notify users when errors occur"

**Code Pattern → User Story**:

- Login endpoint with OAuth → "As a user, I can sign in using my social account"
- Shopping cart logic → "As a customer, I can add items to my cart for later purchase"
- Report generation → "As an analyst, I can generate reports on system activity"

## Next Steps

After generating spec.md:

- **Clarify** with domain experts using speckit-clarify.
- **Plan** modernization/refactoring with speckit-plan.
- **Compare** the generated spec with actual requirements to identify gaps.

## 国内适配

- 支持中文文档和中文注释
- 示例代码兼容国内开发环境
- 提供中文 FAQ 和常见问题解答

## 能力边界

### ✅ 适用场景
- 当你需要使用此技能对应的技术栈时
- 当项目需要遵循最佳实践时
- 当需要快速上手或深入理解核心概念时

### ⚠️ 需要注意
- 复杂业务逻辑需要结合具体场景调整
- 性能优化需要根据实际数据量评估

### ❌ 不适用场景
- 不相关的技术栈或框架
- 需要完全自定义的特殊场景

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
