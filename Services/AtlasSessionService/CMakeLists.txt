# AtlasSessionService — workspace session state and project context service

set(SOURCES
    src/AtlasSessionService.cpp
)

add_library(AtlasSessionService STATIC ${SOURCES})

target_include_directories(AtlasSessionService
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_link_libraries(AtlasSessionService PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(AtlasSessionService)

message(STATUS "AtlasSessionService: configured")
