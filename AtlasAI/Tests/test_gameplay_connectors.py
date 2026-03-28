"""
test_gameplay_connectors.py
Tests for J1 (GameplayConnector), J2 (ContractRewardConnector),
J7 (MarketContractBridge) — Python behavioural/design tests.
"""

import pytest
from typing import List, Optional


# =============================================================================
# J1 — GameplayConnector
# =============================================================================

class EHUDFeedbackType:
    ItemReceived     = "ItemReceived"
    CreditsGained    = "CreditsGained"
    MissionProgress  = "MissionProgress"
    ResourceExtracted = "ResourceExtracted"
    LootTableRolled  = "LootTableRolled"
    NotificationAlert = "NotificationAlert"


class HUDFeedbackEvent:
    def __init__(self, feedback_type: str, player_id: int,
                 label: str = "", item_id: str = "",
                 amount: float = 0.0, quantity: int = 0):
        self.type       = feedback_type
        self.player_id  = player_id
        self.label      = label
        self.item_id    = item_id
        self.amount     = amount
        self.quantity   = quantity


class SalvageCompletionEvent:
    def __init__(self, player_id: int, wreck_id: int,
                 loot_table_id: str, seed: int = 0,
                 credit_multiplier: float = 1.0):
        self.player_id         = player_id
        self.wreck_entity_id   = wreck_id
        self.loot_table_id     = loot_table_id
        self.random_seed       = seed
        self.credit_multiplier = credit_multiplier


class MiningCompletionEvent:
    def __init__(self, player_id: int, node_id: int,
                 resource_type: str, units_extracted: float):
        self.player_id       = player_id
        self.node_id         = node_id
        self.resource_type   = resource_type
        self.units_extracted = units_extracted


class MissionProgressEvent:
    def __init__(self, player_id: int, mission_id: str,
                 objective_id: str, progress_delta: float = 1.0):
        self.player_id      = player_id
        self.mission_id     = mission_id
        self.objective_id   = objective_id
        self.progress_delta = progress_delta


class RewardSummary:
    def __init__(self, player_id: int, credits: float,
                 item_ids: List[str], quantities: List[int],
                 items_inserted: int, mission_advanced: bool = False):
        self.player_id          = player_id
        self.credits_awarded    = credits
        self.item_ids           = item_ids
        self.quantities         = quantities
        self.item_types_inserted = items_inserted
        self.mission_advanced   = mission_advanced


class GameplayConnector:
    def __init__(self):
        self._hud_cb       = None
        self._mission_cb   = None
        self._hud_log: List[HUDFeedbackEvent] = []
        self._reward_count = 0

    def initialize(self) -> bool:
        self._reward_count = 0
        self._hud_log.clear()
        return True

    def shutdown(self):
        self._hud_log.clear()
        self._hud_cb     = None
        self._mission_cb = None
        self._reward_count = 0

    def set_hud_callback(self, cb): self._hud_cb = cb
    def set_mission_progress_callback(self, cb): self._mission_cb = cb

    def _fire_hud(self, evt: HUDFeedbackEvent):
        self._hud_log.append(evt)
        if self._hud_cb: self._hud_cb(evt)

    def on_salvage_completed(self, evt: SalvageCompletionEvent) -> RewardSummary:
        credits = 500.0 * evt.credit_multiplier
        items   = ["scrap_metal", "salvaged_electronics"]
        qtys    = [5, 2]
        self._reward_count += 1

        for item, qty in zip(items, qtys):
            self._fire_hud(HUDFeedbackEvent(
                EHUDFeedbackType.ItemReceived, evt.player_id,
                label=f"Salvage: +{qty}x {item}",
                item_id=item, quantity=qty))

        if credits > 0:
            self._fire_hud(HUDFeedbackEvent(
                EHUDFeedbackType.CreditsGained, evt.player_id,
                label=f"Credits: +{int(credits)}", amount=credits))

        self._fire_hud(HUDFeedbackEvent(
            EHUDFeedbackType.LootTableRolled, evt.player_id,
            label=f"Loot table rolled: {evt.loot_table_id}"))

        return RewardSummary(evt.player_id, credits, items, qtys, len(items))

    def on_mining_completed(self, evt: MiningCompletionEvent) -> RewardSummary:
        self._reward_count += 1
        self._fire_hud(HUDFeedbackEvent(
            EHUDFeedbackType.ResourceExtracted, evt.player_id,
            label=f"Mined: +{int(evt.units_extracted)} {evt.resource_type}",
            item_id=evt.resource_type, amount=evt.units_extracted))
        return RewardSummary(evt.player_id, 0.0,
                              [evt.resource_type], [int(evt.units_extracted)], 1)

    def advance_mission_objective(self, evt: MissionProgressEvent):
        if self._mission_cb: self._mission_cb(evt)
        self._fire_hud(HUDFeedbackEvent(
            EHUDFeedbackType.MissionProgress, evt.player_id,
            label=f"Mission progress: {evt.mission_id} / {evt.objective_id}"))

    def apply_loot_reward(self, player_id: int, loot_table_id: str,
                           credit_multiplier: float = 1.0,
                           seed: int = 0) -> RewardSummary:
        evt = SalvageCompletionEvent(player_id, 0, loot_table_id,
                                     seed, credit_multiplier)
        return self.on_salvage_completed(evt)

    def award_credits(self, player_id: int, amount: float, reason: str = ""):
        label = f"{reason} +{int(amount)}" if reason else f"Credits: +{int(amount)}"
        self._fire_hud(HUDFeedbackEvent(
            EHUDFeedbackType.CreditsGained, player_id,
            label=label, amount=amount))
        self._reward_count += 1

    @property
    def recent_hud_events(self): return list(self._hud_log)
    def clear_hud_log(self): self._hud_log.clear()
    @property
    def total_rewards_issued(self): return self._reward_count


