# DropBox — Asset Intake Staging Area

## Purpose

`DropBox/` is the **primary drop point** for all new raw assets, archives, and files
that need to be integrated into the project.  It is designed to receive files that
are too large or too transient to commit directly to git.

> **Key rule:** zip archives and other binary blobs placed here are **git-ignored**
> by the `.gitignore` inside this folder.  They stay on your local machine only.
> Once processed, those files are no longer needed here.

---

## Workflow

```
[You drop a file here]
        │
        ▼
  DropBox/my-asset.zip        ← local only, not committed
        │
        ▼
  python3 Scripts/Intake/process_intake.py --source dropbox
        │
        ▼
  Files routed to canonical destinations (Atlas/, NovaForge/, Docs/, …)
        │
        ▼
  DropBox/ is empty again  ✓
```

1. **Drop** any file (zip, md, source, data) into this directory.
2. **Run** the intake processor:
   ```bash
   python3 Scripts/Intake/process_intake.py
   ```
   The processor scans **both** `Intake/` and `DropBox/` automatically.
3. **Review** routing decisions in the console output or `Logs/intake/intake_log.jsonl`.
4. **Commit** only the newly-routed files — `DropBox/` stays empty (and git-ignored for binaries).

---

## What is ignored here

The `.gitignore` inside `DropBox/` ignores the following file types so they never
bloat the git repository:

| Pattern | Rationale |
|---|---|
| `*.zip` | Large archives — integrate content instead of committing raw zips |
| `*.7z` | Same |
| `*.rar` | Same |
| `*.tar`, `*.tar.gz`, `*.tgz` | Same |
| `*.gz` | Compressed blobs |
| `*.bz2` | Compressed blobs |
| `*.xz` | Compressed blobs |
| `*.exe`, `*.msi`, `*.dmg`, `*.pkg` | Installer binaries |
| `*.fbx`, `*.obj`, `*.dae` | Raw 3-D source meshes (use ASSET_MANIFEST + runtime) |
| `*.psd`, `*.ai`, `*.sketch` | Source art files |
| `*.mp4`, `*.avi`, `*.mov` | Video files |
| `*.wav`, `*.mp3`, `*.ogg` | Audio blobs |

Text files (`.md`, `.json`, `.h`, `.cs`, `.py`, etc.) **are** tracked so that
lightweight drop-ins can be versioned when desired.

---

## What ends up here vs. Intake/

| Use `DropBox/` when… | Use `Intake/` when… |
|---|---|
| Dropping a large zip or binary asset | Dropping a small text file or code snippet |
| You have downloaded a release archive | You want the file committed and versioned after routing |
| You want git to ignore the raw file | You want CI to see the file in a subsequent build after routing and committing |

Both folders are processed by the same `process_intake.py` script.

---

## See also

- [`Intake/README.md`](../Intake/README.md) — original staging area for text files
- [`Docs/Architecture/intake_policy.md`](../Docs/Architecture/intake_policy.md) — full routing rules
- [`Scripts/Intake/process_intake.py`](../Scripts/Intake/process_intake.py) — routing script
