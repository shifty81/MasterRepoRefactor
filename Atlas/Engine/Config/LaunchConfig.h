// LaunchConfig.h
// Atlas Engine — runtime launch configuration parsed from CLI args and config file.

#pragma once
#include <string>
#include <vector>
#include <cstdint>

namespace atlas
{

/// The execution mode requested at startup.
enum class ELaunchMode : uint8_t
{
    Game,       ///< NovaForge game client (full HUD, no editor panels)
    Editor,     ///< Atlas editor shell with AtlasAI integration
    Server,     ///< NovaForge headless dedicated server
    Playtest,   ///< Automated PlaytestSession smoke-test run (headless)
};

/// Configuration resolved by LaunchConfig::Parse().
struct LaunchParams
{
    ELaunchMode mode          = ELaunchMode::Game;
    std::string configFile;           ///< Path to project config JSON (optional)
    std::string repoRoot;             ///< Explicit repo root override (optional)
    std::string saveName;             ///< Save slot to load at startup (optional)
    bool        headless      = false;///< Suppress all window creation
    bool        enableBridge  = false;///< Start AtlasAI bridge server
    bool        devMode       = false;///< Enable F12 dev overlay at startup
    uint16_t    bridgePort    = 8765; ///< Bridge server port
    std::vector<std::string> extraArgs;
};

/// Parses command-line arguments into a LaunchParams struct.
///
/// Recognised flags:
///   --mode <game|editor|server|playtest>
///   --config <path>
///   --repo-root <path>
///   --save <name>
///   --headless
///   --bridge [--bridge-port <port>]
///   --dev
class LaunchConfig
{
public:
    LaunchConfig() = default;

    /// Parse argc/argv as supplied to main().  Returns true on success.
    bool Parse(int argc, char* argv[]);

    /// Parse a pre-tokenised list of arguments (useful for tests).
    bool Parse(const std::vector<std::string>& args);

    const LaunchParams& Params() const { return m_params; }

    /// Human-readable string describing the resolved configuration.
    std::string Describe() const;

    /// True if Parse() encountered an unrecognised or invalid argument.
    bool HasError() const { return !m_error.empty(); }
    const std::string& Error() const { return m_error; }

private:
    LaunchParams m_params;
    std::string  m_error;

    bool ApplyFlag(const std::string& key, const std::string& value);
    static ELaunchMode ParseMode(const std::string& s, bool& ok);
};

} // namespace atlas
