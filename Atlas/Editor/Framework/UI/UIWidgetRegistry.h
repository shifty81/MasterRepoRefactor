#pragma once
#include <string>
#include <unordered_map>
#include <functional>

namespace atlas::editor {

class UIWidgetRegistry {
public:
    using WidgetFactory = std::function<void()>;

    static UIWidgetRegistry& Instance();

    void Register(const std::string& id, WidgetFactory factory);
    void Unregister(const std::string& id);

    /** Invokes the widget factory for `id`. Returns true if found, false otherwise. */
    bool InvokeWidget(const std::string& id);

private:
    UIWidgetRegistry() = default;
    std::unordered_map<std::string, WidgetFactory> m_widgets;
};

} // namespace atlas::editor
