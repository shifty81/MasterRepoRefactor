using System;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows;
using Microsoft.VisualStudio.Shell;
using Microsoft.VisualStudio.Shell.Interop;

namespace AtlasAIVSIX
{
    /// <summary>
    /// SelfBuildToolWindow — dockable Visual Studio tool window for the
    /// AtlasAI self-build loop (M7-13).
    ///
    /// Hosts <see cref="SelfBuildToolWindowControl"/> which provides start/stop
    /// controls, a live log, and approve/reject buttons for Assist/SemiAuto modes.
    /// </summary>
    [Guid("c3d4e5f6-a7b8-9012-cdef-012345678902")]
    public sealed class SelfBuildToolWindow : ToolWindowPane
    {
        private SelfBuildToolWindowControl? _control;

        public SelfBuildToolWindow() : base(null)
        {
            Caption = "AtlasAI Self-Build";
        }

        public override object Content
        {
            get
            {
                if (_control == null)
                    _control = new SelfBuildToolWindowControl();
                return _control;
            }
        }
    }
}
