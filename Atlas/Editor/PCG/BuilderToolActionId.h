#pragma once

#include <cstdint>

namespace Atlas::Editor {

enum class BuilderToolActionIdV2 : uint32_t {
    PreviewMesh    = 100,
    ValidateEntity = 101,
    RunDiagnostics = 102,
    ExportPCGSeed  = 103,
};

} // namespace Atlas::Editor
