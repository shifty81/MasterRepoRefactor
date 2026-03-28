#include "SaveCoordinator.h"

namespace Runtime::SaveLoad
{
    bool SaveCoordinator::SaveSlot(const SaveSlotMetadata& metadata)
    {
        // TODO:
        // - freeze mutation
        // - serialize profile/session/world delta domains
        // - write slot metadata and hashes
        return SerializeDomains(metadata);
    }

    bool SaveCoordinator::LoadSlot(const std::string& slotId)
    {
        // TODO:
        // - validate slot
        // - restore deterministic baseline
        // - apply domain data in stable order
        return RestoreDomains(slotId);
    }

    std::vector<SaveSlotMetadata> SaveCoordinator::ListSlots() const
    {
        // TODO: query save backend / slot registry
        return {};
    }

    bool SaveCoordinator::SerializeDomains(const SaveSlotMetadata& /*metadata*/)
    {
        return true;
    }

    bool SaveCoordinator::RestoreDomains(const std::string& /*slotId*/)
    {
        return true;
    }
}
