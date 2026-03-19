# UTIL_RunWrapper.md

## Purpose
Universal entry point for all NotebookLM skill scripts. Ensures every script runs inside the correct Python virtual environment (.venv), auto-creating it on first run. All other scripts depend on this wrapper.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/run.py`
- **Current interfaces:** `python scripts/run.py <script_name.py> [args...]`
- **Dependencies:** Python 3.13.7 system installation, `scripts/setup_environment.py`
- **Dependents:** Every other script in the skill (AUTH_Manager, SVC_AskQuestion, SVC_NotebookManager, SVC_CleanupManager)

## Core Logic & Functionality
1. Parses `sys.argv` to get target script name + passthrough args
2. Normalizes script name (strips `scripts/` prefix if given, adds `.py` if missing)
3. Calls `ensure_venv()` — checks if `.venv/` exists; if not, runs `setup_environment.py` with system Python
4. Resolves `venv_python` path (Windows: `.venv/Scripts/python.exe`, Unix: `.venv/bin/python`)
5. Builds and executes `subprocess.run([venv_python, script_path] + args)`
6. Propagates exit code from child process

## Current Quality Assessment
- **Completeness:** Fully functional for its purpose
- **Code Quality:** Clean, well-structured, handles both Windows and Unix paths
- **Test Coverage:** No automated tests; manually verified
- **Documentation:** Inline comments present; SKILL.md documents usage

## Technical Debt & Improvement Areas
- No retry logic if subprocess fails due to transient issues
- Error messages could be more specific (e.g., distinguish Python version issues from missing venv)
- Does not validate that `script_name` is a safe/known script name (minor security consideration)

## Interface Definition

```python
# CLI usage:
python scripts/run.py <script_name.py> [args...]

# Key functions:
def get_venv_python() -> Path  # Returns path to venv Python executable
def ensure_venv() -> Path      # Creates venv if absent, returns venv Python path
def main() -> None             # Parses args, ensures venv, executes target script
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Running `python scripts/run.py auth_manager.py status` completes without error
- [ ] First run creates `.venv/` directory automatically
- [ ] Script handles both `script.py` and `scripts/script.py` as input formats
- [ ] Nonexistent script name exits with code 1 and clear error message

### Input Validation Criteria
- [ ] Missing script argument prints usage and exits 1
- [ ] Invalid script name prints helpful error with looked-for path

### Error Handling Criteria
- [ ] Setup failure (venv creation) exits 1 with message
- [ ] KeyboardInterrupt handled gracefully (exit 130)
- [ ] Subprocess exceptions caught and reported

### Quality Criteria
- [ ] Windows and Unix paths handled correctly
- [ ] Exit code propagated from child process

## Future Enhancement Opportunities
- Add allowlist of known script names for security
- Add `--help` flag that lists available scripts
- Add version flag to display skill version from CHANGELOG.md
