#pragma once
// Atlas/cpp_client/include/ui/atlas/atlas_widgets.h
//
// Editor-side shim that re-exports all Atlas UI types and widget
// declarations needed by Atlas Editor panels.
//
// The canonical NovaForge client widget implementations live in
//   NovaForge/Client/App/include/ui/atlas/atlas_widgets.h
// Atlas/Editor cannot cross the NovaForge boundary, so this header
// provides self-contained declarations that satisfy the editor build.
// Both copies must be kept in sync when widget APIs change.

#include "atlas_types.h"   // Vec2, Rect, Color, PanelState, TextInputState, ...
#include <string>
#include <vector>
#include <functional>
#include <cstdint>

namespace atlas {

// ── Forward declarations ─────────────────────────────────────────────
struct AtlasContext;

// ── Panel API ────────────────────────────────────────────────────────

struct PanelFlags {
    bool showHeader   = true;
    bool showClose    = true;
    bool showMinimize = true;
    bool compactMode  = false;
    bool locked       = false;
    bool drawBorder   = true;
};

bool panelBegin(AtlasContext& ctx, const char* title,
                Rect& bounds, const PanelFlags& flags = {},
                bool* open = nullptr);
void panelEnd(AtlasContext& ctx);

// ── Buttons ──────────────────────────────────────────────────────────

bool button(AtlasContext& ctx, const char* label, const Rect& r);
bool iconButton(AtlasContext& ctx, WidgetID id, const Rect& r,
                const Color& iconColor, const char* symbol = nullptr);

// ── Progress / Status Bars ───────────────────────────────────────────

void progressBar(AtlasContext& ctx, const Rect& r,
                 float fraction, const Color& fillColor,
                 const char* label = nullptr);

struct ArcSegment { float startDeg; float endDeg; Color color; float fraction; };
void statusArc(AtlasContext& ctx, Vec2 center, float innerR, float outerR,
               const std::vector<ArcSegment>& segments);

void capRing(AtlasContext& ctx, Vec2 center, float radius,
             float capacitorFraction, int segments = 24);

// ── Module Slot ──────────────────────────────────────────────────────

struct ModuleSlotInfo {
    WidgetID    id           = 0;
    Color       iconColor    = {80, 160, 220, 255};
    bool        active       = false;
    float       cooldownFrac = 0.0f;
    const char* tooltip      = nullptr;
};

bool moduleSlot(AtlasContext& ctx, const Rect& r, const ModuleSlotInfo& info);

// ── Overview / Target ────────────────────────────────────────────────

struct OverviewEntry {
    std::string name;
    std::string type;
    float       distance  = 0.0f;
    Color       nameColor = {200, 200, 200, 255};
    bool        selected  = false;
    bool        hostile   = false;
};

bool overviewRow(AtlasContext& ctx, const Rect& r, const OverviewEntry& entry);
void targetCard(AtlasContext& ctx, const Rect& r, const OverviewEntry& target,
                float shieldFrac, float armorFrac, float hullFrac);

// ── Text Input ───────────────────────────────────────────────────────

bool textInput(AtlasContext& ctx, const Rect& r, TextInputState& state,
               const char* placeholder = nullptr);

// ── Label / Separator / Tree ─────────────────────────────────────────

void label(AtlasContext& ctx, Vec2 pos, const char* text,
           const Color& color = {200, 200, 200, 255});
void separator(AtlasContext& ctx, const Rect& r);
bool treeNode(AtlasContext& ctx, WidgetID id, const Rect& r,
              const char* label, bool& expanded);
void scrollbar(AtlasContext& ctx, const Rect& r,
               float contentHeight, float& scrollOffset);

} // namespace atlas
