#pragma once
#include <string>
#include <vector>
#include <functional>
#include <unordered_map>

namespace Atlas::Engine {

/// Phase 25C — Solar system spatial and performance optimizer.
/// Analyses celestial body distributions, LOD boundaries, streaming budgets,
/// and NPC spawn densities to produce an optimisation report with actionable
/// recommendations for the runtime solar system manager.
class SolarSystemOptimizer {
public:
    enum class OptimizationTarget { Memory, CPU, GPU, Streaming, All };
    enum class SeverityLevel { Info, Warning, Error, Critical };
    enum class LODBoundaryPolicy { Static, Dynamic, Adaptive };

    struct CelestialMetrics {
        std::string celestialId;
        std::string name;
        float orbitRadius{1.0f};
        float radius{1000.0f};
        int activeLODLevel{0};
        float streamingPriority{1.0f};
        float memoryBudgetMB{64.0f};
        int activeNPCCount{0};
        bool inStreamingRange{false};
        bool culled{false};
    };

    struct OptimizationHint {
        std::string hintId;
        std::string celestialId;
        SeverityLevel severity{SeverityLevel::Info};
        std::string category;
        std::string message;
        std::string actionCode;
        float estimatedSavingMB{0.0f};
        float estimatedCPUSaving{0.0f};
    };

    struct BudgetThresholds {
        float maxMemoryMB{2048.0f};
        float maxStreamingBandwidthMBps{200.0f};
        int maxVisibleCelestials{32};
        int maxActiveNPCs{500};
        float maxRenderDistanceKm{1000.0f};
        float lodSwitchHysteresis{0.05f};
    };

    struct OptimizationReport {
        std::string systemId;
        OptimizationTarget target{OptimizationTarget::All};
        int celestialsAnalysed{0};
        int hintsGenerated{0};
        int criticalCount{0};
        int warningCount{0};
        float estimatedTotalSavingMB{0.0f};
        std::vector<OptimizationHint> hints;
        std::vector<std::string> appliedActions;
        std::string summary;
        bool budgetExceeded{false};
    };

    // Configuration
    void SetBudgetThresholds(const BudgetThresholds& thresholds);
    const BudgetThresholds& GetBudgetThresholds() const { return m_thresholds; }
    void SetLODBoundaryPolicy(LODBoundaryPolicy policy);
    LODBoundaryPolicy GetLODBoundaryPolicy() const { return m_lodPolicy; }

    // Celestial metrics registration
    bool RegisterCelestial(const CelestialMetrics& metrics);
    bool UnregisterCelestial(const std::string& celestialId);
    bool UpdateCelestialMetrics(const std::string& celestialId,
                                  const CelestialMetrics& metrics);
    bool SetCelestialLOD(const std::string& celestialId, int lodLevel);
    bool SetCelestialStreamingPriority(const std::string& celestialId,
                                        float priority);
    bool SetCelestialNPCCount(const std::string& celestialId, int count);
    int GetRegisteredCount() const { return static_cast<int>(m_celestials.size()); }
    const CelestialMetrics* GetCelestialMetrics(const std::string& celestialId) const;
    std::vector<std::string> GetRegisteredIds() const;

    // Analysis
    OptimizationReport Analyse(const std::string& systemId,
                                 OptimizationTarget target = OptimizationTarget::All);
    bool IsOverMemoryBudget() const;
    bool IsOverNPCBudget() const;
    bool IsOverStreamingBudget(float bandwidthMBps) const;
    float GetTotalEstimatedMemoryMB() const;
    int GetTotalActiveNPCs() const;
    int GetVisibleCelestialCount() const;

    // LOD recommendations
    std::vector<std::string> GetCelestialsNeedingLODIncrease() const;
    std::vector<std::string> GetCelestialsNeedingLODDecrease() const;
    std::vector<std::string> GetCandidatesForCulling() const;

    // Streaming priority
    std::vector<std::pair<std::string, float>> GetSortedByStreamingPriority() const;
    bool RecalculateStreamingPriorities(float playerPosX, float playerPosY,
                                          float playerPosZ);

    // Apply optimisations
    int ApplyAllHints(const OptimizationReport& report);
    bool ApplyHint(const OptimizationHint& hint);

    // Callbacks
    using OptimizationCallback = std::function<void(const OptimizationReport&)>;
    void SetOnAnalysisCompleteCallback(OptimizationCallback cb);
    using BudgetExceededCallback = std::function<void(const std::string& budgetType)>;
    void SetOnBudgetExceededCallback(BudgetExceededCallback cb);

    // Persistence
    bool SaveReport(const OptimizationReport& report,
                     const std::string& filePath) const;
    bool LoadThresholds(const std::string& filePath);
    void Clear();

private:
    BudgetThresholds m_thresholds;
    LODBoundaryPolicy m_lodPolicy{LODBoundaryPolicy::Adaptive};
    std::unordered_map<std::string, CelestialMetrics> m_celestials;
    OptimizationCallback m_onAnalysisComplete;
    BudgetExceededCallback m_onBudgetExceeded;
    int m_nextHintIndex{0};
};

} // namespace Atlas::Engine
