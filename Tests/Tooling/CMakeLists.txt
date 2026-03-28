# Build verification tests for Services layer

masterrepo_add_test(
    ServicesCompileTest
    SOURCES services_compile_test.cpp
    DEPS    AtlasBuildService
            AtlasAssetService
            AtlasWorldService
            AtlasSessionService
            AtlasTelemetryService
)

message(STATUS "Tests/Tooling: configured")
