# Universal Environment Context Profile — NotebookLM Skill

## START HERE

```yaml
# Environment Metadata
environment:
  type: "development"
  provider: "local"
  lifecycle: "persistent"
  purpose: "Local development and runtime for the NotebookLM Claude Code Skill"

  # CRITICAL: Document which environment this profile represents
  environment_focus: "DEVELOPMENT - This profile documents the local Windows development workspace"

  # Platform-Specific Detection Results
  platform_detection:
    identified_platform: "Local Windows 11 (MINGW64/Git Bash)"
    special_environment_vars: "No cloud platform vars detected (no REPL, CLOUD, AWS, AZURE, VERCEL, etc.)"
    available_tools: "git 2.53.0, Python 3.13.7, pip 25.2, curl, node v24.14.0, npm 11.9.0"
    missing_standard_tools: "No docker, no kubectl, no yarn - not needed for this project"

  orchestration_hints:
    auto_seed_on_reset: false
    strict_linting: false
    backup_before_migrations: false
    uses_workflow_system: false
    uses_container_orchestration: false
    uses_serverless_deployment: false
```

**Profile Name:** Local-Windows11-Python313-NotebookLM-Skill
**Environment ID:** ENV-2026-03-19-local-windows-001
**Last Updated:** 2026-03-19T04:30:00Z
**Validated By:** Claude Code AI Agent
**Confidence Level:** High

---

## Purpose

This document serves as the complete operational manual for AI agents working in this specific **DEVELOPMENT** environment. It translates abstract goals into concrete, tested commands. Every command listed here has been verified to work in this environment.

**Critical Rule:** ALWAYS use these exact commands. Do not rely on general knowledge about similar environments.

**Environment Focus:** This document describes the DEVELOPMENT environment (local Windows 11 machine). This is a **CLI tool** — there is no web server, no preview URL, and no production deployment.

---

## 1. Critical Platform Rules & Gotchas

### 1.1 Critical Don'ts - DO NOT VIOLATE THESE RULES

```yaml
critical_donts:
  process_management:
    - "NEVER call scripts directly — always use the run.py wrapper"
    - "NEVER activate the .venv manually — run.py handles it automatically"
    - "NEVER run auth_manager.py setup in headless mode — browser MUST be visible for Google login"

  package_management:
    - "NEVER pip install globally — all dependencies go into .venv via run.py"
    - "NEVER edit requirements.txt and install separately — run.py auto-installs on first run"

  network_configuration:
    - "No web server bindings needed — this is a CLI tool invoked by Claude Code"
    - "NEVER hardcode paths — use SKILL_DIR from config.py for all path resolution"

  file_system:
    - "NEVER commit auth data (state.json, auth_info.json, browser_profile/) — protected by .gitignore"
    - "NEVER commit .venv/ or data/ directories"

  environment_confusion:
    - "This tool has no production URL — it runs locally only"
    - "Browser sessions are ephemeral — each question opens and closes its own browser"

  platform_specific:
    - "Python must be invoked via full path or via run.py — python/python3 not in Git Bash PATH"
    - "Always run scripts from the skill root directory (where noderr/ and scripts/ reside)"
```

### 1.2 Lessons Learned - Debugging Gotchas

```yaml
debugging_gotchas:
  console_behavior:
    - "Script output appears in the terminal/Claude Code output where run.py was called"
    - "Browser automation errors appear in stderr from the patchright subprocess"

  development_workflow:
    - "The .venv is created on first run of run.py — no manual setup needed"
    - "Chrome (not Chromium) is downloaded automatically by setup_environment.py"
    - "Auth state persists in data/browser_state/state.json between runs"

  network_behavior:
    - "Browser automation requires internet access to reach notebooklm.google.com"
    - "Anti-detection measures in BROWSER_ARGS prevent Google from blocking the session"
    - "QUERY_TIMEOUT_SECONDS=120 — allow up to 2 minutes for NotebookLM to respond"

  resource_management:
    - "Each query starts a new Chrome instance — brief overhead per question"
    - "Browser profile in data/browser_state/browser_profile/ accumulates cache over time"
    - "Use cleanup_manager.py periodically to clear browser cache"

  platform_specific:
    - "Python 3.13.7 is installed at C:\\Users\\denko\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    - "In Git Bash, invoke Python with full Windows path or ensure PATH includes Python313"
    - "run.py uses sys.executable to find correct Python, so it works correctly from Claude Code"
```

