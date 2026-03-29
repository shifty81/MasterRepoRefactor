#pragma once

// NOTE: This file is the Atlas-editor-side copy of the AtlasRenderer declaration.
// It must be kept in sync with NovaForge/Client/include/ui/atlas/atlas_renderer.h.
// Both copies exist because Atlas/Editor cannot include across the NovaForge
// boundary; the canonical source is the NovaForge copy.

#include "atlas_types.h"
#include <vector>
#include <cstdint>

namespace atlas {

struct UIVertex {
    float x, y;
    float u, v;
    float r, g, b, a;
};

class AtlasRenderer {
public:
    AtlasRenderer();
    ~AtlasRenderer();

    bool init();
    void shutdown();

    void begin(int windowW, int windowH);
    void end();

    void drawRect(const Rect& r, const Color& c);
    void drawRectGradient(const Rect& r,
                          const Color& topLeft, const Color& topRight,
                          const Color& botRight, const Color& botLeft);
    void drawRoundedRect(const Rect& r, const Color& c, float radius);
    void drawRectOutline(const Rect& r, const Color& c, float width = 1.0f);
    void drawRoundedRectOutline(const Rect& r, const Color& c,
                                float radius, float width = 1.0f);
    void drawLine(Vec2 a, Vec2 b, const Color& c, float width = 1.0f);
    void drawCircle(Vec2 centre, float radius, const Color& c, int segments = 32);
    void drawCircleOutline(Vec2 centre, float radius, const Color& c,
                           float width = 1.0f, int segments = 32);
    void drawArc(Vec2 centre, float innerR, float outerR,
                 float startAngle, float endAngle,
                 const Color& c, int segments = 32);
    void drawProgressBar(const Rect& r, float fraction,
                         const Color& fg, const Color& bg);
    float drawText(const std::string& text, Vec2 pos,
                   const Color& c, float scale = 1.0f);
    float measureText(const std::string& text, float scale = 1.0f) const;

    void pushClip(const Rect& r);
    void popClip();

private:
    uint32_t m_shaderProgram = 0;
    uint32_t m_vao = 0;
    uint32_t m_vbo = 0;
    uint32_t m_fontTexture = 0;
    int      m_uniformProj = -1;
    int      m_uniformUseTex = -1;
    int      m_uniformTex = -1;

    std::vector<UIVertex> m_vertices;
    static constexpr size_t MAX_VERTICES = 65536;

    int  m_windowW = 1280;
    int  m_windowH = 720;
    bool m_inFrame = false;

    std::vector<Rect> m_clipStack;

    void flush();
    void addQuad(float x0, float y0, float x1, float y1,
                 float u0, float v0, float u1, float v1,
                 const Color& c);
    void addQuadGradient(float x0, float y0, float x1, float y1,
                         const Color& tl, const Color& tr,
                         const Color& br, const Color& bl);
    void addTriangle(float x0, float y0,
                     float x1, float y1,
                     float x2, float y2,
                     const Color& c);
    void buildFontTexture();
};

} // namespace atlas
