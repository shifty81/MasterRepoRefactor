# Master Project Standard

This document is the source-of-truth target used by the compliance scanner.

## 1. Project direction

### 1.1 Visual + world standard
- The project follows a **hybrid voxel + low-poly** direction.
- Voxels are responsible for:
  - structural mass
  - damage
  - mining
  - repair
  - procedural world generation
- Low-poly assets are responsible for:
  - visual readability
  - modular attachments
  - interactable object presentation
  - ship / station / prop silhouette language

### 1.2 Character standard
- The in-game player suit/backpack assembly is called a **rig**.
- Equippable gameplay systems should support a tiered quality model across:
  - character equipment
  - rigs
  - ships
  - mechs
  - rovers
  - hover bikes

### 1.3 Season standard
- Seasons must be configurable in both client and server settings.
- Server-side enforcement is the default authority model.
- Baseline target season length is approximately **6 months** unless a game mode overrides it.

### 1.4 UI standard
- Project-facing UI should remain **custom UI**.
- Do not introduce ImGui as the primary user-facing runtime/editor UI layer for this project standard.
- Internal debug-only overlays may exist, but they should not replace the custom UI direction.

## 2. Repo structure standard

The repo should keep major concerns split by top-level area:

```text
MasterRepo/
├── AI/
├── Agents/
├── Builder/
├── Config/
├── Core/
├── Docs/
├── Editor/
├── Engine/
├── PCG/
├── Projects/
├── Runtime/
├── Tests/
├── Tools/
└── UI/
```

## 3. Documentation standard

Each major system should have:
- one primary Markdown overview
- a responsibility section
- dependency notes
- data contracts or schema notes where applicable
- at least one diagram (ASCII or structured list)

Recommended doc map:
- AI / Arbiter
- Core
- Engine
- Editor
- Builder
- PCG
- Runtime / Game
- Tools / Agents
- Config / Schemas
- Archive / Legacy boundaries

## 4. Naming standard

- Use `Rig` terminology instead of generic `Suit` when referring to the player wearable assembly in project docs and gameplay-facing systems.
- Avoid legacy EVE-derived names in active gameplay content unless intentionally preserved in an archived area.
- Prefer one canonical spelling for duplicated domains. Example: choose either `Localization` or `Localisation`, not both in active modules.

## 5. Schema standard

JSON-backed config/data should be:
- documented
- stable in key naming
- versionable when save-data or gameplay-critical
- separated by concern:
  - engine config
  - editor config
  - builder config
  - AI config
  - game/project config
  - content data
  - recipes / items / prefabs / ships / scenes

## 6. Tooling standard

The project should support:
- repo documentation generation
- compliance scanning
- code audit / dependency analysis
- asset pipeline tooling
- build/test tooling
- AI-assisted orchestration via Arbiter

## 7. Compliance severity

Scanner output levels:
- `PASS` = matches standard
- `WARN` = acceptable drift, duplication, missing polish, or soft violation
- `FAIL` = missing required structure or explicit standard violation
