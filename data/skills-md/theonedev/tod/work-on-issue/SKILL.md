---
name: work-on-issue
description: Implement work for a OneDev issue. Use when the user asks to start, pick up, or continue issue work.
---

# Work on a OneDev issue

Set up the issue branch, read the relevant context, and implement the work.

## Prerequisites

- `tod` is installed and configured.
- The current repository belongs to the issue's project.

## Stop on error

Run the workflow sequentially. On any command failure, missing required
output, or failed precondition, stop immediately, report the command and
error, and wait for the user. Do not continue, repair state beyond the
current step, or retry silently.

## Workflow

Given an `<issue-reference>` (e.g. `123`, `#123`, `myproject#123`, or
`PROJ-123`):

1. **Prepare the checkout.** Prepare the checkout to work on the issue,
   unless the user explicitly asks not to, or wants to switch to a different
   checkout.

   Check out the issue branch locally:
   ```bash
   tod issue checkout <issue-reference>
   ```
   The command creates the issue branch on the server when necessary,
   switches the local checkout to it, and sets up remote tracking. If it
   fails because the working directory has uncommitted changes, stop and ask
   the user to commit or stash them before re-running the skill.

   Confirm the current branch
   ```bash
   git symbolic-ref --short HEAD
   ```
   The branch name should conform to format `[optional prefix/]issue-<issue number>[-optional suffix]`

2. **Determine the work specification.** The
   work to do may come from the user's prompt directly or from the issue
   on OneDev:

   | Work instruction source | Primary specification | Issue context |
   |-------------------------|---------------------|---------------|
   | User prompt specifies the work | The prompt (concrete task, scope, approach, or constraints beyond naming the issue) | Fetch below; use title, description, and comments as supplementary background |
   | Prompt only names the issue | Issue title and description | Comments are supplementary (clarifications, constraints, hints) |

   When the prompt is the primary specification, still fetch issue metadata
   and discussion as context — do not skip ahead to step 3 from partial output:
   ```bash
   tod issue get <issue-reference>
   tod issue get-comments <issue-reference>
   tod get-login-name
   ```

   When the prompt only names the issue, the same commands are required;
   without that context you cannot plan the work reliably.

   Match your login name against roles in issue detail and each comment 
   to understand your role, position, and previous
   involvements in the context.

   **When the work is to investigate a build failure or fix a failed build,
   gather and examine build evidence before planning code changes.** Given
   the relevant `<build-reference>`:
   ```bash
   tod build get <build-reference>
   tod build get-log <build-reference>
   ```
   Read the build detail and log content carefully to identify the failure:

   - If the log contains a statement like
     `Dependency build is required to be successful but failed: <dependency-build-reference>`,
     get the dependency build detail. If its commit hash is the same as the
     current build, investigate or fix the dependency build failure instead;
     repeat this process for same-commit dependency build failures. If the
     dependency build's commit hash differs from the current build, conclude
     that the current build failure is caused by this dependency build.
   - If the log contains a statement like
     `<report-name>: found problems with severity <severity-level> or higher`,
     fetch the referenced problems report:
     ```bash
     tod build get-code-problems <build-reference> <report-name> <severity-level>
     ```
     Problems may point to workspace files, 1-based line ranges, or
     non-workspace artifacts used by the project.
   - Inspect referenced workspace files as necessary. Inspect
     `.onedev-buildspec.yml` when job configuration may be involved, and 
     run below command to get its schema if you need to modify it:
     ```
     tod build get-spec-schema
     ```
   - If useful, inspect changes since the previous successful build:
     ```bash
     tod build get-changes-since-success <build-reference>
     ```

   **Inspect embedded resources.** Download every linked image or file from
   the issue description and comments:

   - Find image and file links in the description and every comment
     (`![alt](url)` and `[label](url)`).
   - For each URL, save it locally using the URL **exactly** as it
     appears in the markdown (do not rewrite or normalize it):
     ```bash
     tod download <resource-url> <output-file>
     ```
   - Open images and read other downloaded files as needed.

3. **Assess, plan, and execute.** Check the requested work against the
   current code and behavior before deciding whether code changes are needed.
   The work product may be code changes, issue comments explaining the decision,
   or both. Implement any needed code changes in the working copy, and draft
   every issue comment that should be posted, including explanatory responses,
   status updates, or any update claiming that a fix has been implemented. Do 
   not post comments in this workflow.

   Present all resulting work to the user for possible amendment, including code
   changes and drafted comments. Leave the working copy on the issue branch with
   all work, saved for later submission.
