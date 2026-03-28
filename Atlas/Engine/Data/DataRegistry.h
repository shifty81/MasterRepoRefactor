#pragma once

#include "Modules/ModuleRegistry.h"
#include <string>
#include <vector>

class DataRegistry
{
public:
    bool Initialize(const std::string& DataRoot);
    void Shutdown();

    const std::vector<ModuleDefinition>& GetLoadedModuleDefinitions() const;

private:
    bool LoadModuleDefinitions(const std::string& ModuleDirectory);

    std::vector<ModuleDefinition> ModuleDefinitions;
};
