// PCGDebugSystem.h
// Atlas Editor — PCG seed control, regeneration triggers, and debug visualization.

#pragma once
#include "PCG/PCGDebugTypes.h"

#include <functional>
#include <string>

namespace atlas::editor::pcg {

/// Callback invoked when the user requests a PCG regeneration pass.
using RegenerateCallback = std::function<void(uint32_t seed)>;

/// Editor-side system that exposes PCG seed control and debug visualisation.
class PCGDebugSystem
{
public:
    bool Initialize();
    void Shutdown();

    // ---- seed panel ----------------------------------------------------
    uint32_t GetActiveSeed()   const { return m_state.activeSeed; }
    void     SetSeed(uint32_t seed);

    /// Regenerate the entire world with the current seed.
    void RegenerateWorld();

    /// Regenerate only the selected region/sector.
    void RegenerateSelected(const std::string& regionId);

    void SetRegenerateCallback(RegenerateCallback cb) { m_regenCb = std::move(cb); }

    // ---- spawn-point visualization ------------------------------------
    void AddSpawnPoint(const PCGSpawnPoint& point);
    void ClearSpawnPoints();
    void SetShowSpawnPoints(bool show) { m_state.showSpawnPoints = show; }

    // ---- region bounds visualization ----------------------------------
    void AddRegionBounds(const PCGGenerationBounds& bounds);
    void ClearRegionBounds();
    void SetShowBounds(bool show) { m_state.showBounds = show; }

    // ---- rule inspector -----------------------------------------------
    void RegisterRule(const PCGRuleInspectorEntry& rule);
    bool OverrideRule(const std::string& ruleId, const std::string& reason);
    bool ClearOverride(const std::string& ruleId);
    bool LockContent(const std::string& regionId);

    const PCGDebugState& GetState() const { return m_state; }

private:
    PCGDebugState     m_state;
    RegenerateCallback m_regenCb;
};

} // namespace atlas::editor::pcg
