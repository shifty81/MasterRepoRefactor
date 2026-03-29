#pragma once
#include <string>
#include <vector>

namespace Atlas::Engine {

/// Phase 17C — Dev Solar System scaffold.
/// Loads and manages a star system from a JSON descriptor.
class SolarSystemManager {
public:
    struct CelestialBody {
        std::string id;
        std::string type;
        std::string name;
        float orbitRadius{0.0f};
        int pcgSeed{0};
    };

    bool LoadFromFile(const std::string& jsonPath);
    bool LoadFromJson(const std::string& jsonString);
    void Unload();

    const std::string& GetSystemId() const { return m_systemId; }
    const std::string& GetSystemName() const { return m_systemName; }
    int GetCelestialCount() const { return static_cast<int>(m_celestials.size()); }
    const CelestialBody* FindCelestial(const std::string& id) const;

private:
    std::string m_systemId;
    std::string m_systemName;
    std::vector<CelestialBody> m_celestials;
    bool m_loaded{false};
};

} // namespace Atlas::Engine
