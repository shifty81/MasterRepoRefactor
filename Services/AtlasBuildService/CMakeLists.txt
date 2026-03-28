# AtlasBuildService — build orchestration service

set(SOURCES
    src/AtlasBuildService.cpp
)

add_library(AtlasBuildService STATIC ${SOURCES})

target_include_directories(AtlasBuildService
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_link_libraries(AtlasBuildService PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(AtlasBuildService)

message(STATUS "AtlasBuildService: configured")
