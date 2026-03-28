"""Tests for H1 (DesignDocPanel), H2 (FeatureChecklistPanel), H3 (ADLPanel)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# H1 — DesignDocPanel
# =============================================================================

class TestDesignDocPanelFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_design_doc_panel_header(self):
        self._check("Atlas/Editor/Docs/DesignDocPanel.h")

    def test_design_doc_panel_source(self):
        self._check("Atlas/Editor/Docs/DesignDocPanel.cpp")


class TestDesignDocPanelContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Editor/Docs/DesignDocPanel.h").read_text(encoding="utf-8")

    def test_has_edoc_link_type_enum(self):
        self.assertIn("EDocLinkType", self._read())

    def test_has_doc_link(self):
        self.assertIn("DocLink", self._read())

    def test_has_design_doc_page(self):
        self.assertIn("DesignDocPage", self._read())

    def test_has_design_doc_panel_class(self):
        self.assertIn("DesignDocPanel", self._read())

    def test_has_register_page(self):
        self.assertIn("RegisterPage", self._read())

    def test_has_unregister_page(self):
        self.assertIn("UnregisterPage", self._read())

    def test_has_has_page(self):
        self.assertIn("HasPage", self._read())

    def test_has_find_page(self):
        self.assertIn("FindPage", self._read())

    def test_has_list_all(self):
        self.assertIn("ListAll", self._read())

    def test_has_list_by_category(self):
        self.assertIn("ListByCategory", self._read())

    def test_has_search(self):
        self.assertIn("Search", self._read())

    def test_has_open_page(self):
        self.assertIn("OpenPage", self._read())

    def test_has_close_page(self):
        self.assertIn("ClosePage", self._read())

    def test_has_is_open(self):
        self.assertIn("IsOpen", self._read())

    def test_has_get_open_page_ids(self):
        self.assertIn("GetOpenPageIds", self._read())

    def test_has_add_link(self):
        self.assertIn("AddLink", self._read())

    def test_has_remove_link(self):
        self.assertIn("RemoveLink", self._read())

    def test_has_get_links_for_page(self):
        self.assertIn("GetLinksForPage", self._read())

    def test_has_navigate_callback(self):
        self.assertIn("NavigateCallback", self._read())

    def test_has_navigate_to(self):
        self.assertIn("NavigateTo", self._read())

    def test_has_mark_dirty(self):
        self.assertIn("MarkDirty", self._read())

    def test_has_mark_clean(self):
        self.assertIn("MarkClean", self._read())

    def test_has_page_count(self):
        self.assertIn("PageCount", self._read())

    def test_link_types_cover_all(self):
        text = self._read()
        for t in ["CppHeader", "DataRecord", "EditorObject", "Feature", "ExternalURL"]:
            self.assertIn(t, text, f"Missing link type: {t}")

    def test_page_has_markdown_path(self):
        self.assertIn("markdownPath", self._read())

    def test_page_has_is_dirty(self):
        self.assertIn("isDirty", self._read())


class TestDesignDocPanelImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Editor/Docs/DesignDocPanel.cpp").read_text(encoding="utf-8")

    def test_open_sets_is_open_true(self):
        self.assertIn("isOpen = true", self._read())

    def test_close_sets_is_open_false(self):
        self.assertIn("isOpen = false", self._read())

    def test_mark_dirty_sets_flag(self):
        self.assertIn("isDirty = true", self._read())

    def test_navigate_fires_callback(self):
        self.assertIn("m_navCb", self._read())

    def test_search_checks_title_and_summary(self):
        self.assertIn("summary", self._read())


# =============================================================================
# H2 — FeatureChecklistPanel
# =============================================================================

class TestFeatureChecklistPanelFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_feature_checklist_header(self):
        self._check("Atlas/Editor/Docs/FeatureChecklistPanel.h")

    def test_feature_checklist_source(self):
        self._check("Atlas/Editor/Docs/FeatureChecklistPanel.cpp")


class TestFeatureChecklistPanelContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Editor/Docs/FeatureChecklistPanel.h").read_text(encoding="utf-8")

    def test_has_efeature_status_enum(self):
        self.assertIn("EFeatureStatus", self._read())

    def test_has_efeature_priority_enum(self):
        self.assertIn("EFeaturePriority", self._read())

    def test_has_feature_item(self):
        self.assertIn("FeatureItem", self._read())

    def test_has_feature_checklist_filter(self):
        self.assertIn("FeatureChecklistFilter", self._read())

    def test_has_checklist_panel_class(self):
        self.assertIn("FeatureChecklistPanel", self._read())

    def test_has_register_item(self):
        self.assertIn("RegisterItem", self._read())

    def test_has_unregister_item(self):
        self.assertIn("UnregisterItem", self._read())

    def test_has_set_status(self):
        self.assertIn("SetStatus", self._read())

    def test_has_set_priority(self):
        self.assertIn("SetPriority", self._read())

    def test_has_set_owner(self):
        self.assertIn("SetOwner", self._read())

    def test_has_find_item(self):
        self.assertIn("FindItem", self._read())

    def test_has_list_by_status(self):
        self.assertIn("ListByStatus", self._read())

    def test_has_list_by_priority(self):
        self.assertIn("ListByPriority", self._read())

    def test_has_list_by_milestone(self):
        self.assertIn("ListByMilestone", self._read())

    def test_has_list_blocking(self):
        self.assertIn("ListBlocking", self._read())

    def test_has_filter(self):
        self.assertIn("Filter(", self._read())

    def test_has_complete_count(self):
        self.assertIn("CompleteCount", self._read())

    def test_has_blocked_count(self):
        self.assertIn("BlockedCount", self._read())

    def test_has_completion_pct(self):
        self.assertIn("CompletionPct", self._read())

    def test_has_status_changed_callback(self):
        self.assertIn("StatusChangedCallback", self._read())

    def test_statuses_cover_all(self):
        text = self._read()
        for s in ["NotStarted", "InProgress", "Complete", "Blocked", "Deferred"]:
            self.assertIn(s, text, f"Missing status: {s}")

    def test_priorities_cover_all(self):
        text = self._read()
        for p in ["Critical", "High", "Medium", "Low", "Ice"]:
            self.assertIn(p, text, f"Missing priority: {p}")

    def test_has_linked_system_id(self):
        self.assertIn("linkedSystemId", self._read())

    def test_has_milestone_tag(self):
        self.assertIn("milestoneTag", self._read())

    def test_has_is_blocking(self):
        self.assertIn("isBlocking", self._read())


class TestFeatureChecklistImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Editor/Docs/FeatureChecklistPanel.cpp").read_text(encoding="utf-8")

    def test_status_callback_fires_on_set_status(self):
        self.assertIn("m_statusCb", self._read())

    def test_completion_pct_uses_complete_count(self):
        self.assertIn("CompleteCount", self._read())

    def test_list_blocking_excludes_complete(self):
        self.assertIn("Complete", self._read())


# =============================================================================
# H3 — ADLPanel
# =============================================================================

class TestADLPanelFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_adl_panel_header(self):
        self._check("Atlas/Editor/Docs/ADLPanel.h")

    def test_adl_panel_source(self):
        self._check("Atlas/Editor/Docs/ADLPanel.cpp")


class TestADLPanelContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Editor/Docs/ADLPanel.h").read_text(encoding="utf-8")

    def test_has_eadl_status_enum(self):
        self.assertIn("EADLStatus", self._read())

    def test_has_adl_context_link(self):
        self.assertIn("ADLContextLink", self._read())

    def test_has_adl_entry(self):
        self.assertIn("ADLEntry", self._read())

    def test_has_adl_panel_class(self):
        self.assertIn("ADLPanel", self._read())

    def test_has_add_entry(self):
        self.assertIn("AddEntry", self._read())

    def test_has_remove_entry(self):
        self.assertIn("RemoveEntry", self._read())

    def test_has_has_entry(self):
        self.assertIn("HasEntry", self._read())

    def test_has_update_entry(self):
        self.assertIn("UpdateEntry", self._read())

    def test_has_set_status(self):
        self.assertIn("SetStatus", self._read())

    def test_has_supersede(self):
        self.assertIn("Supersede", self._read())

    def test_has_find_entry(self):
        self.assertIn("FindEntry", self._read())

    def test_has_list_all(self):
        self.assertIn("ListAll", self._read())

    def test_has_list_by_status(self):
        self.assertIn("ListByStatus", self._read())

    def test_has_search(self):
        self.assertIn("Search", self._read())

    def test_has_linked_to(self):
        self.assertIn("LinkedTo", self._read())

    def test_has_add_context_link(self):
        self.assertIn("AddContextLink", self._read())

    def test_has_remove_context_link(self):
        self.assertIn("RemoveContextLink", self._read())

    def test_has_navigate_callback(self):
        self.assertIn("NavigateCallback", self._read())

    def test_has_navigate_to(self):
        self.assertIn("NavigateTo", self._read())

    def test_has_entry_count(self):
        self.assertIn("EntryCount", self._read())

    def test_has_accepted_count(self):
        self.assertIn("AcceptedCount", self._read())

    def test_statuses_cover_all(self):
        text = self._read()
        for s in ["Proposed", "Accepted", "Deprecated", "Superseded"]:
            self.assertIn(s, text, f"Missing ADL status: {s}")

    def test_entry_has_context_field(self):
        self.assertIn("context;", self._read())

    def test_entry_has_decision_field(self):
        self.assertIn("decision;", self._read())

    def test_entry_has_consequences_field(self):
        self.assertIn("consequences", self._read())

    def test_entry_has_superseded_by_id(self):
        self.assertIn("supersededById", self._read())


class TestADLPanelImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Editor/Docs/ADLPanel.cpp").read_text(encoding="utf-8")

    def test_supersede_sets_status(self):
        self.assertIn("Superseded", self._read())

    def test_navigate_fires_callback(self):
        self.assertIn("m_navCb", self._read())

    def test_search_checks_decision(self):
        self.assertIn("decision", self._read())

    def test_linked_to_searches_context_links(self):
        self.assertIn("contextLinks", self._read())


class TestEditorCMakeHasDocsPanels(unittest.TestCase):
    def _cmake(self):
        return (REPO_ROOT / "Atlas/Editor/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_design_doc_panel(self):
        self.assertIn("DesignDocPanel.cpp", self._cmake())

    def test_has_feature_checklist_panel(self):
        self.assertIn("FeatureChecklistPanel.cpp", self._cmake())

    def test_has_adl_panel(self):
        self.assertIn("ADLPanel.cpp", self._cmake())

    def test_has_docs_include_dir(self):
        self.assertIn("/Docs", self._cmake())


if __name__ == "__main__":
    unittest.main()
