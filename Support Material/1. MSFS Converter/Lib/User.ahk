; Functions.ahk

GoTo EndOfUser

;;;;;;;;;;;;;;;
; ASOBO TO P3D
;;;;;;;;;;;;;;;
; Aircraft CFG
;;;;;;;;;;;;;;;
Asobo:
{
	Global TargetPath
	Global tmpCfg
	Global aircraftP3D
	Global airP3D
	Global airDat
	
	DebugAppend("`n    ----------------------------------------")
	DebugAppend("[I] Initiated MSFS to P3D Conversion Process")
	DebugAppend("    ----------------------------------------`n")
	
	; Cleaning Up
	FileCreateDir, %TargetPath%\P3D Model
	tmpCfg = %TargetPath%\P3D Model\tmp.cfg
	aircraftP3D = %TargetPath%\P3D Model\aircraft.cfg
	airP3D = %TargetPath%\P3D Model\airP3D.txt
	IniRead, airDat, msfs.ini, Paths, AirDat
	airDat = %airDat%\aired.ini
	
	If FileExist(tmpCfg)
		FileDelete, %tmpCfg%

	If FileExist(aircraftP3D)
		FileDelete, %aircraftP3D%
		
	If FileExist(airP3D)
		FileDelete, %airP3D%
		
	To_Aircraft()
	To_Air()
	
	If FileExist(tmpCfg)
		FileDelete, %tmpCfg%
		
	DebugAppend("`n    ----------------------------------------")
	DebugAppend("[I] MSFS to P3D Conversion Process Ended")
	DebugAppend("    ----------------------------------------`n")
		
	return
}

To_Aircraft()
{

	; Merging all config files
	Loop, *.cfg
	{
	  FileRead, aFileContents, %A_LoopFileFullPath% 
	  FileAppend, %aFileContents%, %tmpCfg% 
	}
	
	; Substituting Double-quotes
	FileRead, OldText, %tmpCfg%
	StringReplace, NewText, OldText, ", <q>, All
	FileDelete, %tmpCfg% 
	FileAppend, %NewText%, %tmpCfg% 
	
	; Parsing through Config Keys
	IniRead, Sections, .\Templates\cfg.txt
	Loop, parse, Sections, `n, `r
	{
		Section = %A_LoopField%
	
		StringRight, SectionSuffix, Section, 2
		
		; Checking for MULTI-SECTIONS
		If (SectionSuffix == ".n"){
			StringTrimRight, SectionRoot, Section, 1
			multiSection = 1
		}
		else
			multiSection = 0
		
		Loop, ; Looping .n Sections
		{
			IniRead, Keys, .\Templates\cfg.txt, %Section%
			
			If (multiSection = 1){
				m := A_Index-1
				SectionUpdated = %SectionRoot%%m%
				IniRead, CheckSection, %tmpCfg%, %SectionUpdated%

				If (!CheckSection)
					break
			}
			else
				SectionUpdated = %Section%
			
			Loop, parse, Keys, `n, `r
			{
				Key = %A_LoopField%
				
				StringRight, KeySuffix, Key, 2
				
				; Checking for MULTI-KEYS
				If (KeySuffix == ".n"){
					StringTrimRight, KeyRoot, Key, 1
					multiKey = 1
				}
				else
					multiKey = 0

				Loop, ; Looping .n Keys
				{
					
					If (multiKey = 1){
						n := A_Index-1
						KeyUpdated = %KeyRoot%%n%
						
						IniRead, CheckKey, %tmpCfg%, %SectionUpdated%, %KeyUpdated%
						Value = %CheckKey%
						
						If (CheckKey == "ERROR") 
							break
					}
					else{
						KeyUpdated = %Key%
						IniRead, Value, %tmpCfg%, %SectionUpdated%, %KeyUpdated%
					}
					
					If (Value != "ERROR")
						IniWrite, %Value%, %aircraftP3D%, %SectionUpdated%, %KeyUpdated%

					If (multiKey = 0)
						break
				}
			}
			
			If (multiSection = 0)
				break
		}
	}
	
	; Substituting Double-quotes again
	FileRead, OldText, %aircraftP3D%
	StringReplace, NewText, OldText, <q>, ", All
	FileDelete, %aircraftP3D% 
	FileAppend, %NewText%, %aircraftP3D% 
		
	DebugAppend("[I] Aircraft.cfg File Succesfuly Generated")
	return
}

To_Air()
{	
	airLine := []
	IniRead, Sections, %tmpCfg%
	id := 0 ; Initializing Multi
	recCount := 0 ; Initializing record count
	head := "Found " . airDat
	
	FileAppend, %head%`r`n , %airP3D%
	
	Loop, Read, .\Templates\air.txt
	{
		
		;Parsing air.txt line by line
		Loop, parse, A_LoopReadLine, CSV
		{
			airLine[A_Index] := A_LoopField
		}
		
		;Obtaining matches from CFG Files
		Loop, parse, Sections, `n, `r
		{
			Section = %A_LoopField%
			Key := airLine[1]
			IniRead, Value, %tmpCfg%, %Section%, %Key%
			
			If (Value != "ERROR")
			{
				If ((airLine[3] == "P") or (airLine[3] == "X"))
				{	
					If (airLine[2] = 1549)
						recCount-=0.5
					func_Air_noMulti(airLine, airP3D, Value)
					recCount++
				}
				else
				{
					If (airLine[2] != id)
						recCount++
					id := func_Air_Multi(airLine, airP3D, Value, id)
				}
				
				break
			}
				
		}
	}
	
	tail_1 := "Record count: " . Round(recCount,0)
	
	FileAppend, `r`n%tail_1%`r`n, %airP3D%

	DebugAppend("[I] AIR File Succesfuly Generated")
	Return
}

P3D:
{
	MsgBox, Hola
	return
}

EndOfUser: