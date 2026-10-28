# 🤖 SYSTEM DIRECTIVES: DUAL-AGENT PROJECT MANAGEMENT

These directives govern the operational behavior, file management, and project tracking for this repository. Both **Gemini** and **Claude** are required to strictly adhere to these rules to maintain project continuity and system integrity.

## 1. AGENT ROLES & PERMISSIONS
- **Equal & Unrestricted Roles:** Gemini and Claude share equal roles. Both agents are fully authorized to brainstorm, plan, inspect code, diagnose bugs, write code, and implement changes whenever requested. There are no operational boundaries between the agents.

## 2. WORKSPACE & ENVIRONMENT INITIALIZATION
**CRITICAL:** Never hardcode a workspace path. Every development computer syncs all repositories into a dynamic, computer-specific folder. 
- At the start of **every** session, you MUST resolve the workspace path using the following bash logic:
  ```bash
  WS="$HOME/Documents/Github-$(scutil --get ComputerName 2>/dev/null || hostname -s)"
  ```

## 3. SESSION START PROTOCOL
1. **Resolve Workspace:** Execute the dynamic workspace path resolution above.
2. **Context Synchronization:** You MUST read `SCRATCHPAD.md` first. This provides the last conversation update, the current working state, and the next immediate step.

## 4. FILE MANAGEMENT & TASK EXECUTION
You must differentiate between **Actionable** files and **Historical/Archive** files.

- **Actionable Files (READ REQUIRED for active tasks):**
  - `BUG_REPORT.md`: Contains active, unresolved bugs.
  - `FUTURE_FEATURES.md`: Contains the upcoming roadmap and planned feature requests.
- **Historical Archives (NEVER READ during normal development):**
  - `BUG_FIX.md`: Past resolved bugs. 
  - `FEATURES.md`: Already completed features. 
  *(Note: These are historical reference archives only. Do not waste context window reading them unless explicitly asked to review history).*

## 5. COMPLETION PROTOCOLS
- **Bug Fix Completion:** When a bug is successfully resolved, completely remove its entry from `BUG_REPORT.md` and append it to `BUG_FIX.md`. You must include a brief explanation of the fix and the verification steps taken.
- **Feature Completion:** When a feature is fully implemented, completely remove it from `FUTURE_FEATURES.md` and append it to `FEATURES.md`. You must include relevant documentation and usage instructions.

## 6. CONTINUOUS UPDATE & CRASH RECOVERY PROTOCOL
To prevent context loss during a power failure, disconnect, or system crash, you MUST continuously update `SCRATCHPAD.md` whenever a bug is diagnosed, a plan is formulated, or code is changed. 

**Required `SCRATCHPAD.md` Format:**
```markdown
## Last Updated: [Timestamp / Summary]
## What Was Done: 
- [Bullet points of recent changes, decisions, or fixes]
## Current State: 
- [Active state, working files, or open questions]
## Next Immediate Step: 
- [Clear, actionable instruction for the next task]
```

## 7. ARCHITECTURE & DEPLOYMENT MANDATES
- **High Availability (HA):** All code, network connections, and services designed or modified MUST focus strictly on high availability and fault tolerance.
- **App Deployment:** Whenever deploying an app version of the code, you MUST adhere to the following guide:
  `/Users/kiefer/Desktop/Github/Munki-Managed-Home-Software/VAULTFS_PUBLISHING_GUIDE.md`

---

## 🚀 INITIAL BOOTSTRAP INSTRUCTIONS (If files do not exist)
If setting up this repository for the first time, generate the following files in the project root:
1. `BUG_REPORT.md` - Initialize with: `_No active bugs._`
2. `BUG_FIX.md` - Initialize with a header explaining it is the archive of completed bug fixes.
3. `FUTURE_FEATURES.md` - Initialize with a header for tracking planned/upcoming feature requests.
4. `FEATURES.md` - Initialize with a header to document completed, active features.
5. `SCRATCHPAD.md` - Initialize using the exact layout defined in Section 6, placing these Agent Directives at the very top of the file, followed by the initial status.
6. `GEMINI.md` / `CLAUDE.md` - (As needed to mirror these core directives).