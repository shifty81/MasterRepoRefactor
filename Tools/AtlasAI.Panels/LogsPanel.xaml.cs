using System.Windows;
using System.Windows.Controls;

namespace AtlasAI.Panels;

public partial class LogsPanel : UserControl
{
    private int _entryCount = 0;

    public LogsPanel()
    {
        InitializeComponent();
    }

    public void AppendLog(string message)
    {
        _entryCount++;
        LogTextBlock.Text += $"\n[{_entryCount}] {message}";
        LogStatusBlock.Text = $"{_entryCount} entries";
        LogScroller.ScrollToEnd();
    }

    private void Clear_Click(object sender, RoutedEventArgs e)
    {
        LogTextBlock.Text = string.Empty;
        _entryCount = 0;
        LogStatusBlock.Text = "0 entries";
    }

    private void Export_Click(object sender, RoutedEventArgs e)
    {
        // Scaffold — wire to file export service
    }
}
