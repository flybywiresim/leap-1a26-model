; Functions.ahk

GoTo EndOfFunctions

;;;;;;;;;;;;;;;
; Functions
;;;;;;;;;;;;;;;
func_Air_noMulti(airLine, airP3D, Value)
{
	; Getting number of rows and columns
	StringReplace, Value, Value, %A_SPACE%,, All
	rowsNoComments := StrSplit(Value, ";")
	rows := StrSplit(rowsNoComments[1], ",")
	
	; Header
	id := Format("{:04} ",airLine[2])
	h1 := "Record: " . id . airLine[6]
	If (airLine[3] == "P")  
		h2 := "Points: " . rows.MaxIndex()
	Else
	{
		cols := StrSplit(rows[1], ":")
		h2 := "columns: " . cols.MaxIndex() . "  " . "rows: " . rows.MaxIndex()
	}
	
	If ((airLine[2] = 1549) and (airLine[3] == "P"))
		FileAppend, `r`n%h1%`r`n, %airP3D%
	Else If ((airLine[2] = 1549) and (airLine[3] == "X"))
		FileAppend, %h2%`r`n, %airP3D%
	Else
		FileAppend, `r`n%h1%`r`n%h2%`r`n, %airP3D%
	
	Loop, % rows.MaxIndex()
	{
		fields := StrSplit(rows[A_Index], ":")
		line := ""
		; Check whether the table is the Mach vs. 17 fields
		If (airLine[8] == "tbl17")
		{
			line := Round(fields[2]*2048, 0)
		}
		Else
		{
			Loop, % fields.MaxIndex()
			{
				i := A_INDEX
				fields[i] := Format("{1:0.6f}", fields[i])
				If (i = 1)
					line := fields[i]
				Else
					line := line . A_TAB . fields[i]
			}
		}
		
		If (airLine[3] == "P")
		{
			FileAppend, %line%`r`n, %airP3D%
		}
		Else
		{
			FileAppend, %line%%A_TAB%`r`n, %airP3D%
		}
	}
	
	Return
}

func_Air_Multi(airLine, airP3D, Value, id)
{
	Value := StrSplit(Value, ";")
	Value := Trim(Value[1])
	
	airLine[2]+=0
	
	If (airline[5] == "DOUBLE")
			Value := Format("{1:0.6f}", Value)
	
	If (airLine[2] != id)
	{
		; Header
		id := Format("{:04} ",airLine[2])
		h1 := "Record: " . id . airLine[7]
		h2 := "FIELD 0x" . airLine[2] . A_TAB . airLine[4] . A_TAB . airLine[5] . A_TAB . Value . A_TAB . airLine[6]
		
		FileAppend, `r`n%h1%`r`n%h2%`r`n, %airP3D%
	}
	else
	{
		h2 := "FIELD 0x" . airLine[2] . A_TAB . airLine[4] . A_TAB . airLine[5] . A_TAB . Value . A_TAB . airLine[6]
		id := airLine[2]
		
		FileAppend, %h2%`r`n, %airP3D%
	}
	
	Return id
}

checkIniFile(x)
{
	if(x = 0){
		if FileExist("msfs.ini"){
			IniRead, AirVar, msfs.ini, Paths, Aircraft
			IniRead, TargetVar, msfs.ini, Paths, Target
			If (AirVar != 0)
				GuiControl,,AirPath,%AirVar%
			If (TargetVar != 0)
				GuiControl,,TargetPath,%TargetVar%
		}
		else{
			IniWrite, 0, msfs.ini, Paths, Aircraft
			IniWrite, 0, msfs.ini, Paths, Target
			IniWrite, 0, msfs.ini, Paths, AirDat
		}
	}
	else{
		GuiControlGet, AirPath
		GuiControlGet, TargetPath
		IniWrite, %AirPath%, msfs.ini, Paths, Aircraft
		IniWrite, %TargetPath%, msfs.ini, Paths, Target
	}
	return
}

