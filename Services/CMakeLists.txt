# Services — atlas backend service stubs (build, asset, world, session, telemetry)

add_subdirectory(AtlasBuildService)
add_subdirectory(AtlasAssetService)
add_subdirectory(AtlasWorldService)
add_subdirectory(AtlasSessionService)
add_subdirectory(AtlasTelemetryService)

message(STATUS "Services: configured")
