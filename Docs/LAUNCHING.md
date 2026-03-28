# Building and Launching MasterRepo

> **See also:** [Docs/Design/MASTER_REPO_DIRECTIVE.md](Design/MASTER_REPO_DIRECTIVE.md) · [Docs/Roadmaps/roadmap.md](Roadmaps/roadmap.md)

---

## Prerequisites

| Tool | Minimum version |
|---|---|
| CMake | 3.20 |
| C++ compiler | C++20 support (GCC 12+, Clang 14+, MSVC 2022) |
| Python | 3.10+ (for AtlasAI and test suite) |
| Git | Any recent version |

Optional:

| Tool | Required for |
|---|---|
| Node.js 18+ | AtlasAI WebhookIntegration TypeScript build |
| .NET 6 SDK | AtlasAI HostApp (C# WPF) |
| Ninja | Faster CMake builds (`-G Ninja`) |

---

## Quick Start

### 1 — Build

```bash
# Debug build (default)
./Scripts/Build/build.sh

# Release build with tests
./Scripts/Build/build.sh --config Release --tests
```

The compiled executable is placed at:

```
Build/NovaForge/App/MasterRepoRuntime
```

### 2 — Launch

```bash
# Launch the game client
./Scripts/Run/launch.sh --mode game

# Launch the editor shell
./Scripts/Run/launch.sh --mode editor

# Launch the editor with AtlasAI bridge enabled
./Scripts/Run/launch.sh --mode editor --bridge

# Run a headless playtest (CI smoke test)
./Scripts/Run/launch.sh --mode playtest --headless

# Build first, then launch in editor mode
./Scripts/Run/launch.sh --build --mode editor
```

---

## Launch Modes

| Mode | Description |
|---|---|
| `game` | NovaForge game client. Full HUD active, no editor panels. |
| `editor` | Atlas editor shell. All panels, gizmos, and the AtlasAI integration dock. |
| `server` | NovaForge headless dedicated server. No rendering, no UI. |
| `playtest` | Automated `PlaytestSession` smoke-test run. Returns exit code 0 (pass) or 1 (fail). |

---

## Launch Flags

| Flag | Default | Description |
|---|---|---|
| `--mode <mode>` | `game` | Execution mode (see table above) |
| `--config <Debug\|Release\|Shipping>` | `Debug` | Which build artefacts to run |
| `--build` | off | Rebuild before launching |
| `--headless` | off | Suppress all window creation (for CI / playtest) |
| `--bridge` | off | Start the AtlasAI bridge server |
| `--bridge-port <port>` | `8765` | Port for the AtlasAI bridge REST/WebSocket server |
| `--dev` | off | Enable the F12 dev overlay at startup |
| `--save <name>` | — | Load a named save slot on boot |

---

## Boot Sequence

```
main()
  ├── LaunchConfig::Parse(argc, argv)       ← resolve mode and flags
  ├── RuntimeBootstrap::Initialize(mode)    ← core engine systems
  │     ├── LoadCoreSystems()               ← logger, config, ECS, event bus
  │     ├── LoadPlatformSystems(mode)       ← rendering, UI, networking, editor
  │     └── LoadGameModules()               ← gameplay system hooks
  ├── GameSystemsRegistry                   ← all subsystems register + mark ready
  ├── WorldBootstrap::RunAll()              ← ordered phase sequence:
  │     ├── LoadConfig
  │     ├── LoadDataRegistry
  │     ├── InitialiseGameplaySystems
  │     ├── LoadOrGenerateWorld
  │     ├── SpawnPlayer
  │     ├── BootstrapUI
  │     └── BootstrapEditor  (editor mode only)
  └── Engine::Run()                         ← main loop until quit
```

---

## Playtest / CI Smoke Test

The `playtest` mode runs a `TestHarness` with one or more `PlaytestSession`
instances in headless mode and exits with code `0` (all pass) or `1` (any failure).

```bash
# Run the full playtest suite
./Scripts/Run/launch.sh --mode playtest --headless
echo "Exit: $?"

# The same thing via CMake/CTest after a test build:
./Scripts/Build/build.sh --config Debug --tests
cd Build && ctest --output-on-failure
```

---

## Python Tests

The AtlasAI test suite (Python pytest) covers all gameplay, engine, and AI module
designs without requiring a compiled build:

```bash
pip install pytest
python -m pytest AtlasAI/Tests/ -v
```

---

## Manual CMake Build

If you prefer to drive CMake directly:

```bash
cmake -S . -B Build -DCMAKE_BUILD_TYPE=Debug -DMASTERREPO_BUILD_TESTS=ON
cmake --build Build --parallel
```

Add `-DNOVAFORGE_ENABLE_ATLASAI_INTEGRATION=ON -DNOVAFORGE_ENABLE_BRIDGE_SERVER=ON`
to build with full AtlasAI bridge support.

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `Executable not found` | Build not run yet | Run `./Scripts/Build/build.sh` first |
| `Failed to initialize MasterRepoEditorRuntime` | Missing data files or config | Check `Data/` directory exists and contains valid JSON |
| Bridge connection refused | AtlasAI bridge not started | Launch with `--bridge` or start AtlasAI HostApp separately |
| CMake can't find glm/nlohmann | Missing third-party deps | Run `./Scripts/Setup/install_deps.sh` |
