"""AtlasAI Phase 40B — Data Validator Pipeline.

Manages validation rule entries, results, and reports
for the DataValidatorTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ValidationRuleEntry:
    """A validation rule definition."""
    rule_id: str
    rule_name: str
    rule_type: str = "Schema"
    scope: str = "Asset"
    severity: str = "Error"
    expr: str = ""
    enabled: bool = True

    @property
    def is_schema(self) -> bool:
        return self.rule_type == "Schema"

    @property
    def is_critical(self) -> bool:
        return self.severity == "Critical"

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def has_expr(self) -> bool:
        return bool(self.expr)

    @property
    def is_error(self) -> bool:
        return self.severity in ("Error", "Critical")


@dataclass
class ValidationResultEntry:
    """A validation result record."""
    result_id: str
    rule_id: str
    asset_id: str = ""
    severity: str = "Error"
    message: str = ""
    passed: bool = False

    @property
    def is_passed(self) -> bool:
        return self.passed

    @property
    def is_failed(self) -> bool:
        return not self.passed

    @property
    def is_error(self) -> bool:
        return self.severity == "Error"

    @property
    def is_warning(self) -> bool:
        return self.severity == "Warning"

    @property
    def is_critical(self) -> bool:
        return self.severity == "Critical"

    @property
    def has_message(self) -> bool:
        return bool(self.message)


@dataclass
class ValidationReportEntry:
    """A validation report entry."""
    report_id: str
    asset_id: str = ""
    state: str = "Pending"
    result_ids: list = field(default_factory=list)
    error_count: int = 0
    warning_count: int = 0

    @property
    def is_passed(self) -> bool:
        return self.state == "Passed"

    @property
    def is_failed(self) -> bool:
        return self.state == "Failed"

    @property
    def is_pending(self) -> bool:
        return self.state == "Pending"

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    @property
    def has_warnings(self) -> bool:
        return self.warning_count > 0

    @property
    def total_issues(self) -> int:
        return self.error_count + self.warning_count


class DataValidatorPipeline:
    """Pipeline managing data validation rules, results, and reports."""

    def __init__(self) -> None:
        self._rules: Dict[str, ValidationRuleEntry] = {}
        self._results: Dict[str, Dict[str, ValidationResultEntry]] = {}
        self._reports: Dict[str, Dict[str, ValidationReportEntry]] = {}

    def add_rule(self, entry: ValidationRuleEntry) -> bool:
        if not entry.rule_id:
            return False
        self._rules[entry.rule_id] = entry
        if entry.rule_id not in self._results:
            self._results[entry.rule_id] = {}
        return True

    def get_rule(self, rule_id: str) -> Optional[ValidationRuleEntry]:
        return self._rules.get(rule_id)

    def remove_rule(self, rule_id: str) -> bool:
        if rule_id not in self._rules:
            return False
        del self._rules[rule_id]
        self._results.pop(rule_id, None)
        return True

    def get_all_rules(self) -> List[ValidationRuleEntry]:
        return list(self._rules.values())

    def add_result(self, rule_id: str, result: ValidationResultEntry) -> bool:
        if rule_id not in self._rules:
            return False
        if rule_id not in self._results:
            self._results[rule_id] = {}
        self._results[rule_id][result.result_id] = result
        return True

    def remove_result(self, rule_id: str, result_id: str) -> bool:
        if rule_id not in self._results:
            return False
        if result_id not in self._results[rule_id]:
            return False
        del self._results[rule_id][result_id]
        return True

    def get_results_for_rule(self, rule_id: str) -> List[ValidationResultEntry]:
        return list(self._results.get(rule_id, {}).values())

    def add_report(self, asset_id: str, report: ValidationReportEntry) -> bool:
        if not asset_id:
            return False
        if asset_id not in self._reports:
            self._reports[asset_id] = {}
        self._reports[asset_id][report.report_id] = report
        return True

    def remove_report(self, asset_id: str, report_id: str) -> bool:
        if asset_id not in self._reports:
            return False
        if report_id not in self._reports[asset_id]:
            return False
        del self._reports[asset_id][report_id]
        return True

    def get_reports_for_asset(self, asset_id: str) -> List[ValidationReportEntry]:
        return list(self._reports.get(asset_id, {}).values())

    def get_passed_results(self) -> List[ValidationResultEntry]:
        results = []
        for rule_results in self._results.values():
            results.extend(r for r in rule_results.values() if r.passed)
        return results

    def get_failed_results(self) -> List[ValidationResultEntry]:
        results = []
        for rule_results in self._results.values():
            results.extend(r for r in rule_results.values() if not r.passed)
        return results

    def get_critical_rules(self) -> List[ValidationRuleEntry]:
        return [r for r in self._rules.values() if r.severity == "Critical"]

    def get_enabled_rules(self) -> List[ValidationRuleEntry]:
        return [r for r in self._rules.values() if r.enabled]

    def get_rules_by_scope(self, scope: str) -> List[ValidationRuleEntry]:
        return [r for r in self._rules.values() if r.scope == scope]

    def validate(self, entry: ValidationRuleEntry) -> bool:
        return bool(entry.rule_id) and bool(entry.rule_name)

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    @property
    def is_empty(self) -> bool:
        return len(self._rules) == 0

    def clear(self) -> None:
        self._rules.clear()
        self._results.clear()
        self._reports.clear()
