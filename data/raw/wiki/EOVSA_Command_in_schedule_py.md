# EOVSA Schedule Command Summary
This document summarizes the schedule commands for controlling the **Expanded Owens Valley Solar Array (EOVSA)**.

## **ACC-handled Commands**

| Command | Description |
|---|---|
| `ABORT` | Aborts all commands sent to ACC but not yet executed |
| `CLEAROFF` | Sets all AzEl or RaDec offsets to zero |
| `DCMATTN` | Sets VPOL and HPOL attenuations for DCM modules in manual mode |
| `DCMAUTO-OFF` | Enables manual attenuation mode for DCM modules |
| `DCMAUTO-ON` | Enables automatic attenuation mode for DCM modules |
| `DCMOFFSET` | Sets 50 DCM attenuation offset increments (for test use) |
| `DCMOFFSET-CLEAR` | Clears the current 50 DCM offset attenuations |
| `DCMTABLE` | Uploads a base attenuation table to DCM modules |
| `DPPOFFSET-OFF` | Disables DPP-sent DCM offset recommendations |
| `DPPOFFSET-ON` | Enables DPP-sent DCM offset recommendations (default behavior) |
| `FEM-INIT` | Initializes FEM attenuations from acc.ini |
| `FEMAUTO-ON` | Enables AGC (Automatic Gain Control) for FEM |
| `FEMAUTO-OFF` | Disables AGC for FEM |
| `FEMATTN` | Manually selects FEM attenuation level from FEMATTN.txt |
| `HATTN` | Manually sets HPOL base attenuators (first/second) |
| `VATTN` | Manually sets VPOL base attenuators (first/second) |
| `FSEQ-FILE` | Uploads a frequency sequence file to the Hittite synthesizer |
| `FSEQ-INIT` | Initializes synthesizer from acc.ini |
| `FSEQ-ON` | Starts the tuning sequence |
| `FSEQ-OFF` | Stops the tuning sequence |
| `FSEQ-SCRIPT` | Sends scripted commands to the Hittite synthesizer |
| `LO1A-REBOOT` | Reboots LO1A synthesizer via PDU controller |
| `LO1B-REBOOT` | Not implemented |
| `LO1A-WRITE` | Sends command to LO1A synthesizer |
| `LO1B-WRITE` | Sends command to LO1B synthesizer |
| `SERVICE` | Moves antennas to service position and removes them from subarrays |
| `SUBARRAY1` | Assigns antennas to subarray1 |
| `SUBARRAY2` | Assigns antennas to subarray2 |
| `SYNC` | Restarts the real-time executable on all targeted cRIOs |
| `TRACKTABLE` | Uploads tracking table to antennas |
| `TRAJ-FILE` | Uploads trajectory file to antennas |
| `UNLISTEDCOMMAND` | Sends unknown command to be executed by antenna cRIO |
