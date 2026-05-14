---
name: project-onboarding
description: Creates a comprehensive onboarding guide for any codebase. Analyzes project structure, architecture decisions, user flows, coding patterns, and generates an expert-level introduction that explains where to start and how things work. Use when running `/project-onboarding` to understand a new project.
---

# Project Onboarding

## Overview

Acts as an expert guide for any codebase, analyzing the project comprehensively and generating a clear onboarding document. This skill reads through the entire project, understands the architecture, traces user flows, identifies patterns, and creates a source of truth document that explains how everything works.

Like having a senior developer who's been on the project since day one walk you through the codebase.

## When to Use

- Running `/project-onboarding` in a new project
- Need to understand project architecture quickly
- Joining an open source project or existing team
- Want to understand user flows and development patterns
- Need a comprehensive project overview document

## Command Usage

```bash
# Basic usage - analyzes current directory, outputs to PROJECT_GUIDE.md
/project-onboarding

# Specify output location
/project-onboarding --output docs/ONBOARDING.md

# Control analysis depth
/project-onboarding --depth quick        # 30-60 min analysis (default)
/project-onboarding --depth thorough     # 2-3 hour deep dive
```

## Analysis Process

The skill performs systematic analysis in phases, each with time limits to ensure efficiency:

### Phase 1: Project Discovery (10 minutes max)
- Detect project type (web app, CLI, library, mobile, etc.)
- Find entry points and main files
- Identify package managers and dependencies
- Map directory structure and organization

### Phase 2: Architecture Analysis (20 minutes max)
- Extract key architectural decisions
- Identify patterns and conventions
- Find configuration files and build processes
- Understand data flow and system boundaries

### Phase 3: User Flow Mapping (15 minutes max)
- **End User Flows**: How users interact with the application
- **Developer Flows**: How to add features, run tests, deploy
- Entry points for both types of flows

### Phase 4: Code Pattern Analysis (15 minutes max)
- Extract coding style and conventions from real code
- Identify component patterns and abstractions
- Find testing strategies and frameworks
- Document naming conventions and file organization

### Phase 5: Dependency & Library Analysis (10 minutes max)
- UI component libraries (Material-UI, Chakra, custom)
- Internal libraries and shared utilities
- AI skills and automation (Cursor skills, other .md skills)
- Key external dependencies and their usage

### Phase 6: Guide Generation (5 minutes max)
- Synthesize all analysis into structured document
- Generate actionable next steps
- Add timestamp and generation metadata

## Guide Output Structure

The generated guide follows this template:

```markdown
# [Project Name] - Onboarding Guide

*Generated on [timestamp] by Cursor Project Onboarding*

## Quick Start
- How to get the dev environment running
- Essential commands (build, test, dev, lint)
- First steps for new contributors

## Architecture Overview
- High-level system design
- Key architectural decisions and reasoning
- Technology stack and major dependencies

## User Flows
### End User Journey
- How users navigate and use the application
- Main features and workflows
### Developer Journey
- How to implement new features
- Testing and debugging workflows
- Deployment and release process

## Code Patterns & Standards
- Real code examples showing conventions
- Naming patterns and file organization
- Component/module patterns
- Error handling approaches

## Component Libraries & Dependencies
- UI libraries and design systems
- Internal shared libraries
- Key external dependencies
- Custom utilities and helpers

## AI Skills & Automation
- Cursor skills found in the project
- Other AI/automation tools configured
- Development workflow automation

## Entry Points for Common Tasks
- Adding a new feature: Start here
- Fixing a bug: Look here first
- Understanding data flow: Key files
- Modifying UI: Component locations

## Development Workflow
- Branch strategy and git workflow
- Code review process
- Testing requirements
- CI/CD pipeline

## Troubleshooting & FAQ
- Common setup issues
- Debugging tips specific to this project
- Where to find help and documentation
```

## Implementation Steps

When `/project-onboarding` is invoked, execute these steps systematically:

