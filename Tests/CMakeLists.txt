# MasterRepo repo-level tests

include(TestingConfig)

add_subdirectory(Integration)
add_subdirectory(BuildVerification)
add_subdirectory(Tooling)

message(STATUS "Tests: configured")
