#include "common/Clock.h"

#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>

namespace Atlas::Common {

std::string UtcNowIso8601() {
    using namespace std::chrono;
    const auto now = system_clock::now();
    const std::time_t tt = system_clock::to_time_t(now);

    std::tm utc{};
#if defined(_WIN32)
    gmtime_s(&utc, &tt);
#else
    gmtime_r(&tt, &utc);
#endif

    std::ostringstream oss;
    oss << std::put_time(&utc, "%Y-%m-%dT%H:%M:%SZ");
    return oss.str();
}

} // namespace Atlas::Common