DebugAppend(Data)
{
	GuiControlGet, Debug
	GuiControl,, Debug, %Debug%%Data%`n
	ControlSend, Edit3, {ctrl down}{End}{ctrl up}
	Return
}

;;;;;;;;;;;;;;;
; Subroutines
;;;;;;;;;;;;;;;
BrowseAircraft:
{
	Thread, NoTimers
	FileSelectFolder, airDir,*C:\, 3
	GuiControl,,AirPath,%airDir%
	Thread, NoTimers, false
	return
}


BrowseTarget:
{
	Thread, NoTimers
	FileSelectFolder, targetDir,*C:\, 3
	GuiControl,,TargetPath,%targetDir%
	Thread, NoTimers, false
	return
}

Verify:
{
	GuiControlGet, AirPath
	GuiControlGet, TargetPath
	DebugAppend("    ------------------------------")
	DebugAppend("[I] Initiated Verification Process")
	DebugAppend("    ------------------------------`n")
	checkIniFile(1)
	
	c1=0
	c2=0
	c3=0
	c4=0
	c5=0
	c6=0
	c7=0
	c8=0
	; Check AIR file
	DebugAppend("[I] Checking for minimum critical files")
	If (FileExist(AirPath "\*.air")){
		loop, %AirPath%\*.air{
			Number := A_Index
		}
		If (Number > 1){
			Gui Font
			DebugAppend("[X] ---- More than ONE AIR file found")
			c1=-1
		}
		else if (Number = 1){
			Loop, %AirPath%\*.air
				air_file = %A_LoopFileName%
			DebugAppend("[I] ---- AIR File - " air_file " - found")
			c1=1
		}
		else{
			DebugAppend("[X] ---- AIR File NOT found")
		}
	}
	
	; Check Aircraft file
	If (FileExist(AirPath "\aircraft.cfg")){
		DebugAppend("[I] ---- aircraft.cfg File found")
		c2=1
	}
	else
		DebugAppend("[X] ---- aircraft.cfg File NOT found")
	
	; Check Engines file
	If (FileExist(AirPath "\engines.cfg")){
		DebugAppend("[I] ---- engines.cfg File found")
		c5=1
	}
	else
		DebugAppend("[X] ---- engines.cfg File NOT found")
		
	; Check FM file
	If (FileExist(AirPath "\flight_model.cfg")){
		DebugAppend("[I] ---- flight_model.cfg File found")
		c6=1
	}
	else
		DebugAppend("[X] ---- flight_model.cfg File NOT found")
		
	DebugAppend("`n[I] Checking for additional files")
	
	; Check Cameras file
	If (FileExist(AirPath "\cameras.cfg")){
		DebugAppend("[I] ---- cameras.cfg File found")
		c3=1
	}
	else
		DebugAppend("[X] ---- cameras.cfg File NOT found")
		
	; Check Cockpit file
	If (FileExist(AirPath "\cockpit.cfg")){
		DebugAppend("[I] ---- cockpit.cfg File found")
		c4=1
	}
	else
		DebugAppend("[X] ---- cockpit.cfg File NOT found")
		
	; Check Gameplay file
	If (FileExist(AirPath "\gameplay.cfg")){
		DebugAppend("[I] ---- gameplay.cfg File found")
		c7=1
	}
	else
		DebugAppend("[X] ---- gameplay.cfg File NOT found")
		
	; Check Systems file
	If (FileExist(AirPath "\systems.cfg")){
		DebugAppend("[I] ---- systems.cfg File found")
		c8=1
	}
	else
		DebugAppend("[X] ---- systems.cfg File NOT found")
		
	If (c1 = -1)
		DebugAppend("[X] Verification FAILED")
		
	DebugAppend("")
	If (c1 + c2 = 2){
		DebugAppend("[I] Prepar3D Structure FOUND and Activated")
		GuiControl,Enable,P3D
	}
	
	If (c2 + c5 + c6 = 3){
		DebugAppend("[I] Minimum MSFS2020 Structure FOUND and Activated")
		GuiControl,Enable,Asobo
	}
	If ((c1 + c2 != 2) and (c2 + c5 + c6 != 3)){
		DebugAppend("[X] Failed to construct MSFS and/ or P3D structures")
	}
	return
}

EndOfFunctions: