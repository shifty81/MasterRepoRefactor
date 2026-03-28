# Repo Patch Guide

## Atlas service landing points

### Security
- `Atlas/Services/Security/SessionAuthority/`
- `Atlas/Services/Security/CapabilityResolver/`
- `Atlas/Services/Security/PathPolicyService/`
- `Atlas/Services/Security/AuditEventWriter/`

### Archive
- `Atlas/Services/Archive/ArchiveIntakeService/`

### Bridge
- `Atlas/Services/Bridge/CommandBroker/`
- `Atlas/Services/Bridge/BridgeService/`

## CMake patch idea
Add a tooling-only target:
```cmake
add_subdirectory(Atlas/Services)
```

Then guard with editor/dev flags:
```cmake
if(MASTERREPO_BUILD_EDITOR AND ATLAS_ENABLE_EDITOR)
    add_subdirectory(Atlas/Services)
endif()
```

## Runtime rule
Do not link the hardening services into shipping runtime binaries.
