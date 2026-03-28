# NovaForge Gameplay — game systems, factions, economy, missions, combat

set(NOVAFORGE_GAMEPLAY_SOURCES
    src/NovaForgeGameplay_stub.cpp

    # Combat
    Combat/CombatSystem.cpp

    # Economy
    Economy/TradeMarket.cpp
    Economy/ResourceRegistry.cpp

    # Factions
    Factions/FactionRegistry.cpp

    # Missions
    Missions/MissionRegistry.cpp

    # Mining
    Mining/MiningSystem.cpp

    # Exploration
    Exploration/ExplorationSystem.cpp

    # PCG
    PCG/PCGWorldGen.cpp

    # Progression
    Progression/ProgressionSystem.cpp

    # Player Systems
    PlayerSystems/PlayerController.cpp

    # Builder
    Builder/BuilderSystem.cpp
)

add_library(NovaForgeGameplay STATIC ${NOVAFORGE_GAMEPLAY_SOURCES})

target_include_directories(NovaForgeGameplay
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(NovaForgeGameplay PUBLIC AtlasEngine)

masterrepo_set_compiler_warnings(NovaForgeGameplay)

message(STATUS "NovaForgeGameplay: configured")
