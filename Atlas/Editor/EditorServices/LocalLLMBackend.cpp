#include "LocalLLMBackend.h"

#include <algorithm>
#include <cstdlib>
#include <sstream>
#include <string>

// ---------------------------------------------------------------------------
// Minimal HTTP POST implementation
// Platform note: uses libcurl when available, falls back to a simple
// platform socket approach. Phase 3 will wire this to AtlasEngine's network
// layer for non-blocking requests.
// ---------------------------------------------------------------------------
#if defined(_WIN32)
#  define PLATFORM_WINDOWS
#elif defined(__linux__) || defined(__APPLE__)
#  define PLATFORM_POSIX
#endif

#ifdef PLATFORM_WINDOWS
#  include <winsock2.h>
#  include <ws2tcpip.h>
#  pragma comment(lib, "ws2_32.lib")
#else
#  include <sys/socket.h>
#  include <netdb.h>
#  include <arpa/inet.h>
#  include <unistd.h>
#endif

namespace atlas::ai {

// ---------------------------------------------------------------------------
// System prompt
// ---------------------------------------------------------------------------
const char* LocalLLMBackend::k_systemPrompt =
    "You are an expert C++ and Python developer working on NovaForge, "
    "a PVE space simulator built with C++17 and the custom Atlas Engine "
    "(ECS, OpenGL, AtlasUI). You follow the project's conventions strictly:\n"
    "- snake_case filenames/methods in cpp_server/ and cpp_client/.\n"
    "- PascalCase filenames/methods in engine/ and editor/.\n"
    "- All code in namespace atlas (sub-namespaces: ecs, systems, components, "
    "network, pcg, sim).\n"
    "- ECS systems extend SingleComponentSystem<TComponent>.\n"
    "- Mutating methods return bool. Query methods return safe defaults.\n"
    "- Use atlas::Logger, never std::cout in cpp_server/.\n"
    "- #ifndef NOVAFORGE_<SUBSYSTEM>_<FILE>_H include guards.\n"
    "Always propose minimal, surgical changes. Label every code block with its "
    "file path on the opening fence line, e.g.: ```cpp path/to/file.cpp";

// ---------------------------------------------------------------------------
// Construction
// ---------------------------------------------------------------------------
LocalLLMBackend::LocalLLMBackend(
    const std::string& baseUrl,
    const std::string& model,
    int                timeoutMs)
    : m_baseUrl(baseUrl.empty()
          ? EnvOrDefault("NOVAFORGE_LLM_URL", "http://localhost:11434")
          : baseUrl)
    , m_model(model.empty()
          ? EnvOrDefault("NOVAFORGE_LLM_MODEL", "deepseek-coder")
          : model)
    , m_timeoutMs(timeoutMs)
{
}

// ---------------------------------------------------------------------------
// Configuration setters
// ---------------------------------------------------------------------------
void LocalLLMBackend::SetBaseUrl(const std::string& url) { m_baseUrl = url; }
void LocalLLMBackend::SetModel(const std::string& model)  { m_model  = model; }
void LocalLLMBackend::SetTimeout(int ms)                  { m_timeoutMs = ms; }

// ---------------------------------------------------------------------------
// Availability check
// ---------------------------------------------------------------------------
bool LocalLLMBackend::IsAvailable() const {
    // Quick /api/tags ping — low timeout
    const std::string quickUrl = m_baseUrl + "/api/tags";
    // We just need to see if the server responds; ignore the body.
    const std::string body = HttpPost(quickUrl, "{}");
    return !body.empty();
}

// ---------------------------------------------------------------------------
// Query
// ---------------------------------------------------------------------------
AIResponse LocalLLMBackend::Query(const std::string& prompt,
                                   const AIContext&   context) {
    if (prompt.empty()) {
        return AIResponse{"", 0.0f};
    }

    const std::string url     = m_baseUrl + "/api/chat";
    const std::string payload = BuildPayload(prompt, context);
    const std::string raw     = HttpPost(url, payload);

    if (raw.empty()) {
        // Server unreachable — zero confidence so AIAggregator falls back
        return AIResponse{
            "Local LLM unavailable. Is Ollama running? Run: ollama serve",
            0.0f
        };
    }

    std::string text = ParseResponse(raw);
    if (text.empty()) {
        return AIResponse{"LLM returned an empty response.", 0.1f};
    }

    // High confidence — this is a real LLM response
    return AIResponse{std::move(text), 0.95f};
}

// ---------------------------------------------------------------------------
// Build JSON payload for /api/chat
// ---------------------------------------------------------------------------
std::string LocalLLMBackend::BuildPayload(const std::string& prompt,
                                           const AIContext&   context) const {
    // Build a minimal JSON string for the Ollama /api/chat endpoint.
    // Using manual serialization to avoid external JSON dependencies.
    auto esc = [](const std::string& s) -> std::string {
        std::string out;
        out.reserve(s.size());
        for (char c : s) {
            switch (c) {
                case '"':  out += "\\\""; break;
                case '\\': out += "\\\\"; break;
                case '\n': out += "\\n";  break;
                case '\r': out += "\\r";  break;
                case '\t': out += "\\t";  break;
                default:   out += c;      break;
            }
        }
        return out;
    };

    // Assemble context string
    std::ostringstream ctx;
    if (!context.projectName.empty())
        ctx << "Project: " << context.projectName << "\n";
    if (!context.selectedAsset.empty())
        ctx << "Selected asset: " << context.selectedAsset << "\n";
    if (!context.networkMode.empty())
        ctx << "Network mode: " << context.networkMode << "\n";

    std::string userContent = ctx.str().empty()
        ? prompt
        : ctx.str() + "\n" + prompt;

    std::ostringstream json;
    json << "{"
         << "\"model\":\"" << esc(m_model) << "\","
         << "\"stream\":false,"
         << "\"messages\":["
         <<   "{\"role\":\"system\",\"content\":\"" << esc(k_systemPrompt) << "\"},"
         <<   "{\"role\":\"user\",\"content\":\"" << esc(userContent) << "\"}"
         << "]"
         << "}";
    return json.str();
}

// ---------------------------------------------------------------------------
// Parse the response body
// ---------------------------------------------------------------------------
std::string LocalLLMBackend::ParseResponse(const std::string& body) {
    // Extract the "content" field from the JSON response.
    // Pattern:  "content":"<value>"
    // This is intentionally simple to avoid JSON lib dependencies.
    const std::string key = "\"content\":\"";
    const size_t start    = body.find(key);
    if (start == std::string::npos) return "";

    size_t pos = start + key.size();
    std::string result;
    while (pos < body.size()) {
        char c = body[pos++];
        if (c == '\\' && pos < body.size()) {
            char esc = body[pos++];
            switch (esc) {
                case '"':  result += '"';  break;
                case '\\': result += '\\'; break;
                case 'n':  result += '\n'; break;
                case 'r':  result += '\r'; break;
                case 't':  result += '\t'; break;
                default:   result += esc;  break;
            }
        } else if (c == '"') {
            break;  // end of content string
        } else {
            result += c;
        }
    }
    return result;
}

// ---------------------------------------------------------------------------
// Minimal HTTP POST (synchronous, blocking)
// ---------------------------------------------------------------------------
std::string LocalLLMBackend::HttpPost(const std::string& url,
                                       const std::string& jsonBody) const {
    // Parse URL into host, port, path
    std::string host, path;
    int port = 80;

    std::string stripped = url;
    if (stripped.substr(0, 7) == "http://")  stripped = stripped.substr(7);
    if (stripped.substr(0, 8) == "https://") stripped = stripped.substr(8);

    const size_t slashPos = stripped.find('/');
    const std::string hostPort = (slashPos != std::string::npos)
        ? stripped.substr(0, slashPos)
        : stripped;
    path = (slashPos != std::string::npos) ? stripped.substr(slashPos) : "/";

    const size_t colonPos = hostPort.find(':');
    if (colonPos != std::string::npos) {
        host = hostPort.substr(0, colonPos);
        port = std::stoi(hostPort.substr(colonPos + 1));
    } else {
        host = hostPort;
    }

    // Build HTTP/1.1 request
    std::ostringstream req;
    req << "POST " << path << " HTTP/1.1\r\n"
        << "Host: " << host << ":" << port << "\r\n"
        << "Content-Type: application/json\r\n"
        << "Content-Length: " << jsonBody.size() << "\r\n"
        << "Connection: close\r\n"
        << "\r\n"
        << jsonBody;
    const std::string request = req.str();

    // Connect and send (use getaddrinfo on both platforms for thread-safety)
#ifdef PLATFORM_WINDOWS
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);
#endif

