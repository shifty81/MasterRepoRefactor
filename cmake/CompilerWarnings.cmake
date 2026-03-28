# MasterRepo compiler warning configuration

function(masterrepo_set_compiler_warnings target)
    if(MSVC)
        target_compile_options(${target} PRIVATE
            /W4
            /WX
            /FS      # serialise PDB writes (prevents C1041 in parallel builds)
            /wd4100  # unreferenced formal parameter
            /wd4505  # unreferenced local function has been removed
        )
    elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(${target} PRIVATE
            -Wall
            -Wextra
            -Wpedantic
            -Werror
            -Wno-unused-parameter
        )
    endif()
endfunction()
