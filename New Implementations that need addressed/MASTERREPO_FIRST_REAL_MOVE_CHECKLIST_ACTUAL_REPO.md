# MASTERREPO_FIRST_REAL_MOVE_CHECKLIST_ACTUAL_REPO

## Purpose
This is the **first real execution checklist** based on the **actual contents** of your uploaded `MasterRepo`.

This is not generic anymore.  
It is built from the repo’s real top-level structure, current CMake layout, and the actual folders/files already present.

---

# What I found in the current repo

## Current top-level structure actually present
Your uploaded `MasterRepo` currently contains these major roots:

- `Core/`
- `Engine/`
- `UI/`
- `Editor/`
- `Runtime/`
- `Builder/`
- `PCG/`
- `AI/`
- `Agents/`
- `IDE/`
- `Tools/`
- `Projects/NovaForge/`
- `Docs/`
- `Config/`
- `Tests/`
- plus support areas like `Archive/`, `Experiments/`, `External/`, `Logs/`, `Plugins/`, `Scripts/`, `TrainingData/`, `Versions/`, `WorkspaceState/`

## Current build shape actually present
Your root `CMakeLists.txt` currently builds in this order:

- `Core`
- `Versions`
- `Engine`
- `UI`
- `Editor`
- `Runtime`
- `AI`
- `Agents`
- `Builder`
- `PCG`
- `IDE`
- `Tools`
- `TrainingData`
- `Projects/NovaForge`

It also currently does this globally:

```cmake
include_directories(${CMAKE_SOURCE_DIR})
```

That is a major migration concern because it makes dependency leakage very easy.

## Actual NovaForge project content currently present
Inside `Projects/NovaForge/` you currently have:

- `Assets/`
- `Config/`
- `Data/`
- `Modules/`
- `Parts/`
- `Prefabs/`
- `Recipes/`
- `Scenes/`
- `Ships/`
- `UI/`
- `NovaForgeHUD.h`
- `main.cpp`

## Actual mixed zones currently present
These are the biggest mixed-ownership areas right now:

- `Editor/`
- `Runtime/`
- `AI/`
- `Agents/`
- `IDE/`
- `Tools/`

These should **not** be bulk-moved as-is.

---

# The best first real move sequence

This is the safest actual sequence for your repo.

## Do first
1. **Create the new ownership zones without moving everything yet**
2. **Move only the cleanest content first**
3. **Do not touch the mixed zones in the first pass**
4. **Keep the build alive after every move**

---

# PHASE A — Create the new target folders first

## Create these folders in the actual repo first
At repo root, create:

- `Atlas/`
- `NovaForge/`
- `Arbiter/`
- `Shared/`

Then immediately create these subfolders:

### Atlas
- `Atlas/Core/`
- `Atlas/Engine/`
- `Atlas/UI/`
- `Atlas/Runtime/`
- `Atlas/Editor/`

### NovaForge
- `NovaForge/App/`
- `NovaForge/Gameplay/`
- `NovaForge/World/`
- `NovaForge/Tools/`
- `NovaForge/Data/`
- `NovaForge/Content/`
- `NovaForge/Integrations/Arbiter/`

### Arbiter
- `Arbiter/HostApp/`
- `Arbiter/AIEngine/`
- `Arbiter/Archive/`
- `Arbiter/Automation/`
- `Arbiter/ProjectAdapters/NovaForge/`

### Shared
- `Shared/ArbiterBridgeContract/include/`
- `Shared/ProjectManifests/`

✅ **Checkpoint**
- New folders exist
- Nothing major has moved yet
- Repo should still configure

---

# PHASE B — First real files to add before moving code

## Add these files immediately
These are the first files to create, before moving code:

### Shared contract
- `Shared/ArbiterBridgeContract/include/ArbiterBridgeTypes.h`

### Project manifest
- `Shared/ProjectManifests/novaforge.project.json`

### New docs
- `Docs/Architecture/repo_boundaries.md`
- `Docs/Architecture/dependency_rules.md`
- `Docs/Integration/arbiter_bridge.md`

✅ **Checkpoint**
- Shared exists
- docs exist
- architecture truth is now anchored in-repo

---

# PHASE C — First safe code moves from the actual repo

These are the **lowest-risk actual moves** from what is currently in your repo.

## Move Group 1 — Core → Atlas/Core
Move the entire current `Core/` folder into:

- `Atlas/Core/`

