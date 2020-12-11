<img src="https://raw.githubusercontent.com/flybywiresim/fbw-branding/master/png/FBW-Logo.png" placeholder="Flybywire" width="300"/>

# LEAP-1A26 Engine Model & Control

![status](https://img.shields.io/badge/status-Unstable%2F%20WIP-blue)
![license](https://img.shields.io/github/license/flybywiresim/leap-1a26-model)

## About
A **FlyByWire** Repo focused on the **analysis**, **development** and full **integration** of a realistic **CFM LEAP-1A26** engine model and control (FADEC). 

Please be aware we are still within the **assessment** and **analysis** phase of this initiative, so **_no installations or integrations can be performed yet within the Sim_**.

Stay tuned for updates!

## Roadmap
Tentative roadmap is as follows (it will be updated accordingly):

- [x] Understand Asobo's Engine model approach (basically engines.cfg)
- [x] Gather data and information on the LEAP-1A (Official/ Unofficial)
- [x] Physical/ theoretical modeling
- [ ] External model emulation with Matlab/ Simulink (through Simconnect)
    - [ ] Engine coarse testing (FCOM/ RL behaviour)
    - [ ] Engine fine-tune and specifities (spool-times, random behaviours, ...)
    - [ ] Visual parameter integration and validation (i.e. ECAM, ...)
- [ ] External model simulation with SimConnect (WASM)


## Requirements
* Python code developed and ran in **Jupyter Notebooks** on python 3.8.3 for x64.

## Additional context and Disclaimer
For anything related to the engine and/ or this repo, do not hesitate in 'pinging' me. 
_Discord username_: **TazX#0405**