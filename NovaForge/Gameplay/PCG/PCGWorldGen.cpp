// PCGWorldGen.cpp
#include "PCGWorldGen.h"
#include <cstdlib>
#include <sstream>

namespace NovaForge::Gameplay::PCG
{

void PCGWorldGen::initialise() {}
void PCGWorldGen::shutdown()   {}

void PCGWorldGen::generate(const PCGGenerationParams& p)
{
    clear();
    std::srand(p.worldSeed);

    for (uint32_t i = 0; i < p.sectorCount; ++i)
    {
        PCGSector sec;
        sec.sectorId    = static_cast<uint64_t>(i + 1);
        sec.seed        = static_cast<uint32_t>(std::rand());
        sec.sizeAU      = p.avgSectorSize * (0.5f + (std::rand() % 100) / 100.0f);
        sec.systemCount = 3 + (std::rand() % 8);
        std::ostringstream n; n << "Sector-" << (i + 1);
        sec.name = n.str();
        sectors_.push_back(sec);

        for (uint32_t j = 0; j < sec.systemCount; ++j)
        {
            PCGStarSystem sys;
            sys.systemId    = static_cast<uint64_t>(i * 100 + j + 1);
            sys.sectorId    = sec.sectorId;
            sys.seed        = static_cast<uint32_t>(std::rand());
            sys.planetCount = 1 + (std::rand() % 8);
            sys.hasStation  = ((std::rand() % 100) < static_cast<int>(p.stationDensity * 100));
            std::ostringstream sn; sn << sec.name << "-SYS" << (j + 1);
            sys.name = sn.str();
            systems_.push_back(sys);
        }
    }
}

std::vector<PCGSector> PCGWorldGen::getSectors() const { return sectors_; }

std::vector<PCGStarSystem> PCGWorldGen::getSystemsInSector(uint64_t sectorId) const
{
    std::vector<PCGStarSystem> result;
    for (const auto& s : systems_)
        if (s.sectorId == sectorId) result.push_back(s);
    return result;
}

PCGStarSystem PCGWorldGen::getSystem(uint64_t systemId) const
{
    for (const auto& s : systems_)
        if (s.systemId == systemId) return s;
    return {};
}

void PCGWorldGen::clear() { sectors_.clear(); systems_.clear(); }

} // namespace NovaForge::Gameplay::PCG
