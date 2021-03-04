from SimConnect import *

def ac_init(aq, ae):
    # Check and set initial aircraft settings:
    # AP1 ON, ATHR ON, FD ON & CLB
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
    
    aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:1", 82)
    aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:2", 82)
    
    return
  
def crz_alt_ias(sm, aq, ae, altitude, ias):
    # Altitude - set FCU Altitude, choose Selected mode 
    # & force final Altitude
    target_altitude = int(altitude)
    event_to_trigger = ae.find("AP_ALT_VAR_SET_ENGLISH")  
    event_to_trigger(target_altitude)
    asi = Event(b'ALTITUDE_SLOT_INDEX_SET', sm)
    asi(1)
    aq.set("INDICATED_ALTITUDE", altitude)
    
    # Speed(IAS) - set FCU IAS, choose Selected mode 
    # & force final Speed
    target_speed = int(ias)
    event_to_trigger = ae.find("AP_SPD_VAR_SET")  
    event_to_trigger(target_speed)
    ssi = Event(b'SPEED_SLOT_INDEX_SET', sm)
    ssi(1)
    aq.set("AIRSPEED_INDICATED", ias)
    
    return
    
def W_n_B(aq):
    empty_weight = float(aq.get("EMPTY_WEIGHT"))
    max_gross_weight = float(aq.get("MAX_GROSS_WEIGHT"))
    stations = int(aq.get("PAYLOAD_STATION_COUNT"))
    fuel_weight_gallon = float(aq.get("FUEL_WEIGHT_PER_GALLON"))
    max_fuel_gal = float(aq.get("FUEL_TOTAL_CAPACITY"))
    max_fuel_lbs = max_fuel_gal*fuel_weight_gallon
    max_payload = (max_gross_weight-empty_weight)-max_fuel_lbs
    station = []
    
    # Obtain present Weight, CG and Fuel conditions
    actual_cg = aq.get("CG_PERCENT")
    actual_weight = aq.get("TOTAL_WEIGHT")
    actual_fuel = aq.get("FUEL_TOTAL_QUANTITY")
    total_fuel = float(actual_fuel)*float(fuel_weight_gallon)
    
    for i in range(1, stations+1):
        payload = "PAYLOAD_STATION_WEIGHT:" + str(i)
        station.append(aq.get(payload))
        
    return total_fuel, station