### Why this is safe first
`Core/` is the cleanest foundational layer already present in the repo.

### Actual content currently in Core
Examples currently present:
- `Core/Allocator/PoolAllocator/*`
- `Core/ArchiveSystem/*`
- `Core/AssetMetadata/*`
- `Core/Cache/LRUCache/*`
- `Core/Config/*`
- `Core/CrashReport/*`
- `Core/DataTable/*`
- `Core/DeterministicSeed/*`
- `Core/EventDispatcher/*`
- `Core/EventLog/*`
- `Core/EventReplay/*`
- `Core/Events/*`
- `Core/FeatureFlags/*`
- `Core/GameState/*`
- `Core/HotReload/*`
- `Core/JobSystem/*`
- `Core/Localization/*`
- `Core/Messaging/*`

### Caution inside Core
Audit these before accepting them as truly foundational:
- `Core/CloudSync/`
- `Core/CodeIntelligence/`
- `Core/LocalCIPipeline/`

These may belong in:
- `Atlas/Core/` if kept as platform/dev foundation
- or later in `Tools/` / `Arbiter/` if they are really tooling-heavy

### First real action
- Move `Core/` → `Atlas/Core/`
- Update root and module CMake references
- Build immediately

✅ **Checkpoint**
- `Atlas/Core/` exists with real code
- `AtlasCore` target can be mapped
- no gameplay logic should remain mixed into it

---

## Move Group 2 — Engine → Atlas/Engine
Move the current `Engine/` folder into:

- `Atlas/Engine/`

### Actual content currently present
Examples currently present:
- `Engine/Animation/*`
- `Engine/Audio/*`
- `Engine/Camera/*`
- `Engine/Cinematic/*`
- `Engine/Core/*`
- `Engine/Debug/*`
- `Engine/Decals/*`
- `Engine/Graphics/*`
- `Engine/Input/*`
- `Engine/Lighting/*`
- `Engine/Lod/*`
- `Engine/Net/*`

### Why this is safe early
This is already clearly engine-owned and currently below project level in the build graph.

### Caution inside Engine
Watch for project-specific assumptions in:
- `Engine/Core/RuntimeBootstrap.*`
- any subsystem that assumes NovaForge-specific data or world semantics

### First real action
- Move `Engine/` → `Atlas/Engine/`
- Update `CMakeLists.txt`
- Build immediately

✅ **Checkpoint**
- `AtlasEngine` now represents real migrated code

---

## Move Group 3 — UI → Atlas/UI
Move current `UI/` into:

- `Atlas/UI/`

### Actual content currently present
Examples:
- `UI/Accessibility/*`
- `UI/Animation/*`
- `UI/GUISystem/*`
- `UI/Layouts/*`
- `UI/Localization/*`
- `UI/Themes/*`
- `UI/Widgets/*`

### Why this is safe
This is one of the clearest generic layers already in the repo.

### Caution
Do not move NovaForge HUD layout or game UI assets here.
Those belong in NovaForge.

✅ **Checkpoint**
- `Atlas/UI/` becomes the native custom UI foundation

---

# PHASE D — First safe NovaForge moves from the actual repo

The cleanest actual moves from `Projects/NovaForge/` are the **data/content folders**, not `main.cpp`.

## Move Group 4 — NovaForge data definitions
Move from:

- `Projects/NovaForge/Config/`
- `Projects/NovaForge/Data/`
- `Projects/NovaForge/Modules/`
- `Projects/NovaForge/Parts/`
- `Projects/NovaForge/Recipes/`

To:

- `NovaForge/Data/Config/`
- `NovaForge/Data/Definitions/Universe/`
- `NovaForge/Data/Factions/`
- `NovaForge/Data/Modules/`
- `NovaForge/Data/Parts/`
- `NovaForge/Data/Recipes/`

### Actual files currently present
Examples:
- `Projects/NovaForge/Config/game.json`
- `Projects/NovaForge/Config/player_settings.json`
- `Projects/NovaForge/Data/Universe/systems.json`
- `Projects/NovaForge/Data/factions.json`
- `Projects/NovaForge/Data/gas_types.json`
- `Projects/NovaForge/Modules/cockpit_module.json`
- `Projects/NovaForge/Modules/engine_module.json`
- `Projects/NovaForge/Parts/cockpit_mk1.json`
- `Projects/NovaForge/Parts/starter_hull.json`
- `Projects/NovaForge/Parts/thruster_basic.json`
- `Projects/NovaForge/Recipes/crafting_recipes.json`

