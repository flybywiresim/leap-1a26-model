import pandas as pd
import random
        
def data_read(phase, inFile):
    df = pd.read_csv(inFile)
    df = df.rename(columns = {'ALT.':'Alt', 'MACH':'Mach'}, inplace=False)
    df = df[df['PHASE'] == phase]
    df = df.reset_index(drop=True)   
    return df
    
def a32x_state_rnd(df, n):
    for i in range(1,n):
        weight=0
        while (weight < 90900) or (weight > 174165):
            row = random.randint(0,len(df))
            weight = df.WEIGHT[row]
    
    weight=0    
    while (weight < 90900) or (weight > 174165):
        row = random.randint(0,len(df))
        weight = df.WEIGHT[row]
        altitude = df.Alt[row]
        tas = df.TAS[row]
        mach = df.Mach[row]
        n1 = df.N1[row]
    return weight, altitude, tas, mach, n1

def a32x_state_nrm(df, row):     
    weight = df.WEIGHT[row]
    altitude = df.Alt[row]
    tas = df.TAS[row]
    mach = df.Mach[row]
    n1 = df.N1[row]
    
    return weight, altitude, tas, mach, n1
