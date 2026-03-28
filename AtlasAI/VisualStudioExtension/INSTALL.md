# AtlasAI AI — Visual Studio Extension

## Installation

### Option A — Install from `.vsix` file (local build)

1. Build the extension:
   ```
   dotnet build VisualStudioExtension/AtlasAIVSIX/AtlasAIVSIX.csproj -c Release
   ```
   The `.vsix` file is written to `VisualStudioExtension/AtlasAIVSIX/bin/Release/AtlasAIVSIX.vsix`.

2. Double-click `AtlasAIVSIX.vsix` — the VS 2022 VSIX Installer opens automatically.

3. Click **Install**, then restart Visual Studio when prompted.

### Option B — Install from Visual Studio Marketplace *(coming soon)*

Search for **"AtlasAI AI"** in **Extensions → Manage Extensions** inside Visual Studio 2022.

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Visual Studio | 2022 (17.x) — Community, Professional, or Enterprise |
| .NET Framework | 4.7.2 or later |
| AtlasAI backend | Running locally (see below) |

---

## Starting the AtlasAI backend

The VSIX auto-detects the AtlasAI backend on **port 8001** (AtlasAIEngine) or **port 8000** (PythonBridge).

Start the backend before opening Visual Studio:

```bash
# PythonBridge (lightweight, port 8000)
python AIEngine/PythonBridge/fastapi_bridge.py

# AtlasAIEngine (full agentic backend, port 8001)
python AIEngine/AtlasAIEngine/server.py
```

Or run the one-click setup:
```bash
python setup_arbiter.py
```

---

## Usage

| Action | Shortcut |
|--------|----------|
| Open Chat Panel | **Ctrl+Alt+A** |
| Ask AtlasAI about selection | **Ctrl+Shift+A** |
| Explain this code | **Ctrl+Shift+E** |
| Fix this error | **Ctrl+Shift+F** |
| Refactor with AtlasAI | **Ctrl+Shift+R** |
| Generate unit tests | **Ctrl+Shift+T** |
| Add documentation | **Ctrl+Shift+D** |
| Review this file | **Ctrl+Shift+V** |
| Insert code from chat | **Ctrl+Shift+I** |

### Inline suggestions

Type `// AtlasAI: <description>` on any line and press **Tab** — AtlasAI generates a code completion for the description.

### AI fix suggestions in Error List

After every failed build, AtlasAI requests AI fix suggestions and surfaces them as **Messages** in the VS Error List (View → Error List → Messages tab).

---

## Settings

Open **Tools → Options → AtlasAI AI** to configure:

- **Backend URL** — defaults to `http://localhost:8001`
- **Persona** — AtlasAI Assistant / Coder / Teacher / Organizer
- **Enable TTS** — read AI responses aloud
- **Enable inline suggestions** — toggle `// AtlasAI:` completions

---

## Publishing to the VS Marketplace

1. Ensure you have a [Visual Studio Marketplace publisher account](https://marketplace.visualstudio.com/manage).
2. Install `vsce` (the VS Extension CLI):
   ```bash
   npm install -g @vscode/vsce
   ```
3. Package:
   ```bash
   cd VisualStudioExtension/AtlasAIVSIX
   dotnet build -c Release
   ```
4. Upload `bin/Release/AtlasAIVSIX.vsix` at https://marketplace.visualstudio.com/manage.