### Why this is safe
These are clearly project data assets and belong under NovaForge ownership.

✅ **Checkpoint**
- project data is no longer buried inside `Projects/NovaForge/`
- data paths are updated
- data load still works

---

## Move Group 5 — NovaForge content assets
Move from:

- `Projects/NovaForge/Assets/`
- `Projects/NovaForge/Prefabs/`
- `Projects/NovaForge/Scenes/`
- `Projects/NovaForge/UI/`

To:

- `NovaForge/Content/Assets/`
- `NovaForge/Content/Prefabs/`
- `NovaForge/Content/Scenes/`
- `NovaForge/Content/UI/`

### Actual files currently present
Examples:
- `Projects/NovaForge/Assets/asset_manifest.json`
- `Projects/NovaForge/Prefabs/starter_ship.json`
- `Projects/NovaForge/Scenes/default.scene`
- `Projects/NovaForge/Scenes/main_scene.json`
- `Projects/NovaForge/UI/hud_layout.json`

### Caution
- `NovaForgeHUD.h` is **not** a content asset
- do **not** move it here

✅ **Checkpoint**
- NovaForge content ownership is clean
- scene/prefab/UI asset paths are updated

---

## Move Group 6 — Ship definitions
Move from:

- `Projects/NovaForge/Ships/`

To one of these:
- `NovaForge/World/Ships/` if they are world templates
- `NovaForge/Data/Definitions/Ships/` if they are pure data definitions

### Actual files currently present
- `Projects/NovaForge/Ships/nova_fighter.json`
- `Projects/NovaForge/Ships/patrol_cruiser.json`

### Recommendation
Use:
- `NovaForge/Data/Definitions/Ships/`

That keeps them clearly data-driven for now.

✅ **Checkpoint**
- ship defs have a permanent home

---

# DO NOT MOVE THESE YET

These are the actual repo areas you should **not** move in the first real pass.

## 1. `Projects/NovaForge/main.cpp`
### Why not yet
This is almost certainly your most mixed file.
It needs to be split into:
- `NovaForge/App/NovaForgeApp/`
- `NovaForge/App/Bootstrap/`
- `NovaForge/App/Session/`
- `NovaForge/Client/HUD/`
- `NovaForge/Client/Input/`

## 2. `Projects/NovaForge/NovaForgeHUD.h`
### Why not yet
This needs a decision first:
- runtime HUD code → `NovaForge/Client/HUD/`
- pure UI asset/config → `NovaForge/Content/UI/`

It is not a safe blind move.

## 3. `Runtime/`
### Why not yet
Actual current contents include:
- `Runtime/Combat/`
- `Runtime/Factions/`
- `Runtime/Gameplay/`
- `Runtime/Universe/`
- `Runtime/BuilderRuntime/`
- `Runtime/NPC/`
- `Runtime/Economy/`

This is heavily mixed with project/runtime/gameplay/editor-adjacent responsibilities.

## 4. `Editor/`
### Why not yet
Actual current contents include:
- `Editor/Core/`
- `Editor/BuilderEditor/`
- `Editor/PCGEditor/`
- `Editor/GUIEditor/`
- `Editor/Panels/*`
- `Editor/Tools/*`

This must be split file-by-file between:
- `Atlas/Editor/`
- `NovaForge/Tools/`

## 5. `AI/`, `Agents/`, `IDE/`
### Why not yet
These are too mixed to move safely without reclassification.

Examples actually present:
- `AI/OllamaClient/`
- `AI/KnowledgeIngestion/`
- `AI/SessionMemory/`
- `AI/Arbiter/`
- `IDE/AIChat/`
- `IDE/NLAssistant/`
- `Agents/CodeAgent/`
- `Agents/EditorAgent/`
- `Agents/PCGAgent/`
- `Agents/SelfBuildAgent/`

These need to be sorted into:
- `Arbiter/AIEngine/`
- `Arbiter/HostApp/`
- `Arbiter/Automation/`
- `Arbiter/ProjectAdapters/NovaForge/`

---

# FIRST BUILD-SYSTEM FIXES YOU SHOULD MAKE BEFORE BIG MOVES

These are the actual most important build fixes to do first.

## Fix 1 — Stop relying on global include leakage
Current root CMake has:

```cmake
include_directories(${CMAKE_SOURCE_DIR})
```

### Why this matters
This hides bad dependencies and makes refactoring much harder.

