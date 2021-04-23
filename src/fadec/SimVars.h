#pragma once

// SimConnect data types for sending the sim updates.
enum DataTypesID {
  FuelControls,
};

// Fuel controls.
struct FuelControlData {
  // Left Inner Wing Fuel Quantity in US Gallons.
  double FuelLeft;

  // Right Inner Wing Fuel Quantity in US Gallons.
  double FuelRight;

  // Center Fuel Quantity in US Gallons.
  double FuelCenter;
};

// A collection of SimVar unit enums.
class Units {
 public:
  ENUM Percent = get_units_enum("Percent");
  ENUM Pounds = get_units_enum("Pounds");
  ENUM Pph = get_units_enum("Pounds per hour");
  ENUM Gallons = get_units_enum("Gallons");
  ENUM Feet = get_units_enum("Feet");
  ENUM FootPounds = get_units_enum("Foot pounds");
  ENUM FeetMin = get_units_enum("Feet per minute");
  ENUM Number = get_units_enum("Number");
  ENUM Mach = get_units_enum("Mach");
  ENUM SluggerSlugs = get_units_enum("Slug per cubic feet");
  ENUM Celsius = get_units_enum("Celsius");
  ENUM Bool = get_units_enum("Bool");
  ENUM Hours = get_units_enum("Hours");
  ENUM Seconds = get_units_enum("Seconds");
};

// A collection of SimVar enums.
class SimVars {
 public:
  Units* m_Units;

  // Collection of MSFS Simulation Variables
  ENUM correctedN1 = get_aircraft_var_enum("TURB ENG CORRECTED N1");
  ENUM correctedFF = get_aircraft_var_enum("TURB ENG CORRECTED FF");
  ENUM PlaneAltitude = get_aircraft_var_enum("PLANE ALTITUDE");
  ENUM PlaneAltitudeAGL = get_aircraft_var_enum("PLANE ALT ABOVE GROUND");
  ENUM AirSpeedMach = get_aircraft_var_enum("AIRSPEED MACH");
  ENUM AmbientTemp = get_aircraft_var_enum("AMBIENT TEMPERATURE");
  ENUM VerticalSpeed = get_aircraft_var_enum("VERTICAL SPEED");
  ENUM StdTemp = get_aircraft_var_enum("STANDARD ATM TEMPERATURE");
  ENUM SimOnGround = get_aircraft_var_enum("SIM ON GROUND");
  ENUM EngineTime = get_aircraft_var_enum("GENERAL ENG ELAPSED TIME");

  ENUM TankLeftAuxCapacity = get_aircraft_var_enum("FUEL TANK LEFT AUX CAPACITY");
  ENUM TankRightAuxCapacity = get_aircraft_var_enum("FUEL TANK RIGHT AUX CAPACITY");
  ENUM TankLeftCapacity = get_aircraft_var_enum("FUEL TANK LEFT MAIN CAPACITY");
  ENUM TankRightCapacity = get_aircraft_var_enum("FUEL TANK RIGHT MAIN CAPACITY");
  ENUM TankCenterCapacity = get_aircraft_var_enum("FUEL TANK CENTER CAPACITY");

  ENUM TankLeftAuxQuantity = get_aircraft_var_enum("FUEL TANK LEFT AUX QUANTITY");
  ENUM TankRightAuxQuantity = get_aircraft_var_enum("FUEL TANK RIGHT AUX QUANTITY");
  ENUM TankLeftQuantity = get_aircraft_var_enum("FUEL TANK LEFT MAIN QUANTITY");
  ENUM TankRightQuantity = get_aircraft_var_enum("FUEL TANK RIGHT MAIN QUANTITY");
  ENUM TankCenterQuantity = get_aircraft_var_enum("FUEL TANK CENTER QUANTITY");
  ENUM FuelTotalQuantity = get_aircraft_var_enum("FUEL TOTAL QUANTITY");
  ENUM FuelWeightGallon = get_aircraft_var_enum("FUEL WEIGHT PER GALLON");

