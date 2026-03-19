# CONFIG_SkillDefinition.md

## Purpose
The SKILL.md file is the primary interface between Claude Code and the NotebookLM skill. Claude Code reads this file to understand when to activate the skill, how to use each script, and what workflow to follow. It is the operational manual Claude reads, not the human documentation.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `SKILL.md`
- **Current interfaces:** Read by Claude Code skill system via YAML frontmatter + markdown content
- **Dependencies:** None (static file)
- **Dependents:** Claude Code (reads on skill activation), all scripts (documented here)

## Core Logic & Functionality

### YAML Frontmatter
```yaml
---
name: notebooklm
description: Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini. Browser automation, library management, persistent auth. Drastically reduced hallucinations through document-only responses.
---
```

### Key Sections
1. **When to Use This Skill** — trigger conditions (explicit mention, URL sharing, "ask my docs")
2. **Critical: Add Command - Smart Discovery** — workflow for adding notebooks without known metadata
3. **Critical: Always Use run.py Wrapper** — mandatory usage pattern with examples
4. **Core Workflow** — 4-step flow: check auth → authenticate → manage library → ask questions
5. **Follow-Up Mechanism** — CRITICAL: Claude must analyze response and ask follow-ups automatically
6. **Script Reference** — complete CLI reference for all scripts
7. **Troubleshooting** — common errors and solutions

### Follow-Up Mechanism (Critical Behavior)
Every NotebookLM answer ends with "EXTREMELY IMPORTANT: Is that ALL you need to know?" — Claude MUST:
1. Stop, analyze the answer vs the original request
2. Identify information gaps
3. Ask follow-up questions to fill gaps
4. Synthesize all answers before responding to user

## Current Quality Assessment
- **Completeness:** Covers all scripts and critical workflows; recently updated for v1.3.0
- **Code Quality:** Well-structured with clear sections; CRITICAL callouts for non-obvious behaviors
- **Test Coverage:** N/A — static documentation
- **Documentation:** This IS the documentation (self-referential)

## Technical Debt & Improvement Areas
- Selector values in troubleshooting section may drift from config.py
- Smart Add workflow uses hardcoded question text — could be improved with dynamic notebook type detection
- Follow-up mechanism described but not enforced — depends on Claude following instructions

## Interface Definition

```yaml
# YAML frontmatter (Claude Code reads this):
---
name: notebooklm
description: <used for skill search/activation>
---

# Usage (Claude follows workflow from this file):
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Claude Code loads skill when user mentions "NotebookLM" or shares a notebook URL
- [ ] YAML frontmatter `name` matches skill directory name (notebooklm)
- [ ] All CLI examples in SKILL.md are syntactically correct

### Input Validation Criteria
- [ ] N/A — static file

### Error Handling Criteria
- [ ] Troubleshooting section covers all known failure modes

### Quality Criteria
- [ ] run.py wrapper usage enforced in all code examples (no direct script calls)
- [ ] Follow-up mechanism clearly described with step-by-step instructions
- [ ] Smart Add workflow prevents Claude from using generic/unknown descriptions

## Future Enhancement Opportunities
- Add version header matching CHANGELOG.md version
- Add environment requirements section (local Claude Code only, no web UI)
- Auto-validate CLI examples against actual script argparse definitions
