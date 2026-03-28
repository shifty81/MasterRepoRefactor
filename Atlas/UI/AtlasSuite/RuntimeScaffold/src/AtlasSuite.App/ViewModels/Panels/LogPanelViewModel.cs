using System.Collections.ObjectModel;

namespace AtlasSuite.App.ViewModels.Panels;

public sealed class LogPanelViewModel : ViewModelBase
{
    public ObservableCollection<string> Entries { get; } = [];

    public void Append(string message)
    {
        Entries.Add($"[{DateTime.Now:HH:mm:ss}] {message}");
    }
}
