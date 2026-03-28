// RenderViewport.cpp
// Atlas Engine — scene viewport renderer.

#include "Rendering/RenderViewport.h"

#include <algorithm>

namespace atlas::rendering {

bool RenderViewport::Initialize(const ViewportConfig& cfg)
{
    m_config      = cfg;
    m_frameNumber = 0;
    m_initialized = true;

    // All layers enabled by default.
    for (uint8_t i = 0; i <= static_cast<uint8_t>(ERenderLayer::ImGui); ++i)
        m_layerEnabled[i] = true;

    // Apply config-level flags.
    if (!cfg.enableDebug)        m_layerEnabled[static_cast<uint8_t>(ERenderLayer::DebugOverlay)] = false;
    if (!cfg.enableEditorOverlay) m_layerEnabled[static_cast<uint8_t>(ERenderLayer::EditorOverlay)] = false;
    if (!cfg.enableHUD)           m_layerEnabled[static_cast<uint8_t>(ERenderLayer::HUD)] = false;

    return true;
}

void RenderViewport::Shutdown()
{
    m_chunks.clear();
    m_entities.clear();
    m_debugLines.clear();
    m_debugTexts.clear();
    m_hudElems.clear();
    m_highlights.clear();
    m_passDelegates.clear();
    m_initialized = false;
}

void RenderViewport::Resize(uint32_t width, uint32_t height)
{
    m_config.width  = width;
    m_config.height = height;
}

// ---- scene submission ---------------------------------------------------

void RenderViewport::SubmitVoxelChunk(const VoxelChunkDrawable& chunk)
{
    m_chunks.push_back(chunk);
}

void RenderViewport::SubmitEntity(const EntityDrawable& entity)
{
    m_entities.push_back(entity);
}

void RenderViewport::SubmitDebugLine(const DebugLine& line)
{
    m_debugLines.push_back(line);
}

void RenderViewport::SubmitDebugText(const DebugText& text)
{
    m_debugTexts.push_back(text);
}

void RenderViewport::SubmitHUDElement(const HUDElement& elem)
{
    // Deduplicate by ID.
    for (auto& e : m_hudElems)
        if (e.id == elem.id) { e = elem; return; }
    m_hudElems.push_back(elem);
}

void RenderViewport::SubmitSelectionHighlight(const SelectionHighlight& sel)
{
    m_highlights.push_back(sel);
}

bool RenderViewport::UpdateHUDElement(const std::string& id, const std::string& newText)
{
    for (auto& e : m_hudElems)
    {
        if (e.id == id) { e.text = newText; return true; }
    }
    return false;
}

bool RenderViewport::SetHUDElementVisible(const std::string& id, bool visible)
{
    for (auto& e : m_hudElems)
    {
        if (e.id == id) { e.visible = visible; return true; }
    }
    return false;
}

// ---- pass delegates -----------------------------------------------------

void RenderViewport::RegisterPassDelegate(ERenderLayer layer, RenderPassDelegate fn)
{
    m_passDelegates[static_cast<uint8_t>(layer)] = std::move(fn);
}

// ---- render loop --------------------------------------------------------

void RenderViewport::BeginFrame()
{
    m_stats.clear();
    m_debugLines.clear();
    m_debugTexts.clear();
    m_highlights.clear();
}

void RenderViewport::RenderFrame()
{
    if (!m_initialized) return;

    static constexpr ERenderLayer kLayerOrder[] = {
        ERenderLayer::Background,
        ERenderLayer::VoxelChunks,
        ERenderLayer::Entities,
        ERenderLayer::Transparent,
        ERenderLayer::DebugOverlay,
        ERenderLayer::HUD,
        ERenderLayer::EditorOverlay,
        ERenderLayer::ImGui,
    };

    for (ERenderLayer layer : kLayerOrder)
    {
        if (IsLayerEnabled(layer))
            ExecutePass(layer);
    }

    ++m_frameNumber;
}

void RenderViewport::EndFrame()
{
    // Persistent drawables (chunks, entities, HUD) survive frame boundaries.
    // Per-frame drawables (debug lines, highlights) are cleared in BeginFrame.
}

void RenderViewport::ExecutePass(ERenderLayer layer)
{
    RenderPassStats stats;
    stats.layer = layer;

    auto it = m_passDelegates.find(static_cast<uint8_t>(layer));
    if (it != m_passDelegates.end())
        it->second(layer, m_config);

    // Count stub draw calls from submitted data.
    switch (layer)
    {
        case ERenderLayer::VoxelChunks:
            stats.drawCalls = static_cast<uint32_t>(m_chunks.size());
            break;
        case ERenderLayer::Entities:
            stats.drawCalls = static_cast<uint32_t>(m_entities.size());
            break;
        case ERenderLayer::DebugOverlay:
            stats.drawCalls = static_cast<uint32_t>(m_debugLines.size() +
                                                      m_debugTexts.size());
            break;
        case ERenderLayer::HUD:
            stats.drawCalls = static_cast<uint32_t>(m_hudElems.size());
            break;
        case ERenderLayer::EditorOverlay:
            stats.drawCalls = static_cast<uint32_t>(m_highlights.size());
            break;
        default:
            break;
    }
    m_stats.push_back(stats);
}

// ---- layer toggles ------------------------------------------------------

void RenderViewport::SetLayerEnabled(ERenderLayer layer, bool enabled)
{
    m_layerEnabled[static_cast<uint8_t>(layer)] = enabled;
}

bool RenderViewport::IsLayerEnabled(ERenderLayer layer) const
{
    auto it = m_layerEnabled.find(static_cast<uint8_t>(layer));
    return (it != m_layerEnabled.end()) ? it->second : true;
}

} // namespace atlas::rendering
