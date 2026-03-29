#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P21 Tool — Virtual shadow map configuration, page pool management, and invalidation debugging.
class VirtualShadowMapTool : public ITool {
public:
    enum class VSMCacheMode { Disabled, Static, Dynamic, Hybrid, Forced, Custom };
    enum class PagePoolStatus { Empty, Partial, Full, Overflowed, Defragmenting, Custom };
    enum class InvalidationCause { LightMove, ObjectMove, MaterialChange, ForcedFlush, SceneUpdate, Custom };

    struct VSMConfigDef {
        std::string configId;
        std::string name;
        VSMCacheMode cacheMode{VSMCacheMode::Dynamic};
        int pageResolution{128};
        int maxPagePoolSize{4096};
        float shadowBiasScale{1.0f};
        bool enableClipmaps{true};
        bool logInvalidations{false};
    };

    struct PagePoolEntry {
        std::string poolId;
        std::string configId;
        PagePoolStatus status{PagePoolStatus::Empty};
        int totalPages{4096};
        int usedPages{0};
        int cachedPages{0};
        float defragProgressPct{0.0f};
        bool autoDefrag{true};
    };

    struct InvalidationRecord {
        std::string recordId;
        std::string configId;
        InvalidationCause cause{InvalidationCause::SceneUpdate};
        std::string triggerActorId;
        long long timestamp{0};
        int pagesInvalidated{0};
        float costMs{0.0f};
        bool wasCached{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "VirtualShadowMapTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateVSMConfig(const VSMConfigDef& def);
    bool DeleteVSMConfig(const std::string& configId);
    const VSMConfigDef* GetVSMConfig(const std::string& configId) const;
    std::vector<std::string> GetAllConfigIds() const;
    bool SetCacheMode(const std::string& configId, VSMCacheMode mode);
    bool SetPageResolution(const std::string& configId, int resolution);
    bool SetMaxPagePoolSize(const std::string& configId, int maxSize);
    bool SetShadowBiasScale(const std::string& configId, float scale);
    bool SetEnableClipmaps(const std::string& configId, bool enabled);
    bool SetLogInvalidations(const std::string& configId, bool enabled);

    std::string RegisterPagePool(const PagePoolEntry& entry);
    bool UnregisterPagePool(const std::string& poolId);
    const PagePoolEntry* GetPagePool(const std::string& poolId) const;
    std::vector<std::string> GetPagePoolsByConfig(const std::string& configId) const;
    bool TriggerDefrag(const std::string& poolId);
    bool SetAutoDefrag(const std::string& poolId, bool enabled);
    std::vector<std::string> GetOverflowedPools() const;

    std::string RecordInvalidation(const InvalidationRecord& record);
    const InvalidationRecord* GetInvalidation(const std::string& recordId) const;
    std::vector<std::string> GetInvalidationsByConfig(const std::string& configId) const;
    std::vector<std::string> GetInvalidationsByCause(InvalidationCause cause) const;
    void FlushInvalidationLog();
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, VSMConfigDef> m_configs;
    std::unordered_map<std::string, PagePoolEntry> m_pagePools;
    std::unordered_map<std::string, InvalidationRecord> m_invalidations;
    int m_nextConfigIndex{0};
};

} // namespace Atlas::Editor
