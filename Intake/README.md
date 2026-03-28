# Intake — Root-Level Staging Area

## Purpose

This directory is the **only sanctioned staging area** for content that has not yet been classified and routed to its permanent location in the repository.

**Do not commit files directly to the repository root.**  Drop them here instead.

---

## How the intake pipeline works

1. Place any new file or folder (zip, markdown, source code, docs, config) into this `Intake/` directory.
2. Run the intake processor:
   ```bash
   python3 Scripts/Intake/process_intake.py
   ```
3. The processor classifies every item, moves it to the correct destination per project guidelines, and writes a log to `Logs/intake/`.
4. Review the log output to confirm routing decisions.
5. Commit the result (the files are now in their canonical locations; `Intake/` should be empty again).

---

## Classification rules (summary)

Full rules live in [`Docs/Architecture/intake_policy.md`](../Docs/Architecture/intake_policy.md).

| Content type | Destination |
|---|---|
| `.zip` archive | `Docs/Archive/ZipFiles/` — then extract + migrate per sprint process |
| Design / vision `.md` | `Docs/Design/` |
| Architecture `.md` | `Docs/Architecture/` |
| Roadmap / planning `.md` | `Docs/Roadmaps/` or `Docs/Archive/Planning/` |
| Chat export / transcript | `Docs/Archive/Chats/` → converted to structured `.md` in `Docs/Design/` |
| Engine C++/H source | `Atlas/Engine/<Subsystem>/` |
| Editor C++/H source | `Atlas/Editor/<Subsystem>/` |
| Gameplay C++/H source | `NovaForge/Gameplay/<System>/` |
| Python / AI tooling | `AtlasAI/` |
| Build / CI scripts | `Scripts/` |
| Tests | `AtlasAI/Tests/` (Python) or `Tests/` (integration) |
| Data / JSON | `NovaForge/Data/` |
| Third-party libraries | `ThirdParty/` |

---

## What is forbidden at root level

The repo root must contain only:

```
Atlas/          AtlasAI/        CMakeLists.txt  Docs/
Intake/         LICENSE         NovaForge/      README.md
Scripts/        Services/       Shared/         Tests/
ThirdParty/     Tools/          cmake/
.gitignore      .github/
```

Any file or directory outside this set will cause `Scripts/Validate/validate_root.py` to fail.

---

## CI enforcement

The `validate_root.py` script runs in CI and will **fail the build** if any stray file is found at repository root. Use this directory to stage work-in-progress content before routing it.
