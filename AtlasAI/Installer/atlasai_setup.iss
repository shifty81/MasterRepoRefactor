; ─── AtlasAI — Inno Setup installer script (M8-1) ─────────────────────────────
;
; Bundles the WPF HostApp, Python runtime, AtlasAIEngine, and PythonBridge
; into a single Windows installer (.exe) using Inno Setup 6.
;
; Prerequisites before building:
;   1. Publish the WPF app:
;      dotnet publish HostApp/AtlasAIHost.csproj -c Release -r win-x64 --self-contained
;      Output → HostApp/bin/Release/net9.0-windows/win-x64/publish/
;
;   2. Download a Python embedded distribution (e.g. python-3.12.3-embed-amd64.zip)
;      and extract it to:  Installer/python-embed/
;
;   3. Install dependencies into the embedded Python:
;      Installer/python-embed/python.exe -m pip install --target Installer/python-pkgs \
;        -r AIEngine/AtlasAIEngine/requirements.txt \
;        -r AIEngine/PythonBridge/requirements.txt
;
; Build:
;   iscc Installer/atlasai_setup.iss
;
; The resulting setup.exe is placed in Installer/Output/
; ─────────────────────────────────────────────────────────────────────────────

#define MyAppName    "AtlasAI"
#define MyAppVersion "0.5.0"
#define MyAppPublisher "shifty81"
#define MyAppURL     "https://github.com/shifty81/AtlasAI"
#define MyAppExeName "AtlasAIHost.exe"
#define MyAppGUID    "{{C3A2B1F0-7E4D-4A9C-B832-1F5E2D3C4A7B}"

; Paths relative to the repo root (run iscc from the repo root)
#define WpfPublish   "HostApp\bin\Release\net9.0-windows\win-x64\publish"
#define PythonEmbed  "Installer\python-embed"
#define PythonPkgs   "Installer\python-pkgs"
#define AiEngine     "AIEngine\AtlasAIEngine"
#define PyBridge     "AIEngine\PythonBridge"
#define AiCli        "AIEngine\atlasai_cli.py"
#define RepoConfig   "AIEngine\AtlasAIEngine\configs"

[Setup]
AppId={#MyAppGUID}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases/latest
DefaultDirName={autopf}\AtlasAI
DefaultGroupName=AtlasAI
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=Installer\Output
OutputBaseFilename=atlasai-setup-{#MyAppVersion}
SetupIconFile=HostApp\atlasai.ico
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.19041
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\AtlasAIHost.exe
WizardStyle=modern
WizardSmallImageFile=HostApp\atlasai_small.bmp
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=AtlasAI AI-Powered Development Platform
VersionInfoCopyright=Copyright (C) 2024 {#MyAppPublisher}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";   Description: "{cm:CreateDesktopIcon}";   GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunch";   Description: "Add AtlasAI to Quick Launch bar";                                    Flags: unchecked
Name: "addtopath";     Description: "Add 'atlasai' CLI to PATH (recommended)";

[Files]
; ── WPF HostApp (self-contained .NET 9 publish) ────────────────────────────
Source: "{#WpfPublish}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; ── Embedded Python runtime ────────────────────────────────────────────────
Source: "{#PythonEmbed}\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs createallsubdirs

; ── Python packages (installed dependencies) ──────────────────────────────
Source: "{#PythonPkgs}\*"; DestDir: "{app}\python\Lib\site-packages"; Flags: ignoreversion recursesubdirs createallsubdirs

; ── AtlasAIEngine backend ──────────────────────────────────────────────────
Source: "{#AiEngine}\*"; DestDir: "{app}\AIEngine\AtlasAIEngine"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__,*.pyc,.git,logs\*,workspace\*"

; ── PythonBridge backend ───────────────────────────────────────────────────
Source: "{#PyBridge}\*"; DestDir: "{app}\AIEngine\PythonBridge"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__,*.pyc,.git"

; ── AtlasAI CLI ────────────────────────────────────────────────────────────
Source: "{#AiCli}"; DestDir: "{app}\AIEngine"; Flags: ignoreversion

; ── Default config files ───────────────────────────────────────────────────
Source: "{#RepoConfig}\*"; DestDir: "{app}\AIEngine\AtlasAIEngine\configs"; Flags: ignoreversion recursesubdirs createallsubdirs

; ── Readme and license ─────────────────────────────────────────────────────
Source: "README.md";  DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "LICENSE";    DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\AIEngine\AtlasAIEngine\logs";    Permissions: users-modify
Name: "{app}\AIEngine\AtlasAIEngine\workspace"; Permissions: users-modify
Name: "{app}\Memory\ConversationLogs";         Permissions: users-modify
Name: "{app}\Projects";                        Permissions: users-modify

[Icons]
Name: "{group}\AtlasAI";                   Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\Uninstall AtlasAI";         Filename: "{uninstallexe}"
Name: "{commondesktop}\AtlasAI";           Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\AtlasAI"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunch

[Run]
; Launch AtlasAI after installation (optional)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; Register file associations and app path for PATH addition
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\App Paths\AtlasAIHost.exe"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName}"
Root: HKCU; Subkey: "Software\AtlasAI"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\AtlasAI"; ValueType: string; ValueName: "Version";     ValueData: "{#MyAppVersion}"

[Code]
// ── Optional: Add atlasai CLI to PATH ─────────────────────────────────────
procedure CurStepChanged(CurStep: TSetupStep);
var
  OldPath, NewPath, CliDir: String;
begin
  if (CurStep = ssPostInstall) and IsTaskSelected('addtopath') then
  begin
    CliDir := ExpandConstant('{app}\AIEngine');
    if not RegQueryStringValue(HKCU, 'Environment', 'PATH', OldPath) then
      OldPath := '';
    if Pos(Lowercase(CliDir), Lowercase(OldPath)) = 0 then
    begin
      NewPath := OldPath;
      if (Length(NewPath) > 0) and (NewPath[Length(NewPath)] <> ';') then
        NewPath := NewPath + ';';
      NewPath := NewPath + CliDir;
      RegWriteStringValue(HKCU, 'Environment', 'PATH', NewPath);
    end;
  end;
end;

// ── Remove from PATH on uninstall ─────────────────────────────────────────
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  OldPath, CliDir, NewPath: String;
  Pos1: Integer;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    CliDir := ExpandConstant('{app}\AIEngine');
    if RegQueryStringValue(HKCU, 'Environment', 'PATH', OldPath) then
    begin
      Pos1 := Pos(Lowercase(CliDir), Lowercase(OldPath));
      if Pos1 > 0 then
      begin
        NewPath := OldPath;
        Delete(NewPath, Pos1, Length(CliDir));
        if (Pos1 > 1) and (NewPath[Pos1 - 1] = ';') then
          Delete(NewPath, Pos1 - 1, 1);
        RegWriteStringValue(HKCU, 'Environment', 'PATH', NewPath);
      end;
    end;
  end;
end;
