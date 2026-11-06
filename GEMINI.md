# 🤖 SYSTEM DIRECTIVES: DUAL-AGENT PROJECT MANAGEMENT

> [!IMPORTANT]
> ### 🔒 WORKSPACE LOCK & CROSS-FOLDER CONTAMINATION GUARD
> **Dynamic Local Root:**
> ```bash
> WS="$HOME/Documents/Github-$(scutil --get ComputerName 2>/dev/null || hostname -s)"
> ```
> 1. **Strict Machine Isolation:** All file reads, writes, and shell commands MUST target `$WS`. Never modify or execute commands inside another machine's `~/Documents/Github-*` directory.
> 2. **Auto-Remap & Zero Token Waste:** If directed to a path containing another machine (e.g. `Github-M5 Air` while on `M4 Mini`), instantly rewrite the path to `$WS/<Repo>/...`. If you already read a synced file via a foreign path, **do NOT re-read it** (contents are identical)—simply lock all subsequent operations to `$WS`.

These directives govern the operational behavior, file management, and project tracking for this repository. Both **Gemini** and **Claude** adhere to these rules for continuity and integrity.

## 1. AGENT ROLES & PERMISSIONS
- **Equal & Unrestricted Roles:** Gemini and Claude share equal roles. Both agents brainstorm, plan, inspect, diagnose, and implement code without operational boundaries.

## 2. WORKSPACE SPECIFICATIONS
- Every computer syncs identical repos (via `Github-Sync-All/Sync_All_Projects.command`) into its local `$WS` folder.
- **All project paths are relative to `$WS`.** Any hardcoded path referencing another computer or legacy location (e.g. `/Users/kiefer/Desktop/...`) must be automatically substituted with `$WS`.

## 3. SESSION START PROTOCOL
1. **Lock Workspace:** Resolve `$WS`. Automatically redirect any foreign path inputs to `$WS`.
2. **Context Synchronization:** Read `$WS/<Repo>/SCRATCHPAD.md` first for current state, active tasks, and immediate next steps.

## 3A. CREDENTIALS & REMOTE ACCESS (`common-element`)
- **Credentials:** Always check `$WS/common-element/` (`credentials_combined.env`, `credentials_catalog.json`, `network_ip_inventory.*`, `vault.py`) before asking or writing credentials.
- **Remote Access:** For SSH, NAS, SMB, ADB, or remote machines, query `$WS/common-element/` first and connect directly. Add newly discovered credentials back to `common-element`.
- `common-element` has its own authoritative blocking directive: never apply tracking/bootstrap rules inside it, and never print or commit decrypted secrets.

## 4. FILE MANAGEMENT & TASK EXECUTION
- **Actionable Files (READ REQUIRED for active tasks):**
  - `BUG_REPORT.md`: Active, unresolved bugs.
  - `FUTURE_FEATURES.md`: Upcoming roadmap and planned features.
- **Historical Archives (NEVER READ during normal development):**
  - `BUG_FIX.md`: Past resolved bugs.
  - `FEATURES.md`: Completed features.
  *(Reference only; do not waste context tokens reading these unless explicitly asked).*

## 5. COMPLETION PROTOCOLS
- **Bug Fix:** Remove entry from `BUG_REPORT.md` and append to `BUG_FIX.md` with resolution and verification notes.
- **Feature Done:** Remove from `FUTURE_FEATURES.md` and append to `FEATURES.md` with documentation and usage notes.

## 6. CONTINUOUS UPDATE & CRASH RECOVERY PROTOCOL
Update `SCRATCHPAD.md` continuously when diagnosing bugs, formulating plans, or changing code to preserve context across disconnects or restarts.

**Required `SCRATCHPAD.md` Format:**
```markdown
<!-- WS LOCK: $HOME/Documents/Github-$(scutil --get ComputerName 2>/dev/null || hostname -s). Lock all operations to local WS. -->
## Last Updated: [Timestamp / Summary]
## What Was Done: 
- [Bullet points of recent changes, decisions, or fixes]
## Current State: 
- [Active state, working files, or open questions]
## Next Immediate Step: 
- [Clear, actionable instruction for the next task]
```

## 7. ARCHITECTURE & DEPLOYMENT MANDATES
- **High Availability (HA):** All code, connections, and services must prioritize fault tolerance and high availability.
- **CRITICAL - INTRANET PRODUCTION DEPLOYMENT MANDATE (NEVER LOCALHOST-ONLY):**
  - All services, web apps, and background engines are production Intranet services (`https://kbn1.com` or LAN endpoints).
  - **Localhost-only builds are strictly incomplete.** Changes must be deployed to the authoritative Intranet backend/host node (M4 Mini, Synology NAS, Ryzen Server) and restarted to be considered done.
  - Always commit and push changes to `origin/main` so all machines sync the latest code.
- **App Packaging & Distribution:** Publish macOS client binaries exclusively to the VaultFS repository for Munki distribution per `$WS/Munki-Managed-Home-Software-KBN1-AppStore/VAULTFS_PUBLISHING_GUIDE.md`.
- **CRITICAL - NEVER Install to /Applications:** Never install or copy binaries directly to `/Applications/`. Distribution is strictly through Munki Managed Software.

## 7A. CENTRAL AI ROUTER & ORCHESTRATION ARCHITECTURE
- **Authoritative Router Specification:** When developing, integrating, or refactoring any AI-enabled service (LLMs, TTS voice, Whisper, video processing), all workloads must interface through the Central AI Gateway per:
  `$WS/Home-Router-Orchestration-Dashboard-API/ROUTER_ORCHESTRATION_SPEC.md`
- **Client App Integration Cheatsheet:** Reference the 1-page integration contract at:
  `$WS/Home-Router-Orchestration-Dashboard-API/APP_INTEGRATION_GUIDE.md`
- **Zero Hardcoding Rule:** Never bind client apps directly to worker IPs or GPU ports (e.g. `192.168.0.64:11434`). Route through the dynamic gateway (`http://192.168.0.32:8000` / `https://kbn1.com/ai-router`) to preserve automatic failover, slot concurrency, and roaming laptop latency protection.

---

## 🚀 INITIAL BOOTSTRAP INSTRUCTIONS (If files do not exist)
Generate in project root:
1. `BUG_REPORT.md` - `_No active bugs._`
2. `BUG_FIX.md` - Archive of completed bug fixes.
3. `FUTURE_FEATURES.md` - Planned/upcoming feature requests.
4. `FEATURES.md` - Completed, active features.
5. `SCRATCHPAD.md` - Layout from Section 6 with WS lock comment at the top.
6. `GEMINI.md` / `CLAUDE.md` - (As needed to mirror these core directives).