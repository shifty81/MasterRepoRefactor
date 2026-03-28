# AtlasEditor — editor framework, panels, commands, selection, tools

set(ATLAS_EDITOR_SOURCES
    src/AtlasEditor_stub.cpp
    # add source files here as editor framework systems are implemented
)

add_library(AtlasEditor STATIC ${ATLAS_EDITOR_SOURCES})

target_include_directories(AtlasEditor
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(AtlasEditor PUBLIC AtlasRuntime)

masterrepo_set_compiler_warnings(AtlasEditor)

message(STATUS "AtlasEditor: configured")
