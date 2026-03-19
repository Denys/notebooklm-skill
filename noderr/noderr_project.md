# Project Overview: NotebookLM Claude Code Skill

---

**Purpose of this Document:** This `noderr_project.md` is a core artifact of the Noderr v1.9 system. It provides a comprehensive high-level summary of the project, including its goals, scope, technology stack, architecture, coding standards, and quality priorities. The AI Agent will reference this document extensively for context and guidance throughout the development lifecycle, as detailed in `noderr_loop.md`.

---

### 1. Project Goal & Core Problem

*   **Goal:** Enable Claude Code to query Google NotebookLM notebooks directly via browser automation, receiving source-grounded, Gemini-powered answers exclusively from uploaded documents.
*   **Core Problem Solved:** When Claude reads local documentation files, it consumes massive tokens, misses context, and hallucinates APIs. Users also waste time copy-pasting between NotebookLM browser and their editor. This skill eliminates both problems by having Claude ask NotebookLM directly — zero copy-paste, zero hallucinations.

---

### 2. Scope & Key Features (MVP Focus)

*   **Minimum Viable Product (MVP) Description:** A working Claude Code Skill that authenticates with Google, manages a local notebook library, and queries any NotebookLM notebook via browser automation — returning source-grounded answers with citation backing.

*   **Key Features (In Scope for MVP):**
    *   `Authentication Management`: One-time Google login via visible Chrome browser. Persistent session cookies stored locally. Status check, reauth, and clear commands.
    *   `Notebook Library Management`: CRUD operations on a local JSON library. Add notebooks with required metadata (name, description, topics), list, search by topic, activate default, remove.
    *   `NotebookLM Query Interface`: Browser automation that types a question into NotebookLM, waits for Gemini's streaming response, extracts the answer text, and returns it to Claude.
    *   `Environment Setup`: Auto-creation of Python virtual environment (.venv), dependency installation (patchright, python-dotenv), Chrome download — all on first run via run.py wrapper.
    *   `Data Cleanup`: Browser cache clearing, auth data removal, library reset — with options to preserve notebook metadata.

*   **Key Features (Explicitly OUT of Scope for MVP):**
    *   `Automated Document Upload`: Users must manually upload documents to NotebookLM via browser. No programmatic upload API exists.
    *   `Multi-Account Support`: Single Google account per installation. No account switching.
    *   `Session Persistence`: Each query starts a fresh browser session. Stateless by design to avoid state contamination.
    *   `Web UI or API Server Mode`: CLI tool only. No HTTP server, no REST API.

---

### 3. MVP Implementation Status

**MVP Completion: 83% (15 of 18 total NodeIDs implemented)**

| Feature | Existing NodeIDs | Missing NodeIDs |
|---------|-----------------|-----------------|
| Environment Setup | UTIL_RunWrapper, SVC_SetupEnvironment | — |
| Authentication | AUTH_Manager | — |
| Browser Automation | SVC_BrowserSession, UTIL_BrowserUtils, SVC_AskQuestion | SVC_RetryLogic |
| Notebook Management | SVC_NotebookManager | — |
| Data Storage | DATA_NotebookLibrary, DATA_AuthInfo, DATA_BrowserState | — |
| Configuration | CONFIG_Settings, CONFIG_SkillDefinition, CONFIG_Requirements, SVC_SkillInit | — |
| Cleanup | SVC_CleanupManager | — |
| Testing | — | TEST_AuthFlow, TEST_QueryFlow |

**Missing for MVP Completion:**
*   `TEST_AuthFlow` — Automated test for authentication setup and verification workflow
*   `TEST_QueryFlow` — End-to-end automated test for querying a NotebookLM notebook
*   `SVC_RetryLogic` — Dedicated retry/recovery logic for browser crashes and rate limits (currently manual workaround via cleanup_manager.py)

---

### 4. Technology Stack

*   **Language:** Python 3.13.7 (also compatible with 3.11+)
*   **Browser Automation:** Patchright 1.55.2 (Playwright fork with anti-detection patches)
*   **Browser:** Google Chrome (downloaded automatically by setup_environment.py — NOT Chromium, for fingerprint stability with Google services)
*   **Config:** python-dotenv 1.0.0 (optional .env file for headless/stealth settings)
*   **Python Package Manager:** pip 25.2 (via isolated .venv per skill installation)
*   **Version Control:** Git 2.53.0 (Windows), hosted at github.com/PleasePrompto/notebooklm-skill
*   **Platform:** Local Windows 11 (MINGW64/Git Bash), also compatible with Linux/Mac
*   **Current Version:** v1.3.0

---

### 5. Architecture Overview

The skill follows a **stateless, process-per-query** pattern:

```
User Request → Claude Code reads SKILL.md
    → Bash: python scripts/run.py <script.py> [args]
        → run.py: venv check → ensure_venv()
        → Target Script: auth / notebook / ask
            → Patchright: Chrome launch → notebooklm.google.com
            → Response extracted from DOM
    → Answer returned to Claude → User gets source-grounded answer
```

**Key architectural decisions:**
*   **run.py as universal wrapper:** All scripts must be called via `run.py` to ensure the .venv is initialized and activated. Direct script calls fail without the venv context.
*   **Hybrid Authentication:** Persistent Chrome profile (user_data_dir) + manual cookie injection from state.json — workaround for Playwright bug #36139 where session cookies don't persist across browser launches.
*   **Stateless sessions:** Each browser session is fresh to avoid state contamination between queries. Auth state persists via file system (state.json), not in-memory.
*   **Local-only data:** All auth data, library metadata, and browser state stored in data/ directory, protected by .gitignore. Never committed to git.
*   **No framework dependencies:** Pure Python stdlib + patchright + python-dotenv. No web frameworks, no databases.

---

### 6. Coding Standards & Conventions

*   **NodeID Convention:** `TYPE_Name` (e.g., `AUTH_Manager`, `SVC_AskQuestion`, `CONFIG_Settings`)
*   **Script pattern:** Each script is self-contained with argparse for CLI args, callable independently via run.py
*   **All paths via config.py:** Use `SKILL_DIR`, `DATA_DIR`, `BROWSER_STATE_DIR`, etc. — never hardcode paths
*   **Always use run.py:** Scripts must be invoked as `python scripts/run.py <script.py> [args]`
*   **Auth-first pattern:** Scripts that open NotebookLM check auth status before launching browser
*   **Error exit codes:** `sys.exit(1)` on failure, `sys.exit(0)` on success

---

### 7. Quality Priorities

1.  **Reliability:** Browser automation must handle NotebookLM UI changes gracefully (update selectors in config.py when needed)
2.  **Security:** Sensitive auth data must never be committed to git (enforced by .gitignore)
3.  **Usability:** Zero-configuration first run — run.py handles all setup automatically
4.  **Minimal dependencies:** Only patchright + python-dotenv in requirements.txt
5.  **Source-grounded answers:** The entire value proposition is zero hallucinations — answers only from NotebookLM sources, never invented by Claude

---

### 8. Environment

*   Development environment: fully documented in `noderr/environment_context.md`
*   Project type: **CLI Tool / Claude Code Skill** — no web server, no URLs, no deployment
*   Install location: `~/.claude/skills/notebooklm/` (symlink, junction, or copy from source)
*   Runtime invocation: Claude Code reads `SKILL.md` frontmatter, triggers skill, uses Bash tool to call `python scripts/run.py ...`
*   Environment focus: DEVELOPMENT — local Windows 11 machine (denko / denkovalov@gmail.com)
