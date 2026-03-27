# Atlas — engine, editor framework, runtime foundations, custom UI

include(AtlasTargets)
include(CompilerWarnings)

# AtlasCore: core primitives, containers, memory, math, logging
add_subdirectory(Core)

# AtlasEngine: ECS, world, scene, assets, rendering, physics
add_subdirectory(Engine)

# AtlasRuntime: application framework, game loop, simulation
add_subdirectory(Runtime)

if(MASTERREPO_BUILD_EDITOR AND ATLAS_ENABLE_EDITOR)
    # AtlasEditor: editor framework, panels, tools, services
    add_subdirectory(Editor)
endif()

# AtlasUI: custom UI framework
add_subdirectory(UI)

message(STATUS "Atlas: modules configured")
