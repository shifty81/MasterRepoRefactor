using System.Windows;
using System.Windows.Controls;

namespace AtlasAI.Panels;

public partial class ChatPanel : UserControl
{
    public ChatPanel()
    {
        InitializeComponent();
    }

    private void Send_Click(object sender, RoutedEventArgs e)
    {
        var text = InputTextBox.Text.Trim();
        if (string.IsNullOrEmpty(text)) return;
        ChatHistoryBlock.Text += $"\nYou: {text}";
        InputTextBox.Clear();
    }
}