class TestGameplayConnector:
    def setup_method(self):
        self.gc = GameplayConnector()
        assert self.gc.initialize()

    # ---- initialization ------------------------------------------------
    def test_initialize_clears_state(self):
        assert self.gc.total_rewards_issued == 0
        assert len(self.gc.recent_hud_events) == 0

    def test_shutdown_resets(self):
        self.gc.award_credits(1, 100.0)
        self.gc.shutdown()
        assert self.gc.total_rewards_issued == 0

    # ---- salvage pipeline ----------------------------------------------
    def test_salvage_returns_reward_summary(self):
        evt = SalvageCompletionEvent(101, 999, "wreck_loot_A")
        summary = self.gc.on_salvage_completed(evt)
        assert summary.player_id == 101
        assert summary.credits_awarded > 0
        assert len(summary.item_ids) >= 2
        assert summary.item_types_inserted == len(summary.item_ids)

    def test_salvage_fires_hud_events(self):
        evt = SalvageCompletionEvent(101, 999, "wreck_loot_A")
        self.gc.on_salvage_completed(evt)
        events = self.gc.recent_hud_events
        types = [e.type for e in events]
        assert EHUDFeedbackType.ItemReceived in types
        assert EHUDFeedbackType.CreditsGained in types
        assert EHUDFeedbackType.LootTableRolled in types

    def test_salvage_credit_multiplier(self):
        evt_base = SalvageCompletionEvent(1, 1, "t", credit_multiplier=1.0)
        evt_2x   = SalvageCompletionEvent(1, 1, "t", credit_multiplier=2.0)
        base = self.gc.on_salvage_completed(evt_base)
        self.gc.clear_hud_log()
        two_x = self.gc.on_salvage_completed(evt_2x)
        assert two_x.credits_awarded == pytest.approx(base.credits_awarded * 2.0)

    def test_salvage_hud_callback_invoked(self):
        received = []
        self.gc.set_hud_callback(lambda e: received.append(e))
        self.gc.on_salvage_completed(SalvageCompletionEvent(5, 1, "tbl"))
        assert len(received) >= 3  # items + credits + loot-table-rolled

    def test_salvage_reward_count_increments(self):
        self.gc.on_salvage_completed(SalvageCompletionEvent(1, 1, "t"))
        assert self.gc.total_rewards_issued == 1
        self.gc.on_salvage_completed(SalvageCompletionEvent(1, 1, "t"))
        assert self.gc.total_rewards_issued == 2

    def test_apply_loot_reward_equivalent_to_salvage(self):
        summary = self.gc.apply_loot_reward(5, "loot_t", credit_multiplier=1.5)
        assert summary.player_id == 5
        assert summary.credits_awarded == pytest.approx(750.0)

    # ---- mining pipeline -----------------------------------------------
    def test_mining_completed_fires_resource_event(self):
        evt = MiningCompletionEvent(42, 7, "iron_ore", 100.0)
        summary = self.gc.on_mining_completed(evt)
        assert summary.player_id == 42
        assert "iron_ore" in summary.item_ids
        events = self.gc.recent_hud_events
        assert any(e.type == EHUDFeedbackType.ResourceExtracted for e in events)

    def test_mining_extracts_correct_units(self):
        evt = MiningCompletionEvent(1, 1, "cobalt", 75.5)
        summary = self.gc.on_mining_completed(evt)
        assert summary.quantities[0] == 75  # int conversion

    def test_mining_hud_label_contains_resource(self):
        evt = MiningCompletionEvent(1, 1, "titanium", 30.0)
        self.gc.on_mining_completed(evt)
        events = self.gc.recent_hud_events
        assert any("titanium" in e.label for e in events)

    # ---- mission progress -----------------------------------------------
    def test_mission_progress_fires_hud(self):
        evt = MissionProgressEvent(3, "m_001", "obj_kill_5")
        self.gc.advance_mission_objective(evt)
        events = self.gc.recent_hud_events
        assert any(e.type == EHUDFeedbackType.MissionProgress for e in events)

    def test_mission_progress_callback_called(self):
        received = []
        self.gc.set_mission_progress_callback(lambda e: received.append(e))
        evt = MissionProgressEvent(3, "m_002", "obj_deliver")
        self.gc.advance_mission_objective(evt)
        assert len(received) == 1
        assert received[0].mission_id == "m_002"

    def test_mission_hud_label_contains_ids(self):
        evt = MissionProgressEvent(1, "m_alpha", "destroy_station")
        self.gc.advance_mission_objective(evt)
        events = self.gc.recent_hud_events
        assert any("m_alpha" in e.label for e in events)

    # ---- credit award -----------------------------------------------
    def test_award_credits_fires_hud(self):
        self.gc.award_credits(9, 250.0, "bonus")
        events = self.gc.recent_hud_events
        assert any(e.type == EHUDFeedbackType.CreditsGained for e in events)
        assert any(e.amount == pytest.approx(250.0) for e in events)

    def test_award_credits_increments_reward_count(self):
        before = self.gc.total_rewards_issued
        self.gc.award_credits(1, 100.0)
        assert self.gc.total_rewards_issued == before + 1

    def test_award_credits_label_without_reason(self):
        self.gc.award_credits(1, 500.0)
        events = self.gc.recent_hud_events
        assert any("500" in e.label for e in events)

    # ---- clear log -----------------------------------------------
    def test_clear_hud_log(self):
        self.gc.on_salvage_completed(SalvageCompletionEvent(1, 1, "t"))
        assert len(self.gc.recent_hud_events) > 0
        self.gc.clear_hud_log()
        assert len(self.gc.recent_hud_events) == 0

    # ---- multiple players -----------------------------------------------
    def test_multiple_players_tracked(self):
        self.gc.award_credits(1, 100.0)
        self.gc.award_credits(2, 200.0)
        player_ids = {e.player_id for e in self.gc.recent_hud_events}
        assert 1 in player_ids
        assert 2 in player_ids


