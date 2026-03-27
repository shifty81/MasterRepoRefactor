# MasterRepo global build options

option(MASTERREPO_BUILD_TESTS       "Build repo-level tests"            ON)
option(MASTERREPO_BUILD_TOOLS       "Build developer tools"             ON)
option(MASTERREPO_BUILD_EDITOR      "Build editor targets"              ON)
option(MASTERREPO_BUILD_CLIENT      "Build client game targets"         ON)
option(MASTERREPO_BUILD_SERVER      "Build server game targets"         ON)

option(ATLAS_ENABLE_EDITOR          "Enable Atlas editor systems"       ON)
option(ATLAS_ENABLE_TOOLS_RUNTIME   "Enable Atlas tools runtime hooks"  ON)

option(NOVAFORGE_ENABLE_ARBITER_INTEGRATION
    "Enable NovaForge Arbiter bridge integration"                       ON)

# Epic 7: Compile-time feature guards
# These flags ensure tooling-only code never leaks into shipping binaries.
option(NOVAFORGE_ENABLE_BRIDGE_SERVER
    "Enable the in-process bridge server (editor/dev builds only)"      ON)

option(NOVAFORGE_ENABLE_AUDIT_LOGGING
    "Enable bridge audit logging to disk (dev/editor builds only)"      ON)
