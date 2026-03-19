---
name: skills-maintenance
description: Maintain @duyet/skills repository - add, update, validate skills, generate documentation, and manage releases. Use when making changes to this skills repository.
---

# Skills Repository Maintenance

Guidelines for maintaining the @duyet/skills repository. This skill ensures consistency across all skills and proper repository management.

## When to Invoke This Skill

Use this skill when:
- Adding a new skill to the repository
- Updating existing skill content
- Running validation checks
- Regenerating README.md from skill definitions
- Bumping versions and creating releases
- Fixing skill structure issues

## Repository Structure

```
skills/
├── skill-name/
│   └── SKILL.md              # Main skill file with frontmatter
├── skills-maintenance/
│   └── SKILL.md              # This file
├── scripts/
│   ├── validate-skills.js    # Validates skill structure
│   └── generate-readme.js    # Regenerates README.md
├── CLAUDE.md                 # Repository documentation
├── AGENTS.md                 # Agent coordination patterns
├── README.md                 # Auto-generated from skills
├── package.json              # NPM scripts and metadata
└── .gitignore                # Standard ignores
```

## Adding a New Skill

### Step 1: Create Directory and SKILL.md

```bash
# Create skill directory
mkdir -p ~/project/skills/new-skill-name

# Create SKILL.md with frontmatter
cat > ~/project/skills/new-skill-name/SKILL.md << 'EOF'
---
name: new-skill-name
description: Brief description of what this skill does. When to use it.
---

# Skill Name

Brief description of the skill's purpose.

## When to Use

Use this skill when:
- [Condition 1]
- [Condition 2]

## Instructions

[Detailed instructions for the agent]
EOF
```

### Step 2: Validate the Skill

```bash
cd ~/project/skills
bun run validate
```

Fix any validation errors before proceeding.

### Step 3: Regenerate README

```bash
cd ~/project/skills
bun run generate:readme
```

This updates README.md with the new skill in the appropriate category.

### Step 4: Commit with Semantic Commit

```bash
cd ~/project/skills
git add -A
git commit -m "feat(skills): add new-skill-name

- Add new skill for [purpose]
- Includes [key features]

Co-Authored-By: duyetbot <duyetbot@users.noreply.github.com>"
git push
```

## Updating an Existing Skill

### Step 1: Edit SKILL.md

Make changes to the skill's SKILL.md file.

### Step 2: Validate Changes

```bash
cd ~/project/skills
bun run validate
```

### Step 3: Update README (if description changed)

```bash
cd ~/project/skills
bun run generate:readme
```

### Step 4: Commit with Semantic Commit

```bash
cd ~/project/skills
git add -A
git commit -m "feat(skill-name): update [what changed]

- [Change 1]
- [Change 2]

Co-Authored-By: duyetbot <duyetbot@users.noreply.github.com>"
git push
```

## Removing a Skill

### Step 1: Remove Directory

```bash
cd ~/project/skills
rm -rf old-skill-name
```

### Step 2: Regenerate README

```bash
bun run generate:readme
```

### Step 3: Commit

```bash
git add -A
git commit -m "fix(skills): remove old-skill-name

- Removed unused skill
- Reason: [why removed]

Co-Authored-By: duyetbot <duyetbot@users.noreply.github.com>"
git push
```

## Version Bumping

Follow semantic versioning (semver) in `package.json`:

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fix, docs only | Patch | 1.0.0 → 1.0.1 |
| New skill, minor changes | Minor | 1.0.0 → 1.1.0 |
| Breaking change (structure, API) | Major | 1.0.0 → 2.0.0 |

### Bumping Version

```bash
# Edit package.json version
cd ~/project/skills
# [edit package.json version]

# Commit version bump
git add package.json
git commit -m "chore: bump version to X.Y.Z

Co-Authored-By: duyetbot <duyetbot@users.noreply.github.com>"

# Create and push tag
git tag v$(node -p "require('./package.json').version")
git push origin master --tags
```

## Skill Structure Requirements

Every SKILL.md file must:

1. **Start with frontmatter** (YAML between `---`)
   ```yaml
   ---
   name: skill-name
   description: Brief description
   ---
   ```

2. **Name matches directory**
   - Directory: `skill-name/`
   - Frontmatter: `name: skill-name`

3. **Description is present**
   - Should be concise (one line)
   - Should explain when to use the skill

4. **Content after frontmatter**
   - At minimum, a heading and brief instructions
   - Preferably sections: When to Use, Instructions, Examples

## Validation Rules

The `validate-skills.js` script checks:

- ✅ Each directory has a `SKILL.md` file
- ✅ `SKILL.md` starts with `---` (frontmatter opening)
- ✅ `name` field exists in frontmatter
- ✅ `name` matches directory name
- ✅ `description` field exists in frontmatter
- ✅ Frontmatter closes with `---`

## Available Scripts

```bash
# List all skills
bun run list

# Format all skill files with Prettier
bun run format

# Validate skill structure
bun run validate

# Regenerate README from skills
bun run generate:readme
```

## Commit Convention

Use semantic commits with `skills` scope (unless modifying a specific skill):

```
feat(skills): add new-skill
feat(skills): update scripts
fix(skills): fix validation bug
docs(skills): update README
chore: bump version
```

For specific skill changes:
```
feat(skill-name): add new feature
fix(skill-name): fix bug in instructions
docs(skill-name): improve documentation
```

Always include co-author:
```
Co-Authored-By: duyetbot <duyetbot@users.noreply.github.com>
```

## Remote Repository

- **URL**: `git@github.com:duyet/skills.git`
- **HTTPS**: `https://github.com/duyet/skills`
- **Branch**: `master`

## Related Documentation

- `CLAUDE.md` - Repository-level documentation
- `AGENTS.md` - Agent coordination patterns
- `README.md` - Generated skill catalog
- [skills.sh](https://skills.sh) - Skills ecosystem
- [Agent Skills Specification](https://agentskills.io/specification)

## Quick Checklist

Before committing changes:

- [ ] All skills validated (`bun run validate`)
- [ ] README regenerated if skills added/removed (`bun run generate:readme`)
- [ ] Commit follows semantic commit format
- [ ] Co-author included in commit message
- [ ] Changes pushed to remote
