import pandas as pd
import fbw
import logger
import time
from SimConnect import *

def cruise(w, points):
    df = fbw.data_read('CRZ')
    logger.test_header(w, "CRZ")
    start_time = time.time()
    i = 1
    weight, altitude, ias = fbw.a32x_state(df)
    logger.test_env(w, weight, altitude, ias, i, points)
    
    ## Create SimConnect link
    sm = SimConnect()
    aq = AircraftRequests(sm, _time=0)
    ae = AircraftEvents(sm)
    
    ############################################
    ## Check Environment and Aircraft Status:
    ## - AP1 ON, ATHR ON, FD ON
    ############################################
    AP = aq.get("AUTOPILOT_MASTER")
    ATHR = aq.get("AUTOTHROTTLE_ACTIVE")
    FD = aq.get("AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE")
    
    event_to_trigger = ae.find("TOGGLE_FLIGHT_DIRECTOR")
    event_to_trigger()
    event_to_trigger()
    
    if (AP == 0):
        event_to_trigger = ae.find("AP_MASTER")
        event_to_trigger()
    if (ATHR == 0):
        event_to_trigger = ae.find("AUTO_THROTTLE_ARM")
        event_to_trigger()
    if (FD == 0):
        event_to_trigger = ae.find("TOGGLE_FLIGHT_DIRECTOR")
        event_to_trigger()
    
    ## Set Throttle to CLIMB
    aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:1", 82)
    aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:2", 82)
    
    ## Set Key Aircraft Parameters   
    asi = Event(b'ALTITUDE_SLOT_INDEX_SET', sm)
    ssi = Event(b'SPEED_SLOT_INDEX_SET', sm)

    ## Altitude
    target_altitude = int(altitude)
    event_to_trigger = ae.find("AP_ALT_VAR_SET_ENGLISH")  
    event_to_trigger(target_altitude)
    asi(1)
    aq.set("INDICATED_ALTITUDE", altitude)
    
    ## Speed
    target_speed = int(ias)
    event_to_trigger = ae.find("AP_SPD_VAR_SET")  
    event_to_trigger(target_speed)
    ssi(1)
    aq.set("AIRSPEED_INDICATED", ias)
    
    ####################################
    ## Check Altitude/ Speed Stability 
    ####################################
    error_alt = 1
    error_ias = 1
    actual_vs = 1000
    while error_alt > 1 or error_ias > 1 or abs(actual_vs) > 20:
        actual_alt = aq.get("INDICATED_ALTITUDE")
        actual_ias = aq.get("AIRSPEED_INDICATED")
        actual_vs = aq.get("VERTICAL_SPEED")
        error_alt = abs((actual_alt-altitude)/altitude)*100
        error_ias = abs((actual_ias-ias)/ias)*100
        msg = "Alt: " + str(error_alt) + "  IAS: " + str(error_ias) + "  VS: " + str(actual_vs)
        w.updateStatus(msg)
        #time.sleep(1)
    
    print(error_alt, " ", error_ias, " ", actual_vs)
    
    ## Tweak Aircraft Weight
    actual_weight = aq.get("TOTAL_WEIGHT")
    
    print(actual_weight)
    elapsed_time = time.time()-start_time
    #w.statusBar().showMessage("Elapsed= " + str(elapsed_time))
    
    #sm.quit()
    exit()

    return
