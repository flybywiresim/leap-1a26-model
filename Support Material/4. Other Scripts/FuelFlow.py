import time
from SimConnect import *

sm = SimConnect()
aq = AircraftRequests(sm, _time=0)
ae = AircraftEvents(sm)

event_to_trigger = ae.find("AUTOBRAKE_DISARM")
event_to_trigger("TRUE")

exit()
