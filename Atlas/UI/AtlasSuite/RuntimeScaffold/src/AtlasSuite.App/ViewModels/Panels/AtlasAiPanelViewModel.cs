namespace AtlasSuite.App.ViewModels.Panels;

public sealed class AtlasAiPanelViewModel : ViewModelBase
{
    private string _request = string.Empty;
    private string _response = "AtlasAI ready.";

    public string Request
    {
        get => _request;
        set
        {
            _request = value;
            RaisePropertyChanged();
        }
    }

    public string Response
    {
        get => _response;
        set
        {
            _response = value;
            RaisePropertyChanged();
        }
    }
}
