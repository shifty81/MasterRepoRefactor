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