# =============================================================================
# J2 — ContractRewardConnector
# =============================================================================

class ContractRewardDefinition:
    def __init__(self, contract_id: str, contract_type: str,
                 base_credit_reward: float = 0.0,
                 faction_standing_delta: float = 0.0,
                 primary_faction_id: int = 0,
                 skill_xp_amount: float = 0.0,
                 reward_skill_id: str = "",
                 required_standing: float = -10.0,
                 required_skill_level: float = 0.0,
                 required_skill_id: str = ""):
        self.contract_id             = contract_id
        self.contract_type           = contract_type
        self.base_credit_reward      = base_credit_reward
        self.faction_standing_delta  = faction_standing_delta
        self.primary_faction_id      = primary_faction_id
        self.skill_xp_amount         = skill_xp_amount
        self.reward_skill_id         = reward_skill_id
        self.required_standing       = required_standing
        self.required_skill_level    = required_skill_level
        self.required_skill_id       = required_skill_id


class ContractRewardConnector:
    def __init__(self):
        self._contracts: List[ContractRewardDefinition] = []
        self._completed_count = 0
        self._credit_cb   = None
        self._standing_cb = None
        self._skill_cb    = None
        self._standing_query = None
        self._skill_query    = None

    def initialize(self) -> bool:
        self._completed_count = 0
        return True

    def shutdown(self):
        self._contracts.clear()
        self._completed_count = 0

    def register_contract(self, defn: ContractRewardDefinition):
        for i, c in enumerate(self._contracts):
            if c.contract_id == defn.contract_id:
                self._contracts[i] = defn; return
        self._contracts.append(defn)

    def unregister_contract(self, contract_id: str) -> bool:
        before = len(self._contracts)
        self._contracts = [c for c in self._contracts
                           if c.contract_id != contract_id]
        return len(self._contracts) < before

    def has_contract(self, cid: str) -> bool:
        return any(c.contract_id == cid for c in self._contracts)

    def find_contract(self, cid: str) -> Optional[ContractRewardDefinition]:
        for c in self._contracts:
            if c.contract_id == cid: return c
        return None

    @property
    def contract_count(self): return len(self._contracts)

    def set_credit_callback(self, cb): self._credit_cb = cb
    def set_standing_callback(self, cb): self._standing_cb = cb
    def set_skill_xp_callback(self, cb): self._skill_cb = cb
    def set_standing_query(self, q): self._standing_query = q
    def set_skill_query(self, q): self._skill_query = q

    def on_contract_completed(self, player_id: int, contract_id: str,
                               perf_mult: float = 1.0) -> float:
        defn = self.find_contract(contract_id)
        if not defn: return 0.0

        credits = defn.base_credit_reward * perf_mult
        if self._credit_cb and credits > 0:
            self._credit_cb(player_id, credits, f"Contract: {contract_id}")

        if defn.faction_standing_delta != 0.0 and defn.primary_faction_id != 0:
            current = 0.0
            if self._standing_query:
                current = self._standing_query(player_id, defn.primary_faction_id)
            evt = {
                "player_id": player_id,
                "faction_id": defn.primary_faction_id,
                "delta": defn.faction_standing_delta * perf_mult,
                "new_standing": current + defn.faction_standing_delta * perf_mult,
            }
            if self._standing_cb: self._standing_cb(evt)

        if defn.skill_xp_amount > 0 and defn.reward_skill_id:
            evt = {
                "player_id": player_id,
                "skill_id": defn.reward_skill_id,
                "xp_gained": defn.skill_xp_amount * perf_mult,
            }
            if self._skill_cb: self._skill_cb(evt)

        self._completed_count += 1
        return credits

    def check_eligibility(self, player_id: int, contract_id: str) -> dict:
        defn = self.find_contract(contract_id)
        if not defn:
            return {"eligible": False, "fail_reason": "Contract not found"}

        if defn.required_standing > -10.0 and defn.primary_faction_id != 0:
            standing = 0.0
            if self._standing_query:
                standing = self._standing_query(player_id, defn.primary_faction_id)
            if standing < defn.required_standing:
                return {"eligible": False,
                        "fail_reason": f"Insufficient standing ({standing:.1f})",
                        "player_standing": standing}

        if defn.required_skill_level > 0 and defn.required_skill_id:
            level = 0.0
            if self._skill_query:
                level = self._skill_query(player_id, defn.required_skill_id)
            if level < defn.required_skill_level:
                return {"eligible": False,
                        "fail_reason": f"Insufficient skill ({level:.1f})",
                        "player_skill_level": level}

        return {"eligible": True}

    def get_available_contracts(self, player_id: int) -> List[ContractRewardDefinition]:
        return [c for c in self._contracts
                if self.check_eligibility(player_id, c.contract_id)["eligible"]]

    @property
    def completed_count(self): return self._completed_count