  // Collection of local variables for the FADEC model.
  ID Engine1EGT;
  ID Engine2EGT;
  ID Engine1FF;
  ID Engine2FF;
  ID Engine1PreFF;
  ID Engine2PreFF;
  ID EngineCycleTime;
  ID EngineImbalance;
  ID FuelUsedLeft;
  ID FuelUsedRight;
  ID FuelLeftPre;
  ID FuelRightPre;
  ID FuelAuxLeftPre;
  ID FuelAuxRightPre;
  ID FuelCenterPre;
  ID FuelOverflowLeft;
  ID FuelOverflowRight;

  SimVars() { this->initializeVars(); }

  void initializeVars() {
    // Initializing LVars
    Engine1EGT = register_named_variable("A32NX_ENGINE_EGT:1");
    Engine2EGT = register_named_variable("A32NX_ENGINE_EGT:2");
    Engine1FF = register_named_variable("A32NX_ENGINE_FF:1");
    Engine2FF = register_named_variable("A32NX_ENGINE_FF:2");
    Engine1PreFF = register_named_variable("A32NX_ENGINE_PRE_FF:1");
    Engine2PreFF = register_named_variable("A32NX_ENGINE_PRE_FF:2");
    EngineImbalance = register_named_variable("A32NX_ENGINE_IMBALANCE");
    FuelUsedLeft = register_named_variable("A32NX_FUEL_USED:1");
    FuelUsedRight = register_named_variable("A32NX_FUEL_USED:2");
    FuelLeftPre = register_named_variable("A32NX_FUEL_LEFT_PRE");
    FuelRightPre = register_named_variable("A32NX_FUEL_RIGHT_PRE");
    FuelAuxLeftPre = register_named_variable("A32NX_FUEL_AUX_LEFT_PRE");
    FuelAuxRightPre = register_named_variable("A32NX_FUEL_AUX_RIGHT_PRE");
    FuelCenterPre = register_named_variable("A32NX_FUEL_CENTER_PRE");
    EngineCycleTime = register_named_variable("A32NX_ENGINE_CYCLE_TIME");

    this->setEngine1EGT(0);
    this->setEngine2EGT(0);
    this->setEngine1FF(0);
    this->setEngine2FF(0);
    this->setEngine1PreFF(0);
    this->setEngine2PreFF(0);
    this->setEngineImbalance(0);
    this->setFuelUsedLeft(0);
    this->setFuelUsedRight(0);
    this->setFuelLeftPre(0);
    this->setFuelRightPre(0);
    this->setFuelAuxLeftPre(0);
    this->setFuelAuxRightPre(0);
    this->setFuelCenterPre(0);
    this->setEngineCycleTime(0);

    m_Units = new Units();
  }

  // Collection of LVar 'set' Functions
  void setEngine1EGT(FLOAT64 value) { set_named_variable_value(Engine1EGT, value); }
  void setEngine2EGT(FLOAT64 value) { set_named_variable_value(Engine2EGT, value); }
  void setEngine1FF(FLOAT64 value) { set_named_variable_value(Engine1FF, value); }
  void setEngine2FF(FLOAT64 value) { set_named_variable_value(Engine2FF, value); }
  void setEngine1PreFF(FLOAT64 value) { set_named_variable_value(Engine1PreFF, value); }
  void setEngine2PreFF(FLOAT64 value) { set_named_variable_value(Engine2PreFF, value); }
  void setEngineImbalance(FLOAT64 value) { set_named_variable_value(EngineImbalance, value); }
  void setFuelUsedLeft(FLOAT64 value) { set_named_variable_value(FuelUsedLeft, value); }
  void setFuelUsedRight(FLOAT64 value) { set_named_variable_value(FuelUsedRight, value); }
  void setFuelLeftPre(FLOAT64 value) { set_named_variable_value(FuelLeftPre, value); }
  void setFuelRightPre(FLOAT64 value) { set_named_variable_value(FuelRightPre, value); }
  void setFuelAuxLeftPre(FLOAT64 value) { set_named_variable_value(FuelAuxLeftPre, value); }
  void setFuelAuxRightPre(FLOAT64 value) { set_named_variable_value(FuelAuxRightPre, value); }
  void setFuelCenterPre(FLOAT64 value) { set_named_variable_value(FuelCenterPre, value); }
  void setEngineCycleTime(FLOAT64 value) { set_named_variable_value(EngineCycleTime, value); }

