[log] Session started — 2026-03-29T04:11:09Z
[log] Log file: /c/GIT PROJECTS/MasterRepoRefactor/Logs/build/build_20260329_001109.log
================================================================
  MasterRepo Build
  Config  : Debug
  Jobs    : 8
  Tests   : OFF
  Bridge  : OFF
  BuildDir: /c/GIT PROJECTS/MasterRepoRefactor/Build
================================================================

──────────────────────────────────────────────────────────────
  [2026-03-29T04:11:09Z] CMake Configure
──────────────────────────────────────────────────────────────
[cmake] Configuring ...
-- Building for: Visual Studio 17 2022
-- Selecting Windows SDK version 10.0.26100.0 to target Windows 10.0.19045.
-- The CXX compiler identification is MSVC 19.38.33145.0
-- The C compiler identification is MSVC 19.38.33145.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x64/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x64/cl.exe - skipped
-- Detecting C compile features
-- Detecting C compile features - done
CMake Deprecation Warning at Build/_deps/glm-src/CMakeLists.txt:1 (cmake_minimum_required):
  Compatibility with CMake < 3.10 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
  to tell CMake that the project requires at least <min> but has been updated
  to work with policies introduced by <max> or earlier.


CMake Deprecation Warning at Build/_deps/glm-src/CMakeLists.txt:2 (cmake_policy):
  Compatibility with CMake < 3.10 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
  to tell CMake that the project requires at least <min> but has been updated
  to work with policies introduced by <max> or earlier.


-- GLM: Version 1.0.1
-- GLM: Build with C++ features auto detection
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - not found
-- Found Threads: TRUE
-- Including Win32 support
CMake Deprecation Warning at Build/_deps/glew-src/CMakeLists.txt:1 (cmake_minimum_required):
  Compatibility with CMake < 3.10 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
  to tell CMake that the project requires at least <min> but has been updated
  to work with policies introduced by <max> or earlier.


-- Found OpenGL: opengl32
-- Shared: AtlasBridgeContract configured
-- Shared: MasterLogger (header-only) configured
-- AtlasCore: configured
-- AtlasEngine: configured
-- AtlasRuntime: configured
-- AtlasEditor: configured
-- AtlasUI: configured
-- Atlas: modules configured
-- NovaForgeGameplay: configured
-- NovaForgeWorld: configured
-- NovaForgeSave: configured
-- NovaForgeUI: configured
-- NovaForgeApp: configured
-- NovaForge Client: configured
-- NovaForge Server: configured
-- NovaForge: modules configured
-- AtlasBuildService: configured
-- AtlasAssetService: configured
-- AtlasWorldService: configured
-- AtlasSessionService: configured
-- AtlasTelemetryService: configured
-- Services: configured
-- Configuring done (23.3s)
-- Generating done (0.5s)
-- Build files have been written to: C:/GIT PROJECTS/MasterRepoRefactor/Build

──────────────────────────────────────────────────────────────
  [2026-03-29T04:11:33Z] CMake Build
