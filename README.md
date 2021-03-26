<img src="https://raw.githubusercontent.com/flybywiresim/fbw-branding/master/png/FBW-Logo.png" placeholder="Flybywire" width="300"/>

# LEAP-1A26 Engine Model & Control

![status](https://img.shields.io/badge/status-Unstable%2F%20WIP-blue)
![license](https://img.shields.io/github/license/flybywiresim/leap-1a26-model)

## About
A **FlyByWire** Repo focused on the **analysis**, **development** and full **integration** of a realistic **CFM LEAP-1A26** engine model and control (FADEC). 

Please be aware we are still within the **assessment** and **analysis** phase of this initiative, so **_no installations or integrations can be performed yet within the Sim_**.

Stay tuned for updates!

## Legend
:heavy_check_mark: Issue/ feature completely solved/ developed and integrated in the master in its final and definitive version

:warning: Issue/ feature partially solved/ developed and integrated in the master or dev/ experimental branch

:x: Issue/ feature pending

:hourglass: Work in progress

## Roadmap
Tentative roadmap is as follows (it will be updated accordingly):

- [x] Understand Asobo's Engine model approach (basically engines.cfg) :heavy_check_mark:
- [x] Gather data and information on the LEAP-1A (Official/ Unofficial) :heavy_check_mark:
- [x] Physical/ theoretical modeling :heavy_check_mark:

#### Engine Primary Parameter Modeling
 - [x] N1 and N2 :warning: 
 - [x] EGT :heavy_check_mark: 
 - [x] Fuel Flow :heavy_check_mark: 
  
#### Engine Secondary Parameter Modeling
 - [ ] Oil Qty, Pressure and Temperature 
 - [ ] Vibration Parameters
 - [ ] Nacelle Temperature

#### FADEC/ EEC
 - [ ] Start-up and Ignition 
    - [ ] Auto :hourglass:
    - [ ] Manual 
 - [ ] Thrust Limits :hourglass:
 - [ ] EGT and OAT Limiting
 - [x] Fuel Injector/ Dumper :heavy_check_mark:
 - [ ] Idle Management
     - [x] Minimum Idle :heavy_check_mark:
     - [ ] Approach Idle
 - [ ] Thrust Reverse Management

#### Visuals
- [ ] Upper ECAM
   - [ ] Units (Metric & Imperial) :hourglass:
   - [ ] Overall Fidelity (i.e. N2 decimals above 100%)
- [ ] Lower ECAM
   - [ ] Units (Metric & Imperial) :hourglass:
   - [ ] Engine Page Fidelity
   - [ ] Fuel Page Fidelity :hourglass:
 
#### Misc/ Non-Normal Ops
 - [x] Independent Engine Control :heavy_check_mark:
 - [ ] Windmilling
 - [ ] Gravity Feeding
 - [ ] Engine Cycle and Wear


## Requirements
* Python code developed and ran in **Jupyter Notebooks** on python 3.8.3 for x64.
* MSFS Converter developed with **AutoHotKey 1.1.30** for x64

## Additional context and Disclaimer
For anything related to the engine and/ or this repo, do not hesitate in 'pinging' me. 
_Discord username_: **TazX [Z+1]#0405**