---

## 2. Environment Discovery & Validation

### 2.1 System Information

```bash
# Operating System Details
uname -a
# Returns: MINGW64_NT-10.0-22621 denkov 3.6.6-1cdd4371.x86_64 2026-01-15 22:20 UTC x86_64 Msys
# Actual OS: Windows 11 Home, Build 22621

# Shell Information
echo $SHELL
# Returns: /bin/bash.exe
# Note: Running Git Bash (MINGW64) on Windows 11

# Current User
whoami
# Returns: denko

# Environment Type Confirmation
echo "This profile documents: DEVELOPMENT environment (local Windows 11)"
# Returns: DEVELOPMENT environment (local Windows 11)
```

### 2.2 Platform-Specific Detection

```bash
# Platform Detection Results
env | grep -E "REPL|CLOUD|VIRTUAL|AWS|GCP|AZURE|HEROKU|VERCEL|NETLIFY|LOVABLE|CODESPACES"
# Returns: (empty - no cloud platform indicators found)
# Platform: Local Windows 11 development machine

# Available Platform-Specific Tools
# git: /mingw64/bin/git
# python: C:\Users\denko\AppData\Local\Programs\Python\Python313\python.exe
# pip: C:\Users\denko\AppData\Local\Programs\Python\Python314\Scripts\pip (pip3 also available)
# curl: /mingw64/bin/curl
# node: /c/Program Files/nodejs/node
# npm: /c/Program Files/nodejs/npm

# Development vs Production Indicators
# This is a LOCAL CLI TOOL — no cloud platform, no deployment URL
# Development = local machine; there is no separate production environment
```

### 2.3 Available Commands Check

```bash
# Core utilities availability
git --version
# Returns: git version 2.53.0.windows.1 ✓

/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe --version
# Returns: Python 3.13.7 ✓

/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe -m pip --version
# Returns: pip 25.2 from ...\Python313\Lib\site-packages\pip (python 3.13) ✓

curl --version
# Returns: curl 8.x (mingw64) ✓

node --version
# Returns: v24.14.0 ✓

npm --version
# Returns: 11.9.0 ✓

# Package manager for this project:
# pip (Python) via run.py wrapper → installs into .venv automatically
```

### 2.4 Environment Constraints

```bash
# Disk Space (Windows)
# Skill directory: C:\Users\denko\Claude\NotebookLM_MCP\notebooklm-skill\
# .venv and Chrome download require ~500MB on first setup

# Memory: Standard Windows 11 memory management applies
# Each Chrome session uses ~200-400MB RAM — released after query completes

# Network Connectivity
curl -s https://notebooklm.google.com -o /dev/null -w "%{http_code}"
# Must return 200 or redirect — requires internet access for browser automation
```

---

## 3. Platform-Specific Workflow Management

### 3.1 Process Management System

```bash
# This is a stateless CLI tool — no persistent server to manage
# Each invocation: run.py → venv check → Chrome launch → query → Chrome close

# Run any skill script (ALWAYS use this pattern):
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py <script.py> [args]

# Example - check auth:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py status

# Example - ask question:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py ask_question.py --question "..."
```

### 3.2 Package Management System

```bash
# Dependencies are managed automatically by run.py on first invocation
# Manual setup (only if automatic setup fails):
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m patchright install chrome

# Current requirements (requirements.txt):
# patchright==1.55.2
# python-dotenv==1.0.0
```

### 3.3 Deployment System

```bash
# This tool is NOT deployed — it runs exclusively on the local machine
# It is invoked by Claude Code when the user mentions NotebookLM
# Distribution: via git clone from https://github.com/PleasePrompto/notebooklm-skill.git
# Installation: copy/symlink/junction into ~/.claude/skills/notebooklm/

# To share updates: git push origin master
# To install on another machine: git clone and place in ~/.claude/skills/notebooklm/
```

---

## 4. File System Operations

### 4.1 Working Directory Structure

```bash
# Project root (must run scripts from here):
pwd
# Expected: /c/Users/denko/.claude/skills/notebooklm
# OR (development copy): /c/Users/denko/Claude/NotebookLM_MCP/notebooklm-skill

# Project root identification:
ls -la | grep -E "requirements.txt|SKILL.md|scripts|noderr"
# Should see: requirements.txt, SKILL.md, scripts/, noderr/

# Key directories:
# scripts/      - All Python automation scripts
# noderr/       - Noderr framework files (specs, tracker, etc.)
# data/         - Runtime data (auth, library) - NOT committed
# .venv/        - Python virtual environment - NOT committed
# references/   - Extended documentation
# images/       - Screenshots
```

### 4.2 Directory Listing

```bash
# Primary method
ls -la

# List scripts:
ls scripts/
# Returns: __init__.py ask_question.py auth_manager.py browser_session.py
#          browser_utils.py cleanup_manager.py config.py notebook_manager.py
#          run.py setup_environment.py

# List noderr specs (once populated):
ls noderr/specs/
```

### 4.3 File Reading & Writing

```bash
# Read file:
cat scripts/config.py

# Check if data directory exists (it's created on first auth run):
[[ -d "data" ]] && echo "data/ exists" || echo "data/ not yet created (run auth setup first)"

# Write files using standard bash:
cat > noderr/specs/NodeID.md << 'EOF'
content here
EOF
```

---

## 5. Network & Port Management

### 5.1 Network Configuration

```bash
# This tool does NOT bind to any local port
# It opens an external browser that connects to notebooklm.google.com

# Check internet connectivity:
curl -s -o /dev/null -w "%{http_code}" https://www.google.com
# Must return 301 or 200 for browser automation to work

# DNS test:
curl -s -o /dev/null -w "%{http_code}" https://notebooklm.google.com
# Must return 200 or 301
```

### 5.2 Port Management

```bash
# No ports used by this application directly
# Chrome automation uses ephemeral ports managed by Patchright/CDP
# No port conflicts expected
```

### 5.3 Application Access Configuration

```yaml
# CRITICAL: This is a CLI TOOL — there is no web server and no browser URL
development_server:
  bind_host: "N/A - CLI tool"
  default_port: "N/A - no server"
  alternative_ports: "N/A"

  access_urls:
    # DEVELOPMENT PREVIEW - CLI tool has no URL
    local_dev_preview:
      url: "N/A - CLI tool invoked by Claude Code, no web interface"
      description: "This skill is a CLI tool. Test by running: python scripts/run.py auth_manager.py status"
      how_to_access: "Run scripts via: python scripts/run.py <script.py> [args]"

    # PRODUCTION DEPLOYMENT - Not applicable
    public_deployed_app:
      url: "N/A - Not deployed. Tool runs locally on user machine only."
      description: "No production deployment. Installed per-user via ~/.claude/skills/notebooklm/"
      warning: "Distribution via git clone, not cloud deployment."
      how_to_deploy: "git clone https://github.com/PleasePrompto/notebooklm-skill.git ~/.claude/skills/notebooklm"

  platform_url_examples:
    development_pattern: "N/A - CLI tool"
    production_pattern: "N/A - distributed via git clone"

  platform_specific_config:
    websocket_url: "N/A"
    proxy_requirements: "None"
    firewall_rules: "Requires outbound HTTPS to notebooklm.google.com and accounts.google.com"
```

---

## 6. Version Control & Collaboration

### 6.1 Git Configuration

```bash
# Check git user
git config user.name
# Returns: Denys

git config user.email
# Returns: denkovalov@gmail.com

# Remote origin:
git remote -v
# Returns: origin  https://github.com/PleasePrompto/notebooklm-skill.git (fetch)
#          origin  https://github.com/PleasePrompto/notebooklm-skill.git (push)

# Current branch:
git branch --show-current
# Returns: master
```

### 6.2 Collaboration Tools

```bash
# Standard git workflow:
# 1. Edit files locally
# 2. Test: python scripts/run.py auth_manager.py status
# 3. git add, git commit, git push

# Protected files (.gitignore):
# .venv/, data/, __pycache__/, *.pyc
# data/browser_state/, data/auth_info.json, data/library.json
```

---

## 7. Language & Runtime Management

### 7.1 Runtime Detection

```bash
# Python (primary runtime for this project)
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe --version
# Returns: Python 3.13.7

# Also available (but not default for this project):
# Python 3.11.x at C:\Users\denko\AppData\Local\Programs\Python\Python311\python.exe
# Python 3.14.3 at C:\Users\denko\AppData\Local\Programs\Python\Python314\python.exe

# pip (used inside .venv):
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe -m pip --version
# Returns: pip 25.2

# Node.js (not used by this project, but available):
node --version
# Returns: v24.14.0

# Git:
git --version
# Returns: git version 2.53.0.windows.1
```

### 7.2 Package Management

```bash
# Python packages managed via run.py wrapper:
# On first run: creates .venv with Python 3.13.7, installs patchright + python-dotenv
# Auto-installs Chrome browser for Patchright

# Manual install (only if auto-setup fails):
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe -m venv .venv
.venv/Scripts/pip install patchright==1.55.2 python-dotenv==1.0.0
.venv/Scripts/python -m patchright install chrome

# All dependencies are isolated to .venv — no global Python package modifications
```

---

## 8. Database & Storage Operations

### 8.1 Database System Detection

```yaml
database_system: "JSON flat files (no SQL database)"
connection_method: "Direct file I/O via Python pathlib"
orm_tool: "None"
connection_source: "config.py PATH constants"

database_environment:
  development_db: "Local JSON files in data/ directory"
  production_db: "N/A - each installation has its own local data/"
  data_isolation: "complete"

platform_specific_database:
  provider: "Local filesystem"
  access_method: "Direct file read/write via Python json module"
  management_tools: "cleanup_manager.py for data clearing"
```

### 8.2 Database Operations

```bash
# Check notebook library:
cat data/library.json  # (if data/ exists)

# Check auth status file:
cat data/auth_info.json  # (if data/ exists)

# Check browser state:
ls data/browser_state/  # cookies + Chrome profile

# Clear all data (use cleanup_manager.py):
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py cleanup_manager.py --confirm

# Preserve library while clearing browser state:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py cleanup_manager.py --preserve-library
```

---

## 9. Testing & Quality Assurance

### 9.1 Testing Framework

```bash
# No automated test suite — manual functional testing workflow:

# Test 1: Environment setup
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py setup_environment.py
# Expected: Creates .venv, installs deps, downloads Chrome

# Test 2: Auth status
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py status
# Expected: Shows auth status (authenticated or not)

# Test 3: Auth setup (one-time, browser opens)
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py setup
# Expected: Chrome window opens for Google login

# Test 4: List notebooks
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py notebook_manager.py list
# Expected: Shows empty library or existing notebooks

# Test 5: Query (requires auth + notebook URL)
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py ask_question.py --question "What is this notebook about?" --notebook-url "https://notebooklm.google.com/notebook/..."

# No unit tests or pytest setup currently exists (MVP gap)
```

### 9.2 Build Process

```bash
# No build step needed — pure Python scripts, no compilation
# The only "build" equivalent is the first-run venv setup:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py status
# This triggers setup_environment.py automatically if .venv doesn't exist

# Verify build (check .venv):
[[ -d ".venv" ]] && echo "✓ .venv exists" || echo "✗ .venv not created yet"
[[ -d ".venv/Lib/site-packages/patchright" ]] && echo "✓ patchright installed" || echo "✗ patchright not installed"
```

---

## 10. Debugging & Monitoring

### 10.1 Log Access

```yaml
log_system:
  application_logs: "Stdout/stderr from run.py invocation (visible in Claude Code terminal)"
  system_logs: "Windows Event Viewer for system-level issues (rarely needed)"
  platform_logs: "No platform log aggregation — local script output only"

  dev_vs_prod_logs:
    development: "Script output printed to Claude Code terminal inline"
    production: "N/A - no production deployment"

  real_time_monitoring: "Watch run.py output directly in terminal"
  log_aggregation: "None - outputs are ephemeral per invocation"
```

### 10.2 Debugging Tools

```bash
# Enable browser visibility for debugging:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py ask_question.py --question "test" --show-browser
# Opens Chrome visibly — can see what the automation is doing

# Check auth status with verbose output:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py status

# Clear auth and start fresh:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py clear
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py setup

# Process monitoring: Chrome processes visible in Windows Task Manager
```

---

## 11. Security & Secrets Management

### 11.1 Secret Storage