  // Collection of SimVar/LVar 'get' Functions
  FLOAT64 getEngine1FF() { return get_named_variable_value(Engine1FF); }
  FLOAT64 getEngine2FF() { return get_named_variable_value(Engine2FF); }
  FLOAT64 getEngine1PreFF() { return get_named_variable_value(Engine1PreFF); }
  FLOAT64 getEngine2PreFF() { return get_named_variable_value(Engine2PreFF); }
  FLOAT64 getEngineImbalance() { return get_named_variable_value(EngineImbalance); }
  FLOAT64 getEngineCycleTime() { return get_named_variable_value(EngineCycleTime); }
  FLOAT64 getFuelUsedLeft() { return get_named_variable_value(FuelUsedLeft); }
  FLOAT64 getFuelUsedRight() { return get_named_variable_value(FuelUsedRight); }
  FLOAT64 getFuelLeftPre() { return get_named_variable_value(FuelLeftPre); }
  FLOAT64 getFuelRightPre() { return get_named_variable_value(FuelRightPre); }
  FLOAT64 getFuelAuxLeftPre() { return get_named_variable_value(FuelAuxLeftPre); }
  FLOAT64 getFuelAuxRightPre() { return get_named_variable_value(FuelAuxRightPre); }
  FLOAT64 getFuelCenterPre() { return get_named_variable_value(FuelCenterPre); }
  FLOAT64 getCN1(int index) { return aircraft_varget(correctedN1, m_Units->Percent, index); }
  FLOAT64 getFF(int index) { return aircraft_varget(correctedFF, m_Units->Pph, index); }
  FLOAT64 getMach() { return aircraft_varget(AirSpeedMach, m_Units->Mach, 0); }
  FLOAT64 getPlaneAltitude() { return aircraft_varget(PlaneAltitude, m_Units->Feet, 0); }
  FLOAT64 getPlaneAltitudeAGL() { return aircraft_varget(PlaneAltitudeAGL, m_Units->Feet, 0); }
  FLOAT64 getVerticalSpeed() { return aircraft_varget(VerticalSpeed, m_Units->FeetMin, 0); }
  FLOAT64 getAmbientTemperature() { return aircraft_varget(AmbientTemp, m_Units->Celsius, 0); }
  FLOAT64 getStdTemperature() { return aircraft_varget(StdTemp, m_Units->Celsius, 0); }
  FLOAT64 getSimOnGround() { return aircraft_varget(SimOnGround, m_Units->Bool, 0); }
  FLOAT64 getTankLeftAuxCapacity() { return aircraft_varget(TankLeftAuxCapacity, m_Units->Gallons, 0); }
  FLOAT64 getTankRightAuxCapacity() { return aircraft_varget(TankRightAuxCapacity, m_Units->Gallons, 0); }
  FLOAT64 getTankLeftCapacity() { return aircraft_varget(TankLeftCapacity, m_Units->Gallons, 0); }
  FLOAT64 getTankRightCapacity() { return aircraft_varget(TankRightCapacity, m_Units->Gallons, 0); }
  FLOAT64 getTankCenterCapacity() { return aircraft_varget(TankCenterCapacity, m_Units->Gallons, 0); }
  FLOAT64 getTankLeftAuxQuantity() { return aircraft_varget(TankLeftAuxQuantity, m_Units->Gallons, 0); }
  FLOAT64 getTankRightAuxQuantity() { return aircraft_varget(TankRightAuxQuantity, m_Units->Gallons, 0); }
  FLOAT64 getTankLeftQuantity() { return aircraft_varget(TankLeftQuantity, m_Units->Gallons, 0); }
  FLOAT64 getTankRightQuantity() { return aircraft_varget(TankRightQuantity, m_Units->Gallons, 0); }
  FLOAT64 getTankCenterQuantity() { return aircraft_varget(TankCenterQuantity, m_Units->Gallons, 0); }
  FLOAT64 getFuelTotalQuantity() { return aircraft_varget(FuelTotalQuantity, m_Units->Gallons, 0); }
  FLOAT64 getFuelWeightGallon() { return aircraft_varget(FuelWeightGallon, m_Units->Pounds, 0); }
  FLOAT64 getEngineTime(int index) { return aircraft_varget(EngineTime, m_Units->Seconds, index); }
};