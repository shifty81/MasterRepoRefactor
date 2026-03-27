# Shared CMake target helpers

function(shared_add_contract name)
    add_library(${name} INTERFACE)
    target_include_directories(${name}
        INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/include"
    )
endfunction()
