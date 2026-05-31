EOVSA Schedule Commands

NOTE: All Schedule commands accept as optional arguments a list of antennas to which the command should selectively sent. Accepted syntaxes are:

Command ant1 ant2 ant3

Command ant1-3

Command subarray1

Command subarray2

If no antenna list is indicated, the command is sent to all antennas currently in subarray1

# Commands handled directly by ACC	

### ABORT

	Aborts all commands sent to ACC but not yet executed

### CLEAROFF [antenna list]

	Sets all AzEl or RaDec offsets to zero

### DCMATTN HPOLattn VPOLattn [antenna list]

	Indicates the VPOL and HPOL attenuations for the DCM modules indicated in the list. The attenuations are applied on the next second start.

	Warning: The command is executed only if the DCM modules are in manual mode (see the DCMAUTO-ON and DCMAUTO-OFF command below)

### DCMAUTO-OFF [antenna list]

	Sets the DCM modules in the manual attenuation mode. This mode allows the attenuations requested by the DCMATTN to be applied.

### DCMAUTO-ON [antenna list]

	Sets the DCM modules in the automatic attenuation mode. This mode ignores the manual DCMATTN commands and applies the attenuation set through the DCMOFFSET mechanism.



### DCMOFFSET  inc1 inc2…..inc50

	Sets the 50 DCM attenuation offset increments to be added to the current list of DCM offset attenuations to be cycled during each second, starting with the next second boundary. The command expects up to 50 arguments. If fewer arguments are provided, the existing set is repeated in the same sequence until all 50 slots are filled. This command is only intended for testing. During normal operations, the DCM offsets states are requested by the DPP computer when needed. 

Warning: The command is executed only if the DCM modules are in auto mode (see the DCMAUTO-ON and DCMAUTO-OFF command below).

NOTE

The DCM offsets are changed on the edge of the next second after a TCP/IP message is received by ACC at the TCP.dpp.port  (default port: 6344-set in ACC.ini file ). The message is expected to be a fixed length binary string having the following format

50 32bit integers (I32)

### DCMOFFSET-CLEAR 

Clears the current list of 50 DCM offset attenuations that are applied when DCMAUTO-ON is set.

Warning: This command clears the offset attenuations for all DCM modules. 

### DCMTABLE  [antennalist] filename

Request the antenna list portion of a specific DCM base attenuation table to be uploaded on the respective DCM modules. The DCM table must have 30 columns and 50 rows, each pair of adjacent columns listing the HPOL-VPOL pairs for each of the 50 slots of a tuning sequence. The DCM table text file must be located in the ACC “c:\parm” directory and its default name is “DCM.txt”. 

The DCM/table_timeout key in the ACC.ini files have to be manually edited in order to modify the default timeout (ms) of the DCM modules when a table is broadcasted.

The actual DCM attenuations for a given tuning slot are calculated based on the following formula 

#### DCM_atten[pol,tuning_index]=DCM_base_atten[pol,tuning_index]+DCM_offset[broadcasted]



### DPPOFFSET-OFF

	Ignores DCM offset attenuation recommendations sent by DPP but still allows setting the offsets via the DCMOFFSET schedule command.

### DPPOFFSET-ON

	Applies DCM offset attenuation recommendations sent by DPP but still allows setting the offsets via the DCMOFFSET schedule command. 

NOTE: This is the default behavior of the system after each hardware ACC reboot or after a REBOOT or RESET command is sent via TCP/IP to the emergency 6543 acc.solar.ini port



### FEM-INIT

	Initialize all front-end module base attenuations with the values read from the ACC initialization file: “c:\ni-rt\startup\acc.ini”.

### FEMAUTO-ON [antennalist]

		Turn on AGC mode (equivalent to AGC 1)

### FEMAUTO-OFF [antennalist]

		Turn off AGC mode (equivalent to AGC 0)

### FEMATTN hlevel vlevel [antennalist]

	Manually selects the front-end attenuation levels for the antennas indicated in the list to be applied on the next second boundary. The attenuation level selects the corresponding entry in the “c:\parms\FEMATTN.txt” attenuation FEM table located on each the cRIOs.

	The attenuation  level set by this command is saved in the [FEM AGC] section of the “c:\ni-rt\startup\crio.ini” and it is automatically applied when the module is restarted.

	Warning:  The attenuation level setting may be overwritten by the AGC loop, if active.

The format of the table is as shown below (column heads are added here for clarity)



