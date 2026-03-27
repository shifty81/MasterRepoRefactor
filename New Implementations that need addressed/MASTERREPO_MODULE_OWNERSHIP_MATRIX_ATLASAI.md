# MASTERREPO MODULE OWNERSHIP MATRIX (ATLASAI VERSION)

## Purpose

This matrix defines where each subsystem belongs in the final consolidated architecture so refactors do not drift or duplicate responsibility.

---

## Ownership Matrix

| Subsystem | Final Owner | Source / Donor | Notes | Action |
|---|---|---|---|---|
| Engine core | AtlasCore | MasterRepo | Core native runtime ownership stays here | Keep / expand |
| ECS / simulation | AtlasRuntime | MasterRepo | Native gameplay simulation authority | Keep / refactor as needed |
| Rendering / viewport | AtlasRender | MasterRepo | Rendering stays native, not WPF | Keep |
| Native editor-backend | AtlasEditorBackend | MasterRepo + NovaForge requirements | Handles scene/world/asset editor operations | Expand |
| Game rules / gameplay systems | NovaForge.Systems on Atlas runtime | NovaForge + MasterRepo | Port subsystem by subsystem into MasterRepo | Migrate |
| Factions / standings / security | NovaForge.Systems | NovaForge | Data-driven game logic | Migrate |
| Economy / missions / PVE loops | NovaForge.Systems | NovaForge | Strong candidate for game module migration | Migrate |
| Modular ship systems | NovaForge.Systems | NovaForge | Must align with Atlas content/entity architecture | Migrate carefully |
| Interiors / boarding / on-foot logic | NovaForge.Systems | NovaForge | Requires engine support + content tooling | Stage after core systems |
| PCG / builder integration | AtlasToolsNative + NovaForge.Systems | MasterRepo + NovaForge | Native generation backend with game rules on top | Merge |
| Content schemas / data definitions | NovaForge.Data | NovaForge | Normalize formats before full migration | Migrate first |
| Asset pipeline / import / cooking | AssetService + AtlasToolsNative | MasterRepo | Tool-facing service with native backend | Keep / expose service |
| Build orchestration | BuildService | MasterRepo + Arbiter concepts | Exposed to WPF shell | Refactor |
| Test orchestration | TestService | MasterRepo | Useful for AI-assisted development workflow | Expose service |
| Logs / telemetry stream | Atlas backend services | MasterRepo | Stream to AtlasAI UI | Expose service |
| AI orchestration | AtlasAI.Core | ArbiterAI + MasterRepo AI systems | Central AI routing and automation layer | Rename + merge |
| Agents / planning | AtlasAI.Agents | ArbiterAI | Maintain modular agent architecture | Rename + merge |
| Memory / archive index | AtlasAI.Memory / AtlasAI.Archive | ArbiterAI + Arbiter | Can support docs, repo, notes, references | Merge |
| Chat UX | AtlasAI.Chat | Arbiter | Main user interaction layer in WPF | Rename + keep |
| Workspace shell | AtlasAI.WpfHost / AtlasAI.Shell | Arbiter | Main desktop shell | Rename + keep |
| Archive browser | AtlasAI.Archive UI | Arbiter | Strong fit for WPF | Keep / refine |
| Docs / design viewer | AtlasAI.UI | Arbiter + new work | Supports markdown, docs, PDFs, web content | Expand |
| Project explorer | AtlasAI.UI | Arbiter concepts | Repo/workspace navigation | Build/refine |
| Visual Studio integration | AtlasAI.Services | Arbiter concepts | External IDE assistance/integration | Refactor |
| Tray app / notifications | AtlasAI.WpfHost | Arbiter | Background desktop integration | Rename + keep |
| WebView-based embedded panels | AtlasAI.UI | Arbiter | Use only where appropriate | Selectively keep |
| Server/client product builds | AtlasRuntime + product targets | MasterRepo | Must remain separate from tooling release build | Keep strict separation |
| Dedicated AI local server | AIService / AtlasAI.Core | MasterRepo + ArbiterAI | Shared service for shell and automation | Merge |
| User/workspace profile system | AtlasAI.Workspace | Arbiter | Needed for multi-workspace future | Keep / refine |

---

## Final Ownership Rules

### Atlas.* owns

- engine
- runtime
- rendering
- native editor-backend
- build/test/content services
- authoritative simulation and asset operations

### AtlasAI.* owns

- WPF shell
- chat UX
- archive UX
- docs/tasks/log panels
- AI orchestration
- desktop workflow integration
- automation and workspace-level user interaction

### NovaForge.* owns

- game-specific systems
- progression/economy/faction logic
- content schemas
- gameplay loops
- design-driven requirements for editor and tools

---

## Things to Delete or Avoid

- duplicate editor logic in both WPF and native layers
- old `Arbiter` branding after migration completes
- direct WPF dependency inside runtime/game modules
- multiple AI control planes doing the same job
- duplicated archive/index/memory implementations

---

## Recommended Migration Order by Ownership

1. Lock names and ownership
2. Stand up AtlasAI WPF shell
3. Expose Atlas backend services
4. Merge AI orchestration into AtlasAI.Core
5. Migrate Arbiter workflows into AtlasAI UI
6. Migrate NovaForge data schemas
7. Migrate NovaForge gameplay systems in priority order
8. Remove legacy duplicate modules
