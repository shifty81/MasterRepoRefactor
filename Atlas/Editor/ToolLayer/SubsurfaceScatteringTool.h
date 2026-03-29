#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P28 Tool — Subsurface scattering profile authoring, scatter kernel editing, and SSS preview.
class SubsurfaceScatteringTool : public ITool {
public:
    enum class ScatterModel { Burley, Separable, Random, ChristensenBurley, Custom };
    enum class TransmissionMode { Thick, Thin, Wrap, Custom };
    enum class SSSChannel { Red, Green, Blue, All, Custom };
    enum class ProfileQuality { Low, Medium, High, Ultra, Custom };

    struct SSSProfileDef {
        std::string profileId;
        std::string profileName;
        ScatterModel scatterModel{ScatterModel::Burley};
        ProfileQuality quality{ProfileQuality::Medium};
        float scatterRadiusR{1.0f};
        float scatterRadiusG{0.7f};
        float scatterRadiusB{0.5f};
        float subsurfaceColor[3]{0.8f, 0.4f, 0.3f};
        float opacity{1.0f};
        bool enabled{true};
    };

    struct TransmissionProfileDef {
        std::string transmissionId;
        std::string profileId;
        TransmissionMode mode{TransmissionMode::Thick};
        float transmittanceR{0.2f};
        float transmittanceG{0.1f};
        float transmittanceB{0.05f};
        float thickness{1.0f};
        bool shadowCast{true};
        bool enabled{true};
    };

    struct SSSKernelDef {
        std::string kernelId;
        std::string profileId;
        SSSChannel channel{SSSChannel::All};
        int sampleCount{32};
        float scatterScale{1.0f};
        float worldUnitScale{0.1f};
        bool useFollowSurface{true};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SubsurfaceScatteringTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateProfile(const SSSProfileDef& def);
    bool DeleteProfile(const std::string& profileId);
    bool EnableProfile(const std::string& profileId, bool enabled);
    bool SetScatterModel(const std::string& profileId, ScatterModel model);
    const SSSProfileDef* GetProfile(const std::string& profileId) const;
    std::vector<std::string> GetAllProfileIds() const;
    std::vector<std::string> GetProfilesByModel(ScatterModel model) const;
    std::vector<std::string> GetEnabledProfiles() const;
    bool AddTransmission(const std::string& profileId, const TransmissionProfileDef& def);
    bool RemoveTransmission(const std::string& profileId, const std::string& transmissionId);
    bool SetTransmissionMode(const std::string& transmissionId, TransmissionMode mode);
    const TransmissionProfileDef* GetTransmission(const std::string& transmissionId) const;
    std::vector<std::string> GetTransmissionsByProfile(const std::string& profileId) const;
    bool AddKernel(const std::string& profileId, const SSSKernelDef& def);
    bool RemoveKernel(const std::string& profileId, const std::string& kernelId);
    bool SetKernelSampleCount(const std::string& kernelId, int count);
    const SSSKernelDef* GetKernel(const std::string& kernelId) const;
    std::vector<std::string> GetKernelsByProfile(const std::string& profileId) const;
    std::vector<std::string> GetKernelsByChannel(SSSChannel channel) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, SSSProfileDef> m_profiles;
    std::unordered_map<std::string, TransmissionProfileDef> m_transmissions;
    std::unordered_map<std::string, SSSKernelDef> m_kernels;
};

} // namespace Atlas::Editor
