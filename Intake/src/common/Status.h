#pragma once

#include <string>

namespace Atlas::Common {

struct Status {
    bool ok{true};
    std::string message{"ok"};

    static Status Ok(std::string msg = "ok") { return {true, std::move(msg)}; }
    static Status Error(std::string msg) { return {false, std::move(msg)}; }
};

} // namespace Atlas::Common
