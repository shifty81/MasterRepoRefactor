# MasterRepo platform configuration

if(WIN32)
    add_compile_definitions(MASTERREPO_PLATFORM_WINDOWS=1)
elseif(UNIX AND NOT APPLE)
    add_compile_definitions(MASTERREPO_PLATFORM_LINUX=1)
elseif(APPLE)
    add_compile_definitions(MASTERREPO_PLATFORM_MACOS=1)
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_definitions(MASTERREPO_BUILD_DEBUG=1)
elseif(CMAKE_BUILD_TYPE STREQUAL "Release")
    add_compile_definitions(MASTERREPO_BUILD_RELEASE=1)
endif()
