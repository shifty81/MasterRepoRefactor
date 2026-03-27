# NovaForge Gameplay — game systems, factions, economy, missions, combat

set(NOVAFORGE_GAMEPLAY_SOURCES
    src/NovaForgeGameplay_stub.cpp
    # add source files here as gameplay systems are implemented
)

add_library(NovaForgeGameplay STATIC ${NOVAFORGE_GAMEPLAY_SOURCES})

target_include_directories(NovaForgeGameplay
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(NovaForgeGameplay PUBLIC AtlasEngine)

masterrepo_set_compiler_warnings(NovaForgeGameplay)

message(STATUS "NovaForgeGameplay: configured")