### Step 1: Parse Command and Setup
```
1. Parse command flags:
   - Extract --output path (default: PROJECT_GUIDE.md) 
   - Extract --depth level (default: quick)
2. Set time limits based on depth:
   - quick: 70 minutes total
   - thorough: 180 minutes total
3. Initialize analysis results structure
```

### Step 2: Project Discovery (10 min)
```
1. Find project type indicators:
   Glob patterns: ["package.json", "requirements.txt", "Cargo.toml", "go.mod", "pom.xml", "*.csproj", "pubspec.yaml"]
   
2. Identify project structure:
   Glob patterns: ["src/**", "lib/**", "app/**", "components/**", "pages/**", "routes/**"]
   
3. Find documentation:
   Glob patterns: ["README*", "docs/**", ".cursor/skills/**"]
   
4. Detect main entry points:
   Glob patterns: ["main.*", "index.*", "app.*", "server.*", "*.py", "*.js", "*.ts"]
   
5. Read package manifests to understand:
   - Dependencies and their purposes
   - Available scripts and commands
   - Project metadata (name, description)
```

### Step 3: Architecture Analysis (20 min)
```
1. Configuration analysis:
   Glob patterns: ["*config*", "*.config.*", "docker*", "*.yml", "*.yaml", "*.json"]
   Read: Build configs, framework configs, CI/CD files
   
2. Semantic architecture search:
   - "What are the main architectural patterns used in this project?"
   - "How is the application structured and what frameworks are used?"
   - "What are the key design decisions and why were they made?"
   
3. Database/data layer detection:
   Glob patterns: ["*schema*", "*model*", "migration*", "*.sql"]
   Search: "How is data modeling and persistence handled?"
   
4. API/routing analysis:
   Glob patterns: ["*route*", "*api*", "*endpoint*", "*controller*"]
   Search: "How are API endpoints and routes defined?"
```

### Step 4: User Flow Mapping (15 min)
```
1. End-user flow analysis:
   Search: "How do users navigate and interact with this application?"
   Search: "What are the main user journeys and features?"
   Search: "How does authentication and user management work?"
   
2. Developer workflow analysis:
   Read: package.json scripts, Makefile, CI configs
   Search: "How do developers build, test, and deploy this application?"
   Search: "What is the development workflow and setup process?"
   
3. Feature implementation flows:
   Search: "How are new features typically added to this codebase?"
   Search: "What is the testing strategy and how are tests organized?"
```

### Step 5: Code Pattern Analysis (15 min)
```
1. Style and convention extraction:
   Grep patterns: Look for consistent naming patterns
   Read sample files from different areas (components, utils, tests)
   
2. Component/module patterns:
   Search: "What are the common patterns for components and modules?"
   Glob patterns: ["*component*", "*util*", "*helper*", "*service*"]
   
3. Error handling and logging:
   Grep patterns: ["error", "log", "catch", "throw"]
   Search: "How are errors handled and logged in this application?"
   
4. Import/export patterns:
   Grep patterns: ["import", "export", "require"]
   Analyze: Consistent import organization and module structure
```

### Step 6: Library & Skills Detection (10 min)
```
1. UI/Component libraries:
   Grep in package.json: ["react", "vue", "@mui", "chakra", "antd", "bootstrap"]
   Search: "What UI libraries and design systems are used?"
   
2. Cursor skills and automation:
   Glob patterns: [".cursor/skills/*.md", ".cursor/rules/*.md"]
   Read: All found skill files to understand their purpose
   
3. Internal libraries and utilities:
   Glob patterns: ["lib/**", "utils/**", "shared/**", "common/**"]
   Search: "What internal libraries and shared utilities exist?"
   
4. Key dependencies analysis:
   Read: package.json, requirements.txt to identify major dependencies
   Categorize: Frameworks, tools, utilities, testing, build tools
```

### Step 7: Generate Comprehensive Guide (5 min)
```
1. Synthesize findings into structured template
2. Generate real code examples from discovered patterns  
3. Create actionable next steps for developers
4. Add timestamp and generation metadata
5. Save to specified output location
6. Display summary of what was analyzed and generated
```

