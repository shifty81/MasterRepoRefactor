# NovaForge UI — runtime UI shell

set(NOVAFORGE_UI_SOURCES
    src/RuntimeUIShell.cpp
)

add_library(NovaForgeUI STATIC ${NOVAFORGE_UI_SOURCES})

target_include_directories(NovaForgeUI
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(NovaForgeUI PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(NovaForgeUI)

message(STATUS "NovaForgeUI: configured")