class TestContractRewardConnector:
    def setup_method(self):
        self.crc = ContractRewardConnector()
        self.crc.initialize()
        # Standard contract definition.
        self.defn = ContractRewardDefinition(
            "c001", "salvage",
            base_credit_reward=1000.0,
            faction_standing_delta=0.5,
            primary_faction_id=10,
            skill_xp_amount=50.0,
            reward_skill_id="salvage",
        )
        self.crc.register_contract(self.defn)

    # ---- registration --------------------------------------------------
    def test_register_and_find(self):
        assert self.crc.has_contract("c001")
        found = self.crc.find_contract("c001")
        assert found is not None
        assert found.base_credit_reward == 1000.0

    def test_register_updates_existing(self):
        updated = ContractRewardDefinition("c001", "salvage",
                                           base_credit_reward=2000.0)
        self.crc.register_contract(updated)
        assert self.crc.find_contract("c001").base_credit_reward == 2000.0
        assert self.crc.contract_count == 1

    def test_unregister_contract(self):
        assert self.crc.unregister_contract("c001")
        assert not self.crc.has_contract("c001")

    def test_unregister_missing_returns_false(self):
        assert not self.crc.unregister_contract("x999")

    # ---- credit reward --------------------------------------------------
    def test_contract_completed_awards_credits(self):
        received = []
        self.crc.set_credit_callback(lambda pid, amt, reason: received.append(amt))
        credits = self.crc.on_contract_completed(1, "c001")
        assert credits == pytest.approx(1000.0)
        assert len(received) == 1

    def test_performance_multiplier_scales_credits(self):
        received = []
        self.crc.set_credit_callback(lambda pid, amt, r: received.append(amt))
        self.crc.on_contract_completed(1, "c001", perf_mult=1.5)
        assert received[0] == pytest.approx(1500.0)

    def test_zero_credit_reward_no_callback(self):
        no_credits = ContractRewardDefinition("c002", "delivery",
                                              base_credit_reward=0.0)
        self.crc.register_contract(no_credits)
        received = []
        self.crc.set_credit_callback(lambda pid, amt, r: received.append(amt))
        self.crc.on_contract_completed(1, "c002")
        assert len(received) == 0

    def test_missing_contract_returns_zero(self):
        credits = self.crc.on_contract_completed(1, "nonexistent")
        assert credits == 0.0

    # ---- faction standing -----------------------------------------------
    def test_contract_awards_faction_standing(self):
        standings = []
        self.crc.set_standing_callback(lambda e: standings.append(e))
        self.crc.on_contract_completed(1, "c001")
        assert len(standings) == 1
        assert standings[0]["delta"] == pytest.approx(0.5)

    def test_standing_delta_uses_performance_multiplier(self):
        standings = []
        self.crc.set_standing_callback(lambda e: standings.append(e))
        self.crc.on_contract_completed(1, "c001", perf_mult=2.0)
        assert standings[0]["delta"] == pytest.approx(1.0)

    def test_standing_query_used_for_current(self):
        self.crc.set_standing_query(lambda pid, fid: 3.0)
        standings = []
        self.crc.set_standing_callback(lambda e: standings.append(e))
        self.crc.on_contract_completed(1, "c001")
        assert standings[0]["new_standing"] == pytest.approx(3.5)

    # ---- skill XP -------------------------------------------------------
    def test_contract_awards_skill_xp(self):
        xp_events = []
        self.crc.set_skill_xp_callback(lambda e: xp_events.append(e))
        self.crc.on_contract_completed(1, "c001")
        assert len(xp_events) == 1
        assert xp_events[0]["skill_id"] == "salvage"
        assert xp_events[0]["xp_gained"] == pytest.approx(50.0)

    # ---- eligibility gate -----------------------------------------------
    def test_eligible_without_requirements(self):
        free_contract = ContractRewardDefinition("c_free", "delivery",
                                                  base_credit_reward=100.0)
        self.crc.register_contract(free_contract)
        result = self.crc.check_eligibility(1, "c_free")
        assert result["eligible"] is True

    def test_ineligible_insufficient_standing(self):
        gated = ContractRewardDefinition(
            "c_gated", "elite",
            base_credit_reward=5000.0,
            required_standing=5.0,
            primary_faction_id=10)
        self.crc.register_contract(gated)
        self.crc.set_standing_query(lambda pid, fid: 2.0)
        result = self.crc.check_eligibility(1, "c_gated")
        assert result["eligible"] is False
        assert "standing" in result["fail_reason"].lower()

    def test_eligible_with_sufficient_standing(self):
        gated = ContractRewardDefinition(
            "c_gated2", "elite",
            required_standing=3.0,
            primary_faction_id=10)
        self.crc.register_contract(gated)
        self.crc.set_standing_query(lambda pid, fid: 5.0)
        result = self.crc.check_eligibility(1, "c_gated2")
        assert result["eligible"] is True

    def test_ineligible_insufficient_skill(self):
        skilled = ContractRewardDefinition(
            "c_skill", "expert",
            required_skill_level=3.0,
            required_skill_id="combat")
        self.crc.register_contract(skilled)
        self.crc.set_skill_query(lambda pid, sid: 1.0)
        result = self.crc.check_eligibility(1, "c_skill")
        assert result["eligible"] is False
        assert "skill" in result["fail_reason"].lower()

    def test_available_contracts_filters_by_eligibility(self):
        free = ContractRewardDefinition("c_free2", "delivery")
        gated = ContractRewardDefinition(
            "c_gated3", "elite",
            required_standing=8.0,
            primary_faction_id=10)
        self.crc.register_contract(free)
        self.crc.register_contract(gated)
        self.crc.set_standing_query(lambda pid, fid: 2.0)
        available = self.crc.get_available_contracts(1)
        ids = [c.contract_id for c in available]
        assert "c_free2" in ids
        assert "c_gated3" not in ids

    def test_completed_count_increments(self):
        self.crc.on_contract_completed(1, "c001")
        self.crc.on_contract_completed(1, "c001")
        assert self.crc.completed_count == 2


