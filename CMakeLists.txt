cmake_minimum_required(VERSION 3.20)

project(MasterRepo
    VERSION 0.1.0
    DESCRIPTION "MasterRepo — unified engine, game, and AI tooling platform"
    LANGUAGES CXX C
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Include global CMake modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include(Options)
include(PlatformConfig)
include(CompilerWarnings)

# Add subdirectories in dependency order
add_subdirectory(Shared)
add_subdirectory(Atlas)
add_subdirectory(NovaForge)
add_subdirectory(Services)

if(MASTERREPO_BUILD_TESTS)
    enable_testing()
    add_subdirectory(Tests)
endif()