## Analysis Execution Logic

For each analysis phase, follow this pattern:

```
TIME_LIMIT = phase_time_limit
START_TIME = current_time()

try:
    execute_analysis_phase()
catch timeout:
    log("Phase timed out, proceeding with partial results")
    continue_to_next_phase()
catch error:
    log("Phase failed: {error}, continuing with available data")
    continue_to_next_phase()

if current_time() - START_TIME > TIME_LIMIT:
    break_and_proceed_to_next_phase()
```

This ensures the skill completes within reasonable time limits even for very large codebases.

## Quality Gates

Before generating the final guide, verify:

- [ ] **Completeness**: All major architectural decisions identified
- [ ] **Accuracy**: Entry points and flows traced correctly  
- [ ] **Actionability**: Clear next steps for common developer tasks
- [ ] **Readability**: Guide readable in 10-15 minutes
- [ ] **Examples**: Real code snippets showing actual patterns used

## Error Handling

- **Large codebases**: Use targeted sampling rather than exhaustive reading
- **Missing files**: Continue with partial analysis, note what's missing
- **Time limits exceeded**: Generate guide with available analysis
- **Unknown project types**: Focus on generic patterns and structure

## Success Criteria

A successful onboarding guide should answer these questions within 15 minutes of reading:

1. **Where do I start?** - Clear entry points for new developers
2. **How do I add a feature?** - Specific files and patterns to follow  
3. **How does this work?** - User flows and system architecture
4. **What are the rules?** - Coding conventions and standards
5. **What tools exist?** - Available libraries, skills, and automation

The guide should feel like having an expert mentor explain the project personally.

## Skill Execution

When this skill is activated with `/project-onboarding`, execute the following implementation:

### Command Processing
```
1. Parse the user's command for flags:
   - Extract output path from --output flag (default: "PROJECT_GUIDE.md")
   - Extract depth from --depth flag (default: "quick") 
   - Validate and set time limits accordingly

2. Display analysis start message:
   "Starting comprehensive project analysis. This will take 30-60 minutes for quick mode..."
```

### Project Discovery Phase
```
PHASE: Project Discovery (10 minutes max)
START_TIME = now()

# Find project manifests and type indicators
manifest_files = Glob(["package.json", "requirements.txt", "Cargo.toml", "go.mod", "pom.xml", "*.csproj", "pubspec.yaml"])

# Determine project type and tech stack
for manifest in manifest_files:
    content = Read(manifest)
    analyze_dependencies_and_scripts(content)

# Discover project structure
structure_indicators = Glob(["src/**", "lib/**", "app/**", "components/**", "pages/**", "routes/**"])

# Find main entry points  
entry_points = Glob(["main.*", "index.*", "app.*", "server.*"])

# Look for documentation
docs = Glob(["README*", "docs/**/*.md", ".cursor/**/*.md"])

PROJECT_TYPE = determine_project_type(manifest_files)
TECH_STACK = extract_tech_stack(manifest_files)
ENTRY_POINTS = identify_main_entry_points(entry_points)

if time_exceeded(START_TIME, 10):
    log("Project discovery phase timed out, proceeding with found results")
```

### Architecture Analysis Phase  
```
PHASE: Architecture Analysis (20 minutes max)
START_TIME = now()

# Find configuration files
config_files = Glob(["*config*", "*.config.*", "docker*", "*.yml", "*.yaml", "tailwind*", "vite*", "webpack*", "next.config*"])

# Read key configuration files
for config in config_files[:5]:  # Limit to prevent timeout
    content = Read(config)
    extract_architecture_decisions(content)

# Semantic search for architectural insights
architecture_insights = SemanticSearch(
    query="What are the main architectural patterns and design decisions in this project?",
    target_directories=[]
)

data_layer_insights = SemanticSearch(
    query="How is data modeling, persistence, and state management handled?", 
    target_directories=[]
)

framework_insights = SemanticSearch(
    query="What frameworks and libraries are used and how are they configured?",
    target_directories=[]
)

ARCHITECTURE = synthesize_architecture_analysis(config_files, architecture_insights, data_layer_insights, framework_insights)

if time_exceeded(START_TIME, 20):
    log("Architecture analysis timed out, proceeding with available insights")
```