# =============================================================================
# J7 — MarketContractBridge
# =============================================================================

class MarketPricePoint:
    def __init__(self, resource_id: str, current_price: float,
                 base_price: float, supply: float, demand: float,
                 station_id: str = ""):
        self.resource_id   = resource_id
        self.current_price = current_price
        self.base_price    = base_price
        self.supply        = supply
        self.demand        = demand
        self.station_id    = station_id
        self.is_low        = current_price < base_price
        self.is_high       = current_price > base_price


class MarketContractTemplate:
    def __init__(self, template_id: str, contract_type: str,
                 resource_id: str, base_reward: float,
                 source_station: str = "", dest_station: str = "",
                 urgency_mult: float = 1.0, required_qty: int = 0):
        self.template_id        = template_id
        self.contract_type      = contract_type
        self.resource_id        = resource_id
        self.base_reward        = base_reward
        self.source_station_id  = source_station
        self.dest_station_id    = dest_station
        self.urgency_multiplier = urgency_mult
        self.required_quantity  = required_qty
        self.is_active          = False


class MarketContractBridge:
    def __init__(self):
        self._prices: List[MarketPricePoint] = []
        self._templates: List[MarketContractTemplate] = []
        self._fleet_needs: List[str] = []
        self._opportunity_cb = None
        self._activated_count = 0

    def initialize(self) -> bool:
        self._activated_count = 0
        return True

    def shutdown(self):
        self._prices.clear()
        self._templates.clear()
        self._fleet_needs.clear()

    def ingest_price_point(self, p: MarketPricePoint):
        for i, existing in enumerate(self._prices):
            if (existing.resource_id == p.resource_id and
                    existing.station_id == p.station_id):
                self._prices[i] = p; return
        self._prices.append(p)

    def clear_market_data(self): self._prices.clear()

    def has_price_data(self, resource_id: str) -> bool:
        return self.get_price_point(resource_id) is not None

    def get_price_point(self, resource_id: str,
                         station_id: str = "") -> Optional[MarketPricePoint]:
        for p in self._prices:
            if p.resource_id == resource_id:
                if not station_id or p.station_id == station_id: return p
        return None

    def register_template(self, tmpl: MarketContractTemplate):
        for i, t in enumerate(self._templates):
            if t.template_id == tmpl.template_id:
                self._templates[i] = tmpl; return
        self._templates.append(tmpl)

    def has_template(self, tid: str) -> bool:
        return any(t.template_id == tid for t in self._templates)

    @property
    def template_count(self): return len(self._templates)

    def _score_opportunity(self, p: MarketPricePoint) -> float:
        score = 0.0
        if p.demand > p.supply:
            score += 0.5 * (p.demand - p.supply) / (p.demand + 1)
        if p.is_high: score += 0.3
        if p.current_price > p.base_price * 1.2: score += 0.2
        return min(score, 1.0)

    def analyse_opportunities(self):
        result = []
        for tmpl in self._templates:
            p = self.get_price_point(tmpl.resource_id, tmpl.dest_station_id)
            if not p: continue
            score = self._score_opportunity(p)
            if score <= 0: continue
            result.append({
                "template_id": tmpl.template_id,
                "resource_id": tmpl.resource_id,
                "opportunity_score": score,
                "estimated_reward": tmpl.base_reward * tmpl.urgency_multiplier * (1 + score),
                "reason": f"Market demand for {tmpl.resource_id} at {tmpl.dest_station_id}"
            })
        # Fleet needs
        existing_resources = {o["resource_id"] for o in result}
        for need in self._fleet_needs:
            if need not in existing_resources:
                result.append({
                    "template_id": f"fleet_resupply_{need}",
                    "resource_id": need,
                    "opportunity_score": 0.8,
                    "estimated_reward": 1000.0,
                    "reason": f"Fleet resupply need: {need}",
                })
        result.sort(key=lambda x: x["opportunity_score"], reverse=True)
        return result

    def top_opportunities(self, n: int = 5):
        return self.analyse_opportunities()[:n]

    def compute_reward_multiplier(self, resource_id: str,
                                    contract_type: str = "") -> float:
        p = self.get_price_point(resource_id)
        if not p: return 1.0
        if p.demand > 0 and p.supply > 0:
            ratio = p.demand / p.supply
            if ratio > 2.0: return 2.0
            if ratio > 1.0: return ratio
        if p.is_high: return 1.5
        if p.is_low:  return 0.8
        return 1.0

    def activate_top_contracts(self, max_active: int = 5) -> List[str]:
        opps = self.top_opportunities(max_active)
        activated = []
        for opp in opps:
            for t in self._templates:
                if t.template_id == opp["template_id"]:
                    t.is_active = True
                    activated.append(t.template_id)
                    self._activated_count += 1
                    if self._opportunity_cb:
                        self._opportunity_cb(opp)
                    break
        return activated

    def set_fleet_resource_needs(self, needs: List[str]):
        self._fleet_needs = list(needs)

    def get_fleet_resupply_needs(self) -> List[str]:
        return list(self._fleet_needs)

    def set_opportunity_callback(self, cb): self._opportunity_cb = cb

    @property
    def contracts_activated(self): return self._activated_count


