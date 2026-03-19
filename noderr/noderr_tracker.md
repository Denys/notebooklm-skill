# Noderr - Status Map

**Purpose:** This document tracks the development status of all implementable components (NodeIDs) defined in `noderr_architecture.md`. It guides task selection, groups related work via `WorkGroupID`, and provides a quick overview of project progress. It is updated by the AI Agent as per `noderr_loop.md`.

---
**Progress: 89% (16/18 NodeIDs Implemented)**
---

| Status | WorkGroupID | Node ID | Label | Dependencies | Logical Grouping | Spec Link | Classification | Notes / Issues |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 `[VERIFIED]` | | `UTIL_RunWrapper` | Run Wrapper | — | Environment Setup | [Spec](specs/UTIL_RunWrapper.md) | Critical | Universal entry point; all scripts depend on this |
| 🟢 `[VERIFIED]` | | `SVC_SetupEnvironment` | Setup Environment | UTIL_RunWrapper | Environment Setup | [Spec](specs/SVC_SetupEnvironment.md) | Standard | Creates .venv, installs deps, downloads Chrome |
| 🟢 `[VERIFIED]` | | `AUTH_Manager` | Auth Manager | UTIL_RunWrapper, CONFIG_Settings | Authentication | [Spec](specs/AUTH_Manager.md) | Critical | Hybrid auth workaround for Playwright bug #36139 |
| 🟢 `[VERIFIED]` | | `SVC_BrowserSession` | Browser Session | AUTH_Manager, UTIL_BrowserUtils, CONFIG_Settings | Browser Automation | [Spec](specs/SVC_BrowserSession.md) | Critical | Cookie injection + persistent Chrome profile |
| 🟢 `[VERIFIED]` | | `UTIL_BrowserUtils` | Browser Utils | — | Browser Automation | [Spec](specs/UTIL_BrowserUtils.md) | Standard | BrowserFactory + StealthUtils anti-detection |
| 🟢 `[VERIFIED]` | | `SVC_AskQuestion` | Ask Question | SVC_BrowserSession, AUTH_Manager, CONFIG_Settings, SVC_RetryLogic | Browser Automation | [Spec](specs/SVC_AskQuestion.md) | Critical | Core query engine; interacts with NotebookLM |
| 🟢 `[VERIFIED]` | | `SVC_NotebookManager` | Notebook Manager | UTIL_RunWrapper, DATA_NotebookLibrary | Notebook Management | [Spec](specs/SVC_NotebookManager.md) | Critical | CRUD for local notebook library |
| 🟢 `[VERIFIED]` | | `SVC_CleanupManager` | Cleanup Manager | UTIL_RunWrapper, DATA_BrowserState, DATA_AuthInfo, DATA_NotebookLibrary | Cleanup | [Spec](specs/SVC_CleanupManager.md) | Standard | Clears browser cache + optional data reset |
| 🟢 `[VERIFIED]` | | `CONFIG_Settings` | Settings | — | Configuration | [Spec](specs/CONFIG_Settings.md) | Critical | CSS selectors, timeouts, browser args — update when NotebookLM UI changes |
| 🟢 `[VERIFIED]` | | `SVC_SkillInit` | Skill Init | — | Configuration | [Spec](specs/SVC_SkillInit.md) | Standard | Package __init__.py; exports all public modules |
| 🟢 `[VERIFIED]` | | `CONFIG_SkillDefinition` | Skill Definition | — | Configuration | [Spec](specs/CONFIG_SkillDefinition.md) | Critical | SKILL.md; Claude reads this to know when/how to use skill |
| 🟢 `[VERIFIED]` | | `CONFIG_Requirements` | Requirements | — | Configuration | [Spec](specs/CONFIG_Requirements.md) | Standard | patchright==1.55.2, python-dotenv==1.0.0 |
| 🟢 `[VERIFIED]` | | `DATA_NotebookLibrary` | Notebook Library | — | Data Storage | [Spec](specs/DATA_NotebookLibrary.md) | Standard | JSON flat file; local notebook metadata store |
| 🟢 `[VERIFIED]` | | `DATA_AuthInfo` | Auth Info | — | Data Storage | [Spec](specs/DATA_AuthInfo.md) | Standard | JSON flat file; auth status persistence |
| 🟢 `[VERIFIED]` | | `DATA_BrowserState` | Browser State | — | Data Storage | [Spec](specs/DATA_BrowserState.md) | Standard | Cookies (state.json) + Chrome profile directory |
| 🟢 `[VERIFIED]` | | `SVC_RetryLogic` | Retry Logic | CONFIG_Settings | Browser Automation | [Spec](specs/SVC_RetryLogic.md) | High | RetryHandler.run(callable) — exponential backoff + rate-limit fixed delay |
| ⚪️ `[TODO]` | | `TEST_AuthFlow` | Auth Flow Test | AUTH_Manager | Testing | [Spec](specs/TEST_AuthFlow.md) | Standard | Required for MVP — no automated auth tests |
| ⚪️ `[TODO]` | | `TEST_QueryFlow` | Query Flow Test | SVC_AskQuestion, SVC_NotebookManager | Testing | [Spec](specs/TEST_QueryFlow.md) | Standard | Required for MVP — no automated query tests |

---

### Legend for Status:

*   ⚪️ **`[TODO]`**: Task is defined and ready to be picked up if dependencies are met.
*   📝 **`[NEEDS_SPEC]`**: Node has been identified in the architecture but requires a detailed specification.
*   🟡 **`[WIP]`**: Work In Progress. The AI Agent is currently working on this node.
*   🟢 **`[VERIFIED]`**: The node has been implemented, all ARC Verification Criteria are met, the spec is finalized to "as-built", and all outcomes are logged.
*   ❗ **`[ISSUE]`**: A significant issue or blocker has been identified.

---

*(Tracker initialized by Noderr Install & Reconcile on 2026-03-19. 15 existing NodeIDs documented, 3 missing for MVP completion.)*
