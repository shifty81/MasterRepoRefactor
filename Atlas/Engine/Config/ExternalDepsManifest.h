#pragma once
// ExternalDepsManifest.h — Registry of all external/third-party dependencies
// wired into the AtlasEngine and NovaForgeClient CMake targets.
// Maintained as a compile-time reference; not linked at runtime.
//
// All paths are relative to the repository root.  CMake targets expose these
// directories via target_include_directories(... INTERFACE ...) so consumers
// do not need to repeat the paths; this header documents them for reference.

namespace Atlas {
namespace ExternalDeps {

// GLM — OpenGL Mathematics library.
// Header-only; provides vec2/vec3/vec4, mat4, quaternion, and related utilities.
// Used throughout the engine for transforms, physics, and rendering math.
constexpr const char* GLM_INCLUDE_PATH =
    "ThirdParty/glm";

// STB — Sean Barrett's single-file public-domain libraries.
// Primarily stb_image.h for texture loading and stb_image_write.h for export.
// Located inside the NovaForge client external bundle.
constexpr const char* STB_INCLUDE_PATH =
    "NovaForge/Client/App/external/stb";

// nlohmann/json — Modern C++ JSON library (header-only).
// Used for config serialisation, schema validation, and bridge message parsing.
constexpr const char* NLOHMANN_JSON_INCLUDE_PATH =
    "NovaForge/Client/App/external/nlohmann";

// tinygltf — Header-only glTF 2.0 loader/writer (depends on nlohmann/json and stb).
// Used by the asset pipeline to import glTF meshes and scenes.
constexpr const char* TINYGLTF_INCLUDE_PATH =
    "NovaForge/Client/App/external/tinygltf";

// tinyobjloader — Lightweight Wavefront OBJ mesh loader (header-only).
// Used by the asset pipeline for legacy OBJ asset ingestion.
constexpr const char* TINYOBJLOADER_INCLUDE_PATH =
    "NovaForge/Client/App/external/tinyobjloader";

}  // namespace ExternalDeps
}  // namespace Atlas