class TestMarketContractBridge:
    def setup_method(self):
        self.bridge = MarketContractBridge()
        self.bridge.initialize()

    def _add_price(self, resource: str, current: float, base: float,
                   supply: float = 50.0, demand: float = 50.0,
                   station: str = "S1"):
        p = MarketPricePoint(resource, current, base, supply, demand, station)
        self.bridge.ingest_price_point(p)

    def _add_template(self, tid: str, resource: str, reward: float,
                      dest: str = "S1"):
        t = MarketContractTemplate(tid, "delivery", resource, reward,
                                   dest_station=dest)
        self.bridge.register_template(t)

    # ---- price ingestion -----------------------------------------------
    def test_ingest_price_point(self):
        self._add_price("iron_ore", 100.0, 80.0)
        assert self.bridge.has_price_data("iron_ore")

    def test_get_price_point(self):
        self._add_price("iron_ore", 100.0, 80.0)
        p = self.bridge.get_price_point("iron_ore")
        assert p is not None
        assert p.current_price == pytest.approx(100.0)

    def test_price_point_is_high_flag(self):
        self._add_price("gold", 200.0, 100.0)
        p = self.bridge.get_price_point("gold")
        assert p.is_high is True
        assert p.is_low is False

    def test_price_point_is_low_flag(self):
        self._add_price("scrap", 50.0, 100.0)
        p = self.bridge.get_price_point("scrap")
        assert p.is_low is True

    def test_ingest_updates_existing(self):
        self._add_price("iron_ore", 100.0, 80.0, station="S1")
        self._add_price("iron_ore", 150.0, 80.0, station="S1")
        p = self.bridge.get_price_point("iron_ore", "S1")
        assert p.current_price == pytest.approx(150.0)

    def test_clear_market_data(self):
        self._add_price("iron_ore", 100.0, 80.0)
        self.bridge.clear_market_data()
        assert not self.bridge.has_price_data("iron_ore")

    # ---- template registration ----------------------------------------
    def test_register_template(self):
        self._add_template("t_iron", "iron_ore", 500.0)
        assert self.bridge.has_template("t_iron")
        assert self.bridge.template_count == 1

    def test_register_template_updates_existing(self):
        self._add_template("t_iron", "iron_ore", 500.0)
        t2 = MarketContractTemplate("t_iron", "delivery", "iron_ore", 800.0)
        self.bridge.register_template(t2)
        assert self.bridge.template_count == 1

    # ---- opportunity analysis -----------------------------------------
    def test_analyse_opportunities_no_price(self):
        self._add_template("t_iron", "iron_ore", 500.0)
        opps = self.bridge.analyse_opportunities()
        assert len(opps) == 0

    def test_analyse_opportunities_with_high_demand(self):
        self._add_price("iron_ore", 150.0, 80.0, supply=10.0, demand=80.0)
        self._add_template("t_iron", "iron_ore", 500.0)
        opps = self.bridge.analyse_opportunities()
        assert len(opps) > 0
        assert opps[0]["opportunity_score"] > 0

    def test_top_opportunities_limited(self):
        for i in range(10):
            self._add_price(f"res_{i}", 120.0, 80.0, supply=10.0, demand=50.0)
            self._add_template(f"t_{i}", f"res_{i}", 100.0)
        opps = self.bridge.top_opportunities(3)
        assert len(opps) <= 3

    def test_opportunities_sorted_by_score_desc(self):
        # Low demand resource.
        self._add_price("res_low", 80.0, 80.0, supply=100.0, demand=20.0)
        self._add_template("t_low", "res_low", 100.0)
        # High demand resource.
        self._add_price("res_high", 200.0, 80.0, supply=5.0, demand=100.0)
        self._add_template("t_high", "res_high", 500.0)
        opps = self.bridge.analyse_opportunities()
        if len(opps) >= 2:
            assert opps[0]["opportunity_score"] >= opps[1]["opportunity_score"]

    # ---- reward multiplier --------------------------------------------
    def test_reward_multiplier_default_for_unknown(self):
        assert self.bridge.compute_reward_multiplier("unknown") == pytest.approx(1.0)

    def test_reward_multiplier_high_demand(self):
        self._add_price("iron_ore", 100.0, 80.0, supply=10.0, demand=30.0)
        mult = self.bridge.compute_reward_multiplier("iron_ore")
        assert mult > 1.0

    def test_reward_multiplier_cap_at_two(self):
        self._add_price("rare_ore", 200.0, 80.0, supply=1.0, demand=200.0)
        mult = self.bridge.compute_reward_multiplier("rare_ore")
        assert mult <= 2.0

    def test_reward_multiplier_low_price_below_one(self):
        self._add_price("junk", 50.0, 100.0, supply=100.0, demand=10.0)
        mult = self.bridge.compute_reward_multiplier("junk")
        assert mult < 1.0

    # ---- activate contracts -------------------------------------------
    def test_activate_top_contracts(self):
        self._add_price("iron_ore", 200.0, 80.0, supply=5.0, demand=100.0)
        self._add_template("t_iron", "iron_ore", 500.0)
        activated = self.bridge.activate_top_contracts(3)
        assert "t_iron" in activated
        assert self.bridge.contracts_activated >= 1

    def test_activate_fires_opportunity_callback(self):
        self._add_price("iron_ore", 200.0, 80.0, supply=5.0, demand=100.0)
        self._add_template("t_iron", "iron_ore", 500.0)
        received = []
        self.bridge.set_opportunity_callback(lambda o: received.append(o))
        self.bridge.activate_top_contracts(5)
        assert len(received) >= 1

    # ---- fleet needs ---------------------------------------------------
    def test_fleet_resupply_needs(self):
        self.bridge.set_fleet_resource_needs(["fuel_cells", "ammo"])
        needs = self.bridge.get_fleet_resupply_needs()
        assert "fuel_cells" in needs
        assert "ammo" in needs

    def test_fleet_needs_appear_in_opportunities(self):
        self.bridge.set_fleet_resource_needs(["rare_element"])
        opps = self.bridge.analyse_opportunities()
        resources = [o["resource_id"] for o in opps]
        assert "rare_element" in resources

    def test_fleet_needs_high_priority_score(self):
        self.bridge.set_fleet_resource_needs(["critical_part"])
        opps = self.bridge.analyse_opportunities()
        for o in opps:
            if o["resource_id"] == "critical_part":
                assert o["opportunity_score"] >= 0.7
