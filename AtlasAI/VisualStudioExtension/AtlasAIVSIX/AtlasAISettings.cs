using System;
using System.ComponentModel;
using Microsoft.VisualStudio.Shell;

namespace AtlasAIVSIX
{
    /// <summary>
    /// AtlasAI settings page — available via <c>Tools → Options → AtlasAI</c>.
    ///
    /// Settings are persisted automatically in the user's VS profile by the
    /// <see cref="DialogPage"/> base class.
    /// </summary>
    public sealed class ArbiterSettingsPage : DialogPage
    {
        // ── Backend ──────────────────────────────────────────────────────────

        [Category("Backend")]
        [DisplayName("Backend URL")]
        [Description(
            "URL of the running AtlasAI backend. " +
            "Leave blank to auto-detect (tries port 8001, then 8000).")]
        public string BackendUrl { get; set; } = "";

        [Category("Backend")]
        [DisplayName("Connection timeout (seconds)")]
        [Description("HTTP timeout for AI requests. Increase for slow hardware.")]
        public int TimeoutSeconds { get; set; } = 30;

        // ── Persona ──────────────────────────────────────────────────────────

        [Category("AI")]
        [DisplayName("Default persona")]
        [Description(
            "The AtlasAI persona used when no project-specific persona is set. " +
            "Options: AtlasAI, Coder, Teacher, Organizer.")]
        public string DefaultPersona { get; set; } = "Coder";

        [Category("AI")]
        [DisplayName("AI mode")]
        [Description("chat = single-turn. agentic = multi-step task execution.")]
        public string AiMode { get; set; } = "chat";

        // ── Voice ─────────────────────────────────────────────────────────────

        [Category("Voice")]
        [DisplayName("Enable TTS responses")]
        [Description("When enabled, AI responses are read aloud via the AtlasAI TTS engine.")]
        public bool EnableTts { get; set; } = false;

        [Category("Voice")]
        [DisplayName("TTS voice")]
        [Description("Voice identifier passed to the AtlasAI TTS engine (e.g. British_Female).")]
        public string TtsVoice { get; set; } = "British_Female";

        // ── Inline suggestions ────────────────────────────────────────────────

        [Category("Inline Suggestions")]
        [DisplayName("Enable inline completions")]
        [Description("When enabled, typing a // AtlasAI: comment triggers an inline AI suggestion.")]
        public bool EnableInlineSuggestions { get; set; } = true;

        [Category("Inline Suggestions")]
        [DisplayName("Trigger prefix")]
        [Description("The comment prefix that triggers an inline suggestion.")]
        public string InlineTriggerPrefix { get; set; } = "// AtlasAI:";
    }
}
