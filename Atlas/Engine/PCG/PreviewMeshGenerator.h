#pragma once

#include <string>

namespace Atlas::Engine {

class PreviewMeshGenerator {
public:
    bool Generate(const std::string& pcgDescriptor, std::string& outMeshData);
    void SetResolution(int lod);

private:
    int m_lod{0};
};

} // namespace Atlas::Engine
