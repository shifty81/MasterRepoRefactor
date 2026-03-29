#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P13 Tool — Lightmap baking configuration, bounce settings, and light probe setup.
class LightBakerTool : public ITool {
public:
    enum class BakeQuality { Preview, Low, Medium, High, Ultra };
    enum class LightmapBackend { CPU, GPU, Hybrid };
    enum class ProbeLayout { Grid, Volume, Surface, Manual };
    enum class BakeMode { DirectOnly, IndirectOnly, Combined, AmbientOcclusion };

    struct BakeSettings {
        BakeQuality quality{BakeQuality::Medium};
        LightmapBackend backend{LightmapBackend::GPU};
        int texelResolution{512};
        int bounceCount{3};
        float indirectIntensity{1.0f};
        float shadowBias{0.001f};
        bool useDenoiser{true};
        int samplesPerTexel{64};
    };

    struct ProbeSettings {
        ProbeLayout layout{ProbeLayout::Grid};
        float probeSpacingX{5.0f};
        float probeSpacingY{5.0f};
        float probeSpacingZ{5.0f};
        int probeResolution{32};
        bool useOcclusion{true};
        float blendRadius{0.5f};
    };

    struct LightmapAtlasConfig {
        int atlasWidth{2048};
        int atlasHeight{2048};
        int padding{4};
        bool packMeshes{true};
        float uvScale{1.0f};
        std::string atlasOutputPath;
    };

    struct BakeJob {
        std::string jobId;
        std::string name;
        BakeMode mode{BakeMode::Combined};
        BakeSettings settings;
        ProbeSettings probeSettings;
        LightmapAtlasConfig atlasConfig;
        std::string meshId;
        std::string meshPath;
        std::string outputDirectory;
        float bakeProgress{0.0f};
        bool completed{false};
        bool failed{false};
        int elapsedSeconds{0};
        std::string statusMessage;
        std::string linkedSceneId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LightBakerTool"; }
    bool IsActive() const override { return m_active; }

    // Job management
    std::string CreateBakeJob(const std::string& name, BakeMode mode = BakeMode::Combined);
    bool RemoveBakeJob(const std::string& jobId);
    bool SetBakeQuality(const std::string& jobId, BakeQuality quality);
    bool SetBounceCount(const std::string& jobId, int bounces);
    bool SetLightmapResolution(const std::string& jobId, int resolution);
    bool SetBackend(const std::string& jobId, LightmapBackend backend);
    bool SetUseDenoiser(const std::string& jobId, bool enabled);
    bool SetIndirectIntensity(const std::string& jobId, float intensity);
    bool SetMesh(const std::string& jobId, const std::string& meshId, const std::string& path = "");
    bool SetOutputDirectory(const std::string& jobId, const std::string& dir);
    bool SetScene(const std::string& jobId, const std::string& sceneId);

    // Probe management
    bool SetProbeLayout(const std::string& jobId, ProbeLayout layout);
    bool SetProbeSpacing(const std::string& jobId, float x, float y, float z);
    bool SetProbeResolution(const std::string& jobId, int resolution);
    bool SetProbeOcclusion(const std::string& jobId, bool enabled);

    // Atlas config
    bool SetAtlasSize(const std::string& jobId, int width, int height);
    bool SetAtlasPadding(const std::string& jobId, int padding);
    bool SetAtlasOutputPath(const std::string& jobId, const std::string& path);

    // Baking control
    bool StartBake(const std::string& jobId);
    bool CancelBake(const std::string& jobId);
    bool IsBaking(const std::string& jobId) const;
    float GetBakeProgress(const std::string& jobId) const;
    bool BakeAll();
    void CancelAllBakes();

    // Queries
    int GetJobCount() const { return static_cast<int>(m_jobs.size()); }
    const BakeJob* GetJob(const std::string& jobId) const;
    std::vector<std::string> GetJobIds() const;
    std::vector<std::string> GetCompletedJobIds() const;
    std::vector<std::string> GetPendingJobIds() const;

    // Persistence
    bool SaveBakeConfig(const std::string& filePath) const;
    bool LoadBakeConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, BakeJob> m_jobs;
    int m_nextJobIndex{0};
};

} // namespace Atlas::Editor
