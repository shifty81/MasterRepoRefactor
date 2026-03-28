#pragma once
/**
 * MasterLogger.h — Shared C++ logging header for MasterRepo.
 *
 * Provides a lightweight, zero-dependency logging interface that all C++
 * components (Atlas, NovaForge gameplay systems, Services, etc.) can include
 * without pulling in any third-party library.
 *
 * Features
 * --------
 * - Five severity levels: DEBUG, INFO, WARN, ERROR, FATAL
 * - Thread-safe output via std::mutex
 * - Dual sink: console (stderr) + optional rotating log file
 * - Timestamped entries in ISO 8601 format
 * - Convenience macros: MR_LOG_DEBUG, MR_LOG_INFO, MR_LOG_WARN,
 *   MR_LOG_ERROR, MR_LOG_FATAL
 *
 * Quick start
 * -----------
 * @code
 * #include "Shared/Logging/MasterLogger.h"
 *
 * int main() {
 *     MasterLogger::Init("./Logs/myapp", "myapp.log");
 *     MR_LOG_INFO("Application started");
 *     MR_LOG_ERROR("Something went wrong: " << message);
 *     MasterLogger::Shutdown();
 * }
 * @endcode
 */

#include <chrono>
#include <cstdio>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <sstream>
#include <string>
#include <string_view>

#ifdef _WIN32
#  include <direct.h>
#  define MR_MKDIR(p) ::_mkdir(p)
#else
#  include <sys/stat.h>
#  define MR_MKDIR(p) ::mkdir((p), 0755)
#endif

namespace MasterRepo {

enum class LogLevel : int { DEBUG = 0, INFO = 1, WARN = 2, ERR = 3, FATAL = 4 };

class MasterLogger
{
public:
    // ── Lifecycle ────────────────────────────────────────────────────────────

    /** Initialise the singleton.  Call once from main() or App::Initialize().
     *  @param logDir   Directory for the log file (created if it does not exist).
     *  @param filename Log file name, e.g. "server.log".
     *  @param minLevel Minimum level to emit (default: DEBUG).
     */
    static void Init(
        std::string_view logDir  = "./Logs",
        std::string_view filename = "masterrepo.log",
        LogLevel         minLevel = LogLevel::DEBUG)
    {
        auto& inst = instance();
        std::lock_guard<std::mutex> lk(inst.m_mutex);
        inst.m_minLevel = minLevel;

        // Create directory (ignore error if it already exists)
        std::string dir(logDir);
        MR_MKDIR(dir.c_str());

        std::string path = dir + "/" + std::string(filename);
        inst.m_file.open(path, std::ios::app);
        if (!inst.m_file.is_open()) {
            std::cerr << "[MasterLogger] WARNING: cannot open log file: " << path << "\n";
        }
        inst.m_initialised = true;
        inst.writeRaw(LogLevel::INFO, "MasterLogger", "Logger initialised — " + path);
    }

    /** Flush and close the log file. */
    static void Shutdown() {
        auto& inst = instance();
        std::lock_guard<std::mutex> lk(inst.m_mutex);
        if (inst.m_file.is_open()) {
            inst.writeRaw(LogLevel::INFO, "MasterLogger", "Logger shutting down.");
            inst.m_file.close();
        }
    }

    // ── Logging interface ────────────────────────────────────────────────────

    static void Log(LogLevel level, std::string_view tag, std::string_view message) {
        instance().write(level, tag, message);
    }

    static void Debug(std::string_view tag, std::string_view msg) { Log(LogLevel::DEBUG, tag, msg); }
    static void Info (std::string_view tag, std::string_view msg) { Log(LogLevel::INFO,  tag, msg); }
    static void Warn (std::string_view tag, std::string_view msg) { Log(LogLevel::WARN,  tag, msg); }
    static void Error(std::string_view tag, std::string_view msg) { Log(LogLevel::ERR,   tag, msg); }
    static void Fatal(std::string_view tag, std::string_view msg) { Log(LogLevel::FATAL, tag, msg); }

    /** Set the minimum log level at runtime. */
    static void SetLevel(LogLevel level) {
        std::lock_guard<std::mutex> lk(instance().m_mutex);
        instance().m_minLevel = level;
    }

private:
    MasterLogger() = default;

    static MasterLogger& instance() {
        static MasterLogger s_instance;
        return s_instance;
    }

    static std::string levelStr(LogLevel l) {
        switch (l) {
            case LogLevel::DEBUG: return "DEBUG";
            case LogLevel::INFO:  return "INFO ";
            case LogLevel::WARN:  return "WARN ";
            case LogLevel::ERR:   return "ERROR";
            case LogLevel::FATAL: return "FATAL";
        }
        return "?????";
    }

    static std::string timestamp() {
        using namespace std::chrono;
        auto now   = system_clock::now();
        auto t     = system_clock::to_time_t(now);
        auto ms    = duration_cast<milliseconds>(now.time_since_epoch()) % 1000;
        std::tm tm_buf{};
#ifdef _WIN32
        ::localtime_s(&tm_buf, &t);
#else
        ::localtime_r(&t, &tm_buf);
#endif
        std::ostringstream oss;
        oss << std::put_time(&tm_buf, "%Y-%m-%d %H:%M:%S")
            << '.' << std::setfill('0') << std::setw(3) << ms.count();
        return oss.str();
    }

    void write(LogLevel level, std::string_view tag, std::string_view message) {
        std::lock_guard<std::mutex> lk(m_mutex);
        if (static_cast<int>(level) < static_cast<int>(m_minLevel)) return;
        writeRaw(level, tag, message);
    }

    // Must be called with m_mutex held.
    void writeRaw(LogLevel level, std::string_view tag, std::string_view message) {
        std::string line = timestamp()
                         + " [" + levelStr(level) + "] "
                         + std::string(tag) + ": "
                         + std::string(message);
        // Console (stderr so it doesn't pollute stdout captures)
        std::cerr << line << "\n";
        // File
        if (m_file.is_open()) {
            m_file << line << "\n";
            m_file.flush();
        }
    }

    std::mutex   m_mutex;
    std::ofstream m_file;
    LogLevel     m_minLevel  = LogLevel::DEBUG;
    bool         m_initialised = false;
};

} // namespace MasterRepo

// ── Convenience macros ────────────────────────────────────────────────────────
// Usage: MR_LOG_INFO("value = " << x)
#define MR_LOG_TAG  ([]{ \
    constexpr std::string_view f = __FILE__; \
    auto p = f.rfind('/');  if (p == std::string_view::npos) p = f.rfind('\\'); \
    return (p == std::string_view::npos) ? f : f.substr(p + 1); }())

#define MR_LOG(level, msg) do { \
    std::ostringstream _mr_ss; _mr_ss << msg; \
    ::MasterRepo::MasterLogger::Log(::MasterRepo::LogLevel::level, MR_LOG_TAG, _mr_ss.str()); \
} while(0)

#define MR_LOG_DEBUG(msg) MR_LOG(DEBUG, msg)
#define MR_LOG_INFO(msg)  MR_LOG(INFO,  msg)
#define MR_LOG_WARN(msg)  MR_LOG(WARN,  msg)
#define MR_LOG_ERROR(msg) MR_LOG(ERR,   msg)
#define MR_LOG_FATAL(msg) MR_LOG(FATAL, msg)
