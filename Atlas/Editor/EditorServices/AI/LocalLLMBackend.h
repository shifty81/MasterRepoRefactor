#pragma once
#include "AIAggregator.h"
#include <string>
#include <atomic>

namespace atlas::ai {

/**
 * @brief AI backend that calls a locally running LLM server (Ollama / LM Studio).
 *
 * This backend connects to an Ollama or OpenAI-compatible REST API running
 * on localhost — no internet connection required.
 *
 * It provides the highest-quality AI responses of all backends and is
 * selected by AIAggregator when available (confidence 0.95 vs TemplateAIBackend's max 1.0).
 *
 * Setup:
 *   1. Install Ollama: https://ollama.com
 *   2. Pull a model:   ollama pull deepseek-coder
 *   3. Serve:          ollama serve   (runs automatically on port 11434)
 *
 * Environment variables (read at startup):
 *   NOVAFORGE_LLM_URL    Base URL (default: http://localhost:11434)
 *   NOVAFORGE_LLM_MODEL  Model name (default: deepseek-coder)
 */
class LocalLLMBackend : public AIBackend {
public:
    /**
     * @param baseUrl  Ollama or OpenAI-compatible base URL.
     * @param model    Model name (e.g. "deepseek-coder", "codellama:13b").
     * @param timeoutMs HTTP request timeout in milliseconds.
     */
    explicit LocalLLMBackend(
        const std::string& baseUrl   = "",
        const std::string& model     = "",
        int                timeoutMs = 30000);

    ~LocalLLMBackend() override = default;

    AIResponse Query(const std::string& prompt,
                     const AIContext&   context) override;

    // ── Configuration ─────────────────────────────────────────────

    void SetBaseUrl(const std::string& url);
    void SetModel(const std::string& model);
    void SetTimeout(int ms);

    /** Test connectivity to the LLM server (non-blocking, quick). */
    bool IsAvailable() const;

    const std::string& GetModel()   const { return m_model;   }
    const std::string& GetBaseUrl() const { return m_baseUrl; }

private:
    std::string m_baseUrl;
    std::string m_model;
    int         m_timeoutMs;

    // System prompt injected before every user message
    static const char* k_systemPrompt;

    /**
     * Send a synchronous HTTP POST to the Ollama /api/chat endpoint.
     * Returns the response body, or empty string on failure.
     *
     * NOTE: Uses a minimal HTTP implementation (libcurl or platform sockets).
     * Phase 3 integration wires this to the engine's net layer for async.
     */
    std::string HttpPost(const std::string& url,
                         const std::string& jsonBody) const;

    /** Build the JSON payload for the /api/chat endpoint. */
    std::string BuildPayload(const std::string& prompt,
                             const AIContext&   context) const;

    /** Parse the response text from the JSON reply. */
    static std::string ParseResponse(const std::string& body);

    /** Read an env var, returning fallback if not set. */
    static std::string EnvOrDefault(const char* name,
                                    const char* fallback);
};

} // namespace atlas::ai
