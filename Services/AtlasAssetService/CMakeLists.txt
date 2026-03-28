# AtlasAssetService — asset import, export, and metadata service

set(SOURCES
    src/AtlasAssetService.cpp
)

add_library(AtlasAssetService STATIC ${SOURCES})

target_include_directories(AtlasAssetService
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_link_libraries(AtlasAssetService PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(AtlasAssetService)

message(STATUS "AtlasAssetService: configured")
