using System.Windows;

namespace AtlasAI.Shell;

public partial class ShellWindow : Window
{
    public ShellWindow()
    {
        InitializeComponent();
    }

    private void SendChat_Click(object sender, RoutedEventArgs e)
    {
        var input = ChatInputBox.Text.Trim();
        if (string.IsNullOrEmpty(input)) return;
        ChatOutputBlock.Text += $"\nYou: {input}";
        ChatInputBox.Clear();
        StatusTextBlock.Text = "Message sent.";
    }
}
