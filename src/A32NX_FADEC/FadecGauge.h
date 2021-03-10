// A32NX_FADEC.h : Include file for standard system include files,
// or project specific include files.

#ifndef _FADECGAUGE_H_
#define _FADECGAUGE_H_

#ifndef __INTELLISENSE__
#	define MODULE_EXPORT __attribute__( ( visibility( "default" ) ) )
#	define MODULE_WASM_MODNAME(mod) __attribute__((import_module(mod)))
#else
#	define MODULE_EXPORT
#	define MODULE_WASM_MODNAME(mod)
#	define __attribute__(x)
#	define __restrict__
#endif

#include <MSFS\MSFS.h>
#include <MSFS\MSFS_Render.h>
#include <MSFS\Legacy\gauges.h>
#include <SimConnect.h>
#include <fstream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <map>
#include <math.h>

#include "SimVars.h"
#include "common.h"
#include "RegPolynomials.h"
#include "EngineControl.h"

using namespace std;

class FadecGauge
{
private:
    SimVars* simVars;
    bool isConnected = false;

    /// <summary>
    /// Initializes the connection to SimConnect.
    /// </summary>
    /// <returns>True if successful, false otherwise.</returns>
    bool InitializeSimConnect()
    {
        printf("Connecting to SimConnect...\r\n");
        if (SUCCEEDED(SimConnect_Open(&hSimConnect, "FadecGauge", nullptr, 0, 0, 0)))
        {
            printf("SimConnect connected.\r\n");

            //SimConnect_AddToDataDefinition(hSimConnect, DATA_DEFINE_ID::DEFINITION_ENGINE, "TURB ENG CORRECTED FF:1", "Pounds per hour");

            printf("SimConnect registrations complete.\r\n");
            return true;
        }

        printf("SimConnect failed.\r\n");

        return false;
    }

public:

    /// <summary>
    /// Initializes the FD.
    /// </summary>
    /// <returns>True if successful, false otherwise.</returns>
    bool InitializeFADEC()
    {
        if (!this->InitializeSimConnect()) {
            printf("Init SimConnect failed");
            return false;
        }

        EngCntrlInst.init();
        isConnected = true;
        /// SimConnect_CallDispatch(hSimConnect, HandleAxisEvent, this);

        return true;
    }

    /// <summary>
    /// A callback used to update the FD at each tick.
    /// </summary>
    /// <param name="deltaTime">The time since the previous update.</param>
    /// <returns>True if successful, false otherwise.</returns>
    bool OnUpdate(double deltaTime)
    {
        if (isConnected == true) {
            EngCntrlInst.update();
        }

        return true;
    }

    /// <summary>
    /// Kill.
    /// </summary>
    /// <returns>True if succesful, false otherwise.</returns>
    bool KillFADEC()
    {
        isConnected = false;
        this->simVars->setPrePhase(-1);
        this->simVars->setActualPhase(-1);
        unregister_all_named_vars();
        return SUCCEEDED(SimConnect_Close(hSimConnect));
    }
};
#endif