; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{6B4D7E7D-E1D1-4839-89D6-E13D5F57DE5B}
AppName=PrestoPronto
AppVersion= b 0.6.8
;AppVerName=PrestoPronto  b 0.8
AppPublisherURL=http://code.google.com/p/prestopronto/
AppSupportURL=http://code.google.com/p/prestopronto/
AppUpdatesURL=http://code.google.com/p/prestopronto/
;DefaultDirName={pf}\PrestoPronto
DefaultGroupName=PrestoPronto
InfoAfterFile=README.txt
OutputBaseFilename=PrestoPronto_b0.8_setup
Compression=lzma
SolidCompression=yes     
PrivilegesRequired=none
DefaultDirName={code:DefDirRoot}\PrestoPronto

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl" ;


[Code]
function IsRegularUser(): Boolean;
begin
Result := not (IsAdminLoggedOn or IsPowerUserLoggedOn);
end;

function DefDirRoot(Param: String): String;
begin
if IsRegularUser then
Result := ExpandConstant('{localappdata}')
else
Result := ExpandConstant('{pf}')
end;




[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
Name: "{app}\"; Permissions: everyone-modify


[Files] 
Source: "PrestoPronto.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "PCA_GUI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "LinComb_GUI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\PrestoPronto"; Filename: "{app}\PrestoPronto.exe"
Name: "{commondesktop}\PrestoPronto"; Filename: "{app}\PrestoPronto.exe"; Tasks: desktopicon
Name: "{group}\PCA_GUI"; Filename: "{app}\PCA_GUI.exe"
Name: "{commondesktop}\PCA_GUI"; Filename: "{app}\PCA_GUI.exe"; Tasks: desktopicon
Name: "{group}\LinComb_GUI"; Filename: "{app}\LinComb_GUI.exe"
Name: "{commondesktop}\LinComb_GUI"; Filename: "{app}\LinComb_GUI.exe"; Tasks: desktopicon
Name: "{group}\Documentation"; Filename: "{app}\doc"

[Run]
Filename: "{app}\PrestoPronto.exe"; Description: "{cm:LaunchProgram,PrestoPronto}"; Flags: nowait postinstall skipifsilent
;Filename: "{app}\PCA_GUI.exe"; Description: "{cm:LaunchProgram,CA_GUI}"; Flags: nowait postinstall skipifsilent
