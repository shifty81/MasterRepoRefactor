using System.Windows.Controls;
using AtlasSuite.Integration;

namespace AtlasSuite.ViewportHost;

public partial class ViewportHostControl : UserControl
{
    public ViewportHostControl()
    {
        InitializeComponent();
        Loaded += (_, _) => EngineBridge.Instance.AttachViewport(this);
        Unloaded += (_, _) => EngineBridge.Instance.DetachViewport();
    }
}
