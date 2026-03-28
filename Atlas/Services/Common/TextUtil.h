#pragma once

#include <algorithm>
#include <cctype>
#include <filesystem>
#include <fstream>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

namespace Atlas::Common {

inline std::string ReadTextFile(const std::filesystem::path& path) {
    std::ifstream in(path, std::ios::binary);
    std::ostringstream buffer;
    buffer << in.rdbuf();
    return buffer.str();
}

inline std::string Trim(std::string value) {
    auto not_space = [](unsigned char ch) { return !std::isspace(ch); };
    value.erase(value.begin(), std::find_if(value.begin(), value.end(), not_space));
    value.erase(std::find_if(value.rbegin(), value.rend(), not_space).base(), value.end());
    return value;
}

inline std::string ToLower(std::string value) {
    std::transform(value.begin(), value.end(), value.begin(), [](unsigned char ch) {
        return static_cast<char>(std::tolower(ch));
    });
    return value;
}

inline std::vector<std::string> ExtractStringArray(const std::string& json, const std::string& key) {
    const std::string needle = "\"" + key + "\"";
    const auto keyPos = json.find(needle);
    if (keyPos == std::string::npos) {
        return {};
    }

    const auto open = json.find('[', keyPos);
    const auto close = json.find(']', open == std::string::npos ? keyPos : open);
    if (open == std::string::npos || close == std::string::npos || close <= open) {
        return {};
    }

    const std::string content = json.substr(open + 1, close - open - 1);
    std::vector<std::string> out;
    std::string current;
    bool inString = false;
    bool escaping = false;

    for (char ch : content) {
        if (!inString) {
            if (ch == '"') {
                inString = true;
                current.clear();
            }
            continue;
        }

        if (escaping) {
            current.push_back(ch);
            escaping = false;
            continue;
        }

        if (ch == '\\') {
            escaping = true;
            continue;
        }

        if (ch == '"') {
            inString = false;
            out.push_back(current);
            continue;
        }

        current.push_back(ch);
    }

    return out;
}

inline bool ExtractBool(const std::string& json, const std::string& key, bool default_value) {
    std::regex pattern("\"" + key + "\"\\s*:\\s*(true|false)", std::regex::icase);
    std::smatch match;
    if (!std::regex_search(json, match, pattern)) {
        return default_value;
    }
    return ToLower(match[1].str()) == "true";
}

inline std::string ExtractString(const std::string& json, const std::string& key, const std::string& default_value = {}) {
    std::regex pattern("\"" + key + "\"\\s*:\\s*\"([^\"]*)\"", std::regex::icase);
    std::smatch match;
    if (!std::regex_search(json, match, pattern)) {
        return default_value;
    }
    return match[1].str();
}

inline std::vector<std::string> SplitLines(const std::string& text) {
    std::istringstream iss(text);
    std::vector<std::string> lines;
    for (std::string line; std::getline(iss, line); ) {
        lines.push_back(line);
    }
    return lines;
}

inline bool StartsWithPath(const std::filesystem::path& child, const std::filesystem::path& root) {
    const auto c = child.lexically_normal().generic_string();
    const auto r = root.lexically_normal().generic_string();
    if (r.empty()) {
        return false;
    }
    if (c == r) {
        return true;
    }
    return c.size() > r.size() && c.compare(0, r.size(), r) == 0 && c[r.size()] == '/';
}

inline std::string JsonEscape(const std::string& value) {
    std::string out;
    out.reserve(value.size() + 8);
    for (char ch : value) {
        switch (ch) {
        case '\\': out += "\\\\"; break;
        case '"': out += "\\\""; break;
        case '\n': out += "\\n"; break;
        case '\r': out += "\\r"; break;
        case '\t': out += "\\t"; break;
        default: out += ch; break;
        }
    }
    return out;
}

} // namespace Atlas::Common