The actual FEM attenuations applied as the result of a FEMATTN command are given by

#### HPOL_ATTENUATION=HPOL_BASE+FEMATTN.txt(level)

#### VPOL_ATTENUATION=VPOL_BASE+FEMTTTN.txt(level)



Where Attenuation, Base, and FEMATTN.txt(level) are two elements vectors indicating the settings for the First and Second attenuators.

### HATTN first second [antennalist]

 Sets the FEM  HPOL_BASE first and second attenuators for the antennas in the list, and overwrites the corresponding  sections in the global “c:\ni-rt\startup\acc.ini” file, as well as in the local “c:\ni-rt\startup\crio.ini” files.

### VATTN first second [antennalist]

Sets the FEM  VPOL_BASE first and second attenuators for the antennas in the list, and overwrites the corresponding  sections in the global “c:\ni-rt\startup\acc.ini” file, as well as in the local “c:\ni-rt\startup\crio.ini” files.

### FSEQ-FILE filename

Tells ACC to upload to the Hittite synthesizer the frequency sequence located at  “c:\parm\filename”. 

### FSEQ-INIT

Initializes the Hittite synthesizer according to the settings defined in the [LO Configuration] section of the “c:\ni-rt\startup\acc.ini” file.

### FSEQ-ON

Starts the tuning sequence

### FSEQ-OFF

Stops the tuning sequence

### FSEQ-SCRIPT filename

Sends, line by line, to the Hittite synthesizer the command sequence listed in the “c:\parm\filename” script file.

### LO1A-REBOOT

Commands the PDU controller to recycle the power on the LO1A Hittite synthesizer

### LO1B-REBOOT

Not implemented yet

### LO1A-WRITE command

Sends the specified command to the LO1A Hittite synthesizer

### LO1B-WRITE command

Sends the specified command to the LO1B Hittite synthesizer

### SERVICE [anttenalist]

Takes the antennas in the list out of subarray1 or subarray2 and drives them to the service position.

Warning:  Once in service position, the serviced antenna should be put in local operation mode in order to avoid it being controlled by a subsequent schedule command.

### SUBARRAY1 antennalist

Puts all antennas in the list into subarray1.  All antennas than are not listed, but currently in subarray1, are taken out from subarray1.

### NOTE: As of Dec 03 2015, this command no longer switches by default the LO connector to an alternative source. To force the LO connector to switch switches, one must use the new explicit command  SUBARRAY1_SWITCH antennalist



### SUBARRAY2 antennalist

Puts all antennas in the list, which are not already in subarray1, into subarray2. In order to move a given antenna from subarray1 to subarray2, one should first redefine subarray1.

### NOTE: As of Dec 03 2015, this command no longer switches by default the LO connector to an alternative source. To force the LO connector to switch switches, one must use the new explicit command SUBARRAY2_SWITCH antennalist



### SYNC [anttenalist]

Restarts the real-time executable on all cRIOs corresponding to the antenna list.

NOTE: Unlike the general coinvention, not providing a list of antennas commands all cRIOs to restarts their execution.

### TRACKTABLE filename [antennalist]

Uploads to all antennas in the list the tracking table located at “c:\parm\filename”

### TRAJ-FILE filename [antennalist]

Uploads to all cRIOs corresponding to antennas in the list the trajectory file table located at “c:\parm\filename”

### UNLISTEDCOMMAND  [antennalist]

Any command not listed above is sent for local execution to all cRIOs corresponding to antennas in the list.

# Commands handled by cRIOs

NOTE:  These commands are selectively sent by ACC to all antennas in the optional argument antenalist, or, if not present, to all antennas in subarray1

### AGC active [low [high [samples]]]

Activates (1) or deactivates (0) the front end automatic gain control loop, which adjust the FEMATTN level when both of the HPOL and VPOL voltages, averaged over the given number of consecutive samples , cross the low and high voltage limits.  Missing parameter values are uploaded from the [FEM AGC] section of the local “c:\ni-rt\startup\crio.ini” file. All parameters provided when an AGC command is issued are saved in the same file for further use.

NOTE: At startup, the AGC loop is activated or not according with the latest active value written in the initialization file.

### AZELOFF azoff eloff

Sets the Azimuth and Elevation offsets indicated in the argument list

### RADECOFF raoff decoff

Sets the RA and DEC offsets indicated in the argument list

### FLUSH

Flush the existing tracktable from the associated antenna controller

### ND-ON and ND-OFF

Set on/off the local noise diode.

