# NovaForge App — bootstrap, session, project context

set(NOVAFORGE_APP_SOURCES
    # placeholder — add source files here as they are created
)

add_library(NovaForgeApp STATIC ${NOVAFORGE_APP_SOURCES})

target_include_directories(NovaForgeApp
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(NovaForgeApp PUBLIC AtlasRuntime)

masterrepo_set_compiler_warnings(NovaForgeApp)

message(STATUS "NovaForgeApp: configured")