### User Flow Mapping Phase
```
PHASE: User Flow Mapping (15 minutes max)  
START_TIME = now()

# Map end-user flows
user_flows = SemanticSearch(
    query="How do users navigate and interact with this application? What are the main user journeys?",
    target_directories=[]
)

auth_flows = SemanticSearch(
    query="How does user authentication and session management work?",
    target_directories=[]
)

# Map developer flows
dev_workflows = SemanticSearch(
    query="How do developers build, test, and deploy this application? What is the development setup process?",
    target_directories=[]
)

# Analyze available commands
if PROJECT_TYPE in ["javascript", "typescript"]:
    package_json = Read("package.json")
    DEV_COMMANDS = extract_scripts(package_json)
elif PROJECT_TYPE == "python":
    try:
        makefile = Read("Makefile") 
        DEV_COMMANDS = extract_makefile_targets(makefile)
    except:
        DEV_COMMANDS = ["python -m pip install -r requirements.txt", "python main.py"]

USER_FLOWS = synthesize_user_flows(user_flows, auth_flows)
DEVELOPER_FLOWS = synthesize_developer_flows(dev_workflows, DEV_COMMANDS)

if time_exceeded(START_TIME, 15):
    log("User flow mapping timed out, proceeding with available flows")
```

### Code Pattern Analysis Phase
```
PHASE: Code Pattern Analysis (15 minutes max)
START_TIME = now()

# Find representative code files
component_files = Glob(["**/*component*", "**/*Component*"])[:3]
utility_files = Glob(["**/util*", "**/helper*", "**/lib/**"])[:3] 
test_files = Glob(["**/*test*", "**/*spec*"])[:2]

CODE_SAMPLES = {}

# Extract patterns from sample files
for file_path in (component_files + utility_files + test_files):
    try:
        content = Read(file_path)
        CODE_SAMPLES[file_path] = extract_code_patterns(content)
    except:
        continue

# Search for coding conventions
coding_patterns = SemanticSearch(
    query="What are the coding conventions, naming patterns, and style guidelines used in this project?",
    target_directories=[]
)

error_handling = SemanticSearch(
    query="How are errors handled and logged throughout the application?",
    target_directories=[]
)

CODING_PATTERNS = synthesize_code_patterns(CODE_SAMPLES, coding_patterns, error_handling)

if time_exceeded(START_TIME, 15):
    log("Code pattern analysis timed out, proceeding with available patterns")
```

### Library & Skills Detection Phase
```
PHASE: Library & Skills Detection (10 minutes max)
START_TIME = now()

# Find Cursor skills
cursor_skills = Glob([".cursor/skills/*.md", ".cursor/rules/*.md"])
CURSOR_SKILLS = []

for skill_file in cursor_skills:
    skill_content = Read(skill_file)
    CURSOR_SKILLS.append(extract_skill_info(skill_content, skill_file))

# Detect UI libraries and frameworks
ui_libraries = SemanticSearch(
    query="What UI libraries, component libraries, and design systems are used in this project?",
    target_directories=[]
)

# Find internal libraries
internal_libs = Glob(["lib/**", "shared/**", "common/**", "utils/**"])
INTERNAL_LIBRARIES = analyze_internal_libraries(internal_libs[:5])

# Analyze major dependencies
if manifest_files:
    main_manifest = Read(manifest_files[0])
    MAJOR_DEPENDENCIES = categorize_dependencies(main_manifest)

LIBRARIES_AND_TOOLS = synthesize_libraries_analysis(ui_libraries, INTERNAL_LIBRARIES, MAJOR_DEPENDENCIES, CURSOR_SKILLS)

if time_exceeded(START_TIME, 10):
    log("Library detection timed out, proceeding with available libraries")
```

