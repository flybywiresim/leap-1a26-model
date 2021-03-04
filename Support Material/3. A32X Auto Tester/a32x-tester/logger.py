import datetime

def test_header(w, fp):
    x = datetime.datetime.now()
    w.clearText()
    w.log("==================================================", 1)
    w.log(fp + " Testbench Started on " + str(x), 1)
    w.log("==================================================", 1)
    w.log("", 1)

def test_simconnect(w, running):
    if (running == 1):
        w.log("Simconnect.dll loaded!", 1)
        w.log("", 1)
    else:
        w.log("", 1)
        w.log("Simconnect.dll unloaded!", 1)
    
def test_init(w, step):
    if (step == 1):
        w.log("-- AP1, ATH/R and FD Set", 1)
        w.log("", 1)
    else:
        w.log("-- FCU Heading, Altitude and Speed Set to Selected", 1)
        w.log("", 1)

def test_loop(w, step):
    if (step == 1):
        w.log("==================================================", 1)
        w.log("Starting CRZ test loop ...", 1)
        w.log("==================================================", 1)
        w.log("", 1)
    else:
        w.log("", 1)
        w.log("==================================================", 1)
        w.log("Finished CRZ test loop ...", 1)
        w.log("==================================================", 1)
    
def test_obj(w, weight, cg, altitude, tas, mach, n1, i, points):
    w.log("Test [" + str(i) + " of " + str(points) + "] OBJECTIVES: weight=" + str(weight) + ", cg=" + str(cg*100) + ", altitude=" + str(altitude) + ", tas=" + str(tas) + ", M=" + str(mach) + ", n1=" + str(round(n1,1)), 1)
  
def test_actual(w, actual_weight, actual_cg, actual_alt, actual_tas, actual_mach, actual_vs, actual_fn, actual_n1, actual_n2, actual_n1_cor, actual_n2_cor, actual_egt, actual_ff, i, points):
    w.log(", RESULTS: weight=" + str(round(actual_weight,1)) + ", cg=" + str(round(actual_cg*100,1)) + ", altitude=" + str(round(actual_alt,1)) + ", tas=" + str(round(actual_tas,1)) + ", M=" + str(round(actual_mach,3)) + ", vs=" + str(round(actual_vs,1)) + ", fn=" + str(round(actual_fn,1)) + ", n1=" + str(round(actual_n1,1)) + ", n2=" + str(round(actual_n2,1)) + ", cn1=" + str(round(actual_n1_cor,1)) + ", cn2=" + str(round(actual_n2_cor,1)) + ", egt=" + str(round(actual_egt,1)) + ", ff=" + str(round(actual_ff,1)), 0)
    w.log("",1)