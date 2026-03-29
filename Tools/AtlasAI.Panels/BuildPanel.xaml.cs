using System.Windows;
using System.Windows.Controls;

namespace AtlasAI.Panels;

public partial class BuildPanel : UserControl
{
    public BuildPanel()
    {
        InitializeComponent();
    }

    private void Build_Click(object sender, RoutedEventArgs e)
    {
        BuildStatusLabel.Text = "Building…";
        BuildProgress.Value = 0;
        // Scaffold — wire to build service
    }

    private void Cancel_Click(object sender, RoutedEventArgs e)
    {
        BuildStatusLabel.Text = "Cancelled";
        BuildProgress.Value = 0;
    }

    private void ClearBuild_Click(object sender, RoutedEventArgs e)
    {
        BuildOutputBlock.Text = string.Empty;
        BuildStatusLabel.Text = "Idle";
        BuildProgress.Value = 0;
    }

    public void AppendOutput(string line)
    {
        BuildOutputBlock.Text += $"\n{line}";
        BuildScroller.ScrollToEnd();
    }

    public void SetProgress(double value) => BuildProgress.Value = value;
    public void SetStatus(string status) => BuildStatusLabel.Text = status;
}
