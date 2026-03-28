# Intake Policy

> **Enforcement:** `Scripts/Validate/validate_root.py`  
> **Processor:** `Scripts/Intake/process_intake.py`  
> **Staging areas:** `Intake/` (text/code) · `DropBox/` (large binaries & archives)  
> **See also:** [repo_boundaries.md](repo_boundaries.md) · [monorepo_layout.md](monorepo_layout.md)

---

## Purpose

This document defines the rules that govern how any new content is brought into the repository. Every file or directory that enters the project — regardless of its source (chat export, zip archive, raw source, documentation, script) — must be **classified, routed, and documented** according to these rules before being considered committed.

The policy exists to enforce the structural guarantees in `repo_boundaries.md` and `monorepo_layout.md` at the point of ingestion, not after the fact.

---

## The Root Contract

**The repository root is not a working directory.** The only items permitted at root are:

| Item | Type | Reason |
|---|---|---|
| `Atlas/` | Directory | Engine/editor zone |
| `AtlasAI/` | Directory | AI tooling zone |
| `CMakeLists.txt` | File | Root CMake entry point |
| `Docs/` | Directory | Documentation |
| `DropBox/` | Directory | **Staging for large binaries/archives (git-ignored inside)** |
| `Intake/` | Directory | Staging area for text files / code |
| `LICENSE` | File | Open-source licence |
| `NovaForge/` | Directory | Game project zone |
| `README.md` | File | Project overview |
| `Scripts/` | Directory | Automation and tooling |
| `Services/` | Directory | Optional backend services |
| `Shared/` | Directory | Bridge contracts only |
| `Tests/` | Directory | Integration tests |
| `ThirdParty/` | Directory | Vendored libraries |
| `Tools/` | Directory | Developer tools |
| `cmake/` | Directory | CMake modules |
| `.gitignore` | File | Git ignore rules |
| `.github/` | Directory | GitHub Actions and templates |

Anything else triggers a validation failure.

---

## Two Staging Areas

### `Intake/` — text, code, and lightweight files

Use `Intake/` for:
- Markdown documents, chat exports, design notes
- Small source files (`.h`, `.cpp`, `.cs`, `.py`)
- JSON/YAML data or config

Files placed in `Intake/` **are tracked by git** once committed.

### `DropBox/` — large binaries and archives *(git-ignored internally)*

Use `DropBox/` for:
- Zip archives (`.zip`, `.7z`, `.rar`, `.tar.gz`, …)
- 3-D source meshes (`.fbx`, `.obj`, `.blend`)
- Installer binaries (`.exe`, `.msi`, `.dmg`)
- Audio / video blobs

> **Key property:** `DropBox/.gitignore` ignores all binary/archive patterns inside that
> directory.  Dropping a zip into `DropBox/` keeps it **local only** — it will never
> bloat the remote repository.

Both staging areas are processed by the same script:

```bash
python3 Scripts/Intake/process_intake.py          # scans both Intake/ and DropBox/
python3 Scripts/Intake/process_intake.py --source dropbox   # DropBox only
python3 Scripts/Intake/process_intake.py --source intake    # Intake/ only
```

---

## Intake Stages

### Stage 1 — Drop

Place the file or directory into `Intake/` (text/code) or `DropBox/` (archive/binary).
Do not commit zip files directly to root or anywhere else.

### Stage 2 — Classify

Run `Scripts/Intake/process_intake.py --classify` (dry-run). The processor reads every item in both staging areas and prints a routing decision for each.

### Stage 3 — Route

Run `Scripts/Intake/process_intake.py` (no flags) to apply the routing decisions: files are moved to their canonical destinations.

### Stage 4 — Document

The processor auto-appends a row to `Docs/Archive/ZipFiles/README.md` (for archives) or `Docs/Design/` (for design docs). For source code, the processor prints the CMakeLists path that needs updating.

### Stage 5 — Commit

Commit the routed files from their canonical locations. Both staging areas should be empty (only their `README.md` files remain).

---

## Classification Rules

### Archives (`.zip`, `.tar.gz`, `.7z`)

| Condition | Destination |
|---|---|
| All cases | `Docs/Archive/ZipFiles/` |

After routing, the archive must be extracted and its contents migrated individually. The zip itself is retained in `Docs/Archive/ZipFiles/` as a reference artefact.

> **Note on repo size:** Zip files already committed to git history can be pruned with
> [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) once all content has been
> integrated.  The `DropBox/.gitignore` prevents **future** zips from entering git at all.

---

### Documentation (`.md`, `.txt`, `.pdf`)

Classification is based on filename pattern and content signals:

| Signal | Destination |
|---|---|
| Filename contains `DESIGN`, `DIRECTIVE`, `VISION`, `CANON` | `Docs/Design/` |
| Filename contains `ARCHITECTURE`, `BOUNDARY`, `DEPENDENCY`, `LAYOUT` | `Docs/Architecture/` |
| Filename contains `ROADMAP`, `PHASE`, `SPRINT`, `PLAN` | `Docs/Roadmaps/` or `Docs/Archive/Planning/` |
| Filename contains `CHECKLIST`, `MIGRATION`, `EXECUTION` | `Docs/Archive/Planning/` |
| File is a raw chat export / transcript (unformatted, Q&A style) | `Docs/Archive/Chats/` — **and** a structured `.md` must be created in `Docs/Design/` |
| Filename contains `CROSSPLATFORM`, `GUI`, `LAUNCHING`, `SETUP` | `Docs/` (top-level) |
| Any other `.md` | `Docs/Design/` (default) |

