#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P20 Tool — Texture compression profile management, format selection, and mip-chain configuration.
class TextureCompressionTool : public ITool {
public:
    enum class CompressionFormat { DXT1, DXT5, BC4, BC5, BC6H, BC7, ASTC_4x4, ASTC_8x8, ETC2, Uncompressed, Custom };
    enum class MipGenFilter { Box, Triangle, Sinc, Kaiser, Lanczos, Custom };
    enum class TextureUsageType { Diffuse, Normal, Roughness, Metallic, Emissive, Alpha, HDR, Data, Custom };

    struct CompressionProfile {
        std::string profileId;
        std::string name;
        CompressionFormat format{CompressionFormat::BC7};
        TextureUsageType usageType{TextureUsageType::Diffuse};
        bool generateMips{true};
        int maxTextureSize{4096};
        float compressionQuality{1.0f};
        bool sRGB{true};
    };

    struct MipChainConfig {
        std::string configId;
        std::string profileId;
        MipGenFilter genFilter{MipGenFilter::Kaiser};
        int minMipSize{4};
        int maxMipLevels{13};
        float sharpnessBias{0.0f};
        bool preserveAlphaCoverage{false};
    };

    struct TextureFormatOverride {
        std::string overrideId;
        std::string assetPath;
        CompressionFormat overrideFormat{CompressionFormat::BC7};
        std::string reason;
        bool applyToChildren{false};
        int priority{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "TextureCompressionTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateProfile(const CompressionProfile& profile);
    bool RemoveProfile(const std::string& profileId);
    bool SetCompressionFormat(const std::string& profileId, CompressionFormat format);
    bool SetMaxTextureSize(const std::string& profileId, int size);
    bool SetSRGB(const std::string& profileId, bool srgb);
    bool SetCompressionQuality(const std::string& profileId, float quality);
    const CompressionProfile* GetProfile(const std::string& profileId) const;
    std::vector<std::string> GetAllProfileIds() const;
    std::vector<std::string> GetProfilesByUsage(TextureUsageType usage) const;

    std::string CreateMipChainConfig(const MipChainConfig& config);
    bool RemoveMipChainConfig(const std::string& configId);
    bool SetMipGenFilter(const std::string& configId, MipGenFilter filter);
    bool SetMaxMipLevels(const std::string& configId, int levels);
    const MipChainConfig* GetMipChainConfig(const std::string& configId) const;

    std::string AddFormatOverride(const TextureFormatOverride& override);
    bool RemoveFormatOverride(const std::string& overrideId);
    bool ApplyProfileToAsset(const std::string& profileId, const std::string& assetPath);

    bool ValidateProfile(const std::string& profileId) const;
    bool ExportProfiles(const std::string& filePath) const;
    bool ImportProfiles(const std::string& filePath);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, CompressionProfile> m_profiles;
    std::unordered_map<std::string, MipChainConfig> m_mipConfigs;
    std::unordered_map<std::string, TextureFormatOverride> m_overrides;
    int m_nextProfileIndex{0};
};

} // namespace Atlas::Editor
