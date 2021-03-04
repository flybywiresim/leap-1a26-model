import time
from SimConnect import *

sm = SimConnect()
aq = AircraftRequests(sm, _time=0)
ae = AircraftEvents(sm)
n1 = 0

start_time = time.time()
aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:1", 39.2)
time.sleep(0.1)
aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:2", 39.2)
time.sleep(0.1)

while n1 < 49.9:
    n1 = float(aq.get("TURB_ENG_N1:1"))
    
end_time = time.time() - start_time
print("IDLE-50%: " + str(end_time))
time.sleep(2)

start_time = time.time()
aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:1", 100)
time.sleep(0.1)
aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:2", 100)
time.sleep(0.1)

while n1 < 83:
    n1 = float(aq.get("TURB_ENG_N1:1"))
    
end_time = time.time() - start_time
print("50%-TOGA N1: " + str(end_time))

#sm.quit()
exit()
