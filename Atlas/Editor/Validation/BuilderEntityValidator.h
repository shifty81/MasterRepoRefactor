#pragma once

#include <string>
#include <vector>

namespace Atlas::Editor {

class BuilderEntityValidator {
public:
    bool Validate(const std::string& entityJson, std::vector<std::string>& outErrors);
    void SetSchema(const std::string& schemaPath);

private:
    std::string m_schemaPath;
};

} // namespace Atlas::Editor