### Guide Generation Phase
```
PHASE: Guide Generation (5 minutes max)
START_TIME = now()

# Generate comprehensive guide using all collected data
guide_content = generate_onboarding_guide(
    project_type=PROJECT_TYPE,
    tech_stack=TECH_STACK, 
    entry_points=ENTRY_POINTS,
    architecture=ARCHITECTURE,
    user_flows=USER_FLOWS,
    developer_flows=DEVELOPER_FLOWS,
    coding_patterns=CODING_PATTERNS,
    libraries_and_tools=LIBRARIES_AND_TOOLS,
    timestamp=now()
)

# Write guide to specified output location
output_path = user_specified_output_path or "PROJECT_GUIDE.md"
Write(output_path, guide_content)

# Display completion summary
display_completion_summary(output_path, total_analysis_time, discovered_features_count)
```

### Helper Functions
```python
def extract_tech_stack(manifest_files):
    # Analyze manifest files to determine technology stack
    
def determine_project_type(manifest_files):
    # Determine if web app, CLI, library, mobile app, etc.
    
def extract_architecture_decisions(config_content):
    # Parse configuration files for architectural insights
    
def synthesize_user_flows(user_flows, auth_flows):
    # Combine semantic search results into coherent user flow description
    
def extract_code_patterns(file_content):  
    # Analyze code file to extract naming conventions and patterns
    
def generate_onboarding_guide(**analysis_data):
    # Generate final markdown guide using template and analysis results
    
def time_exceeded(start_time, limit_minutes):
    # Check if phase time limit has been exceeded
```

This implementation ensures the skill completes systematically while respecting time limits and handling errors gracefully.

## Guide Template

The `generate_onboarding_guide()` function uses this template structure:

```markdown
# {PROJECT_NAME} - Onboarding Guide

*Generated on {TIMESTAMP} by Cursor Project Onboarding Skill*

## Quick Start

### Prerequisites
{PREREQUISITES_LIST}

### Setup Commands  
```bash
{SETUP_COMMANDS}
```

### Essential Commands
{ESSENTIAL_COMMANDS_TABLE}

### First Steps
{FIRST_STEPS_CHECKLIST}

## Architecture Overview

### Project Type
{PROJECT_TYPE_DESCRIPTION}

### Technology Stack
{TECH_STACK_BREAKDOWN}

### System Design
{ARCHITECTURE_DECISIONS}

### Key Dependencies
{MAJOR_DEPENDENCIES_TABLE}

## User Flows

### End User Journey
{END_USER_FLOWS}

### Developer Journey  
{DEVELOPER_WORKFLOWS}

### Authentication & Access
{AUTH_FLOW_DETAILS}

## Code Patterns & Standards

### File Organization
{FILE_STRUCTURE_EXPLANATION}

### Naming Conventions
{NAMING_PATTERNS_WITH_EXAMPLES}

### Component Patterns
{COMPONENT_EXAMPLES}

### Error Handling
{ERROR_HANDLING_PATTERNS}

### Testing Approach
{TESTING_STRATEGY_DETAILS}

## Component Libraries & Dependencies

### UI Libraries
{UI_LIBRARIES_DETAILS}

### Internal Libraries
{INTERNAL_LIBRARIES_BREAKDOWN}

### Utility Libraries
{UTILITY_DEPENDENCIES}

### Development Tools
{DEV_TOOLS_LIST}

## AI Skills & Automation

### Cursor Skills
{CURSOR_SKILLS_FOUND}

### Development Automation
{AUTOMATION_TOOLS}

### CI/CD Pipeline
{CICD_DETAILS}

## Entry Points for Common Tasks

### Adding a New Feature
**Start here:** {NEW_FEATURE_ENTRY_POINTS}
**Follow this pattern:** {FEATURE_IMPLEMENTATION_PATTERN}
**Test with:** {TESTING_COMMANDS}

### Fixing a Bug  
**Look here first:** {BUG_INVESTIGATION_ENTRY_POINTS}
**Debug with:** {DEBUGGING_TOOLS_AND_COMMANDS}
**Verify fix:** {BUG_VERIFICATION_STEPS}

### Understanding Data Flow
**Key files:** {DATA_FLOW_KEY_FILES}
**Trace from:** {DATA_FLOW_STARTING_POINTS}
**Monitor with:** {DATA_MONITORING_TOOLS}

### Modifying UI/Components
**Component locations:** {UI_COMPONENT_DIRECTORIES}
**Design system:** {DESIGN_SYSTEM_DETAILS}
**Preview changes:** {UI_DEVELOPMENT_WORKFLOW}

## Development Workflow

### Branch Strategy
{BRANCH_STRATEGY_DETAILS}

### Code Review Process  
{CODE_REVIEW_WORKFLOW}

### Testing Requirements
{TESTING_REQUIREMENTS_CHECKLIST}

### Deployment Process
{DEPLOYMENT_WORKFLOW}

## Troubleshooting & FAQ

### Common Setup Issues
{COMMON_SETUP_PROBLEMS}

### Development Environment
{DEV_ENV_TROUBLESHOOTING}

### Build & Test Issues  
{BUILD_TROUBLESHOOTING}

### Where to Find Help
{HELP_RESOURCES}

---

*This guide was automatically generated by analyzing the codebase. For questions or updates, re-run `/project-onboarding` or check the project's main documentation.*
```

