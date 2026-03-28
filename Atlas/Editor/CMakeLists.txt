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

    # Voxel editor workflow (C1)
    Voxel/VoxelChunkEditor.cpp
    Voxel/VoxelEditorMode.cpp

    # PCG debug mode (C4)
    PCG/PCGDebugSystem.cpp

    # Outliner + Inspector completion (C2)
    Outliner/SceneHierarchySystem.cpp

    # Gizmo + Placement completion (C3)
    Gizmos/PlacementSystem.cpp

    # Prefab / Template authoring (C7)
    Prefabs/PrefabLibrary.cpp
    Prefabs/PrefabManager.cpp

    # Editor Dock Layout (B4 editor panel docking)
    Core/EditorDockLayout.cpp

    # AtlasAI editor workflow (E1)
    AI/DiffReviewPanel.cpp

    # Editor Docs panels (H1/H2/H3)
    Docs/DesignDocPanel.cpp
    Docs/FeatureChecklistPanel.cpp
    Docs/ADLPanel.cpp

    # Panels (Console, ECS Inspector, Net Inspector)
    Panels/ConsolePanel.cpp
    Panels/ECSInspectorPanel.cpp
    Panels/NetInspectorPanel.cpp

    # EditorServices — AI backends
    EditorServices/AI/AIAggregator.cpp
    EditorServices/AI/LocalLLMBackend.cpp
    EditorServices/AI/TemplateAIBackend.cpp

    # Framework/UI — theme & widget registry
    Framework/UI/UIThemeManager.cpp
    Framework/UI/UIWidgetRegistry.cpp
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
             "${CMAKE_CURRENT_SOURCE_DIR}/Voxel"
             "${CMAKE_CURRENT_SOURCE_DIR}/PCG"
             "${CMAKE_CURRENT_SOURCE_DIR}/Prefabs"
             "${CMAKE_CURRENT_SOURCE_DIR}/AI"
             "${CMAKE_CURRENT_SOURCE_DIR}/Docs"
             "${CMAKE_CURRENT_SOURCE_DIR}/Panels"
             "${CMAKE_CURRENT_SOURCE_DIR}/EditorServices"
             "${CMAKE_CURRENT_SOURCE_DIR}/Framework/UI"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(AtlasEditor PUBLIC AtlasRuntime)

masterrepo_set_compiler_warnings(AtlasEditor)

message(STATUS "AtlasEditor: configured")