### Immediate recommendation
Do not delete it on day 1 if the repo is fragile, but mark it as temporary and start moving module-by-module toward:

- target-specific include dirs
- narrow public/private dependency exposure

## Fix 2 — Create Shared and Atlas/NovaForge subdirectory stubs early
Before moving lots of files, add:
- `add_subdirectory(Shared)`
- `add_subdirectory(Atlas)`
- `add_subdirectory(NovaForge)`

Then begin moving code into them while the old build still exists.

## Fix 3 — Keep shipping targets free of Arbiter work
Do not let the first pass introduce:
- Arbiter linkage into game runtime
- editor/tooling-only modules into shipping client/server

---

# YOUR ACTUAL FIRST WEEK CHECKLIST

This is what I would do on your real repo, in exact order.

## Day 1
- create `Atlas/`, `NovaForge/`, `Arbiter/`, `Shared/`
- create subfolders listed above
- add Shared contract + manifest files
- commit

## Day 2
- move `Core/` → `Atlas/Core/`
- wire basic `AtlasCore`
- build
- commit

## Day 3
- move `Engine/` → `Atlas/Engine/`
- wire `AtlasEngine`
- build
- commit

## Day 4
- move `UI/` → `Atlas/UI/`
- wire `AtlasUI`
- build
- commit

## Day 5
- move safe NovaForge data/content:
  - `Config/`
  - `Data/`
  - `Modules/`
  - `Parts/`
  - `Recipes/`
  - `Assets/`
  - `Prefabs/`
  - `Scenes/`
  - `UI/`
  - `Ships/`
- update paths
- build
- commit

### Stop there
At the end of this first week, stop and assess before touching:
- `Editor/`
- `Runtime/`
- `AI/`
- `Agents/`
- `IDE/`
- `Projects/NovaForge/main.cpp`

That is the correct break point.

---

# FIRST FILES I WOULD PERSONALLY OPEN FIRST

These are the exact files I would inspect first before making deeper moves:

## Root build
- `CMakeLists.txt`
- `Core/CMakeLists.txt`
- `Engine/CMakeLists.txt`
- `UI/CMakeLists.txt`
- `Projects/NovaForge/CMakeLists.txt`

## Highest-value split candidates
- `Projects/NovaForge/main.cpp`
- `Projects/NovaForge/NovaForgeHUD.h`
- `Runtime/BuilderRuntime/NovaForgeBuilderIntegration.cpp`
- `Runtime/BuilderRuntime/NovaForgeBuilderIntegration.h`
- `Editor/main.cpp`
- `AI/Arbiter/Arbiter.cpp`
- `AI/Arbiter/Arbiter.h`
- `IDE/AIChat/AIChat.cpp`
- `Agents/EditorAgent/EditorAgent.cpp`
- `Agents/CodeAgent/CodeAgent.cpp`

---

# The real “don’t mess this up” rules

## Rule 1
Do **not** start with mixed zones.

## Rule 2
Do **not** split `main.cpp` and `Runtime/` in the same pass.

## Rule 3
Do **not** touch `Editor/` until Atlas/Core, Engine, UI, and NovaForge data/content have already moved.

## Rule 4
After every move:
- configure
- build
- fix
- commit

## Rule 5
Do **not** remove the old global include strategy until enough targets are isolated to survive without it.

---

# Success condition for the first real move pass

You are successful after the first pass when:

- `Atlas/Core/` contains the old `Core/`
- `Atlas/Engine/` contains the old `Engine/`
- `Atlas/UI/` contains the old `UI/`
- `NovaForge/Data/` and `NovaForge/Content/` contain the clean project assets/data
- the repo still builds
- you have not yet destabilized the mixed zones

That is the right first milestone.

---

# Practical summary

On your actual uploaded repo, the best first moves are:

## Move now
- `Core/` → `Atlas/Core/`
- `Engine/` → `Atlas/Engine/`
- `UI/` → `Atlas/UI/`
- safe `Projects/NovaForge/*` data/content → `NovaForge/Data/` and `NovaForge/Content/`
- add `Shared/ArbiterBridgeContract/`
- add `Shared/ProjectManifests/`

## Wait
- `Editor/`
- `Runtime/`
- `AI/`
- `Agents/`
- `IDE/`
- `Projects/NovaForge/main.cpp`
- `Projects/NovaForge/NovaForgeHUD.h`

That is the cleanest path from planning into real execution for this repo.
