# Patch Review Specification

## Purpose
Replace boolean approval with a real reviewable patch workflow for protected-root mutations.

## Patch Lifecycle
- proposed
- validated
- reviewed
- approved
- applied
- reverted
- rejected

## Patch Object
Each patch record must include:
- patchId
- patchHash
- creatorSessionId
- creatorIdentity
- targetPaths
- diffSummary
- diffArtifactPath
- createdUtc
- reviewState

## Approval Object
Each approval record must include:
- approvalId
- patchId
- approvedPatchHash
- reviewerIdentity
- reviewerSessionId
- approvalUtc
- targetPaths
- rationale
- expirationUtc optional
- revoked flag

## Required Directories
```text
%LOCALAPPDATA%/AtlasSuite/PatchQueue/
    Patches/
    Approvals/
    RevertBundles/
```

## Enforcement Rules
Protected-root apply is allowed only if:
- the patch exists
- the patch hash matches the request
- the approval record exists
- the patch is in approved state
- target path list exactly matches the approved set
- the approval is not revoked or expired

## Required Service API
```cpp
struct PatchApplyAuthorization
{
    bool authorized;
    std::string patchId;
    std::string patchHash;
    std::string reviewerIdentity;
    std::string denialReason;
};

PatchApplyAuthorization AuthorizeApply(
    const std::string& patchId,
    const std::vector<std::string>& requestedPaths,
    const std::string& requestedPatchHash);
```

## Required Tests
- deny apply when only a boolean flag is present
- deny hash mismatch
- deny wrong target path set
- allow approved generated-root patch
- allow protected-root patch only through review service