──────────────────────────────────────────────────────────────
[cmake] Building with 8 jobs ...
MSBuild version 17.14.40+3e7442088 for .NET Framework

  1>Checking Build System
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Build/_deps/glfw-src/src/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Build/_deps/glm-src/glm/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Build/_deps/glew-src/CMakeLists.txt
  context.c
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Server/CMakeLists.txt
  glm.cpp
  glew.c
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/Core/CMakeLists.txt
  AtlasCore_stub.cpp
  App.cpp
  init.c
  input.c
  monitor.c
  AtlasCore.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Core\Debug\AtlasCore.lib
  libglew_static.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\_deps\glew-build\lib\Debug\glewd.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Save/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/Engine/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasTelemetryService/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasSessionService/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/UI/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasBuildService/CMakeLists.txt
  platform.c
  RuntimeUIShell.cpp
  AtlasBuildService.cpp
  AtlasEngine_stub.cpp
  AtlasSessionService.cpp
  AtlasTelemetryService.cpp
  SaveManager.cpp
  Renderer.cpp
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasWorldService/CMakeLists.txt
  vulkan.c
  window.c
  egl_context.c
  AtlasWorldService.cpp
  osmesa_context.c
  HUDLayer.cpp
  SaveSystem.cpp
  null_init.c
  glm.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\_deps\glm-build\glm\Debug\glm.lib
  AtlasBuildService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasBuildService\Debug\AtlasBuildService.lib
  RenderViewport.cpp
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/UI/CMakeLists.txt
  null_monitor.c
  AtlasTelemetryService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasTelemetryService\Debug\AtlasTelemetryService.lib
  AtlasUI_stub.cpp
  AtlasSessionService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasSessionService\Debug\AtlasSessionService.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasAssetService/CMakeLists.txt
  null_window.c
  AtlasAssetService.cpp
  Generating Code...
  AtlasUI.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\UI\Debug\AtlasUI.lib
  EngineKernel.cpp
  InventoryScreen.cpp
  null_joystick.c
  AtlasWorldService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasWorldService\Debug\AtlasWorldService.lib
  NovaForgeSave.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Save\Debug\NovaForgeSave.lib
  win32_module.c
  InputManager.cpp
  win32_time.c
  AtlasAssetService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasAssetService\Debug\AtlasAssetService.lib
  win32_thread.c
  ContractBoardUI.cpp
  win32_init.c
  win32_joystick.c
  InputContextManager.cpp
  win32_monitor.c
  StationTerminalUI.cpp
  win32_window.c
  Generating Code...
  AssetNamingRules.cpp
  GameOrchestrator.cpp
  Compiling...
  wgl_context.c
  Generating Code...
  FleetProgressionPanel.cpp
  glfw.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\_deps\glfw-build\src\Debug\glfw3.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Client/CMakeLists.txt
  AssetImportValidator.cpp
  audio_generator.cpp
  audio_manager.cpp
  character_animation_system.cpp
  DataRegistry.cpp
  Generating Code...
  PhysicsWorld.cpp
  NovaForgeUI.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\UI\Debug\NovaForgeUI.lib
  character_mesh_system.cpp
  PhysicsExtensions.cpp
  AudioEngine.cpp
  equipment_attachment_system.cpp
  DevOverlayState.cpp
  AudioSystem.cpp
  fps_hand_system.cpp
  ComponentRegistry.cpp
  NetSession.cpp
  application.cpp
  EntityRegistry.cpp
  ScriptingVM.cpp
  VerticalSliceBootstrap.cpp
  KeybindConfig.cpp
  AirlockController.cpp
  application_entities.cpp
  SaveLoadExtensions.cpp
  AnomalySystem.cpp
  AssetImportRules.cpp
  ContractBoardSystem.cpp
  application_input.cpp
  CraftingSystem.cpp
  PCGDeterminismEngine.cpp
  EVAMovementController.cpp
  application_movement.cpp
  SchemaVersionRegistry.cpp
  EVATransitionController.cpp
  EconomySystem.cpp
  SceneNode.cpp
  application_rendering.cpp
  SceneGraph.cpp
  EndgameGateSystem.cpp
  Generating Code...
  SurvivalController.cpp
  Compiling...
  SceneManager.cpp
  application_state.cpp
  FactionSystem.cpp
  Generating Code...
  AtlasEngine.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Engine\Debug\AtlasEngine.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Gameplay/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/Runtime/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/World/CMakeLists.txt
  AtlasRuntime_stub.cpp
  NovaForgeWorld_stub.cpp
  NovaForgeGameplay_stub.cpp
  World.cpp
  CombatSystem.cpp
  FleetSystem.cpp
  AtlasRuntime.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Runtime\Debug\AtlasRuntime.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/Editor/CMakeLists.txt
  AtlasEditor_stub.cpp
  EditorShell.cpp
  TradeMarket.cpp
  Generating Code...
  NovaForgeWorld.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\World\Debug\NovaForgeWorld.lib
  GameplayManager.cpp
  ResourceRegistry.cpp
  EditorModeController.cpp
  embedded_server.cpp
  LootResolver.cpp
  Generating Code...
  EditorInputRouter.cpp
  Compiling...
  GameplaySessionController.cpp
  FactionRegistry.cpp
  EditorCameraController.cpp
  ExteriorInteractionSystem.cpp
  entity.cpp
  MissionRegistry.cpp
  SelectionSystem.cpp
  InteractionSystem.cpp
  MiningSystem.cpp
  entity_manager.cpp
  SceneOutliner.cpp
  ExplorationSystem.cpp
  InteriorInteractionSystem.cpp
  PCGWorldGen.cpp
  InventorySystem.cpp
  PropertyInspector.cpp
  entity_message_parser.cpp
  GizmoSystem.cpp
  ManufacturingSystem.cpp
  ProgressionSystem.cpp
  CommandStack.cpp
  PlayerController.cpp
  MetaProgressionSystem.cpp
  BuilderSystem.cpp
  TransformCommand.cpp
  MiningSystem.cpp
  PropertyEditCommand.cpp
  SalvageSystem.cpp
  MissionSystem.cpp
  file_logger.cpp
  VoxelEditCommand.cpp
  StationServices.cpp
  ValidationSystem.cpp
  PlayerController.cpp
  game_client.cpp
  ManufacturingQueue.cpp
  VoxelChunkEditor.cpp
  ProgressionSystem.cpp
  ContractRewardSystem.cpp
  VoxelEditorMode.cpp
  FleetSystem.cpp
  SalvageSystem.cpp
  WorldSimSystem.cpp
  PCGDebugSystem.cpp
  SeasonResetSystem.cpp
  InventorySystem.cpp
  SceneHierarchySystem.cpp
  SectorSystem.cpp
  session_manager.cpp
  Generating Code...
  PlacementSystem.cpp
  Compiling...
  StorageSystem.cpp
  ServiceTerminalSystem.cpp
  PrefabLibrary.cpp
  ProgressionRewardSystem.cpp
  ShipInteriorShell.cpp
  Generating Code...
  Compiling...
  PrefabManager.cpp
  UnifiedDataRegistry.cpp
  ShipProgressionSystem.cpp
  ship_physics.cpp
  EditorDockLayout.cpp
  TitanRaceSystem.cpp
  StationServiceSystem.cpp
