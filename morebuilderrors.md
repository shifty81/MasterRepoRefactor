[log] Session started — 2026-03-29T04:33:33Z
[log] Log file: /c/GIT PROJECTS/MasterRepoRefactor/Logs/build/build_20260329_003333.log
================================================================
  MasterRepo Build
  Config  : Debug
  Jobs    : 8
  Tests   : OFF
  Bridge  : OFF
  BuildDir: /c/GIT PROJECTS/MasterRepoRefactor/Build
================================================================

──────────────────────────────────────────────────────────────
  [2026-03-29T04:33:33Z] CMake Configure
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
-- Configuring done (21.9s)
-- Generating done (0.5s)
-- Build files have been written to: C:/GIT PROJECTS/MasterRepoRefactor/Build

──────────────────────────────────────────────────────────────
  [2026-03-29T04:33:56Z] CMake Build
──────────────────────────────────────────────────────────────
[cmake] Building with 8 jobs ...
MSBuild version 17.14.40+3e7442088 for .NET Framework

  1>Checking Build System
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Build/_deps/glfw-src/src/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/Core/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Build/_deps/glm-src/glm/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Build/_deps/glew-src/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Server/CMakeLists.txt
  context.c
  AtlasCore_stub.cpp
  glm.cpp
  glew.c
  App.cpp
  init.c
  input.c
  AtlasCore.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Core\Debug\AtlasCore.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasTelemetryService/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Save/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasBuildService/CMakeLists.txt
  monitor.c
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasSessionService/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/Engine/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/UI/CMakeLists.txt
  AtlasTelemetryService.cpp
  AtlasBuildService.cpp
  libglew_static.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\_deps\glew-build\lib\Debug\glewd.lib
  AtlasSessionService.cpp
  platform.c
  AtlasEngine_stub.cpp
  Renderer.cpp
  RuntimeUIShell.cpp
  vulkan.c
  SaveManager.cpp
  window.c
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasWorldService/CMakeLists.txt
  egl_context.c
  AtlasBuildService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasBuildService\Debug\AtlasBuildService.lib
  osmesa_context.c
  HUDLayer.cpp
  AtlasWorldService.cpp
  RenderViewport.cpp
  glm.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\_deps\glm-build\glm\Debug\glm.lib
  AtlasTelemetryService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasTelemetryService\Debug\AtlasTelemetryService.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/UI/CMakeLists.txt
  null_init.c
  AtlasSessionService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasSessionService\Debug\AtlasSessionService.lib
  SaveSystem.cpp
  null_monitor.c
  EngineKernel.cpp
  null_window.c
  AtlasUI_stub.cpp
  InventoryScreen.cpp
  null_joystick.c
  AtlasWorldService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasWorldService\Debug\AtlasWorldService.lib
  AtlasUI.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\UI\Debug\AtlasUI.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Services/AtlasAssetService/CMakeLists.txt
  InputManager.cpp
  Generating Code...
  win32_module.c
  AtlasAssetService.cpp
  NovaForgeSave.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Save\Debug\NovaForgeSave.lib
  win32_time.c
  win32_thread.c
  ContractBoardUI.cpp
  win32_init.c
  InputContextManager.cpp
  AtlasAssetService.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\Services\AtlasAssetService\Debug\AtlasAssetService.lib
  win32_joystick.c
  win32_monitor.c
  StationTerminalUI.cpp
  win32_window.c
  AssetNamingRules.cpp
  GameOrchestrator.cpp
  Generating Code...
  Compiling...
  wgl_context.c
  Generating Code...
  FleetProgressionPanel.cpp
  AssetImportValidator.cpp
  glfw.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\_deps\glfw-build\src\Debug\glfw3.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Client/CMakeLists.txt
  audio_generator.cpp
  audio_manager.cpp
  character_animation_system.cpp
  DataRegistry.cpp
  Generating Code...
  PhysicsWorld.cpp
  NovaForgeUI.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\UI\Debug\NovaForgeUI.lib
  PhysicsExtensions.cpp
  character_mesh_system.cpp
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
  ContractBoardSystem.cpp
  AssetImportRules.cpp
  application_input.cpp
  CraftingSystem.cpp
  PCGDeterminismEngine.cpp
  EVAMovementController.cpp
  SchemaVersionRegistry.cpp
  application_movement.cpp
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
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/World/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Gameplay/CMakeLists.txt
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/Atlas/Runtime/CMakeLists.txt
  NovaForgeWorld_stub.cpp
  World.cpp
  NovaForgeGameplay_stub.cpp
  CombatSystem.cpp
  FleetSystem.cpp
  AtlasRuntime_stub.cpp
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
  InventorySystem.cpp
  PCGWorldGen.cpp
  PropertyInspector.cpp
  entity_message_parser.cpp
  ManufacturingSystem.cpp
  GizmoSystem.cpp
  ProgressionSystem.cpp
  MetaProgressionSystem.cpp
  CommandStack.cpp
  PlayerController.cpp
  BuilderSystem.cpp
  TransformCommand.cpp
  MiningSystem.cpp
  PropertyEditCommand.cpp
  SalvageSystem.cpp
  MissionSystem.cpp
  VoxelEditCommand.cpp
  file_logger.cpp
  StationServices.cpp
  PlayerController.cpp
  ValidationSystem.cpp
  ManufacturingQueue.cpp
  game_client.cpp
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
  Generating Code...
  session_manager.cpp
  PlacementSystem.cpp
  Compiling...
  StorageSystem.cpp
  ServiceTerminalSystem.cpp
  PrefabLibrary.cpp
  ProgressionRewardSystem.cpp
  ShipInteriorShell.cpp
  Generating Code...
  UnifiedDataRegistry.cpp
  Compiling...
  PrefabManager.cpp
  ShipProgressionSystem.cpp
  EditorDockLayout.cpp
  ship_physics.cpp
  TitanRaceSystem.cpp
  StationServiceSystem.cpp
  Generating Code...
  DiffReviewPanel.cpp
  AnomalySystem.cpp
  StorageSystem.cpp
  DesignDocPanel.cpp
  Compiling...
  solar_system_scene.cpp
  WarSectorSystem.cpp
  TetherController.cpp
  GameplayConnector.cpp
  FeatureChecklistPanel.cpp
  Generating Code...
  ContractRewardConnector.cpp
  editor_command_bus.cpp
  Compiling...
  TitanConstructionSystem.cpp
  ADLPanel.cpp
  MarketContractBridge.cpp
  editor_event_bus.cpp
  TradeSystem.cpp
  ConsolePanel.cpp
  editor_tool_layer.cpp
  scene_bookmark_manager.cpp
  CharacterSystem.cpp
  ECSInspectorPanel.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ConsolePanel.h(5,10): error C1083: Cannot open include file: '../../engine/sim/TickScheduler.h': No such file or directory [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  (compiling source file '../../../Atlas/Editor/Panels/ConsolePanel.cpp')
  
  UpgradeSystem.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  (compiling source file '../../../Atlas/Editor/Panels/ECSInspectorPanel.cpp')
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8): warning C4099: 'atlas::AtlasContext': type name first seen using 'class' now seen using 'struct' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  (compiling source file '../../../Atlas/Editor/Panels/ECSInspectorPanel.cpp')
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Framework\ui\EditorPanel.h(5,25):
      see declaration of 'atlas::AtlasContext'
  
  CharacterControllerShell.cpp
  WarSystem.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(38,28): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(38,21): error C2737: 'rowH': const object must be initialized [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(48,13): error C3861: 'panelBeginStateful': identifier not found [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(55,17): error C2660: 'atlas::textInput': function does not take 5 arguments [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(88,6):
      see declaration of 'atlas::textInput'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(55,17):
      while trying to match the argument list '(atlas::AtlasContext, const char [9], atlas::Rect, atlas::TextInputState, const char [19])'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(56,52): error C3867: 'atlas::TextInputState::text': non-standard syntax; use '&' to create a pointer to member [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(56,17): error C2679: binary '=': no operator found which takes a right-hand operand of type 'overloaded-function' (or there is no acceptable conversion) [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\xstring(3208,32):
      could be 'std::basic_string<char,std::char_traits<char>,std::allocator<char>> &std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator =(const _Elem)'
          with
          [
              _Elem=char
          ]
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\xstring(3200,32):
      or       'std::basic_string<char,std::char_traits<char>,std::allocator<char>> &std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator =(const _Elem *const )'
          with
          [
              _Elem=char
          ]
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\xstring(3150,32):
      or       'std::basic_string<char,std::char_traits<char>,std::allocator<char>> &std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator =(const std::basic_string<char,std::char_traits<char>,std::allocator<char>> &)'
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\xstring(3101,32):
      or       'std::basic_string<char,std::char_traits<char>,std::allocator<char>> &std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator =(std::initializer_list<_Elem>)'
          with
          [
              _Elem=char
          ]
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\xstring(2979,32):
      or       'std::basic_string<char,std::char_traits<char>,std::allocator<char>> &std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator =(std::basic_string<char,std::char_traits<char>,std::allocator<char>> &&) noexcept(<expr>)'
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\xstring(3195,32):
      or       'std::basic_string<char,std::char_traits<char>,std::allocator<char>> &std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator =(const _StringViewIsh &)'
          C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(56,17):
          'std::basic_string<char,std::char_traits<char>,std::allocator<char>> &std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator =(const _StringViewIsh &)': could not deduce template argument for '__formal'
              C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.33130\include\xstring(2396,9):
              'std::enable_if_t<false,int>' : Failed to specialize alias template
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(56,17):
      while trying to match the argument list '(std::string, overloaded-function)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(60,13): error C2660: 'atlas::separator': function does not take 3 arguments [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(95,6):
      see declaration of 'atlas::separator'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(60,13):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, float)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(86,21): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(86,55): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(91,46): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(92,17): error C2664: 'void atlas::label(atlas::AtlasContext &,atlas::Vec2,const char *,const atlas::Color &)': cannot convert argument 3 from 'std::string' to 'const char *' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(92,61):
      No user-defined-conversion operator available that can perform this conversion, or the operator cannot be called
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(93,6):
      see declaration of 'atlas::label'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(92,17):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, std::string, atlas::Color)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(95,21): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(95,48): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(103,13): error C2660: 'atlas::scrollbar': function does not take 5 arguments [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(98,6):
      see declaration of 'atlas::scrollbar'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(103,13):
      while trying to match the argument list '(atlas::AtlasContext, atlas::Rect, float, float, float)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(106,13): error C2660: 'atlas::separator': function does not take 3 arguments [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(95,6):
      see declaration of 'atlas::separator'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(106,13):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, float)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(111,13): error C2664: 'void atlas::label(atlas::AtlasContext &,atlas::Vec2,const char *,const atlas::Color &)': cannot convert argument 3 from 'std::string' to 'const char *' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(111,33):
      No user-defined-conversion operator available that can perform this conversion, or the operator cannot be called
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(93,6):
      see declaration of 'atlas::label'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(111,13):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, std::string)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(117,23): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(116,17): error C2664: 'void atlas::label(atlas::AtlasContext &,atlas::Vec2,const char *,const atlas::Color &)': cannot convert argument 3 from 'std::basic_string<char,std::char_traits<char>,std::allocator<char>>' to 'const char *' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(116,82):
      No user-defined-conversion operator available that can perform this conversion, or the operator cannot be called
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(93,6):
      see declaration of 'atlas::label'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(116,17):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, std::basic_string<char,std::char_traits<char>,std::allocator<char>>)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(122,64): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(127,59): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(127,25): error C2664: 'void atlas::label(atlas::AtlasContext &,atlas::Vec2,const char *,const atlas::Color &)': cannot convert argument 3 from 'std::string' to 'const char *' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(127,49):
      No user-defined-conversion operator available that can perform this conversion, or the operator cannot be called
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(93,6):
      see declaration of 'atlas::label'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(127,25):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, std::string)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(133,17): error C2660: 'atlas::separator': function does not take 3 arguments [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(95,6):
      see declaration of 'atlas::separator'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\ECSInspectorPanel.cpp(133,17):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, float)'
  
  NetInspectorPanel.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  (compiling source file '../../../Atlas/Editor/Panels/NetInspectorPanel.cpp')
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8): warning C4099: 'atlas::AtlasContext': type name first seen using 'class' now seen using 'struct' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  (compiling source file '../../../Atlas/Editor/Panels/NetInspectorPanel.cpp')
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Framework\ui\EditorPanel.h(5,25):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(24,17): error C2039: 'panelBeginStateful': is not a member of 'atlas' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(5,11):
      see declaration of 'atlas'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(24,17): error C3861: 'panelBeginStateful': identifier not found [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(29,27): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(29,17): error C2737: 'pad': const object must be initialized [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(30,27): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(30,17): error C2737: 'rowH': const object must be initialized [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(32,27): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(32,17): error C2737: 'headerH': const object must be initialized [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(36,68): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(36,12): error C2664: 'void atlas::label(atlas::AtlasContext &,atlas::Vec2,const char *,const atlas::Color &)': cannot convert argument 3 from 'std::basic_string<char,std::char_traits<char>,std::allocator<char>>' to 'const char *' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(36,48):
      No user-defined-conversion operator available that can perform this conversion, or the operator cannot be called
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(93,6):
      see declaration of 'atlas::label'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(36,12):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, std::basic_string<char,std::char_traits<char>,std::allocator<char>>)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(40,93): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(40,12): error C2664: 'void atlas::label(atlas::AtlasContext &,atlas::Vec2,const char *,const atlas::Color &)': cannot convert argument 3 from 'std::basic_string<char,std::char_traits<char>,std::allocator<char>>' to 'const char *' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(40,49):
      No user-defined-conversion operator available that can perform this conversion, or the operator cannot be called
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(93,6):
      see declaration of 'atlas::label'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(40,12):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, std::basic_string<char,std::char_traits<char>,std::allocator<char>>)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(47,9): error C2027: use of undefined type 'atlas::AtlasContext' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(22,8):
      see declaration of 'atlas::AtlasContext'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(44,12): error C2664: 'void atlas::label(atlas::AtlasContext &,atlas::Vec2,const char *,const atlas::Color &)': cannot convert argument 3 from 'std::basic_string<char,std::char_traits<char>,std::allocator<char>>' to 'const char *' [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(46,74):
      No user-defined-conversion operator available that can perform this conversion, or the operator cannot be called
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(93,6):
      see declaration of 'atlas::label'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(44,12):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, std::basic_string<char,std::char_traits<char>,std::allocator<char>>)'
  
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(50,12): error C2660: 'atlas::separator': function does not take 3 arguments [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\cpp_client\include\ui\atlas\atlas_widgets.h(95,6):
      see declaration of 'atlas::separator'
      C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\Panels\NetInspectorPanel.cpp(50,12):
      while trying to match the argument list '(atlas::AtlasContext, initializer list, float)'
  
  AIAggregator.cpp
  AnimationController.cpp
  WorldSimController.cpp
  undoable_command_bus.cpp
  LocalLLMBackend.cpp
  EquipmentSystem.cpp
  InputConfig.cpp
  network_manager.cpp
  InputRouter.cpp
  MechPossessionSystem.cpp
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\EditorServices\AI\LocalLLMBackend.cpp(322,28): error C2220: the following warning is treated as an error [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
C:\GIT PROJECTS\MasterRepoRefactor\Atlas\Editor\EditorServices\AI\LocalLLMBackend.cpp(322,28): warning C4996: 'getenv': This function or variable may be unsafe. Consider using _dupenv_s instead. To disable deprecation, use _CRT_SECURE_NO_WARNINGS. See online help for details. [C:\GIT PROJECTS\MasterRepoRefactor\Build\Atlas\Editor\AtlasEditor.vcxproj]
  IntegrationCoordinator.cpp
  TemplateAIBackend.cpp
  CharacterStateAuthority.cpp
  AIBridgeAdapter.cpp
  UIThemeManager.cpp
  TaskParserBridge.cpp
  CharacterTransitionRules.cpp
  UIWidgetRegistry.cpp
  LegacySourceClassifier.cpp
  AnimationLayerSystem.cpp
  Generating Code...
  protocol_handler.cpp
  DataConversionUtils.cpp
  IKSystem.cpp
  FactionAdapter.cpp
  ItemAdapter.cpp
  FPSPresentationSystem.cpp
  LegacyDataAdapter.cpp
  CharacterEditorSystem.cpp
  MissionAdapter.cpp
  ModuleAdapter.cpp
  Generating Code...
  tcp_client.cpp
  Compiling...
  ToolInteractionShell.cpp
  NovaForgeIngestionManifest.cpp
  RecipeAdapter.cpp
  Generating Code...
  CraftingBridgeAdapter.cpp
  NovaForgeGameplay.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Gameplay\Debug\NovaForgeGameplay.lib
  asteroid_field_renderer.cpp
  Generating Code...
  Compiling...
  InteractionBridgeAdapter.cpp
  InventoryBridgeAdapter.cpp
  camera.cpp
  ToolingBridgeAdapter.cpp
  WorkspaceBridgeAdapter.cpp
  damage_effect_helper.cpp
  ModuleRegistry.cpp
  frustum_culler.cpp
  ModuleSubsystem.cpp
  gbuffer.cpp
  AsteroidFieldGenerator.cpp
  healthbar_renderer.cpp
  DerelictGenerator.cpp
  Renderer.cpp
  instanced_renderer.cpp
  SaveManager.cpp
  lighting.cpp
  ToolingSubsystem.cpp
  RuntimeHUDController.cpp
  lod_manager.cpp
  RuntimeHUDRenderer.cpp
  mesh.cpp
  RuntimeUIHooks.cpp
  model.cpp
  VerticalSliceUI.cpp
  StructureRegistry.cpp
  VoxelSubsystem.cpp
  SystemScheduler.cpp
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
  reference_model_analyzer.cpp
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
  NovaForgeClient.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\Debug\NovaForgeClient.lib
  Building Custom Rule C:/GIT PROJECTS/MasterRepoRefactor/NovaForge/Client/CMakeLists.txt
  main.cpp
  NovaForgeClientApp.vcxproj -> C:\GIT PROJECTS\MasterRepoRefactor\Build\NovaForge\Client\Debug\NovaForgeClientApp.exe