**Rule:** `.txt` files that are chat exports must be converted to structured `.md` before or immediately after routing. The raw `.txt` is retained in `Docs/Archive/Chats/`.

---

### C++ / C Source (`.h`, `.hpp`, `.cpp`, `.c`)

Route is determined by the declared namespace and the subsystem name:

| Namespace / subsystem signal | Destination |
|---|---|
| `namespace atlas` / `atlas::` + engine subsystem | `Atlas/Engine/<Subsystem>/` |
| `namespace atlas` / `atlas::` + editor subsystem | `Atlas/Editor/<Subsystem>/` |
| `namespace atlas` / `atlas::` + UI subsystem | `Atlas/UI/<Subsystem>/` |
| `namespace NovaForge` / `NovaForge::` + gameplay | `NovaForge/Gameplay/<System>/` |
| `namespace NovaForge` / `NovaForge::` + app bootstrap | `NovaForge/App/` |
| `namespace NovaForge` / `NovaForge::` + save/world | `NovaForge/Save/` or `NovaForge/World/` |
| Shared / bridge contract | `Shared/AtlasBridgeContract/` or `Shared/ToolProtocol/` |
| Unrecognised namespace | Flagged as **requires manual classification** |

**Rule:** A C++ file may not be routed to `Atlas/` if it contains `#include` paths pointing into `NovaForge/` (boundary violation). `process_intake.py` will flag this.

---

### Python (`.py`)

| Signal | Destination |
|---|---|
| Test file (`test_*.py`) | `AtlasAI/Tests/` |
| AI engine / orchestration | `AtlasAI/AIEngine/AtlasAIEngine/` |
| Validation / CI script | `Scripts/Validate/` or `Scripts/CI/` |
| Build / setup script | `Scripts/Build/` or `Scripts/Setup/` |
| Game tool / data tool | `NovaForge/Tools/` |

---

### C# (`.cs`, `.csproj`, `.sln`)

| Signal | Destination |
|---|---|
| AtlasAI `HostApp` namespace | `AtlasAI/HostApp/` |
| VSIX / extension | `AtlasAI/VisualStudioExtension/` |
| Project adapter | `AtlasAI/ProjectAdapters/` |

---

### Build / CMake (`.cmake`, `CMakeLists.txt`)

| Signal | Destination |
|---|---|
| Root-level CMake module | `cmake/` |
| Engine CMake | `Atlas/CMake/` |
| Game CMake | `NovaForge/CMake/` |

---

### Data / Config (`.json`, `.yaml`, `.toml`, `.ini`)

| Signal | Destination |
|---|---|
| Game data (items, recipes, missions, factions) | `NovaForge/Data/` |
| Engine / editor config | `Atlas/Config/` |
| AtlasAI config / schema | `AtlasAI/` |
| Shared bridge schema | `Shared/ToolProtocol/schemas/` |

---

### Directories

A whole directory dropped into either staging area is processed recursively: every file inside is classified individually. The directory is then moved as a unit to the nearest canonical destination.

---

## Violations and Escalation

If `process_intake.py` cannot determine a confident destination for an item, it will:

1. Print a `[UNCLASSIFIED]` warning.
2. Move the item to `Docs/Archive/Planning/UNCLASSIFIED/` (never to root).
3. Emit a non-zero exit code.

The unclassified item must be manually reviewed and moved before it can be merged to main.

---

## Audit Trail

Every intake run appends a record to `Logs/intake/intake_log.jsonl`:

```json
{
  "timestamp": "2026-03-28T14:00:00Z",
  "source": "DropBox/SomeArchive.zip",
  "destination": "Docs/Archive/ZipFiles/SomeArchive.zip",
  "classification": "zip_archive",
  "dry_run": false
}
```

This log is git-ignored but preserved locally for audit purposes.

---

## Frequently Asked Questions

**Q: I have a large zip that contains both source and docs — what do I do?**  
A: Drop the zip in `DropBox/`. Run `process_intake.py` — it routes the zip to
`Docs/Archive/ZipFiles/`. Then extract it manually and drop the extracted contents back
into `Intake/` or `DropBox/`. Run the processor again to route each file individually.

**Q: I want to add a new top-level directory to the repo.**  
A: That requires an architecture decision. Update `Docs/Architecture/monorepo_layout.md` and `Scripts/Validate/validate_root.py` ALLOWLIST first, then add the directory.

**Q: Does the intake processor modify any file content?**  
A: No. It only moves files and optionally converts `.txt` chat exports to structured `.md` (by wrapping them in a markdown document shell). No source code is modified.

**Q: How do I trim the repo of existing committed zips?**  
A: Use [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/):
```bash
bfg --delete-files "*.zip" --no-blob-protection
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```
All zip content should already be integrated before running BFG.

