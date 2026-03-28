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

# ── External dependencies (header-only and compiled) ─────────────────────────

include(FetchContent)

# GLM — OpenGL Mathematics library (header-only)
# Expected path per ExternalDepsManifest: ThirdParty/glm
if(NOT TARGET glm::glm)
    set(_glm_local "${CMAKE_CURRENT_SOURCE_DIR}/ThirdParty/glm")
    if(EXISTS "${_glm_local}/glm/glm.hpp")
        add_library(glm_vendor INTERFACE)
        add_library(glm::glm ALIAS glm_vendor)
        target_include_directories(glm_vendor INTERFACE "${_glm_local}")
    else()
        FetchContent_Declare(glm
            GIT_REPOSITORY https://github.com/g-truc/glm.git
            GIT_TAG        1.0.1
            GIT_SHALLOW    TRUE
        )
        FetchContent_MakeAvailable(glm)
    endif()
endif()

# GLFW — multi-platform windowing/input library
# Only use FetchContent on non-Linux systems where display libraries are available.
if(NOT TARGET glfw)
    find_package(glfw3 QUIET)
    if(NOT glfw3_FOUND AND NOT (CMAKE_SYSTEM_NAME STREQUAL "Linux"))
        FetchContent_Declare(glfw
            GIT_REPOSITORY https://github.com/glfw/glfw.git
            GIT_TAG        3.4
            GIT_SHALLOW    TRUE
        )
        set(GLFW_BUILD_DOCS     OFF CACHE BOOL "" FORCE)
        set(GLFW_BUILD_TESTS    OFF CACHE BOOL "" FORCE)
        set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
        FetchContent_MakeAvailable(glfw)
    endif()
endif()

# GLEW — OpenGL Extension Wrangler
# Only use FetchContent on non-Linux systems where display libraries are available.
if(NOT TARGET GLEW::GLEW)
    find_package(GLEW QUIET)
    if(NOT GLEW_FOUND AND NOT (CMAKE_SYSTEM_NAME STREQUAL "Linux"))
        FetchContent_Declare(glew
            GIT_REPOSITORY https://github.com/Perlmint/glew-cmake.git
            GIT_TAG        glew-cmake-2.2.0
            GIT_SHALLOW    TRUE
        )
        set(glew-cmake_BUILD_SHARED     OFF CACHE BOOL "" FORCE)
        set(glew-cmake_BUILD_STATIC     ON  CACHE BOOL "" FORCE)
        set(ONLY_LIBS                   ON  CACHE BOOL "" FORCE)
        FetchContent_MakeAvailable(glew)
        # Alias to GLEW::GLEW if the target name differs
        if(TARGET libglew_static AND NOT TARGET GLEW::GLEW)
            add_library(GLEW::GLEW ALIAS libglew_static)
        endif()
    endif()
endif()

# Add subdirectories in dependency order
add_subdirectory(Shared)
add_subdirectory(Atlas)
add_subdirectory(NovaForge)
add_subdirectory(Services)

if(MASTERREPO_BUILD_TESTS)
    enable_testing()
    add_subdirectory(Tests)
endif()