## Template Variable Population

Each `{VARIABLE}` in the template gets populated based on analysis results:

### Project Discovery Variables
- `{PROJECT_NAME}`: Extracted from package.json name field or directory name
- `{PROJECT_TYPE_DESCRIPTION}`: Based on manifest analysis and structure detection
- `{TECH_STACK_BREAKDOWN}`: Formatted list of frameworks, languages, major libraries
- `{PREREQUISITES_LIST}`: Based on project type (Node.js, Python, Docker, etc.)

### Commands and Setup Variables  
- `{SETUP_COMMANDS}`: Installation and initial setup commands
- `{ESSENTIAL_COMMANDS_TABLE}`: Build, test, dev, lint commands in table format
- `{FIRST_STEPS_CHECKLIST}`: Actionable checklist for new contributors

### Architecture Variables
- `{ARCHITECTURE_DECISIONS}`: Key architectural insights from semantic search
- `{MAJOR_DEPENDENCIES_TABLE}`: Dependencies categorized by purpose with descriptions
- `{FILE_STRUCTURE_EXPLANATION}`: Directory structure with purpose explanations

### Flow Variables  
- `{END_USER_FLOWS}`: User journey descriptions with entry points
- `{DEVELOPER_WORKFLOWS}`: Step-by-step developer processes
- `{AUTH_FLOW_DETAILS}`: Authentication/authorization implementation details

### Pattern Variables
- `{NAMING_PATTERNS_WITH_EXAMPLES}`: Real code examples showing conventions
- `{COMPONENT_EXAMPLES}`: Sample component code showing patterns
- `{ERROR_HANDLING_PATTERNS}`: Error handling approaches with examples
- `{TESTING_STRATEGY_DETAILS}`: Testing framework, structure, conventions

### Library Variables
- `{UI_LIBRARIES_DETAILS}`: UI frameworks and component libraries used
- `{INTERNAL_LIBRARIES_BREAKDOWN}`: Internal shared code and utilities  
- `{CURSOR_SKILLS_FOUND}`: Detected Cursor skills with descriptions

### Entry Point Variables
- `{NEW_FEATURE_ENTRY_POINTS}`: Specific files/directories for new features
- `{BUG_INVESTIGATION_ENTRY_POINTS}`: Where to start when debugging
- `{DATA_FLOW_KEY_FILES}`: Important files for understanding data flow
- `{UI_COMPONENT_DIRECTORIES}`: Where UI components are located

### Workflow Variables
- `{BRANCH_STRATEGY_DETAILS}`: Git workflow from config analysis
- `{CODE_REVIEW_WORKFLOW}`: Review process from project conventions
- `{DEPLOYMENT_WORKFLOW}`: CI/CD and deployment process details

