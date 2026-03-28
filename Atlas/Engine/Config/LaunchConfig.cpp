// LaunchConfig.cpp
// Atlas Engine — runtime launch configuration implementation.

#include "LaunchConfig.h"
#include <sstream>
#include <algorithm>
#include <stdexcept>

namespace atlas
{

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

static std::string ToLower(std::string s)
{
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    return s;
}

ELaunchMode LaunchConfig::ParseMode(const std::string& s, bool& ok)
{
    ok = true;
    std::string lower = ToLower(s);
    if (lower == "game")     return ELaunchMode::Game;
    if (lower == "editor")   return ELaunchMode::Editor;
    if (lower == "server")   return ELaunchMode::Server;
    if (lower == "playtest") return ELaunchMode::Playtest;
    ok = false;
    return ELaunchMode::Game;
}

// ---------------------------------------------------------------------------
// Parse (argc/argv)
// ---------------------------------------------------------------------------

bool LaunchConfig::Parse(int argc, char* argv[])
{
    std::vector<std::string> args;
    args.reserve(static_cast<size_t>(argc));
    for (int i = 1; i < argc; ++i)
        args.emplace_back(argv[i]);
    return Parse(args);
}

// ---------------------------------------------------------------------------
// Parse (token list)
// ---------------------------------------------------------------------------

bool LaunchConfig::Parse(const std::vector<std::string>& args)
{
    m_error.clear();

    for (size_t i = 0; i < args.size(); ++i)
    {
        const std::string& tok = args[i];

        auto nextVal = [&]() -> std::string {
            if (i + 1 < args.size()) return args[++i];
            return {};
        };

        if (tok == "--mode")
        {
            bool ok = false;
            m_params.mode = ParseMode(nextVal(), ok);
            if (!ok) { m_error = "Unknown mode value"; return false; }
        }
        else if (tok == "--config")
        {
            m_params.configFile = nextVal();
        }
        else if (tok == "--repo-root")
        {
            m_params.repoRoot = nextVal();
        }
        else if (tok == "--save")
        {
            m_params.saveName = nextVal();
        }
        else if (tok == "--headless")
        {
            m_params.headless = true;
        }
        else if (tok == "--bridge")
        {
            m_params.enableBridge = true;
        }
        else if (tok == "--bridge-port")
        {
            try {
                m_params.bridgePort = static_cast<uint16_t>(std::stoi(nextVal()));
            } catch (...) {
                m_error = "Invalid bridge-port value";
                return false;
            }
        }
        else if (tok == "--dev")
        {
            m_params.devMode = true;
        }
        else if (tok.rfind("--", 0) == 0)
        {
            m_error = "Unrecognised argument: " + tok;
            return false;
        }
        else
        {
            m_params.extraArgs.push_back(tok);
        }
    }
    return true;
}

// ---------------------------------------------------------------------------
// Describe
// ---------------------------------------------------------------------------

std::string LaunchConfig::Describe() const
{
    static const char* kModeNames[] = { "Game", "Editor", "Server", "Playtest" };
    std::ostringstream ss;
    ss << "LaunchConfig { mode=" << kModeNames[static_cast<int>(m_params.mode)];
    if (!m_params.configFile.empty()) ss << " config=" << m_params.configFile;
    if (!m_params.repoRoot.empty())   ss << " repo-root=" << m_params.repoRoot;
    if (!m_params.saveName.empty())   ss << " save=" << m_params.saveName;
    if (m_params.headless)            ss << " headless";
    if (m_params.enableBridge)        ss << " bridge(port=" << m_params.bridgePort << ")";
    if (m_params.devMode)             ss << " dev";
    ss << " }";
    return ss.str();
}

} // namespace atlas
