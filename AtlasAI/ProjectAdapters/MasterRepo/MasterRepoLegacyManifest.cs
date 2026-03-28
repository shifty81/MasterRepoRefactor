// MasterRepoLegacyManifest.cs
// AtlasAI-side manifest loader for the legacy MasterRepo project layout.
//
// Reads masterrepo.legacy.project.json from Shared/ProjectManifests and exposes
// its contents (including legacy-layout overrides) as a strongly-typed model.
//
// Rules:
// - Read-only after construction — no side effects.
// - All path resolution is repo-root-relative.
// - Legacy layout fields are surfaced alongside the standard manifest fields so
//   consumers can detect and compensate for the pre-refactor folder structure.

using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;
using AtlasAI.ProjectAdapters;

namespace AtlasAI.ProjectAdapters.MasterRepo
{
    // ----------------------------------------------------------------
    // Legacy-specific models
    // ----------------------------------------------------------------

    public sealed class LegacyLayoutModel
    {
        [JsonPropertyName("enabled")]
        public bool Enabled { get; init; }

        [JsonPropertyName("sourceRoot")]
        public string SourceRoot { get; init; } = "src";

        [JsonPropertyName("testsRoot")]
        public string TestsRoot { get; init; } = "tests";

        [JsonPropertyName("docsRoot")]
        public string DocsRoot { get; init; } = "docs";

        [JsonPropertyName("legacyNamingPrefix")]
        public string LegacyNamingPrefix { get; init; } = "Arbiter";
    }

    public sealed class LegacyCapabilitiesModel
    {
        [JsonPropertyName("supportsViewportAttach")]
        public bool SupportsViewportAttach { get; init; }

        [JsonPropertyName("supportsLivePatch")]
        public bool SupportsLivePatch { get; init; }

        [JsonPropertyName("supportsAISession")]
        public bool SupportsAISession { get; init; }

        [JsonPropertyName("supportsProjectIndexing")]
        public bool SupportsProjectIndexing { get; init; }

        [JsonPropertyName("supportsMultiWorkspace")]
        public bool SupportsMultiWorkspace { get; init; }
    }

    public sealed class LegacyProjectInfoModel
    {
        [JsonPropertyName("id")]
        public string Id { get; init; } = string.Empty;

        [JsonPropertyName("displayName")]
        public string DisplayName { get; init; } = string.Empty;

        [JsonPropertyName("version")]
        public string Version { get; init; } = string.Empty;

        [JsonPropertyName("description")]
        public string Description { get; init; } = string.Empty;

        [JsonPropertyName("repoRoot")]
        public string RepoRoot { get; init; } = "../../";
    }

    public sealed class LegacyBridgeConfigModel
    {
        [JsonPropertyName("transport")]
        public string Transport { get; init; } = "rest+websocket";

        [JsonPropertyName("host")]
        public string Host { get; init; } = "localhost";

        [JsonPropertyName("restPort")]
        public int RestPort { get; init; } = 57100;

        [JsonPropertyName("wsPort")]
        public int WsPort { get; init; } = 57101;

        [JsonPropertyName("timeoutSeconds")]
        public int TimeoutSeconds { get; init; } = 30;

        [JsonPropertyName("bindLoopbackOnly")]
        public bool BindLoopbackOnly { get; init; } = true;
    }

    public sealed class LegacyBuildTargetModel
    {
        [JsonPropertyName("name")]
        public string Name { get; init; } = string.Empty;

        [JsonPropertyName("displayName")]
        public string DisplayName { get; init; } = string.Empty;

        [JsonPropertyName("configuration")]
        public string Configuration { get; init; } = "Debug";

        [JsonPropertyName("platform")]
        public string Platform { get; init; } = "Win64";
    }

    public sealed class LegacyRepoPathsModel
    {
        [JsonPropertyName("sourceRoot")]
        public string SourceRoot { get; init; } = "Atlas";

        [JsonPropertyName("gameRoot")]
        public string GameRoot { get; init; } = "NovaForge";

