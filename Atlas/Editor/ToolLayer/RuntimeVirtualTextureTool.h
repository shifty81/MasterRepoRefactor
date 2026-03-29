#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P22 Tool — Runtime Virtual Texture volume and material management.
class RuntimeVirtualTextureTool : public ITool {
public:
    enum class RVTLayout { BaseColor, NormalHeight, BaseColorNormalHeight, WorldHeight, Mask, Custom };
    enum class RVTStreamingMode { Disabled, OnDemand, Preload, Adaptive, Background, Custom };
    enum class RVTBuildMode { Manual, Automatic, OnLoad, Incremental, Full, Custom };
    enum class RVTCachePriority { Low, Normal, High, Critical, Persistent, Custom };

    struct RVTVolumeDef {
        std::string volumeId;
        std::string name;
        RVTLayout layout{RVTLayout::BaseColor};
        RVTStreamingMode streamingMode{RVTStreamingMode::OnDemand};
        float boundsExtent{4096.0f};
        int textureSizeX{2048};
        int textureSizeY{2048};
        int numMips{10};
        bool enableCompression{true};
    };

    struct RVTMaterialBinding {
        std::string bindingId;
        std::string volumeId;
        std::string materialId;
        RVTCachePriority cachePriority{RVTCachePriority::Normal};
        int layerIndex{0};
        bool blendUnderLayers{false};
        bool enabled{true};
    };

    struct RVTBuildConfig {
        std::string configId;
        std::string volumeId;
        RVTBuildMode buildMode{RVTBuildMode::Manual};
        int tileSize{128};
        int borderSize{4};
        float buildTimeoutMs{30000.0f};
        bool generateMips{true};
        bool compressOnBuild{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "RuntimeVirtualTextureTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateRVTVolume(const RVTVolumeDef& def);
    bool DeleteRVTVolume(const std::string& volumeId);
    const RVTVolumeDef* GetRVTVolume(const std::string& volumeId) const;
    std::vector<std::string> GetAllVolumeIds() const;

    bool SetRVTLayout(const std::string& volumeId, RVTLayout layout);
    bool SetStreamingMode(const std::string& volumeId, RVTStreamingMode mode);

    bool BindMaterial(const RVTMaterialBinding& binding);
    bool UnbindMaterial(const std::string& bindingId);
    std::vector<RVTMaterialBinding> GetMaterialBindings(const std::string& volumeId) const;

    bool SetBuildConfig(const RVTBuildConfig& config);
    bool TriggerBuild(const std::string& volumeId);
    bool InvalidateCache(const std::string& volumeId);
    std::vector<std::string> GetVolumesWithLayout(RVTLayout layout) const;

    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, RVTVolumeDef> m_volumes;
    std::unordered_map<std::string, RVTMaterialBinding> m_materialBindings;
    std::unordered_map<std::string, RVTBuildConfig> m_buildConfigs;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
