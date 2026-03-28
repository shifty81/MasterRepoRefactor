# Path Canonicalization Specification

## Purpose
Eliminate path traversal, path ambiguity, reparse-point escape, and root-prefix trust errors.

## Goals
Every authorization decision must operate on a canonical path anchored to the repo root.

## Required Canonicalization Pipeline
For every read/write path:
1. normalize separators
2. trim redundant separators
3. collapse `.` and `..`
4. resolve absolute path
5. normalize Windows drive letter case
6. resolve symlinks and junctions where supported
7. verify the final canonical path remains under the configured repo root
8. classify the path against canonical policy roots

## Deny Reasons
```cpp
enum class PathValidationResult
{
    Allowed,
    DeniedOutsideRepo,
    DeniedProtectedRoot,
    DeniedTraversal,
    DeniedReparsePoint,
    DeniedUnknownClass,
    DeniedMalformedPath
};
```

## Required Service API
```cpp
struct CanonicalPathResult
{
    bool success;
    std::string inputPath;
    std::string canonicalPath;
    PathValidationResult result;
    std::string reason;
};

CanonicalPathResult CanonicalizeAndValidate(
    const std::string& repoRoot,
    const std::string& requestedPath,
    FileOperation operation);
```

## Windows Rules
- treat `C:\Repo` and `c:\repo` as the same root after normalization
- reject UNC paths unless explicitly configured and trusted
- reject writes through junctions or reparse points unless the destination root explicitly allows them
- normalize mixed `\` and `/`

## Required Tests
- reject `..\\..\\outside.txt`
- reject canonical path escape through a junction
- allow normalized generated-root write
- deny protected-root direct write
- deny malformed drive path

## Example Policy Decision
```json
{
  "inputPath": "C:\\Repo\\Atlas\\..\\Generated\\spec.md",
  "canonicalPath": "C:\\Repo\\Generated\\spec.md",
  "operation": "write",
  "rootClass": "generated",
  "decision": "allow"
}
```
