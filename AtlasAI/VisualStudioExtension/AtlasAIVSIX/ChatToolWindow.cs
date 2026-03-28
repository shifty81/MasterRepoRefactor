using System;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows;
using Microsoft.VisualStudio.Shell;
using Microsoft.VisualStudio.Shell.Interop;

namespace AtlasAIVSIX
{
    /// <summary>
    /// ChatToolWindow — dockable Visual Studio tool window that hosts the AtlasAI chat UI.
    ///
    /// The chat interface is the same WebView2-hosted web UI served by the AtlasAI backend
    /// at <c>/gui/</c>.  This allows a single web codebase to power both the standalone
    /// Monaco IDE and the VS-embedded panel.
    /// </summary>
    [Guid("b2c3d4e5-f6a7-8901-bcde-f12345678901")]
    public sealed class ChatToolWindow : ToolWindowPane
    {
        private ChatToolWindowControl? _control;

        public ChatToolWindow() : base(null)
        {
            Caption = "AtlasAI Chat";
        }

        public override object Content
        {
            get
            {
                if (_control == null)
                    _control = new ChatToolWindowControl();
                return _control;
            }
        }
    }
}
