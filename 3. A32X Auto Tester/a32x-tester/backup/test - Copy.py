import configparser
import math

cg_f = 0.33
cg_0 = 0.2678
weight = 130000
tolerance = 0.3

# Obtain W&B variables
config = configparser.ConfigParser()
config.read("A32X.ini")

# From flight_model.cfg
max_gross_weight = float(config['A32X']['max_gross_weight'])
empty_weight = float(config['A32X']['empty_weight'])
reference_datum_position = config['A32X']['reference_datum_position'].split(",")
empty_weight_CG_position = config['A32X']['empty_weight_CG_position'].split(",")
station_load_0 = config['A32X']['station_load.0']
station_load_1 = config['A32X']['station_load.1']
station_load_2 = config['A32X']['station_load.2']
station_load_3 = config['A32X']['station_load.3']
station_load_4 = config['A32X']['station_load.4']
station_load_5 = config['A32X']['station_load.5']
LeftMain = config['A32X']['LeftMain'].split(",")
RightMain = config['A32X']['RightMain'].split(",")
Center1 = config['A32X']['Center1'].split(",")
Center2 = config['A32X']['Center2'].split(",")
Center3 = config['A32X']['Center3'].split(",")
LeftAux = config['A32X']['LeftAux'].split(",")
LeftTip = config['A32X']['LeftTip'].split(",")
RightAux = config['A32X']['RightAux'].split(",")
RightTip = config['A32X']['RightTip'].split(",")
wing_area = float(config['A32X']['wing_area'])
wing_span = float(config['A32X']['wing_span'])
wing_root_chord = float(config['A32X']['wing_root_chord'])
wing_sweep = float(config['A32X']['wing_sweep'])
wing_pos_apex_lon = float(config['A32X']['wing_pos_apex_lon'])

# From SimVars
stations = 6 # aq.get("PAYLOAD_STATION_COUNT")
fuel_weight_gallon = 6.7 # float(aq.get("FUEL_WEIGHT_PER_GALLON"))
max_fuel = 7000 # float(aq.get("FUEL_TOTAL_CAPACITY"))

# Calculate MAC
#lemac = wing_pos_apex_lon - ((1-((wing_span*wing_root_chord/12)+(wing_area/6))/(wing_area/2))*wing_span*math.tan(wing_sweep*math.pi/180)/2)
mgc = wing_area/wing_span
mac = (((wing_root_chord-mgc)**2)-(0.25*(2*mgc)**2)+(4*mgc**2))/(3*mgc)

# Initial condition 
#  - set wanted weight 40% fuel/ 60% payload
#  - check values are within limits

obj_fuel_weight = (weight - empty_weight)*0.4
obj_payload_weight = (weight - empty_weight)*0.6

if (obj_fuel_weight > max_fuel*fuel_weight_gallon):
    obj_fuel_weight = max_fuel*fuel_weight_gallon
    obj_payload_weight = (weight - empty_weight) - obj_fuel_weight

# Start with fuel (in lbs) ...
# - Tip Wings
# - Aux Wings
# - First Main Wings
# - Center
wing_tip_total = float(LeftTip[3])*2*fuel_weight_gallon
wing_aux_total = float(LeftAux[3])*2*fuel_weight_gallon
wing_main_total = float(LeftMain[3])*2*fuel_weight_gallon
center_1_total = float(Center1[3])*fuel_weight_gallon
center_2_total = float(Center2[3])*fuel_weight_gallon
center_3_total = float(Center3[3])*fuel_weight_gallon
wing_tip = 0
wing_aux = 0
wing_main = 0
center_1 = 0
center_2 = 0
center_3 = 0

if(wing_tip_total > obj_fuel_weight):
    wing_tip = obj_fuel_weight/2
elif(wing_tip_total + wing_aux_total > obj_fuel_weight):
    wing_tip = wing_tip_total/2
    wing_aux = (obj_fuel_weight-wing_tip_total)/2
elif(wing_tip_total + wing_aux_total + wing_main_total > obj_fuel_weight):
    wing_tip = wing_tip_total/2
    wing_aux = wing_aux_total/2
    wing_main = (obj_fuel_weight-wing_tip_total-wing_aux_total)/2
elif(wing_tip_total + wing_aux_total + wing_main_total + center_1_total > obj_fuel_weight):
    wing_tip = wing_tip_total/2
    wing_aux = wing_aux_total/2
    wing_main = wing_main_total/2
    center_1 = (obj_fuel_weight-wing_tip_total-wing_aux_total-wing_main_total)
elif(wing_tip_total + wing_aux_total + wing_main_total + center_1_total + center_2_total > obj_fuel_weight):
    wing_tip = wing_tip_total/2
    wing_aux = wing_aux_total/2
    wing_main = wing_main_total/2
    center_1 = center_1_total
    center_2 = (obj_fuel_weight-wing_tip_total-wing_aux_total-wing_main_total-center_1_total)
else:
    wing_tip = wing_tip_total/2
    wing_aux = wing_aux_total/2
    wing_main = wing_main_total/2
    center_1 = center_1_total
    center_2 = center_2_total
    center_3 = (obj_fuel_weight-wing_tip_total-wing_aux_total-wing_main_total-center_1_total-center_2_total)
    
# Calculate CG
wing_tip = 0
wing_aux = 0
wing_main = 12060
center_1 = 0
center_2 = 0
center_3 = 0
cg_empty_num = empty_weight*float(empty_weight_CG_position[0])
cg_fuel_num = (wing_tip*float(LeftTip[0])*2)+(wing_aux*float(LeftAux[0])*2)+(wing_main*float(LeftMain[0])*2)+(center_1*float(Center1[0]))+(center_2*float(Center2[0]))+(center_3*float(Center3[0]))
cg_total_den = empty_weight + (wing_tip*2) + (wing_aux*2) + (wing_main*2) + center_1 + center_2 + center_3
if(float(empty_weight_CG_position[0]) < 0):
    lemac = float(empty_weight_CG_position[0])+(cg_0*mac)
else:
    lemac = float(empty_weight_CG_position[0])-(cg_0*mac)
    
cg_total_pct = abs(((cg_empty_num + cg_fuel_num)/cg_total_den)-lemac)/mac

print(obj_fuel_weight)
print(wing_tip)
print(wing_aux)
print(wing_main)
print(center_1)
print(float(Center1[0]))
print(cg_total_den)           
print(lemac)
print(cg_total_pct)