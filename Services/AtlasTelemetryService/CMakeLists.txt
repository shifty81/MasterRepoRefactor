# AtlasTelemetryService — log streaming, diagnostics, and event broadcast service

set(SOURCES
    src/AtlasTelemetryService.cpp
)

add_library(AtlasTelemetryService STATIC ${SOURCES})

target_include_directories(AtlasTelemetryService
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_link_libraries(AtlasTelemetryService PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(AtlasTelemetryService)

message(STATUS "AtlasTelemetryService: configured")
