namespace AtlasAIHost
{
    /// <summary>
    /// Application-level configuration shared across all windows.
    /// Set by <see cref="LauncherWindow"/> before any main window is opened.
    /// </summary>
    internal static class AppConfig
    {
        /// <summary>Always "AtlasAIEngine" — the launcher has been removed.</summary>
        public static string Mode { get; set; } = "AtlasAIEngine";

        /// <summary>
        /// Base URL of the AtlasAI Engine backend (server.py, port 8001 by default).
        /// </summary>
        public static string ApiBaseUrl { get; set; } = "http://127.0.0.1:8001";

        /// <summary>Filesystem path to the AIEngine/AtlasAIEngine directory.</summary>
        public static string AtlasAIEnginePath { get; set; } = string.Empty;

        /// <summary>Port the AtlasAI Engine bridge server should listen on.</summary>
        public static int AtlasAIEnginePort { get; set; } = 8001;

        /// <summary>
        /// The AtlasAI Engine subprocess (if started by the launcher).
        /// Terminated when the application exits.
        /// </summary>
        public static System.Diagnostics.Process? EngineProcess { get; set; }

        /// <summary>
        /// The AtlasAI bridge subprocess started by MainWindow or ProjectWindow
        /// (fastapi_bridge.py on port 8000).  Stored here so App_Exit can always
        /// clean it up regardless of which window started it.
        /// </summary>
        public static System.Diagnostics.Process? BridgeProcess { get; set; }
    }
}
