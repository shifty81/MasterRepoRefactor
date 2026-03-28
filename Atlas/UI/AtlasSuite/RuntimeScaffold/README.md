# Atlas Suite Build Pack v1

This scaffold is a clean C# foundation for the **Atlas Suite** WPF shell and service layer.
It is designed to plug into the existing Master Repo direction:
- executable name and user-facing shell: **Atlas Suite**
- AI subsystem name: **AtlasAI**
- hybrid workflow: engine + editor + runtime + tooling
- project target: **NovaForge**

## Included
- WPF shell project (`AtlasSuite.App`)
- core service/contracts project (`AtlasSuite.Core`)
- AI module stubs (`AtlasSuite.Modules.AI`)
- engine bridge stubs (`AtlasSuite.Modules.Engine`)
- project/workspace module stubs (`AtlasSuite.Modules.Project`)
- plugin abstraction and one sample plugin
- starter workspace layout JSON

## Notes
This pack is intentionally scaffold-first. It favors clean interfaces, registration points, and safe stubs over hidden magic.

## Suggested integration target
Place under:
`Atlas/UI/AtlasSuite/RuntimeScaffold/` or promote into a root `/AtlasSuite/` solution folder once approved.
