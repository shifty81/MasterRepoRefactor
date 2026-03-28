# Shipping Separation Rules

## Goal

Shipping client and server builds must not include AtlasAI UI, tooling code,
or any development-only infrastructure.

## CMake flags

| Flag | Default | Purpose |
|------|---------|---------|
| `MASTERREPO_BUILD_EDITOR` | `ON` | Include editor targets |
| `NOVAFORGE_ENABLE_ATLASAI_INTEGRATION` | `ON` | Include NovaForge bridge layer |
| `MASTERREPO_BUILD_TOOLS` | `ON` | Include developer tool targets |

For a shipping build, set:

```cmake
-DMASTERREPO_BUILD_EDITOR=OFF
-DNOVAFORGE_ENABLE_ATLASAI_INTEGRATION=OFF
-DMASTERREPO_BUILD_TOOLS=OFF
```

## Rules

1. `NovaForge/Integrations/AtlasAI/` must only be compiled when
   `NOVAFORGE_ENABLE_ATLASAI_INTEGRATION=ON`.

2. Atlas editor systems (`Atlas/Editor/`) must only be compiled when
   `ATLAS_ENABLE_EDITOR=ON`.

3. AtlasAI is a C#/.NET project. It must never be referenced by C++ game
   or engine targets directly.

4. Any header in `NovaForge/Integrations/AtlasAI/include/` must be guarded
   and never `#include`d from core gameplay or runtime code.

## Verification

Before any release:

1. Configure with all tooling/editor flags OFF.
2. Confirm CMake configure succeeds.
3. Confirm build succeeds without any AtlasAI or editor artifacts.
4. Confirm no `ArbiterBridge*` symbols appear in shipping binaries.

## Release Procedure

Releases are triggered automatically by pushing a version tag matching `v[0-9]*`
(e.g. `v1.0.0`) to the main branch.  The `.github/workflows/release.yml` workflow
runs two parallel jobs:

### 1. Windows Installer (`build-installer`)

1. Checks out the repository on a `windows-latest` runner.
2. Builds the Inno Setup installer by running:
   ```
   iscc.exe AtlasAI/Installer/atlasai_setup.iss
   ```
3. **Optionally signs** the resulting `AtlasAISetup.exe` using `signtool.exe` if the
   `CODESIGN_PFX` repository secret is set (code-signing certificate passphrase).
4. Uploads `AtlasAI/Installer/Output/AtlasAISetup.exe` as a GitHub Release asset via
   `softprops/action-gh-release@v2`.

### 2. Python Package (`build-python-package`)

1. Checks out the repository on an `ubuntu-latest` runner.
2. Sets up Python 3.12 via `actions/setup-python@v5`.
3. Installs the `build` tool and runs `python -m build AtlasAI/` to produce both
   a wheel (`.whl`) and a source distribution (`.tar.gz`).
4. Uploads both distribution artifacts as GitHub Release assets.

### Pre-release checklist

Before tagging a release:

1. Confirm all CI checks pass on the target commit.
2. Configure a clean build with all tooling/editor flags OFF (see CMake flags above)
   and verify no AtlasAI artifacts appear in the shipping binaries.
3. Bump the version in `AtlasAI/pyproject.toml` (or equivalent) to match the tag.
4. Push the tag: `git tag v1.x.y && git push origin v1.x.y`.
