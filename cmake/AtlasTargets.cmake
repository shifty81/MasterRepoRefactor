# Atlas CMake target helpers

function(atlas_add_library name)
    cmake_parse_arguments(ARG "" "" "SOURCES;DEPS" ${ARGN})
    add_library(${name} STATIC ${ARG_SOURCES})
    target_include_directories(${name}
        PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}/include"
        PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src"
    )
    if(ARG_DEPS)
        target_link_libraries(${name} PUBLIC ${ARG_DEPS})
    endif()
    masterrepo_set_compiler_warnings(${name})
endfunction()
