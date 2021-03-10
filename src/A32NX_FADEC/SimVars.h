#ifndef _SIMVARS_H_
#define _SIMVARS_H_

enum DATA_DEFINE_ID {
    DEFINITION_ENGINE,
};

/// <summary>
/// A collection of SimVar unit enums.
/// </summary>
class Units
{
public:
    /// <summary>
    /// The Percent SimVar unit.
    /// </summary>
    ENUM Percent = get_units_enum("Percent");

    /// <summary>
    /// The Pounds SimVar unit.
    /// </summary>
    ENUM Pounds = get_units_enum("Pounds");

    ENUM Feet = get_units_enum("Feet");

    /// <summary>
    /// The Foot pounds SimVar unit.
    /// </summary>
    ENUM FootPounds = get_units_enum("Foot pounds");

    ENUM FeetMin = get_units_enum("Feet per minute");

    ENUM Number = get_units_enum("Number");

    ENUM Mach = get_units_enum("Mach");

    ENUM SluggerSlugs = get_units_enum("Slug per cubic feet");

    ENUM Celsius = get_units_enum("Celsius");

    ENUM Bool = get_units_enum("Bool");
};

/// <summary>
/// A collection of SimVar enums.
/// </summary>
class SimVars
{
public:
    Units* m_Units;

    /// MSFS Simulation Variables.
    ENUM correctedN1 = get_aircraft_var_enum("TURB ENG CORRECTED N1");

    ENUM PlaneAltitude = get_aircraft_var_enum("PLANE ALTITUDE");

    ENUM PlaneAltitudeAGL = get_aircraft_var_enum("PLANE ALT ABOVE GROUND");

    ENUM AirSpeedMach = get_aircraft_var_enum("AIRSPEED MACH");

    ENUM AmbientTemp = get_aircraft_var_enum("AMBIENT TEMPERATURE");

    ENUM VerticalSpeed = get_aircraft_var_enum("VERTICAL SPEED");

    ENUM StdTemp = get_aircraft_var_enum("STANDARD ATM TEMPERATURE");

    ENUM SimOnGround = get_aircraft_var_enum("SIM ON GROUND");

    /// <summary>
    /// The local variable for the bew EGT model.
    /// </summary>
    ID Engine1EGT;
    ID Engine2EGT;
    ID Engine1FF;
    ID Engine2FF;
    ID EngineCrank;
    ID EngineImbalance;
    ID preFlightPhase;
    ID actualFlightPhase;

    SimVars()
    {
        this->initializeVars();
    }

    void initializeVars() {
        Engine1EGT = register_named_variable("A32NX_ENGINE_EGT:1");
        Engine2EGT = register_named_variable("A32NX_ENGINE_EGT:2");
        Engine1FF = register_named_variable("A32NX_ENGINE_FF:1");
        Engine2FF = register_named_variable("A32NX_ENGINE_FF:2");
		EngineCrank = register_named_variable("A32NX_CRANK_PHASE_SKIPPED");
        EngineImbalance = register_named_variable("A32NX_ENGINE_IMBALANCE");
        preFlightPhase = register_named_variable("A32NX_FLIGHT_STATE_PREVIOUS");
        actualFlightPhase = register_named_variable("A32NX_FLIGHT_STATE_ACTUAL");
        this->setEngine1EGT(500);
        this->setEngine2EGT(500);
        this->setEngine1FF(320);
        this->setEngine2FF(320);
        this->setEngineImbalance(0);
		this->setEngineCrank(0);
        this->setPrePhase(-1);
        this->setActualPhase(-1);
        m_Units = new Units();
    }  

    void setEngine1EGT(FLOAT64 value) {
        set_named_variable_value(Engine1EGT, value);
    }

    void setEngine2EGT(FLOAT64 value) {
        set_named_variable_value(Engine2EGT, value);
    }

    void setEngine1FF(FLOAT64 value) {
        set_named_variable_value(Engine1FF, value);
    }

    void setEngine2FF(FLOAT64 value) {
        set_named_variable_value(Engine2FF, value);
    }

    void setEngineImbalance(FLOAT64 value) {
        set_named_variable_value(EngineImbalance, value);
    }

	void setEngineCrank(FLOAT64 value) {
        set_named_variable_value(EngineCrank, value);
    }

    /// <summary>
    /// 0: Takeoff, 1: Climb, 2: Cruise, 3: Descent, 4: Landing
    /// </summary>
    void setPrePhase(FLOAT64 value) {
        set_named_variable_value(preFlightPhase, value);
    }

    void setActualPhase(FLOAT64 value) {
        set_named_variable_value(actualFlightPhase, value);
    }

    FLOAT64 getPrePhase() {
        return get_named_variable_value(preFlightPhase);
    }

    FLOAT64 getActualPhase() {
        return get_named_variable_value(actualFlightPhase);
    }

    FLOAT64 getEngine1FF() {
        return get_named_variable_value(Engine1FF);
    }

    FLOAT64 getEngine2FF() {
        return get_named_variable_value(Engine2FF);
    }

    FLOAT64 getEngineImbalance() {
        return get_named_variable_value(EngineImbalance);
    }

    FLOAT64 getCN1(int index) {
        return aircraft_varget(correctedN1, m_Units->Percent, index);
    }

    FLOAT64 getMach() {
        return aircraft_varget(AirSpeedMach, m_Units->Mach, 0);
    }

    FLOAT64 getPlaneAltitude() {
        return aircraft_varget(PlaneAltitude, m_Units->Feet, 0);
    }

    FLOAT64 getPlaneAltitudeAGL() {
        return aircraft_varget(PlaneAltitudeAGL, m_Units->Feet, 0);
    }

    FLOAT64 getVerticalSpeed() {
        return aircraft_varget(VerticalSpeed, m_Units->FeetMin, 0);
    }

    FLOAT64 getAmbientTemperature() {
        return aircraft_varget(AmbientTemp, m_Units->Celsius, 0);
    }

    FLOAT64 getStdTemperature() {
        return aircraft_varget(StdTemp, m_Units->Celsius, 0);
    }

    FLOAT64 getSimOnGround() {
        return aircraft_varget(SimOnGround, m_Units->Bool, 0);
    }
};

#endif