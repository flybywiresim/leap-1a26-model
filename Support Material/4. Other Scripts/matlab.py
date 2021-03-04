import time
from SimConnect import *

sm = SimConnect()
aq = AircraftRequests(sm, _time=0)
ae = AircraftEvents(sm)

# target_speed = 260 #240 - 260
# event_to_trigger = ae.find("AP_SPD_VAR_SET")  
# event_to_trigger(target_speed)
 
# time.sleep(0.5)
# ssi = Event(b'SPEED_SLOT_INDEX_SET', sm)
# ssi(1)
# time.sleep(0.5)

# sm.quit()
# exit()

hsi = Event(b'HEADING_SLOT_INDEX_SET', sm)
hsi(1)

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

aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:1", 89.8)
aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:2", 89.8)
    
altitude = 36000
tas = 459

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

event_to_trigger = ae.find("AP_SPD_VAR_SET")  
event_to_trigger(target_speed)
 
time.sleep(0.5)
ssi = Event(b'SPEED_SLOT_INDEX_SET', sm)
time.sleep(0.5)
ssi(1)
aq.set("AIRSPEED_TRUE", tas)
time.sleep(0.5)
aq.set("VERTICAL_SPEED", 0)
time.sleep(0.5)

# aq.set("FUEL_TANK_LEFT_AUX_QUANTITY", 226.67)
# aq.set("FUEL_TANK_RIGHT_AUX_QUANTITY", 226.67)
# aq.set("FUEL_TANK_LEFT_MAIN_QUANTITY", 159.84)
# aq.set("FUEL_TANK_RIGHT_MAIN_QUANTITY", 159.84)
# aq.set("FUEL_TANK_CENTER_QUANTITY", -6)

# # Introducing Payload - Forwards Baggage and Rear Baggage
# aq.set("PAYLOAD_STATION_WEIGHT:1", 0)
# aq.set("PAYLOAD_STATION_WEIGHT:2", 0)
# aq.set("PAYLOAD_STATION_WEIGHT:3", 0)
# aq.set("PAYLOAD_STATION_WEIGHT:4", 3890.142)
# aq.set("PAYLOAD_STATION_WEIGHT:5", 0)
# aq.set("PAYLOAD_STATION_WEIGHT:6", 4140.142)
    
event_to_trigger = ae.find("AP_MASTER")
event_to_trigger()
time.sleep(0.5)
event_to_trigger()
time.sleep(0.5)
sm.quit()
exit()