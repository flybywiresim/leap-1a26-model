; Simple MSFS to FSX/P3D Flight Model Converter
; Author: JM Roldan
; Date: 09/28/2020

SetWorkingDir %A_ScriptDir%
SetBatchLines -1

#SingleInstance Force
#NoEnv
#Persistent
#includeAgain %A_ScriptDir%\Lib\Functions.ahk
#includeAgain %A_ScriptDir%\Lib\User.ahk

;;;;;;;;;;;;;;;
; MAIN WINDOW
;;;;;;;;;;;;;;;
Menu Tray, Icon, %A_ScriptDir%\Icons\msfs.ico

Gui -MaximizeBox
Gui Font, s10 Norm cNavy, Source Code Pro
Gui Add, GroupBox, x24 y16 w500 h146, Settings
Gui Font
Gui Font, s9 Norm cBlack, Source Code Pro
Gui Add, Edit, x136 y56 w329 h21 vAirPath
Gui Add, Edit, x136 y96 w329 h21 vTargetPath
Gui Add, Text, x56 y56 w73 h22 +0x200, Aircraft Path
Gui Add, Text, x56 y96 w73 h22 +0x200, Target Path
Gui Add, Button, x472 y56 w22 h22 gBrowseAircraft, ...
Gui Add, Button, x472 y96 w22 h22 gBrowseTarget, ...
Gui Add, Button, x234 y128 w80 h23 gVerify, &Verify

Gui Add, Button, x167 y170 w105 h24 gAsobo +Disabled vAsobo, &Asobo->P3D
Gui Add, Button, x296 y170 w96 h23 gP3D +Disabled vP3D, &P3D->Asobo

Gui Font
Gui Font, s10 Norm cNavy, Source Code Pro
Gui Add, Text, x35 y196 w73 h22 +0x200, Log
Gui Font, s9 Norm cBlack, Consolas
Gui Add, Edit, Readonly x24 y220 w500 h180 vDebug 

checkIniFile(0)
DebugAppend("[*] Started MSFS Flight Model Converter ...`n")

Gui Show, w548 h420, MSFS Flight Model Converter

Return

GuiEscape:
GuiClose:
    ExitApp
	
	