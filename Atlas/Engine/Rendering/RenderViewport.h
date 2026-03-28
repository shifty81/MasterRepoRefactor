// RenderViewport.h
// Atlas Engine — scene viewport renderer with layered render passes:
// voxel chunks, entities/modules, debug overlays, runtime HUD, editor overlays.

#pragma once
#include <cstdint>
#include <functional>
#include <string>
#include <vector>

namespace atlas::rendering {

// ---------------------------------------------------------------------------
// Render layer ordering
// ---------------------------------------------------------------------------

enum class ERenderLayer : uint8_t
{
    Background   = 0,  ///< skybox / clear colour
    VoxelChunks  = 1,  ///< terrain voxel geometry
    Entities     = 2,  ///< ships, modules, characters
    Transparent  = 3,  ///< transparent meshes, particles
    DebugOverlay = 4,  ///< debug wireframes, bounds, nav
    HUD          = 5,  ///< runtime HUD (health, speed, etc.)
    EditorOverlay= 6,  ///< selection highlights, gizmos, grid
    ImGui        = 7,  ///< dear-imgui / editor panels
};

// ---------------------------------------------------------------------------
// Per-pass stats (diagnostic)
// ---------------------------------------------------------------------------

struct RenderPassStats
{
    ERenderLayer layer         = ERenderLayer::Background;
    uint32_t     drawCalls     = 0;
    uint32_t     triangles     = 0;
    float        gpuTimeMs     = 0.f;
};

// ---------------------------------------------------------------------------
// Viewport configuration
// ---------------------------------------------------------------------------

struct ViewportConfig
{
    uint32_t width          = 1280;
    uint32_t height         = 720;
    float    fovDegrees     = 75.f;
    float    nearPlane      = 0.1f;
    float    farPlane       = 10000.f;
    bool     enableDebug    = false;
    bool     enableEditorOverlay = false;
    bool     enableHUD      = true;
    bool     wireframe      = false;
    bool     enableGrid     = false;
};

// ---------------------------------------------------------------------------
// Camera state
// ---------------------------------------------------------------------------

struct CameraState
{
    float posX = 0.f, posY = 0.f, posZ = 0.f;
    float yaw  = 0.f, pitch = 0.f, roll = 0.f;  ///< Euler degrees
    float fovDegrees = 75.f;
};

// ---------------------------------------------------------------------------
// Scene drawable primitives (minimal representation)
// ---------------------------------------------------------------------------

struct VoxelChunkDrawable
{
    uint64_t    chunkId    = 0;
    float       worldX = 0.f, worldY = 0.f, worldZ = 0.f;
    bool        isDirty    = false;
    uint32_t    meshHandle = 0; ///< opaque GPU handle
};

struct EntityDrawable
{
    uint64_t    entityId   = 0;
    std::string meshId;
    float       posX = 0.f, posY = 0.f, posZ = 0.f;
    float       rotY = 0.f;
    float       scale = 1.f;
    bool        isSelected = false;
};

struct DebugLine
{
    float x0, y0, z0, x1, y1, z1;
    uint32_t colourRGBA = 0xFF0000FF; ///< default red
};

struct DebugText
{
    float       worldX, worldY, worldZ;
    std::string text;
    uint32_t    colourRGBA = 0xFFFFFFFF;
};

// ---------------------------------------------------------------------------
// HUD element (simple 2D overlay)
// ---------------------------------------------------------------------------

struct HUDElement
{
    std::string id;
    std::string text;
    float       screenX = 0.f;  ///< 0-1 normalised
    float       screenY = 0.f;
    bool        visible = true;
};

// ---------------------------------------------------------------------------
// Selection highlight (editor overlay)
// ---------------------------------------------------------------------------

struct SelectionHighlight
{
    uint64_t    entityId = 0;
    uint32_t    colourRGBA = 0x00FF88FF;
    bool        drawWireframe = true;
    bool        drawBounds    = true;
};

// ---------------------------------------------------------------------------
// RenderViewport
// ---------------------------------------------------------------------------

/// Delegate type for each render pass — real backend will implement OpenGL/Vulkan etc.
using RenderPassDelegate = std::function<void(ERenderLayer, const ViewportConfig&)>;

class RenderViewport
{
public:
    RenderViewport()  = default;
    ~RenderViewport() = default;

    bool Initialize(const ViewportConfig& cfg);
    void Shutdown();

    // ---- configuration ----------------------------------------------
    void SetConfig(const ViewportConfig& cfg) { m_config = cfg; }
    const ViewportConfig& GetConfig()   const { return m_config; }
    void Resize(uint32_t width, uint32_t height);

    // ---- camera -----------------------------------------------------
    void SetCamera(const CameraState& cam) { m_camera = cam; }
    const CameraState& GetCamera()   const { return m_camera; }

    // ---- scene submission -------------------------------------------
    void SubmitVoxelChunk(const VoxelChunkDrawable& chunk);
    void SubmitEntity(const EntityDrawable& entity);
    void SubmitDebugLine(const DebugLine& line);
    void SubmitDebugText(const DebugText& text);
    void SubmitHUDElement(const HUDElement& elem);
    void SubmitSelectionHighlight(const SelectionHighlight& sel);

    // ---- update HUD element -----------------------------------------
    bool UpdateHUDElement(const std::string& id, const std::string& newText);
    bool SetHUDElementVisible(const std::string& id, bool visible);

    // ---- per-pass delegate registration -----------------------------
    void RegisterPassDelegate(ERenderLayer layer, RenderPassDelegate fn);

    // ---- main render call -------------------------------------------
    void BeginFrame();
    void RenderFrame();
    void EndFrame();

    // ---- layer enable toggles ---------------------------------------
    void SetLayerEnabled(ERenderLayer layer, bool enabled);
    bool IsLayerEnabled(ERenderLayer layer) const;

    // ---- diagnostics ------------------------------------------------
    const std::vector<RenderPassStats>& GetLastFrameStats() const { return m_stats; }
    uint64_t                            GetFrameNumber()    const { return m_frameNumber; }

    // ---- getters for submitted drawables ----------------------------
    const std::vector<VoxelChunkDrawable>&   GetVoxelChunks()   const { return m_chunks; }
    const std::vector<EntityDrawable>&        GetEntities()      const { return m_entities; }
    const std::vector<DebugLine>&             GetDebugLines()    const { return m_debugLines; }
    const std::vector<HUDElement>&            GetHUDElements()   const { return m_hudElems; }
    const std::vector<SelectionHighlight>&    GetHighlights()    const { return m_highlights; }

private:
    ViewportConfig                 m_config;
    CameraState                    m_camera;

    std::vector<VoxelChunkDrawable>  m_chunks;
    std::vector<EntityDrawable>      m_entities;
    std::vector<DebugLine>           m_debugLines;
    std::vector<DebugText>           m_debugTexts;
    std::vector<HUDElement>          m_hudElems;
    std::vector<SelectionHighlight>  m_highlights;

    std::vector<RenderPassStats>   m_stats;
    uint64_t                       m_frameNumber = 0;
    bool                           m_initialized = false;

    std::unordered_map<uint8_t, RenderPassDelegate> m_passDelegates;
    std::unordered_map<uint8_t, bool>               m_layerEnabled;

    void ExecutePass(ERenderLayer layer);
};

} // namespace atlas::rendering
