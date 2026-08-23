---
name: github-project
description: >
  Conventions for preparing and maintaining my personal projects on GitHub.
disable-model-invocation: true
---

# General

Treat the repository as a public GitHub project.

Keep repository-facing infrastructure simple and proportional to the project's size.

# GitHub Actions

- Add useful CI for building and verifying the project.
- Use the latest stable major versions of established actions.
- Run the same build/test commands used locally.
- Prefer project-provided wrappers and scripts over duplicating build logic in workflow YAML.
- Use official caching mechanisms where useful.
- Keep workflow permissions minimal.

## CI

### Build check

- Run on changes to the default branch and on pull requests targeting it.
- Do not run build/test jobs for documentation-only changes. Documentation-specific jobs may run only when relevant documentation changes.
- Build the project and run tests when present.
- Upload useful build outputs as GitHub Actions artifacts with a short retention period.

### Tag build

- Trigger releases from semantic version tags.
- Prefer `*.*.*` tags over `v*.*.*` unless tooling requires the `v` prefix.
- Only release commits reachable from the protected release/default branch.
- Create a GitHub Release for the tag.
- Attach release build outputs to the GitHub Release when applicable.
- For projects that produce Docker images, publish them to GitHub Container Registry (GHCR) by default. Use another registry only when explicitly requested.
- Tag container images with the release version and update `latest` for normal stable releases.
- Do not invent polished release notes from commit history. Prefer a concise commit list, grouped when explicit commit metadata such as `Changelog: frontend` is available.

## Dependabot

Always configure Dependabot.

- Cover every supported dependency ecosystem used in the monorepo.
- Cover dependency manifests in all relevant modules/subprojects, not only the repository root.
- Always include the `github-actions` ecosystem to keep CI actions updated.
- Prefer grouped updates where appropriate to avoid excessive dependency PR noise.

# README

When a README is requested:

- Keep it concise and practical.
- Explain what the project is before implementation details.
- Include only useful setup, build, run, and usage instructions.
- Prefer examples and commands over long explanations.
- Do not add generic sections merely because GitHub READMEs commonly have them.
- Do not add badges unless they provide useful information.
- Do not use marketing language for small personal projects.


# Licensing

- Use WTFPL unless i request something else
- With WTFPL use `LICENSE` file as original license and `COPYRIGHT` for noticing me.

COPYRIGHT may look like this 
```
Copyright (C) 2026 Ilya Dobryakov

Licensed under WTFPL
```

- If project is license sensitive, create third-party md file for licensing notices and include in `COPYRIGHT` file link to it.
- Disclose AI usage.