        [JsonPropertyName("toolingRoot")]
        public string ToolingRoot { get; init; } = "AtlasAI";

        [JsonPropertyName("sharedRoot")]
        public string SharedRoot { get; init; } = "Shared";

        [JsonPropertyName("docsRoot")]
        public string DocsRoot { get; init; } = "Docs";

        [JsonPropertyName("dataRoot")]
        public string DataRoot { get; init; } = "NovaForge/Data";

        [JsonPropertyName("contentRoot")]
        public string ContentRoot { get; init; } = "NovaForge/Content";

        [JsonPropertyName("scriptsRoot")]
        public string ScriptsRoot { get; init; } = "Scripts";

        [JsonPropertyName("testsRoot")]
        public string TestsRoot { get; init; } = "Tests";
    }

    public sealed class LegacySafetySettingsModel
    {
        [JsonPropertyName("requireDryRunByDefault")]
        public bool RequireDryRunByDefault { get; init; } = true;

        [JsonPropertyName("requireSessionTokenForWrites")]
        public bool RequireSessionTokenForWrites { get; init; } = true;

        [JsonPropertyName("allowedToolActions")]
        public string[] AllowedToolActions { get; init; } = Array.Empty<string>();

        [JsonPropertyName("writeableRoots")]
        public string[] WriteableRoots { get; init; } = Array.Empty<string>();
    }

    // ----------------------------------------------------------------
    // Root manifest document
    // ----------------------------------------------------------------

    public sealed class MasterRepoLegacyManifestDocument
    {
        [JsonPropertyName("project")]
        public LegacyProjectInfoModel Project { get; init; } = new();

        [JsonPropertyName("capabilities")]
        public LegacyCapabilitiesModel Capabilities { get; init; } = new();

        [JsonPropertyName("buildTargets")]
        public LegacyBuildTargetModel[] BuildTargets { get; init; } = Array.Empty<LegacyBuildTargetModel>();

        [JsonPropertyName("bridge")]
        public LegacyBridgeConfigModel Bridge { get; init; } = new();

        [JsonPropertyName("legacyLayout")]
        public LegacyLayoutModel LegacyLayout { get; init; } = new();

        [JsonPropertyName("repoPaths")]
        public LegacyRepoPathsModel RepoPaths { get; init; } = new();

        [JsonPropertyName("safetySettings")]
        public LegacySafetySettingsModel SafetySettings { get; init; } = new();
    }

    // ----------------------------------------------------------------
    // Loader
    // ----------------------------------------------------------------

    public static class MasterRepoLegacyManifest
    {
        private static readonly JsonSerializerOptions s_options = new()
        {
            PropertyNameCaseInsensitive = true,
        };

        /// <summary>
        /// Resolves the manifest path relative to a repo root.
        /// Looks for <c>Shared/ProjectManifests/masterrepo.legacy.project.json</c>.
        /// </summary>
        public static string ResolveManifestPath(string repoRoot)
        {
            return Path.Combine(repoRoot, "Shared", "ProjectManifests",
                                "masterrepo.legacy.project.json");
        }

        /// <summary>
        /// Loads and deserialises the manifest from <paramref name="path"/>.
        /// Throws <see cref="FileNotFoundException"/> if the file is absent.
        /// Throws <see cref="JsonException"/> if the JSON is malformed.
        /// </summary>
        public static MasterRepoLegacyManifestDocument Load(string path)
        {
            if (!File.Exists(path))
                throw new FileNotFoundException(
                    $"MasterRepo legacy manifest not found: {path}", path);

            string json = File.ReadAllText(path);
            return JsonSerializer.Deserialize<MasterRepoLegacyManifestDocument>(
                       json, s_options)
                   ?? throw new JsonException(
                       "Deserialisation of legacy manifest returned null.");
        }

        /// <summary>
        /// Convenience overload: resolves and loads in one call.
        /// </summary>
        public static MasterRepoLegacyManifestDocument LoadFromRepoRoot(string repoRoot)
        {
            return Load(ResolveManifestPath(repoRoot));
        }
    }
}