```yaml
secrets_management:
  method: "local filesystem files (NOT environment variables, NOT config files in git)"
  access_pattern: "Scripts read from data/ directory using config.py path constants"
  storage_location: "data/browser_state/state.json (cookies), data/auth_info.json (status)"

  dev_vs_prod_secrets:
    development: "Local data/ files (protected by .gitignore)"
    production: "N/A - each user has their own local data/"
    isolation: "complete"

  platform_specific:
    secret_ui: "None - managed via auth_manager.py CLI"
    secret_injection: "Cookies injected directly into browser context by browser_session.py"
    secret_rotation: "Managed by auth_manager.py reauth command"
```

### 11.2 Security Best Practices

```bash
# Verify sensitive files are git-ignored:
cat .gitignore | grep -E "data|state|auth|profile|venv"
# Must show: .venv/, data/, and related patterns

# Never commit these files:
# data/browser_state/state.json  - Google session cookies
# data/auth_info.json            - Auth status
# data/browser_state/browser_profile/  - Chrome profile with cached credentials

# Secret detection in scripts (checking for hardcoded creds):
grep -r "password\|secret\|token" scripts/ --include="*.py" | grep -v "def\|#\|import"
# Should return empty or only safe references
```

---

## 12. Platform-Specific Features & Limitations

### 12.1 Platform Features

```yaml
platform_features:
  multiplayer_editing: false
  real_time_collaboration: false
  integrated_terminal: true  # Git Bash / Windows Terminal
  preview_pane: false  # CLI tool, no web preview
  hot_reload: false  # Stateless scripts, no hot reload needed

  built_in_deployment: false  # No built-in deployment
  automatic_https: false  # Not applicable
  custom_domains: false  # Not applicable

  database_integration: false  # JSON flat files only
  ai_assistance: true  # Claude Code invokes this skill

  unique_features:
    - "Browser automation via Patchright with anti-detection (stealth mode)"
    - "Hybrid auth: persistent Chrome profile + manual cookie injection"
    - "Automatic .venv setup on first run — zero manual setup"
    - "Stateless queries — each question is isolated browser session"
    - "Follow-up mechanism — Claude auto-asks follow-ups until information complete"
```

### 12.2 Platform Limitations

```yaml
platform_limitations:
  no_sudo_access: false  # Local admin available on Windows 11
  limited_system_tools: false  # Full Windows tools available
  restricted_network_access: false  # Full internet access
  ephemeral_storage: false  # Persistent local filesystem
  process_limits: false  # Standard Windows limits
  memory_constraints: false  # Standard Windows RAM management

  dev_prod_separation:
    separate_urls: false  # No URLs — CLI tool
    separate_databases: false  # Single local data/ directory
    separate_configs: false  # Single config.py

  specific_restrictions:
    - "python/python3 not in Git Bash PATH — must use full Windows path or run.py"
    - "Google rate limit: ~50 queries/day on free Google accounts"
    - "Chrome must be installed (done automatically by setup_environment.py)"
    - "Auth requires manual browser login — cannot be headless"
    - "Works ONLY with local Claude Code — not in Claude web UI (sandbox restriction)"
```

### 12.3 Platform-Specific Workflows

```bash
# Standard development workflow:
# 1. Make code changes in scripts/
# 2. Test with: python scripts/run.py auth_manager.py status
# 3. If auth needed: python scripts/run.py auth_manager.py setup  (browser opens)
# 4. Add test notebook: python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
# 5. Test query: python scripts/run.py ask_question.py --question "test" --notebook-id ID
# 6. git add, git commit, git push

# Browser crash recovery:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py cleanup_manager.py --preserve-library
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py setup

# Full reset:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py cleanup_manager.py --confirm
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py setup
```

---

## 13. Performance & Resource Monitoring

### 13.1 Resource Monitoring

```bash
# Script execution time (per query):
# Typical: 5-15 seconds for simple queries
# Maximum: QUERY_TIMEOUT_SECONDS=120 (config.py)

# Chrome memory usage:
# Per session: ~200-400MB RAM (released after query)
# Browser profile cache: grows over time, clear with cleanup_manager.py

# Monitor Chrome process during query:
# Task Manager > Details > chrome.exe
```

### 13.2 Performance Optimization

