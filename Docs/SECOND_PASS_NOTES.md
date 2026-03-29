# Second pass notes

This bundle is the next step after the first-pass skeleton.

## What changed
- Replaced placeholder top-level INTERFACE-only Atlas/NovaForge grouping with real module subdirectory CMake files.
- Added module-level `set(..._SOURCES ...)` lists where you can map existing repo files gradually.
- Kept Arbiter integration optional and editor-gated.
- Kept client/server free of Arbiter integration linkage.
- Added a minimal test target for the integration layer.

## Intended migration method
1. Drop these files into the monorepo structure.
2. Start filling the source lists module by module.
3. Move existing source files into the target tree gradually.
4. Keep builds green after each module mapping pass.
5. Only after the module graph is stable, add richer Arbiter bridge implementation.
