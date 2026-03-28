#pragma once

#include <string>
#include <vector>

namespace Runtime::SaveLoad
{
    struct SaveSlotMetadata
    {
        std::string SlotId;
        std::string DisplayName;
        std::string ScenarioId;
        std::string BuildVersion;
        std::string SchemaVersion;
        long long TimestampUtc = 0;
    };

    class SaveCoordinator
    {
    public:
        bool SaveSlot(const SaveSlotMetadata& metadata);
        bool LoadSlot(const std::string& slotId);
        std::vector<SaveSlotMetadata> ListSlots() const;

    private:
        bool SerializeDomains(const SaveSlotMetadata& metadata);
        bool RestoreDomains(const std::string& slotId);
    };
}
