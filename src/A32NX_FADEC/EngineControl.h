#ifndef _ENGINECONTROL_H_
#define _ENGINECONTROL_H_

using namespace std;

class SimVars;
class Ratios;
class Polynomial;
//class Debug;

class EngineControl
{
private:
    SimVars* simVars;
    Ratios* ratios;
    Polynomial* poly;
    //Debug* debug;

    void flightPhase() {
        double simOnGround = simVars->getSimOnGround();
        double altitude = simVars->getPlaneAltitudeAGL();
        double verticalSpeed = simVars->getVerticalSpeed();
        double actualFlightPhase = simVars->getActualPhase();
        double preFlightPhase = simVars->getPrePhase();

        /*debug->text("PRE = ");
        debug->text(std::to_string(preFlightPhase));*/

        // Checking aircraft initial state
        if (preFlightPhase == -1) {
            if (simOnGround == 1) {
                preFlightPhase = 0;
                actualFlightPhase = 0;
            }
            else {
                preFlightPhase = 2;
                actualFlightPhase = 2;
            }
            simVars->setPrePhase(preFlightPhase);
        }  
        else {
            // Takeoff Phase
            if (simOnGround == 1 && preFlightPhase == 0) {
                actualFlightPhase = 0;
            }
            else if (simOnGround == 0 && preFlightPhase == 0 && altitude <= 500) {
                actualFlightPhase = 0;
            }
            // Climb Phase
            else if (simOnGround == 0 && verticalSpeed >= 300 && altitude > 500) {
                actualFlightPhase = 1;
            }
            // Descent Phase
            else if (simOnGround == 0 && verticalSpeed < -1200 && altitude > 500) {
                actualFlightPhase = 3;
            }
            // Landing Phase
            else if (simOnGround == 1 && preFlightPhase != 0) {
                actualFlightPhase = 4;
            }
            else if (simOnGround == 0 && preFlightPhase != 0 && altitude <= 500) {
                actualFlightPhase = 4;
            }
            else  {
                actualFlightPhase = 2;
            }       
        }

        simVars->setActualPhase(actualFlightPhase);

        /*debug->text(" ACTUAL = ");
        debug->text(std::to_string(actualFlightPhase));
        debug->text(" ALT = ");
        debug->text(std::to_string(altitude));
        debug->text(" VS = ");
        debug->text(std::to_string(verticalSpeed));
        debug->text(" GND = ");
        debug->text(std::to_string(simOnGround));*/
    }
    /// <summary>
    /// Engine Imbalance Digital Word:
    /// 00 - Engine, 00 - N2, 00 - FuelFlow, 00 - EGT
    /// </summary>
    /// <param name="initial"></param>
    void EngineImbalance(int initial) 
    {
        int engine = 0;
        int dice = 0;
        int egt_imbalance = 0;
        int ff_imbalance = 0;
        int N2_imbalance = 0;
        string imbalance;

        srand((int)time(0));

        if (initial == 1) {
            // Decide Engine with imbalance
            if ((rand() % 100) + 1 < 50) {
                engine = 1;
            }
            else {
                engine = 2;
            }
            // Obtain EGT imbalance
            egt_imbalance = (rand() % 20) + 1;

            // Obtain FF imbalance
            dice = (rand() % 100) + 1;

            if (dice > 85) {
                ff_imbalance = 40;
            }
            else if (dice < 30) {
                ff_imbalance = 0;
            }
            else {
                ff_imbalance = 20;
            }

            // Obtain N2 imbalance
            N2_imbalance = ((rand() % 30) + 1);

            // Zero Padding and Merging
            imbalance = to_string_with_zero_padding(engine, 2) + to_string_with_zero_padding(egt_imbalance, 2) + \
                to_string_with_zero_padding(ff_imbalance, 2) + to_string_with_zero_padding(N2_imbalance, 2);
            
            simVars->setEngineImbalance(stod(imbalance));
        }

       
         

    }

    void updateEGT(int idx)
    {
        double cn1 = simVars->getCN1(idx);
        double mach = simVars->getMach();
        double altitude = simVars->getPlaneAltitude();
        double ISADelta = simVars->getAmbientTemperature() - simVars->getStdTemperature() ;
        double egtNX = poly->egtNX(cn1, mach, altitude, ISADelta);

        if (idx == 1) {
            simVars->setEngine1EGT(egtNX * ratios->theta2());
        }
        else {
            simVars->setEngine2EGT(egtNX * ratios->theta2());
        }
    }

    void updateFF(int idx)
    {  
        double cn1 = simVars->getCN1(idx);
        double mach = simVars->getMach();
        double altitude = simVars->getPlaneAltitude();
        double ISADelta = simVars->getAmbientTemperature() - simVars->getStdTemperature();
        double actualFlightPhase = simVars->getActualPhase();
        double preFlightPhase = simVars->getPrePhase();
        double prevFuelFlow = 0;
        double flow_out = 0;
        double delta = 0;

        if (idx == 1) {
            prevFuelFlow = simVars->getEngine1FF(); // in Kgs/hr
            /*debug->text(" PAST FF = ");
            debug->text(std::to_string(prevFuelFlow));*/
        }
        else {
            prevFuelFlow = simVars->getEngine2FF(); // in Kgs/hr
        }

        double flowNX = poly->flowNX(idx, cn1, mach, altitude, ISADelta, preFlightPhase, actualFlightPhase) * 0.453592; // in Kgs/hr. preFlightPhase for DEBUG
        
        if (preFlightPhase == actualFlightPhase) {
            flow_out = flowNX;
        }
        else {
            flowNX = flowNX * ratios->delta2() * sqrt(ratios->theta2());
            delta = (prevFuelFlow - flowNX) * 0.995;
            flow_out = flowNX + delta;
            if (abs(delta) <= 20) {
                simVars->setPrePhase(actualFlightPhase);
            }
        }

        if (idx == 1) {
            simVars->setEngine1FF(flow_out);
            /*debug->text(" FF OUT = ");
            debug->text(std::to_string(flow_out));
            debug->text("\n");*/
        }
        else {
            simVars->setEngine2FF(flow_out);
        }

    }

	void updateCrank()
    {
		double temperature = simVars->getAmbientTemperature();
			
		if (temperature <= 288) {
            simVars->setEngineCrank(0);
        }
        else {
            simVars->setEngineCrank(1);
        }
    }

public:
    void init()
    {
        printf("EngineControl init");

        simVars = new SimVars();
        EngineImbalance(1);
    }

    void update()
    {
        flightPhase();
        updateEGT(1);
        updateEGT(2);
        updateFF(1);
        updateFF(2);
		updateCrank();

        //double tc = 700;
        //SimConnect_SetDataOnSimObject(hSimConnect, DATA_DEFINE_ID::DEFINITION_ENGINE, SIMCONNECT_OBJECT_ID_USER, 0, 0, sizeof(double), &tc);
    }

};

EngineControl EngCntrlInst;

#endif