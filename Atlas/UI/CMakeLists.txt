# AtlasUI — custom UI framework, layout, controls, styling, rendering, themes

set(ATLAS_UI_SOURCES
    src/AtlasUI_stub.cpp
    # add source files here as UI framework systems are implemented
)

add_library(AtlasUI STATIC ${ATLAS_UI_SOURCES})

target_include_directories(AtlasUI
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(AtlasUI PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(AtlasUI)

message(STATUS "AtlasUI: configured")
