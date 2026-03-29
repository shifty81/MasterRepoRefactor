#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 20D — Registry for runtime content packs that can be loaded,
/// unloaded, and queried without a full engine restart.  Works in concert
/// with the Python content_pack_loader for cross-boundary pack management.
class ContentPackRegistry {
public:
    enum class PackState { Unloaded, Loading, Loaded, Failed };

    struct PackRecord {
        std::string packId;
        std::string name;
        std::string version;
        std::string manifestPath;
        PackState state{PackState::Unloaded};
        int assetCount{0};
    };

    // Registration
    bool RegisterPack(const std::string& packId, const std::string& name,
                      const std::string& version, const std::string& manifestPath);
    bool UnregisterPack(const std::string& packId);
    bool IsRegistered(const std::string& packId) const;
    int GetPackCount() const { return static_cast<int>(m_packs.size()); }

    // Load / unload
    bool LoadPack(const std::string& packId);
    bool UnloadPack(const std::string& packId);
    bool IsLoaded(const std::string& packId) const;
    int GetLoadedCount() const;

    // Lookup
    const PackRecord* GetPack(const std::string& packId) const;
    std::vector<std::string> GetAllPackIds() const;
    std::vector<PackRecord> GetLoadedPacks() const;

    // Asset count bookkeeping
    bool SetAssetCount(const std::string& packId, int count);

    // Traversal
    void ForEach(const std::function<void(const PackRecord&)>& fn) const;

    // Lifecycle
    void Clear();

    // Callbacks
    void SetOnPackLoadedCallback(std::function<void(const std::string&)> cb);
    void SetOnPackUnloadedCallback(std::function<void(const std::string&)> cb);

private:
    std::unordered_map<std::string, PackRecord> m_packs;
    std::function<void(const std::string&)> m_onLoaded;
    std::function<void(const std::string&)> m_onUnloaded;
};

} // namespace Atlas::Engine
