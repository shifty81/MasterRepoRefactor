# NovaForge App — bootstrap, session, project context

set(NOVAFORGE_APP_SOURCES
    src/NovaForgeApp_stub.cpp
    # add source files here as bootstrap and session systems are implemented
)

add_library(NovaForgeApp STATIC ${NOVAFORGE_APP_SOURCES})

target_include_directories(NovaForgeApp
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(NovaForgeApp PUBLIC AtlasRuntime)

masterrepo_set_compiler_warnings(NovaForgeApp)

message(STATUS "NovaForgeApp: configured")
