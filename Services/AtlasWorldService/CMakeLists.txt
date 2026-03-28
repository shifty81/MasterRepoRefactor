# AtlasWorldService — world/scene query, load, and save service

set(SOURCES
    src/AtlasWorldService.cpp
)

add_library(AtlasWorldService STATIC ${SOURCES})

target_include_directories(AtlasWorldService
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_link_libraries(AtlasWorldService PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(AtlasWorldService)

message(STATUS "AtlasWorldService: configured")
