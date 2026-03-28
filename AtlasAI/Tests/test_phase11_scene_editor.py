"""Tests for Phase 11 — Scene editor systems and editor panels/services/UI."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestSceneTypesFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_scene_types_header(self):
        self._check("Atlas/Engine/Scene/SceneTypes.h")

    def test_scene_node_header(self):
        self._check("Atlas/Engine/Scene/SceneNode.h")

    def test_scene_node_source(self):
        self._check("Atlas/Engine/Scene/SceneNode.cpp")

    def test_scene_graph_header(self):
        self._check("Atlas/Engine/Scene/SceneGraph.h")

    def test_scene_graph_source(self):
        self._check("Atlas/Engine/Scene/SceneGraph.cpp")

    def test_scene_manager_header(self):
        self._check("Atlas/Engine/Scene/SceneManager.h")

    def test_scene_manager_source(self):
        self._check("Atlas/Engine/Scene/SceneManager.cpp")


class TestSceneTypesContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Scene/SceneTypes.h").read_text(encoding="utf-8")

    def test_has_escenenodetype(self):
        self.assertIn("ESceneNodeType", self._read())

    def test_has_scene_transform(self):
        self.assertIn("SceneTransform", self._read())

    def test_has_scene_node_flags(self):
        self.assertIn("SceneNodeFlags", self._read())

    def test_has_static(self):
        self.assertIn("Static", self._read())

    def test_has_dynamic(self):
        self.assertIn("Dynamic", self._read())

    def test_has_light(self):
        self.assertIn("Light", self._read())


class TestSceneNodeContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Scene/SceneNode.h").read_text(encoding="utf-8")

    def test_has_class_scene_node(self):
        self.assertIn("class SceneNode", self._read())

    def test_has_add_child(self):
        self.assertIn("AddChild", self._read())

    def test_has_set_transform(self):
        self.assertIn("SetTransform", self._read())

    def test_has_is_visible(self):
        self.assertIn("IsVisible", self._read())

    def test_has_get_id(self):
        self.assertIn("GetId", self._read())


class TestSceneGraphContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Scene/SceneGraph.h").read_text(encoding="utf-8")

    def test_has_class_scene_graph(self):
        self.assertIn("class SceneGraph", self._read())

    def test_has_create_node(self):
        self.assertIn("CreateNode", self._read())

    def test_has_destroy_node(self):
        self.assertIn("DestroyNode", self._read())

    def test_has_find_node(self):
        self.assertIn("FindNode", self._read())

    def test_has_tick(self):
        self.assertIn("Tick", self._read())


class TestSceneManagerContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Scene/SceneManager.h").read_text(encoding="utf-8")

    def test_has_class_scene_manager(self):
        self.assertIn("class SceneManager", self._read())

    def test_has_load_scene(self):
        self.assertIn("LoadScene", self._read())

    def test_has_unload_scene(self):
        self.assertIn("UnloadScene", self._read())

    def test_has_get_active_graph(self):
        self.assertIn("GetActiveGraph", self._read())


class TestEditorPanelFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_console_panel_header(self):
        self._check("Atlas/Editor/Panels/ConsolePanel.h")

    def test_console_panel_source(self):
        self._check("Atlas/Editor/Panels/ConsolePanel.cpp")

    def test_ecs_inspector_panel_header(self):
        self._check("Atlas/Editor/Panels/ECSInspectorPanel.h")

    def test_ecs_inspector_panel_source(self):
        self._check("Atlas/Editor/Panels/ECSInspectorPanel.cpp")

    def test_net_inspector_panel_header(self):
        self._check("Atlas/Editor/Panels/NetInspectorPanel.h")

    def test_net_inspector_panel_source(self):
        self._check("Atlas/Editor/Panels/NetInspectorPanel.cpp")


class TestEditorServicesAIFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_ai_aggregator_header(self):
        self._check("Atlas/Editor/EditorServices/AI/AIAggregator.h")

    def test_ai_aggregator_source(self):
        self._check("Atlas/Editor/EditorServices/AI/AIAggregator.cpp")

    def test_local_llm_backend_header(self):
        self._check("Atlas/Editor/EditorServices/AI/LocalLLMBackend.h")

    def test_local_llm_backend_source(self):
        self._check("Atlas/Editor/EditorServices/AI/LocalLLMBackend.cpp")

    def test_template_ai_backend_header(self):
        self._check("Atlas/Editor/EditorServices/AI/TemplateAIBackend.h")

    def test_template_ai_backend_source(self):
        self._check("Atlas/Editor/EditorServices/AI/TemplateAIBackend.cpp")


class TestFrameworkUIFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_ui_theme_manager_header(self):
        self._check("Atlas/Editor/Framework/UI/UIThemeManager.h")

    def test_ui_theme_manager_source(self):
        self._check("Atlas/Editor/Framework/UI/UIThemeManager.cpp")

    def test_ui_widget_registry_header(self):
        self._check("Atlas/Editor/Framework/UI/UIWidgetRegistry.h")

    def test_ui_widget_registry_source(self):
        self._check("Atlas/Editor/Framework/UI/UIWidgetRegistry.cpp")


class TestFrameworkUIContent(unittest.TestCase):
    def _read_theme(self):
        return (REPO_ROOT / "Atlas/Editor/Framework/UI/UIThemeManager.h").read_text(encoding="utf-8")

    def _read_registry(self):
        return (REPO_ROOT / "Atlas/Editor/Framework/UI/UIWidgetRegistry.h").read_text(encoding="utf-8")

    def test_theme_manager_has_theme_config(self):
        self.assertIn("ThemeConfig", self._read_theme())

    def test_theme_manager_has_load_theme(self):
        self.assertIn("LoadTheme", self._read_theme())

    def test_theme_manager_has_apply_theme(self):
        self.assertIn("ApplyTheme", self._read_theme())

    def test_widget_registry_has_register(self):
        self.assertIn("Register", self._read_registry())

    def test_widget_registry_has_unregister(self):
        self.assertIn("Unregister", self._read_registry())


class TestSceneCMakeWired(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/CMakeLists.txt").read_text(encoding="utf-8")

    def test_scene_node_cpp_wired(self):
        self.assertIn("Scene/SceneNode.cpp", self._read())

    def test_scene_graph_cpp_wired(self):
        self.assertIn("Scene/SceneGraph.cpp", self._read())

    def test_scene_manager_cpp_wired(self):
        self.assertIn("Scene/SceneManager.cpp", self._read())


class TestEditorCMakeWired(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Editor/CMakeLists.txt").read_text(encoding="utf-8")

    def test_console_panel_cpp_wired(self):
        self.assertIn("Panels/ConsolePanel.cpp", self._read())

    def test_ai_aggregator_cpp_wired(self):
        self.assertIn("EditorServices/AI/AIAggregator.cpp", self._read())

    def test_ui_theme_manager_cpp_wired(self):
        self.assertIn("Framework/UI/UIThemeManager.cpp", self._read())


if __name__ == "__main__":
    unittest.main()
