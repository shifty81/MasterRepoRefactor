# AtlasSuiteBuildPackV1 — Intake Processing Log

**Date processed:** 2026-03-28  
**Source zip:** `AtlasSuiteBuildPackV1.zip` (committed to repo root in commit `1445b7c` by accident, deleted without archiving in `38b4d2a`)  
**Integration target:** `Atlas/UI/AtlasSuite/RuntimeScaffold/`  
**Archive location:** `Docs/Archive/ZipFiles/AtlasSuiteBuildPackV1.zip`

---

## What was in the zip

A clean C# WPF foundation scaffold for the **Atlas Suite** shell and service layer, structured as
a multi-project .NET 8 solution (`AtlasSuite.BuildPack.sln`).

| Project | Purpose |
|---|---|
| `AtlasSuite.App` | WPF shell — window, views, view models, commands |
| `AtlasSuite.Core` | Service contracts, command bus, docking model, job queue, workspace layout |
| `AtlasSuite.Modules.AI` | AtlasAI stub service |
| `AtlasSuite.Modules.Engine` | Engine bridge service stub |
| `AtlasSuite.Modules.Project` | Project context service |
| `AtlasSuite.Plugins.Abstractions` | Plugin interface |
| `AtlasSuite.Plugin.Sample` | Sample salvage plugin |

---

## Errors found and corrected

### ERROR 1 — Eight duplicate implicit `DataTemplate` entries in `MainWindow.xaml` (XAML dead code)

**File:** `src/AtlasSuite.App/Views/MainWindow.xaml` — `Window.Resources`  
**Problem:** The `<Window.Resources>` block contained **9 identical** implicit
`DataTemplate` entries for `{x:Type vm:PanelViewModel}`, plus one extra entry with
`x:Key="IgnoredTemplate"`.  In WPF a resource dictionary may only have one entry per type
as an implicit (keyless) template; duplicates override each other silently, and the named
`IgnoredTemplate` key is a clear sign they were placeholders never cleaned up.
This creates dead-code noise and can cause unpredictable rendering in some WPF hosts.  
**Fix:** Collapsed to a single implicit `DataTemplate` for `PanelViewModel` that routes its
`Content` through a `ContentPresenter`.

---

### ERROR 2 — Two duplicate implicit `DataTemplate` entries in the right `TabControl.Resources` (XAML dead code)

**File:** `src/AtlasSuite.App/Views/MainWindow.xaml` — right-panel `TabControl`  
**Problem:** The right-column `TabControl` had a `<TabControl.Resources>` block with
**three** `DataTemplate` entries for `PanelViewModel` — two keyless and one keyed
`DefaultPanelTemplate`.  Same duplicate-template issue as ERROR 1.  
**Fix:** Removed the `TabControl.Resources` block entirely; the `ItemTemplate` and
`ContentTemplate` properties already supply the correct templates.

---

## Known risk noted (not changed)

**`RunFireAndForget` in `MainWindowViewModel` uses `Task.Run` — threading caution.**

`MainWindowViewModel.RunFireAndForget` dispatches work to the thread-pool via `Task.Run`.
Its error handler calls `LogPanel.Append(...)` which modifies an `ObservableCollection<string>`
from a non-UI thread.  WPF data-binding to an `ObservableCollection` from a background thread
can throw a `NotSupportedException`.  For a scaffold this is acceptable, but wiring in a real
DI container (implementation note #1) should also add proper UI-thread marshalling
(e.g. `Application.Current.Dispatcher.InvokeAsync`) to this error path.

---

## What was NOT changed

All C# logic files (`CommandBus`, `InMemoryJobRunner`, `WorkspaceService`, view models,
modules, plugins) were copied verbatim from the zip; no behavioural logic was altered.

---

## Integration notes

The README inside the zip suggested placing the content under
`Atlas/UI/AtlasSuite/RuntimeScaffold/` — that is where it now lives.  Immediate next
steps per the pack's own `IMPLEMENTATION_NOTES.md`:

1. Wire a real DI container (replace manual `new` in `MainWindow.xaml.cs`).
2. Replace the placeholder docking host with a real docking framework.
3. Connect `EngineBridgeService` to the native Atlas runtime via named pipes or WebSocket.
4. Persist workspace layouts under a user profile path.
5. Add command palette UI and searchable command registry.
6. Add schema registry and AtlasAI task graph execution.
