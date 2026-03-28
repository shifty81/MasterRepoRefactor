# AtlasEditor — editor framework, panels, commands, selection, tools

set(ATLAS_EDITOR_SOURCES
    src/AtlasEditor_stub.cpp
    EditorShell.cpp

    # Core
    Core/EditorModeController.cpp

    # Input
    Input/EditorInputRouter.cpp

    # Camera
    Camera/EditorCameraController.cpp

    # Selection
    Selection/SelectionSystem.cpp

    # Outliner
    Outliner/SceneOutliner.cpp

    # Inspector
    Inspector/PropertyInspector.cpp

    # Gizmos
    Gizmos/GizmoSystem.cpp

    # Commands (undo/redo)
    Commands/CommandStack.cpp
    Commands/TransformCommand.cpp
    Commands/PropertyEditCommand.cpp
    Commands/VoxelEditCommand.cpp

    # Validation toolkit
    Validation/ValidationSystem.cpp
)

add_library(AtlasEditor STATIC ${ATLAS_EDITOR_SOURCES})

target_include_directories(AtlasEditor
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
             "${CMAKE_CURRENT_SOURCE_DIR}/Core"
             "${CMAKE_CURRENT_SOURCE_DIR}/Input"
             "${CMAKE_CURRENT_SOURCE_DIR}/Camera"
             "${CMAKE_CURRENT_SOURCE_DIR}/Selection"
             "${CMAKE_CURRENT_SOURCE_DIR}/Outliner"
             "${CMAKE_CURRENT_SOURCE_DIR}/Inspector"
             "${CMAKE_CURRENT_SOURCE_DIR}/Gizmos"
             "${CMAKE_CURRENT_SOURCE_DIR}/Commands"
             "${CMAKE_CURRENT_SOURCE_DIR}/Validation"
             "${CMAKE_CURRENT_SOURCE_DIR}/Framework"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(AtlasEditor PUBLIC AtlasRuntime)

masterrepo_set_compiler_warnings(AtlasEditor)

message(STATUS "AtlasEditor: configured")