### POSITION azimuth elevation

Requests a given azel position

### RESTART

Reboots the cRIO

### DRIVE-RESET

Resets Antenna controller

### STOP

Stops the antenna

### STOW

Stows the antenna

### TRACK

Sets antenna in track mode

### TEC-LOG

Dumps all TEC register values to the local log file “c:\tec.txt” for debugging purposes

### TEC-INIT

Initializes the TEC controller with register values hard-coded in the crio code.  These were read from a working controller at some time in the past.

### TEC$BC

Reboot the TEC controller to recover from a bad or stuck state.

### TEC$SC

Clear the error status of the TEC controller.  Does nothing other than this, and is purely aesthetic.

### TRAJ-ON and TRAJ-OFF

Starts/Ends the execution of the trajectory script

NOTE: At startup, the WINDSCRAM loop is activated or not according with the latest active written in the initialization file.

### BSCRAM-ON

Activate the BRIGHTSCRAM Monitor

### BSCRAM-OFF

Deactivate the BRIGHTSCRAM Monitor

### BSCRAM-CLEAR

Takes the antenna out of the BRIGHTSCRAM Active State independently of the brightness sensor state.

If the BRIGHTSCRAM Monitor’s operation mode is set to STOW, clearing the BRIGHSCRAM ACTIVE state does not have any effect on the mechanical state of the antenna. If the BRIGHTSCRAM Monitor’s operation mode is set to OFFSET, clearing the BRIGHSCRAM ACTIVE state results in removing the AZEL offsets

Note: If the BRIGHTSCRAM Monitor is active, the antenna may get back in the Active State depending on the state of the brightness sensor.

### BSCRAM-SET

Force the antenna into the BRIGHTSCRAM Active State independently of the brightness sensor state.

### BSCRAM-WAIT seconds

Sets the BRIGHTSCRAM Monitor waiting time before clearing the BRIGHSCRAM ACTIVE state.

Note: This setting is saved in the crio.ini file and remains persistent until changed

### BSCRAM-OFFSET

Sets the BRIGHTSCRAM operation mode to stow the antenna when in active state.

Note: This setting is saved in the crio.ini file and remains persistent until changed

### BSCRAM-OFFSET

Sets the BRIGHTSCRAM operation mode to apply offsets

Note: This setting is saved in the crio.ini file and remains persistent until changed

### BSCRAM-AZELOFF azoff eloff

Sets the Azimuth and Elevation Offsets (degrees) for the BRIGHTSCRAM offset operation mode. 

Note: This setting is saved in the crio.ini file and remains persistent until changed. Default values re AZOFF=0 and ELOFF=10

Warning: No action is taken if less than 2 arguments are provided 

### WSCRAM-ON

Activate the WINDSCRAM Monitor

### WSCRAM-OFF

Deactivate the WINDSCRAM Monitor

### WSCRAM-LIMIT value

Sets the wind speed threshold. 

Note: This setting is saved in the crio.ini file and remains persistent across reboots until changed. 

### WSCRAM-WAIT seconds

Sets the WINDSCRAM Monitor waiting time between checking the wind speed.

Note: This setting is saved in the crio.ini file and remains persistent across reboots until changed. 

### UpdateElevationDiagnostics 1

Requests an update of the elevation trip register.

### UpdateAzimuthDiagnostics 1

Requests an update of the azimuth trip register.

### REGWRITE address value

Writes to a specific (new type) antenna register address the specified value.  This command is ignored by the old type antennas.

For example,

REGWRITE 23386 2 [antlist]

may be used to set the controller in velocity mode.  Note that the velocity rate registers must also be set to control the velocity of motion.  The appropriate registers are:

AzimuthVelocity, or 23585

ElevationVelocity, or 23605

Alternatively, one can write to a specific register address by directly sending a command formed by the name of the register (as defined in the M&C document Controller_registers.xlsx) followed the desired value to be written.

For example one may alternatively set the controller in velocity mode by issuing the command

RUNMODE 2 [antlist]

A possible need for velocity mode is to drive an antenna off a hard limit.  For safety, the only way to do that is to set the controller in velocity mode and provide a velocity in the direction to drive off the limit.  For example, if Ant 6 is on an azimuth low hard limit, one can drive it off by the following sequence:

RUNMODE 2 ANT6

AZIMUTHVELOCITY 5000 ANT6

Wait for hard limit to clear.

AZIMUTHVELOCITY 0 ANT6

TRACK ANT6

