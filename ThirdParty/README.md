# ThirdParty

This folder contains vendored external dependencies.

## Rules

- All third-party source must be clearly separated from first-party code.
- Each vendored package must include its license file.
- Versions must be pinned.
- Avoid modifying vendored sources. Prefer thin wrapper layers in Atlas or Shared.

## VendorPackages/

Each vendor package gets its own subfolder:

```
ThirdParty/VendorPackages/<package-name>/
```
