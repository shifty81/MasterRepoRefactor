# MasterRepo repo-level tests

include(TestingConfig)

add_subdirectory(Integration)
add_subdirectory(BuildVerification)

message(STATUS "Tests: configured")