C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\core\ship_physics.cpp(373,11): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\core\ship_physics.cpp(373,11): warning C4189: 'currentSpeed': local variable is initialized but not referenced [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  Generating Code...
  DiffReviewPanel.cpp
  AnomalySystem.cpp
  StorageSystem.cpp
  Compiling...
  solar_system_scene.cpp
  DesignDocPanel.cpp
  WarSectorSystem.cpp
  TetherController.cpp
  FeatureChecklistPanel.cpp
  GameplayConnector.cpp
  Generating Code...
  editor_command_bus.cpp
  ContractRewardConnector.cpp
  Compiling...
  TitanConstructionSystem.cpp
  ADLPanel.cpp
  editor_event_bus.cpp
  MarketContractBridge.cpp
  ConsolePanel.cpp
  TradeSystem.cpp
  editor_tool_layer.cpp
  scene_bookmark_manager.cpp
  ECSInspectorPanel.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ConsolePanel.h(4,10): error C1083: Cannot open include file: '../../engine/net/NetContext.h': No such file or directory [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  (compiling source file '../../../Atlas/Editor/Panels/ConsolePanel.cpp')
  
  CharacterSystem.cpp
  UpgradeSystem.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.h(4,10): error C1083: Cannot open include file: '../../cpp_client/include/ui/atlas/atlas_widgets.h': No such file or directory [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  (compiling source file '../../../Atlas/Editor/Panels/ECSInspectorPanel.cpp')
  
  NetInspectorPanel.cpp
  CharacterControllerShell.cpp
  WarSystem.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.h(3,10): error C1083: Cannot open include file: '../../engine/net/NetContext.h': No such file or directory [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  (compiling source file '../../../Atlas/Editor/Panels/NetInspectorPanel.cpp')
  
  AIAggregator.cpp
  LocalLLMBackend.cpp
  undoable_command_bus.cpp
  AnimationController.cpp
  WorldSimController.cpp
  network_manager.cpp
  EquipmentSystem.cpp
  InputConfig.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\EditorServices\AI\LocalLLMBackend.cpp(322,28): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\EditorServices\AI\LocalLLMBackend.cpp(322,28): warning C4996: 'getenv': This function or variable may be unsafe. Consider using _dupenv_s instead. To disable deprecation, use _CRT_SECURE_NO_WARNINGS. See online help for details. [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  TemplateAIBackend.cpp
  InputRouter.cpp
  MechPossessionSystem.cpp
  IntegrationCoordinator.cpp
  UIThemeManager.cpp
  CharacterStateAuthority.cpp
  AIBridgeAdapter.cpp
  UIWidgetRegistry.cpp
  TaskParserBridge.cpp
  CharacterTransitionRules.cpp
  Generating Code...
  LegacySourceClassifier.cpp
  AnimationLayerSystem.cpp
  protocol_handler.cpp
  DataConversionUtils.cpp
  IKSystem.cpp
  FactionAdapter.cpp
  ItemAdapter.cpp
  FPSPresentationSystem.cpp
  LegacyDataAdapter.cpp
  CharacterEditorSystem.cpp
  MissionAdapter.cpp
  tcp_client.cpp
  ModuleAdapter.cpp
  Generating Code...
  NovaForgeIngestionManifest.cpp
  Compiling...
  ToolInteractionShell.cpp
  RecipeAdapter.cpp
  Generating Code...
  asteroid_field_renderer.cpp
  CraftingBridgeAdapter.cpp
  NovaForgeGameplay.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Gameplay\Debug\NovaForgeGameplay.lib
  Generating Code...
  Compiling...
  InteractionBridgeAdapter.cpp
C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\rendering\asteroid_field_renderer.cpp(343,73): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\rendering\asteroid_field_renderer.cpp(343,73): warning C4267: '=': conversion from 'size_t' to 'int', possible loss of data [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  InventoryBridgeAdapter.cpp
  camera.cpp
  ToolingBridgeAdapter.cpp
  damage_effect_helper.cpp
  WorkspaceBridgeAdapter.cpp
  ModuleRegistry.cpp
  frustum_culler.cpp
  ModuleSubsystem.cpp
  gbuffer.cpp
  AsteroidFieldGenerator.cpp
  healthbar_renderer.cpp
  DerelictGenerator.cpp
  instanced_renderer.cpp
  Renderer.cpp
  SaveManager.cpp
  lighting.cpp
  ToolingSubsystem.cpp
  lod_manager.cpp
  RuntimeHUDController.cpp
  RuntimeHUDRenderer.cpp
  mesh.cpp
  RuntimeUIHooks.cpp
  model.cpp
  VerticalSliceUI.cpp
  StructureRegistry.cpp
  VoxelSubsystem.cpp
  SystemScheduler.cpp
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  (compiling source file '../../../NovaForge/Client/App/src/rendering/model.cpp')
  
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24): warning C4244: '=': conversion from 'int' to 'char', possible loss of data [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  (compiling source file '../../../NovaForge/Client/App/src/rendering/model.cpp')
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24):
      the template instantiation context (the oldest one first) is
          C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\rendering\model.cpp(60,14):
          see reference to function template instantiation '_OutIt std::transform<std::_String_iterator<std::_String_val<std::_Simple_types<_Elem>>>,std::_String_iterator<std::_String_val<std::_Simple_types<_Elem>>>,int(__cdecl *)(int)>(const _InIt,const _InIt,_OutIt,_Fn)' being compiled
          with
          [
              _OutIt=std::_String_iterator<std::_String_val<std::_Simple_types<char>>>,
              _Elem=char,
              _InIt=std::_String_iterator<std::_String_val<std::_Simple_types<char>>>,
              _Fn=int (__cdecl *)(int)
          ]
  
  World.cpp
  Generating Code...
  Generating Code...
  NovaForgeServer.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Server\Debug\NovaForgeServer.lib
  Compiling...
  particle_system.cpp
  pbr_materials.cpp
  post_processing.cpp
  procedural_mesh_ops.cpp
  procedural_ship_generator.cpp
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  (compiling source file '../../../NovaForge/Client/App/src/rendering/procedural_ship_generator.cpp')
  
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24): warning C4244: '=': conversion from 'int' to 'char', possible loss of data [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  (compiling source file '../../../NovaForge/Client/App/src/rendering/procedural_ship_generator.cpp')
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24):
      the template instantiation context (the oldest one first) is
          C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\rendering\procedural_ship_generator.cpp(901,10):
          see reference to function template instantiation '_OutIt std::transform<std::_String_iterator<std::_String_val<std::_Simple_types<_Elem>>>,std::_String_iterator<std::_String_val<std::_Simple_types<_Elem>>>,int(__cdecl *)(int)>(const _InIt,const _InIt,_OutIt,_Fn)' being compiled
          with
          [
              _OutIt=std::_String_iterator<std::_String_val<std::_Simple_types<char>>>,
              _Elem=char,
              _InIt=std::_String_iterator<std::_String_val<std::_Simple_types<char>>>,
              _Fn=int (__cdecl *)(int)
          ]
  
  reference_model_analyzer.cpp
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  (compiling source file '../../../NovaForge/Client/App/src/rendering/reference_model_analyzer.cpp')
  
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24): warning C4244: '=': conversion from 'int' to 'char', possible loss of data [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  (compiling source file '../../../NovaForge/Client/App/src/rendering/reference_model_analyzer.cpp')
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\algorithm(3456,24):
      the template instantiation context (the oldest one first) is
          C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\rendering\reference_model_analyzer.cpp(144,10):
          see reference to function template instantiation '_OutIt std::transform<std::_String_iterator<std::_String_val<std::_Simple_types<_Elem>>>,std::_String_iterator<std::_String_val<std::_Simple_types<_Elem>>>,int(__cdecl *)(int)>(const _InIt,const _InIt,_OutIt,_Fn)' being compiled
          with
          [
              _OutIt=std::_String_iterator<std::_String_val<std::_Simple_types<char>>>,
              _Elem=char,
              _InIt=std::_String_iterator<std::_String_val<std::_Simple_types<char>>>,
              _Fn=int (__cdecl *)(int)
          ]
  
  renderer.cpp
  resolution_manager.cpp
  shader.cpp
  shadow_map.cpp
  ship_generation_rules.cpp
  ship_part_library.cpp
  station_renderer.cpp
  texture.cpp
  visual_effects.cpp
  warp_effect_renderer.cpp
  window.cpp
  atlas_console.cpp
  atlas_context.cpp
  atlas_hud.cpp
  Generating Code...
C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\rendering\station_renderer.cpp(535): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\NovaForge\Client\App\src\rendering\station_renderer.cpp(535): warning C4701: potentially uninitialized local variable 'normal' used [C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\NovaForgeClient.vcxproj]
  Compiling...
  atlas_pause_menu.cpp
  atlas_renderer.cpp
  atlas_title_screen.cpp
  atlas_widgets.cpp
  atlas_widgets_cards.cpp
  atlas_widgets_effects.cpp
  atlas_widgets_forms.cpp
  atlas_widgets_hud.cpp
  atlas_widgets_lists.cpp
  atlas_widgets_menus.cpp
  atlas_widgets_panels.cpp
  atlas_widgets_sidebar.cpp
  context_menu.cpp
  entity_picker.cpp
  input_handler.cpp
  layout_manager.cpp
  radial_menu.cpp
  rml_ui_manager.cpp
  star_map.cpp
  Generating Code...