    std::string response;

    {
        struct addrinfo hints{}, *res = nullptr;
        hints.ai_family   = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;
        if (getaddrinfo(host.c_str(), std::to_string(port).c_str(), &hints, &res) != 0) {
#ifdef PLATFORM_WINDOWS
            WSACleanup();
#endif
            return "";
        }

#ifdef PLATFORM_WINDOWS
        SOCKET sock = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
        if (sock == INVALID_SOCKET) { freeaddrinfo(res); WSACleanup(); return ""; }

        DWORD timeout_ms = static_cast<DWORD>(m_timeoutMs);
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO,
                   reinterpret_cast<const char*>(&timeout_ms), sizeof(timeout_ms));
        setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO,
                   reinterpret_cast<const char*>(&timeout_ms), sizeof(timeout_ms));

        if (connect(sock, res->ai_addr, static_cast<int>(res->ai_addrlen)) != 0) {
            closesocket(sock); freeaddrinfo(res); WSACleanup(); return "";
        }
        freeaddrinfo(res);

        send(sock, request.c_str(), static_cast<int>(request.size()), 0);

        char buf[4096];
        int n;
        while ((n = recv(sock, buf, sizeof(buf) - 1, 0)) > 0) {
            buf[n] = '\0';
            response += buf;
        }
        closesocket(sock);
        WSACleanup();
#else
        int sock = ::socket(res->ai_family, res->ai_socktype, res->ai_protocol);
        if (sock < 0) { freeaddrinfo(res); return ""; }

        struct timeval tv{};
        tv.tv_sec  = m_timeoutMs / 1000;
        tv.tv_usec = (m_timeoutMs % 1000) * 1000;
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
        setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));

        if (::connect(sock, res->ai_addr, res->ai_addrlen) != 0) {
            ::close(sock); freeaddrinfo(res); return "";
        }
        freeaddrinfo(res);

        ::send(sock, request.c_str(), request.size(), 0);

        char buf[4096];
        ssize_t n;
        while ((n = ::recv(sock, buf, sizeof(buf) - 1, 0)) > 0) {
            buf[n] = '\0';
            response += buf;
        }
        ::close(sock);
#endif
    }

    // Strip HTTP headers (everything before the first blank line)
    const size_t bodyStart = response.find("\r\n\r\n");
    if (bodyStart != std::string::npos)
        return response.substr(bodyStart + 4);
    return response;
}

// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------
std::string LocalLLMBackend::EnvOrDefault(const char* name,
                                            const char* fallback) {
    const char* val = std::getenv(name);
    return (val && val[0] != '\0') ? std::string(val) : std::string(fallback);
}

} // namespace atlas::ai
