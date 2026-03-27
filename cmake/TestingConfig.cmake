# MasterRepo testing configuration

include(CTest)

function(masterrepo_add_test name)
    cmake_parse_arguments(ARG "" "" "SOURCES;DEPS" ${ARGN})
    add_executable(${name} ${ARG_SOURCES})
    if(ARG_DEPS)
        target_link_libraries(${name} PRIVATE ${ARG_DEPS})
    endif()
    add_test(NAME ${name} COMMAND ${name})
endfunction()
