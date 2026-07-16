---
name: auto-update
description: Automatically checks the Git repository for updates to the agents' skills, instructions, or code, and applies updates to keep the ecosystem synchronized.
---

# Auto Update Skill

You are equipped with the **Auto Update Skill**. This skill ensures that your workspace, including your own instructions and the definitions of all sub-agents and modular skills, remains up-to-date with the remote repository.

## Objectives
- Check for updates on the remote repository automatically via a scheduler or upon user request.
- Review changelogs or commit messages before applying changes.
- Safely pull changes without overwriting local configurations or unsaved work.
- Provide error handling for authentication or repository locking issues.

## Repository Setup
The workspace is expected to be a Git repository located at the workspace root directory.

## Workflow & Actions

### 1. Schedule Periodic Checks
To run checking updates in the background automatically:
1. Propose scheduling a checking routine to the user.
2. If approved, utilize the system's `schedule` tool. Set it to run a one-shot reminder or a recurring task that calls this skill.
3. The cron schedule should run periodically (e.g., `0 9 * * *` for every day at 9 AM).

### 2. Check for Remote Updates
When a check is triggered:
1. Try executing `git fetch origin` to retrieve the latest state from the remote repository.
   - **Error Handling:** If git is not installed, the repository is not configured, or authentication fails, catch the error and log a descriptive warning (e.g., *"Cannot fetch remote changes. Please check internet connection or Git configuration"*).
2. Run `git status -uno` to check if the local branch is behind the remote tracking branch (e.g., `origin/main`).
3. Run `git log HEAD..origin/main --oneline` (if behind) to retrieve a list of new changes.

### 3. Identify "What's New" & Prompt
- Extract the latest list of changes from commit messages or the updated `README.md` (What's New section).
- Inform the user of what is new before updating, focusing on major additions, modifications, or breaking changes.

### 4. Safely Pull Changes
If the user consents or if configured to pull automatically:
1. Ensure there are no uncommitted local changes that would be overwritten. Run `git status` to verify.
   - **Conflict Prevention:** If local files are modified, warn the user and suggest stashing or committing changes first. Do not run `git pull` if it will overwrite local modifications.
2. Execute `git pull origin main` (or the active branch name).
3. **Rollback & Conflict Resolution:** If merge conflicts occur, immediately abort or stop. Notify the user immediately with details about conflicting files. Do not try to force changes.
4. Once updated successfully, reload the workspace skills to activate the changes immediately.
