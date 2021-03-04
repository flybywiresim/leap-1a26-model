import time
from SimConnect import *

def ac_init(aq, ae, clb):
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
    
    aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:1", clb)
    aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:2", clb)
    
    aq.set("TRUE_AIRSPEED_SELECTED",1)
    
    return
  
def crz_alt_tas(sm, aq, ae, altitude, tas):
    # Altitude - set FCU Altitude, choose Selected mode 
    # & force final Altitude
    target_altitude = round(float(altitude))

    event_to_trigger = ae.find("AP_ALT_VAR_SET_ENGLISH")   
    event_to_trigger(target_altitude)
    time.sleep(0.5)
    
    asi = Event(b'ALTITUDE_SLOT_INDEX_SET', sm)
    time.sleep(0.5)
    asi(1)
    aq.set("INDICATED_ALTITUDE", altitude)
    
    # Speed(tas) - set FCU tas, choose Selected mode 
    # & force final Speed
    target_speed = round(float(tas))
    actual_speed = 0
    
    while abs(actual_speed-target_speed) > 0.5:
        event_to_trigger = ae.find("AP_SPD_VAR_SET")  
        event_to_trigger(target_speed)
        actual_speed = float(aq.get("AUTOPILOT_AIRSPEED_HOLD_VAR"))
     
    time.sleep(0.5)
    ssi = Event(b'SPEED_SLOT_INDEX_SET', sm)
    time.sleep(0.5)
    ssi(1)
    aq.set("AIRSPEED_TRUE", tas)
    
    aq.set("VERTICAL_SPEED", 0) 
    
    return
    
def W_n_B(aq, weight, cg):
    empty_weight = float(aq.get("EMPTY_WEIGHT"))
    max_gross_weight = float(aq.get("MAX_GROSS_WEIGHT"))
    fuel_weight_gallon = float(aq.get("FUEL_WEIGHT_PER_GALLON"))
    max_fuel_gal = float(aq.get("FUEL_TOTAL_CAPACITY"))
    wing_aux_capacity_gal = float(aq.get("FUEL_TANK_LEFT_AUX_CAPACITY"))
    wing_main_capacity_gal = float(aq.get("FUEL_TANK_LEFT_MAIN_CAPACITY"))
    center_capacity_gal = float(aq.get("FUEL_TANK_CENTER_CAPACITY"))
    max_fuel_lbs = max_fuel_gal*fuel_weight_gallon
    wing_aux_capacity_lbs = wing_aux_capacity_gal*fuel_weight_gallon
    wing_main_capacity_lbs = wing_main_capacity_gal*fuel_weight_gallon
    center_capacity_lbs = center_capacity_gal*fuel_weight_gallon
    max_payload = (max_gross_weight-empty_weight)-max_fuel_lbs
    wing_aux_qty_lbs = 0
    wing_main_qty_lbs = 0
    center_qty_lbs = 0
    
    # Checking fuel and payload limits
    obj_fuel_weight = (weight - empty_weight)*0.4
    obj_payload_weight = (weight - empty_weight)*0.6
    
    if (obj_fuel_weight < 500):
        obj_fuel_weight = 500
        obj_payload_weight = (weight - empty_weight) - obj_fuel_weight
    if (obj_fuel_weight > max_fuel_lbs):
        obj_fuel_weight = max_fuel_lbs
        obj_payload_weight = (weight - empty_weight) - obj_fuel_weight
    
    # Introducing Fuel from Outter to Center
    if (obj_fuel_weight > (wing_aux_capacity_lbs*2)):
        wing_aux_qty_lbs = wing_aux_capacity_lbs
        remaining_fuel_weight = obj_fuel_weight-(wing_aux_capacity_lbs*2)
        if (remaining_fuel_weight > (wing_main_capacity_lbs*2)):
            wing_main_qty_lbs = wing_main_capacity_lbs
            remaining_fuel_weight = remaining_fuel_weight-(wing_main_capacity_lbs*2)
            center_qty_lbs = remaining_fuel_weight
        else:
            wing_main_qty_lbs = remaining_fuel_weight/2
    else: 
        wing_aux_qty_lbs = obj_fuel_weight/2
    
    aq.set("FUEL_TANK_LEFT_AUX_QUANTITY", wing_aux_qty_lbs/fuel_weight_gallon)
    aq.set("FUEL_TANK_RIGHT_AUX_QUANTITY", wing_aux_qty_lbs/fuel_weight_gallon)
    aq.set("FUEL_TANK_LEFT_MAIN_QUANTITY", wing_main_qty_lbs/fuel_weight_gallon)
    aq.set("FUEL_TANK_RIGHT_MAIN_QUANTITY", wing_main_qty_lbs/fuel_weight_gallon)
    aq.set("FUEL_TANK_CENTER_QUANTITY", center_qty_lbs/fuel_weight_gallon)
    
    # Introducing Payload - Forwards Baggage and Rear Baggage
    aq.set("PAYLOAD_STATION_WEIGHT:1", 0)
    aq.set("PAYLOAD_STATION_WEIGHT:2", 0)
    aq.set("PAYLOAD_STATION_WEIGHT:3", 0)
    aq.set("PAYLOAD_STATION_WEIGHT:4", 50+obj_payload_weight/2)
    aq.set("PAYLOAD_STATION_WEIGHT:5", 0)
    aq.set("PAYLOAD_STATION_WEIGHT:6", 50+obj_payload_weight/2)

    # Obtain present Weight, CG and Fuel conditions
    actual_cg = float(aq.get("CG_PERCENT"))
    actual_weight = float(aq.get("TOTAL_WEIGHT"))
    
    # Main CG routine. A tolerance of 5% will be hard-coded
    # with a maximum loop time to break away if such tolerance
    # cannot be obtained
    pump = 1000
    below = -1
    cg_tolerance = abs(cg-actual_cg)/cg
    while (cg_tolerance > 0.01):
        if (actual_cg < cg):
            aq.set("PAYLOAD_STATION_WEIGHT:4", aq.get("PAYLOAD_STATION_WEIGHT:4")-pump)
            aq.set("PAYLOAD_STATION_WEIGHT:6", aq.get("PAYLOAD_STATION_WEIGHT:6")+pump)
            actual_cg = float(aq.get("CG_PERCENT"))
            cg_tolerance = abs(cg-actual_cg)/cg
            if (below == 0):
                pump = pump/2
            below=1
        else:
            aq.set("PAYLOAD_STATION_WEIGHT:4", aq.get("PAYLOAD_STATION_WEIGHT:4")+pump)
            aq.set("PAYLOAD_STATION_WEIGHT:6", aq.get("PAYLOAD_STATION_WEIGHT:6")-pump)
            actual_cg = float(aq.get("CG_PERCENT"))
            cg_tolerance = abs(cg-actual_cg)/cg
            if (below == 1):
                pump = pump/2
            below=0
            
        #print(" CG= " + str(actual_cg) + "below= " + str(below) + " Pump= " + str(pump) + " Tol= " + str(cg_tolerance))
	
    return