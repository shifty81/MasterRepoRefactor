#pragma once

namespace Shared::ArbiterBridge
{
    enum class ResultCode
    {
        Ok = 0,
        InvalidRequest,
        Unauthorized,
        Unsupported,
        InternalError
    };
}