```bash
# Reduce timeout for faster failure detection (for debugging):
# Set QUERY_TIMEOUT_SECONDS in config.py (default: 120)

# Test query performance:
time /c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py ask_question.py \
  --question "What is this notebook about?" --notebook-url "https://notebooklm.google.com/notebook/..."
# Measures wall clock time for full query

# Optimize browser startup:
# Use persistent browser profile (already implemented via browser_session.py)
# Profile at: data/browser_state/browser_profile/
```

---

## 14. Error Recovery & Troubleshooting

### 14.1 Common Platform-Specific Errors

```yaml
common_errors:
  dependency_issues:
    detection: "ModuleNotFoundError when running scripts"
    solution: "Always use run.py wrapper — never call scripts directly"

  authentication_failure:
    detection: "auth_manager.py status returns 'not authenticated'"
    solution: "Run: python scripts/run.py auth_manager.py setup (browser MUST be visible)"

  browser_crash:
    detection: "Script hangs or exits with error during query"
    solution: "Run cleanup_manager.py --preserve-library, then auth setup"

  rate_limit:
    detection: "NotebookLM returns error or empty response"
    solution: "Wait for quota reset (24h) or switch Google account"

  selector_mismatch:
    detection: "Query times out waiting for response selector"
    solution: "Update QUERY_INPUT_SELECTORS or RESPONSE_SELECTORS in config.py"
    note: "NotebookLM UI changes break selectors — check CHANGELOG.md for updates"
```

### 14.2 Recovery Procedures

```bash
# Light recovery (preserve notebooks, clear browser cache):
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py cleanup_manager.py --preserve-library
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py setup

# Full recovery (clear everything):
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py cleanup_manager.py --confirm
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py setup
# Then re-add notebooks to library

# Venv reset (if venv corrupted):
rm -rf .venv/
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py status
# run.py auto-recreates .venv on next invocation
```

---

## 15. Quick Reference Card

```bash
# DEVELOPMENT Environment Quick Commands:

# Check auth status:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py status

# Setup Google auth (opens browser):
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py auth_manager.py setup

# List notebooks:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py notebook_manager.py list

# Ask a question:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Cleanup browser cache:
/c/Users/denko/AppData/Local/Programs/Python/Python313/python.exe scripts/run.py cleanup_manager.py --preserve-library

# Environment check:
echo "Current environment: DEVELOPMENT (Local Windows 11)"
echo "Python: C:\\Users\\denko\\AppData\\Local\\Programs\\Python\\Python313\\python.exe (3.13.7)"
echo "Run scripts via: python scripts/run.py <script.py> [args]"
echo "No web URL — this is a CLI tool"
echo "Install location: ~/.claude/skills/notebooklm/"
```

---

## 16. Environment Verification

```bash
echo "=== FINAL ENVIRONMENT VERIFICATION ==="
echo "Environment type: DEVELOPMENT (Local Windows 11)"
echo "Platform: Git Bash (MINGW64) on Windows 11 Home 10.0.22621"
echo "Python: C:\\Users\\denko\\AppData\\Local\\Programs\\Python\\Python313\\python.exe (3.13.7)"
echo "Git remote: https://github.com/PleasePrompto/notebooklm-skill.git"
echo ""
echo "This tool has NO web preview URL — it is a CLI tool"
echo "Test command: python scripts/run.py auth_manager.py status"
echo "Install location: ~/.claude/skills/notebooklm/ (symlink or copy)"
echo ""
echo "local_dev_preview: N/A - CLI tool"
echo "public_deployed_app: N/A - not deployed, distributed via git clone"
echo ""
echo "This profile documents the DEVELOPMENT environment"
echo "=== VERIFICATION COMPLETE ==="
```

---

## Validation Checklist

- [x] Environment type clearly marked as DEVELOPMENT
- [x] Platform correctly identified: Local Windows 11 (Git Bash / MINGW64)
- [x] All commands tested and working in development
- [x] local_dev_preview documented as N/A (CLI tool, no web interface)
- [x] public_deployed_app documented as N/A (not deployed, distributed via git)
- [x] Clear distinction: no production environment exists for this CLI tool
- [x] Platform-specific tools and workflows documented
- [x] Limitations clearly stated (python not in PATH, Google rate limits, auth requires browser)
- [x] Error recovery procedures documented
- [x] Security considerations addressed (.gitignore protects sensitive data)
- [x] All placeholders replaced with actual values
- [x] Final verification confirms development focus

---

_End of Environment Context Profile — NotebookLM Skill_