### Troubleshooting Variables  
- `{COMMON_SETUP_PROBLEMS}`: Known issues based on project type
- `{HELP_RESOURCES}`: Links to docs, discussions, contacts found in project

This template ensures comprehensive coverage while remaining readable and actionable for new developers.

## Validation and Quality Checks

Before finalizing the guide, perform these validation steps:

### Content Quality Gates
1. **Completeness Check**: Ensure all major sections have meaningful content
2. **Accuracy Verification**: Cross-reference findings with actual project files
3. **Actionability Test**: Verify that entry points and commands are valid
4. **Readability Assessment**: Guide should be scannable in 10-15 minutes

### Post-Generation Validation
```
After guide generation:

1. Check guide length (target: 2000-5000 words)
2. Verify all template variables were populated
3. Validate that code examples are real (not placeholder text)
4. Ensure commands are executable in the current environment
5. Confirm entry points actually exist in the codebase

If validation fails:
- Log specific issues found
- Attempt to regenerate affected sections
- Proceed with partial guide if time limits exceeded
```

## Error Recovery Strategies

### Graceful Degradation
When analysis phases encounter issues:

1. **File Access Errors**: Continue with available files, note missing data
2. **Time Limit Exceeded**: Generate guide with collected data, mark incomplete sections  
3. **Large Codebase**: Use sampling strategy, focus on most important files
4. **Unknown Project Type**: Generate generic structure-based analysis
5. **No Dependencies Found**: Focus on file structure and code pattern analysis

### User Communication
Provide clear status updates throughout the process:

```
"🔍 Analyzing project structure... (1/6 phases complete)"
"📋 Mapping user flows... (3/6 phases complete)"  
"⚠️  Large codebase detected, using targeted sampling approach"
"✅ Analysis complete! Generated 4,200-word onboarding guide."
"💡 Found 3 Cursor skills, 2 component libraries, and 15 key entry points."
```

## Testing Scenarios

The skill has been designed to handle these project types:

### Web Applications
- **React/Next.js apps**: Component analysis, routing patterns, API structure
- **Vue/Nuxt apps**: Component composition, store patterns, build configuration  
- **Angular apps**: Module structure, service patterns, dependency injection
- **Full-stack apps**: Frontend/backend integration, database connections

### Backend Services  
- **Node.js APIs**: Route handlers, middleware patterns, database integration
- **Python web services**: Framework detection (Django/Flask/FastAPI), ORM usage
- **Go services**: Package structure, handler patterns, configuration management
- **Microservices**: Service boundaries, inter-service communication

### CLI Tools & Libraries
- **CLI applications**: Command structure, argument parsing, configuration
- **npm/Python packages**: Public API design, usage examples, testing approach
- **Utility libraries**: Function organization, documentation patterns

### Mobile Applications
- **React Native**: Component patterns, navigation, native module integration  
- **Flutter**: Widget composition, state management, platform-specific code
- **Native iOS/Android**: Project structure, architecture patterns

## Success Metrics

A successful project onboarding guide should achieve:

### Quantitative Measures
- **Analysis completion**: 90%+ of phases complete within time limits
- **Guide length**: 2000-5000 words (comprehensive but scannable)
- **Entry point coverage**: 80%+ of main development tasks have clear starting points
- **Code example quality**: Real code snippets, not placeholder text

### Qualitative Measures  
- **Clarity**: New developer can identify "where to start" within 5 minutes
- **Completeness**: Covers both user experience and developer experience
- **Actionability**: Provides specific next steps, not just descriptions
- **Accuracy**: Commands work, file paths exist, patterns reflect actual code

### User Experience Indicators
- Developer can set up environment from guide instructions
- Developer can locate files for common tasks (add feature, fix bug, etc.)
- Developer understands project conventions without asking questions
- Developer can contribute meaningfully within first day using guide

The skill succeeds when it eliminates the overwhelming "where do I even start?" feeling that blocks newcomers to complex codebases.