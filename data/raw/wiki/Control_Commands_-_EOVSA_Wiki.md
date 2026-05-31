# Control Commands - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Control_Commands
**Scraped:** 2025-08-05 09:12:50

# Control Commands

From EOVSA Wiki

Jump to navigation Jump to search

EOVSA Control Language (Draft 2014-Apr-28)

Updates: 

  * GN: 2013-Jan-13: Introduced new commands related to the Hittite synthesizers: FSEQ-SCRIPT; LO1A-WRITE; LO1B-WRITE. Added subarray arguments to all FSEQ-* commands.
  * GN: 2013-Jan-16: Added a System Recovery Procedures section to this document

The Schedule program needs to send commands and information to the Array Control Computer (ACC) in order to specify antenna pointing coordinates, tuning, and other system parameters that will change from scan to scan and for different modes of operation (e.g. calibrations of various types, normal solar observing, etc.). This document specifies a command language to accomplish this task, with commands at two levels: (1) High-level commands (macro-commands) that accomplish standard operations in a human-readable form, and will mainly be specified in the top layer of the schedule, and (2) atomic commands from which such macro-commands are constructed, that provide flexibility in defining the order and duration of discrete tasks. Examples of macro-commands would include a SOLPNTCAL command, which initiates a pointing procedure that does multiple offsets of the antennas and takes data that will be analyzed for determining frequency-dependent pointing offsets. Examples of atomic commands would be DATA-ON, which starts data recording, or DOSEQ, which initiates a tuning sequence. The schedule will contain macro-commands associated with files of the same name, e.g. the SOLPNTCAL command would be associated with a file named solpntcal.ctl, which contains a list of atomic commands to execute the SOLPNTCAL. These atomic commands are what will be executed (either locally or by sending the command on to the ACC). It is expected that the ACC will return from receiving an atomic command immediately, and if a command takes some time, the ACC will store and execute the commands in the order received. The currently running atomic command will be indicated in the stateframe, and the Schedule program will examine the stateframe to determine when an individual atomic command is completed. The stateframe will also include the macro command currently being executed. This draft document specifies that both macro- and atomic commands be given as ASCII text in UPPER CASE in the stateframe. It can be typed in lower case in the schedule, but will be converted to upper case prior to display and transfer to the ACC. Although the macro-command will be sent to the ACC, typically this is for information only (for writing into the stateframe), and the ACC will act only on the atomic commands. 

## List of Atomic Commands

As noted above, atomic commands will in most cases NOT be issued individually in the schedule, but will be part of higher-level macro-commands. Commands starting with $ are to be initiated locally on the Schedule Computer. In the following, <antlist> refers to a list of antenna numbers (1-13, A, B, TEST) in the currently active subarray. Note that 14, 15, 16 are synonyms for A, B, and TEST. <antlist> is a space-separated list, with dashes indicating a range, e.g. ant1 ant3 ant5-9. There will be two instances of the schedule, one for subarray1 and one for subarray2. All commands issued from the subarray1 schedule by definition only refer to antennas in subarray1, and vice versa. ‘’’If <antlist> is omitted, the command refers to all antennas in the subarray.’’’ If an antenna number in <antlist> is not in the currently active subarray, it is ignored. It is expected that <antlist> will nearly always be omitted (i.e. commands will refer to all antennas in a subarray). If it is desired that a macro-command refer to only some antennas, it is best practice to omit the others from the current subarray first. A note about subarrays: The SUBARRAY2 command defers to the SUBARRAY1 command, i.e. antennas in <antlist> that are already in subarray1 will not be moved to subarray2 by use of the SUBARRAY2 command. Examples: (1) Typical commands for solar observing are SUBARRAY1 1-13, SUBARRAY2 A,B. The TEST input would then be on the “inactive” list and will not receive tracking commands, but its analog backend would be switched according to subarray2. (2) The typical command for calibrations is SUBARRAY1 1-15 (moves A,B to subarray1). (3) Entering SUBARRAY1 1-13 is sufficient to move A,B back to subarray2 without requiring an explicit SUBARRAY2 command. 

### SUBARRAY1 <antlist>

Specify the list of antenna numbers (1-13, A, B) in subarray 1 (the science subarray). Antennas not in subarray1 will be placed in subarray2. Antennas in <antlist> that are currently in subarray2 will be moved to subarray1. 

### SUBARRAY2 <antlist>

Specify the list of active antenna numbers (1-13, A, B) in subarray 2 (the maintenance subarray). Antennas not in either subarray1 or subarray2 will be designated inactive, and will not receive tracking commands (although their analog systems will be switched as for other antennas in subarray2). The SUBARRAY2 command defers to the SUBARRAY1 command, i.e. antennas in <antlist> that are already in subarray1 will not be moved to subarray2 by use of the SUBARRAY2 command. 

### IDLE <antlist>

Stop motion of antennas in <antlist>, but leave them powered. If <antlist> is omitted, all antennas in the current subarray will be idled. 

### STOW <antlist>

Drive antennas in <antlist> to STOW position but leave them powered. If <antlist> is omitted, all antennas in the current subarray will be stowed. 

### POWER-OFF <antlist>

Turn power off for antennas in <antlist> (but leave them at their current positions). To STOW and power off, issue STOW first. If <antlist> is omitted, all antennas in the current subarray will be powered off. 

### POWER-ON <antlist>

Turn power on for antennas in <antlist>. If <antlist> is omitted, all antennas in the current subarray will be powered on. 

### $MK_TABLES <file-stem> <source>

Runs locally on the schedule computer to create both a tracktable named <file-stem>.trk and a delay table <file-stem>.dla for the source designated by <source>, covering the range of time given by the start and stop times of the scan in the schedule. The tracktable is transmitted all at once to the ACC via the TRACKTABLE command, for uploading to the antennas, while the delay table is fed as delay “triplets” one line every 20 s (and coarse delays are calculated and sent to the ROACH boards as needed) by a spawned task. 

### TRACKTABLE <filename>

Specify the filename of the active tracktable. ACC actions are to IDLE the active antennas, clear the existing tracktable, and load the new tracktable (but do not initiate track). See below for definition of the contents of the tracktable. 

### TRACK-AZEL <az> <el> <antlist>

Put all antennas in <antlist> into AZEL mode and point them at a fixed point in the sky specified by <az> and <el> coordinates (degrees). Any existing tracktable is no longer in effect. If <antlist> is omitted, the command applies to all antennas in the current subarray. 

### TRACK-RADEC <ra> <dec> <antlist>

Put all antennas in <antlist> into RADEC mode and track the point specified by <ra> and <dec> coordinates (degrees). Any existing tracktable is no longer in effect. If <antlist> is omitted, the command applies to all antennas in the current subarray. 

### TRACK <antlist>

Initiate tracking of the coordinates loaded into the TRACKTABLE, for all antennas in <antlist>. If <antlist> is omitted, the command applies to all antennas in the current subarray. 

### OFFSET <xoff> <yoff> <antlist>

Point all antennas in <antlist> at a fixed offset specified by <xoff> and <yoff> (degrees) from the current tracking position. The directions of x and y depend on the antenna: (1) if the antenna is an alt-az mount, the offsets will be cross-elevation (xel) and elevation (el), respectively; (2) if the antenna is an equatorial mount, the offsets will be hour-angle/cos(dec) and declination (dec), respectively. If <antlist> is omitted, the command applies to all antennas in the current subarray. 

### TRAJ-FILE <filename>

Specify the filename of a file of a sequence of pointing offsets. ACC action is to load the new trajectory file, but do not initiate trajectory pointing. See below for definition of contents of trajectory file. The command TRAJ-FILE NONE turns off any offsets. 

### TRAJ-ON

Trigger the start of the currently defined trajectory file for the current subarray. This throws an error if TRAJ-FILE is not loaded, and sets TRAJ-OFF state. 

### TRAJ-OFF

Stop the currently running trajectory. ACC action is to issue OFFSET 0 0 to return the array to non-offset tracking. 

### FSEQ-FILE <filename> [<subarray1> <subarray2>]

Specify the filename of the active tuning sequence for the subarray1 or/or subarray2. If no subarray argument is present, subarray1 is assumed. ACC action is to prepare the new sequence definition, but do not initiate sequencing. See below for definition of contents of the sequence file. 

### FSEQ-ON [<subarray1> <subarray2>]

Trigger the start of the currently defined tuning sequence for the current subarray. This throws an error if FSEQ-FILE is not loaded, and sets FSEQ-OFF state. 

### FSEQ-OFF [<subarray1> <subarray2>]

Stop the currently active tuning sequence for the current subarray. [Is this a good idea? What default frequency should it set when stopped? What will be the response of the rest of the system?] 

### LO1A-WRITE <command>

### LO1B-WRITE <command>

Sends the command string to the LO1A or L01B synthesizers. If the command is a Querry, the reply or an error message is included in the schedule.task field. These messages are not intended for normal situations, but may be used for debugging or instant feedback. 
    
    Examples:
    LO1A-Write *idn?Hittite,HMC-t2240,000223,2.5 5.1 
    LO1B-Write *idn?Err->54
    L01A is online, LO1B is offline

### FSEQ-SCRIPT <filename> [<subarray1> <subarray2>]

Sent the command lines in the script <filename> to the LO1A(<subbarray1>) and/or LO1B(<subarray2>) synthesizers.. If no subarray argument is present, the script is sent to LO1A. 

### ND-OFF <antlist>

Turn the noise diode off for all antennas in <antlist>. If <antlist> is omitted, the command applies to all antennas in the current subarray. This throws an error if NDSEQ-ON is currently in effect. 

### ND-ON <antlist>

Turn the noise diode on for all antennas in <antlist>. If <antlist> is omitted, the command applies to all antennas in the current subarray. This throws an error if NDSEQ-ON is currently in effect. 

### NDSEQ-FILE <filename>

Specify the filename of the active noise diode sequence for the current subarray. ACC action is to load the new sequence definition (but do not initiate sequencing). See below for definition of contents of the noisecal file. ===NDSEQ-ON <antlist> Trigger the start of the currently defined noise diode sequence for all antennas in <antlist>. If <antlist> is omitted, the command applies to all antennas in the current subarray. This throws an error if NDSEQ-FILE is not loaded, and sets NDSEQ-OFF state. 

### NDSEQ-OFF <antlist>

Stop sequencing, and turn off, the noise diode for all antennas in <antlist>. If <antlist> is omitted, the command applies to all antennas in the current subarray. 

### FEDB <db> <antlist>

Set the front end attenuator for the antennas in <antlist> to the setting indicated by <db>. If <db> is prefixed with an asterisk (‘*’), it means turn the SKY attenuator ON, otherwise OFF. If <antlist> is omitted, the command applies to all antennas in the current subarray. 

### FEDB-FILE <filename>

Specify the filename of the active attenuation sequence for the current subarray. ACC action is to load the new sequence definition, but do not initiate sequencing. See below for definition of contents of the attenuation sequence file. 

### FEDBSEQ-ON <antlist>

Trigger the start of the currently defined attenuation sequence for all antennas in <antlist>. If <antlist> is omitted, the command applies to all antennas in the current subarray. This throws an error if FEDB-FILE is not loaded, and sets FEDBSEQ-OFF state. 

### FEDBSEQ-OFF <antlist>

Stop sequencing the front-end attenuation for all antennas in <antlist>. If <antlist> is omitted, the command applies to all antennas in the current subarray. 

### FEDBSEQ-AUTO <antlist>

Trigger the start of the attenuation being set dynamically by the DPP. 

### DATA-ON

Trigger the start of data recording. This will normally be automatic at the start of a scan via the WAIT-TRACK command (as soon as the desired minimum number of antennas are tracking), but it may be necessary to have a way to force a start of data recording for certain test purposes. 

### DATA-OFF

Stop data recording. This will normally be automatic at the end of a scan (which can be triggered by NEWSCAN command), but it may be necessary to have a way to force the end of data recording for certain test purposes. 

### WAIT <nsec>

Wait for <nsec> seconds before executing the next following command. Normally the ACC will act on commands as fast as possible, but this allows for delays, if needed. 

### WAIT-TRACK <n>

Main command to initiate the start of a scan. As soon as <n> antennas are tracking, data recording will commence. If <n> is omitted, all antennas in the current subarray must be tracking (could be dangerous). If <n> exceeds the number of antennas in the subarray, it will be suitably decreased to match the number in the subarray. 

### NEWSCAN

Triggers the end of data recording of the current scan, if active, and prepares the system for setting up a new scan. 

### $ROACH-DLA

Triggers a standard manipulation of delay offsets (run locally on the Schedule computer, which sets the ROACH delays) to allow calibration of the ROACH initialization delay ambiguity, which ranges from –3 τ s {\displaystyle \tau _{s}} ![{\\displaystyle \\tau _{s}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7c275a0c624748353b74062f56672cf02b250cab) to 3 τ s {\displaystyle \tau _{s}} ![{\\displaystyle \\tau _{s}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7c275a0c624748353b74062f56672cf02b250cab) ( τ s {\displaystyle \tau _{s}} ![{\\displaystyle \\tau _{s}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7c275a0c624748353b74062f56672cf02b250cab) is the sample clock period, 0.833 ns) relative to the reference antenna. 

### $DLASCAN

Triggers a standard sweep of delay offsets (runs locally on the Schedule computer, which sets the ROACH delays) to allow determination of delay centers relative to the reference antenna. 

## List of File Formats

### TRACKTABLE file format:

The track table is just a list of either RA-Dec or Az-El coordinates, in units of 1/10000th of a degree, followed by the start date and time to be at the given coordinates, with date given in Modified Julian Date (MJD) and time in milliseconds of the day (UT1). See example below. There will be various ways to auto-generate this file for the Sun or calibrators. 
    
    3246805 -109310 55160 3600000 
    3247212 -109173 55160 3900000 
    3247617 -109037 55160 4200000 
    3248018 -108901 55160 4500000 
    3248415 -108764 55160 4800000 
    3248810 -108628 55160 5100000 
    3249202 -108491 55160 5400000 
    3249591 -108355 55160 5700000 
    3249976 -108218 55160 6000000 
    3250359 -108081 55160 6300000

### TRAJ file format:

The trajectory file format is patterned after the TRACKTABLE, but without the absolute time, i.e., it is a list of either HA-Dec or Xel-El offset coordinates, in units of 1/10000th of a degree, followed by the duration in s. See example below, which does a cross-pattern of pointing offsets from -5 to 5 degrees in each axis. Because it does not specify absolute times, this same table can be used for a calibration at any time. 
    
    -50000 0 20
    -20000 0 10
    -10000 0 10
    -5000 0 10
    -2000 0 10
    -1000 0 10
    0 0 10
    1000 0 10
    2000 0 10
    5000 0 10
    10000 0 10
    20000 0 10
    50000 0 10
    0 -50000 20
    0 -20000 10
    0 -10000 10
    0 -5000 10
    0 -2000 10
    0 -1000 10
    0 0 10
    0 1000 10
    0 2000 10
    0 5000 10
    0 10000 10
    0 20000 10
    0 50000 10

### FSEQ file format:

The tuning sequence file format is that required by the Hittite synthesizer (LO-1), and consists of two lines of text. One is a comma-separated list of dwell times, and the second is a comma-separated list of tuning indexes. For now, it is standardized that a tuning sequence should repeat after an integral number of seconds ONLY. The standard bands are defined as integers in steps of 500 MHz, with index 1 corresponding to 1 GHz and index 34 corresponding to 18 GHz. The standard sequence for solar observations is: 
    
    DWELL 20ms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    SEQUENCE  1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 1, 2, 3, 4, 17, 18, 19, 20, 21, 22, 1, 2, 3, 4, 23, 24, 25, 26, 27, 28, 1, 2, 3, 4, 29, 30, 31, 32, 33, 34

which corresponds to 50 tunings, each 20 ms duration. Note the repeat of bands 1, 2, 3 and 4 five times. Note that the dwell time is specified with 33 commas (not 49), since it defines the time for all 34 possible indexes. If we wanted to take data on 10 bands on a calibrator, taking 1 s per band, we could, for example, do 
    
    DWELL 1000ms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    SEQUENCE  5, 7, 9, 11 , 13, 15, 17, 19, 21, 23

Note again the fact that the dwell time is specified with 33 commas, even though the sequence has only 10 frequencies. 

### NDSEQ file format:

The noisecal sequence looks exactly like the tuning sequence, and consists of two lines of text. One is a comma-separated list of dwell times (in seconds), and the second is a comma-separated list of noise diode states--a simple sequence of 0s and 1s specifying if the noise diode should be ON or OFF for each noisecal cycle. For now, it is standardized that the noise diode can be turned on or off at the 1-second tick ONLY. The simplest case of turning the noise diode on for 10 seconds and off for 10 seconds (perhaps suitable for calibrator observations) would be designated by the file contents: 
    
    DWELL 10,,
    SEQUENCE  0, 1

A more complicated way to accomplish the same thing might be 
    
    DWELL 1,,,,,,,,,
    SEQUENCE  0, 0, 0, 1, 1, 1, 1, 1, 0, 0

### FEDB file format:

The front end attenuation sequence looks exactly like the tuning sequence, and consists of two lines of text. One is a comma-separated list of dwell times (in seconds), and the second is a comma-separated list of attenuation states--a simple sequence of integers specifying if the attenuation bit setting for each attenuation cycle. It is standardized that the attenuation can be set at the 1-second tick ONLY. The case of setting attenuation bits on one at a time for 10 seconds each (perhaps suitable for gain calibration) would be designated by the file contents: 
    
    DWELL 10,,,,,,,,,,,
    SEQUENCE  0, 1, 2, 4, 8, 16, *0, *1, *2, *4, *8, *16

The asterisks (‘*’) mean to turn the SKY attenuator ON for these measurements. Although the sky attenuator has 32 settings, it will be programmed only for ON/OFF operation. 

## List of Macro-Commands

This list of macro-commands is based on the types of calibration listed in EOVSA_Calibration.doc, and will certainly be subject to change. Each of these commands should initiate a new scan. Each macro-command will be defined according to a list of atomic commands that resides on the Schedule Computer. 

### SOLPNTCAL <fseqfile> <trajfile> <ndseqfile>

Initiates a solar pointing calibration. Points each active 2-m antenna simultaneously to a set of offsets from the Sun, as defined in the trajectory file <trajfile>, and executes a tuning sequence based on the tuning sequence file <fseqfile>, and noise diode sequence based on the NOISECAL file <ndseqfile>. This is used for three purposes: (1) to obtain the detailed pointing offsets of each antenna as a function of frequency, with fine frequency resolution; (2) to measure the primary beam at each frequency; (3) to measure the off/on Sun total power spectrum. 

### SATPNTCAL

Place holder for either a GPS or GEO(stationary) satellite pointing calibration, deferred for now. 

### XPNTCAL <refant> <tracktable> <trajfile>

Initiates a cross-correlation, or interferometric, pointing calibration, which points the array (including 27-m antennas) to designated calibrator targets specified in the TRACKTABLE file <tracktable>, then offsets the dishes as defined in the TRAJECTORY file <trajfile>, relative to <refant>, which is held fixed. This is used primarily to determine all-sky pointing coefficients. 

### DLACAL <source> <offset> <range>

Initiates pointing to a bright cosmic source designated by <source> (typically 3C84) and issues the DLASCAN command, which sweeps the 27-m delays relative to the tabulated delays + <offset> (in units of τs=0.833 ns), over a window given by ±<range> (in units of τs=0.833 ns), for determining the array delay center table. 

### ROACHDLACAL

Initiates pointing to the XM Blues geostationary satellite at 115 W longitude for determining ROACH initialization delay (±0-3τs ambiguity on startup relative to previous calibration). Issues the $ROACH-DLA command, which steps the delays for the 27-m antennas in a prescribed manner. 

### 2MDLACAL <refant> <offset> <range>

Initiates pointing to the XM Blues geostationary satellite at 115 W longitude for determining 2-m antenna delay centers when the 27-m antennas are not available. The delay center of <refant> is augmented by <offset> (in units of τs=0.833 ns) and swept over <range> (in units of τs=0.833 ns). 

### BPASSCAL <source> <bands>

Points the array to a bright cosmic point source designated by <source> and tunes to each band listed in <bands> (or all bands if omitted) for a sensitive measure of amplitude and phase across each band. Typically, a 10:1 signal-to-noise measurement on 3C84 will take about 23 s on large-small baselines. A 50:1 signal-to-noise measurement on all 34 bands takes about 6 hours. 

### REFCAL <source> <fseqfile>

Points the array to a bright cosmic point source designated by <source> and executes the tuning sequence in <fseqfile>. A full antenna solution at 50:1 signal-to-noise measurement on small-small baselines takes about 1 hour (integrating over 500 MHz bandwidth). 

### FLUXCAL <source> <fseqfile>

Points the array to one of the flux standard point source designated by <source> (either 3C48 or 3C286) and executes the sequence in <fseqfile>. Only the large-small baselines are needed, so a 50:1 measurement requires about 10 minutes. 

### PHASECAL <source> <fseqfile>

Points the array to the cosmic point source designated by <source> and executes the tuning sequence in <fseqfile>. Only the large-small baselines are needed, and it is possible to obtain a 20:1 measurement on a >4 Jy source in less than 1 minute. 

### GAINCAL

Generally performed while the antennas are at their STOW position, the GAINCAL procedure tunes in a standard gaincal sequence (all bands) and alternately turns the noise diode on and off while cycling through all attenuator settings. 

### SUN

Command to point antennas to Sun center and take normal solar observations. 

## Example Definitions of Macro-Commands

On encountering one of the macro-commands listed above, the schedule will look for a file of the same name, with the .ctl extension. Thus, the SUN command would correspond to a file sun.ctl. The content of these .ctl files is merely a list of atomic commands to be executed in order. The duration of each atomic command is variable, but none should ideally take more than a few seconds except for WAIT or WAIT-TRACK. The exact definition of these files will change as we develop experience, but this section should serve as an illustrative example of how it might work. Note that arguments are passed to the .ctl file through the use of #1, #2, etc. 

Example Definitions of Macro-Command   
---  
Macro Command  | Corresponding .ctl file   
SUN  |  $SCAN-STOP  
FSEQ-OFF  
SUBARRAY1 ant1 ant7  
$MK_TABLES sun_tab SUN  
TRACKTABLE sun_tab.radec  
TRACK  
FSEQ-FILE solar.fsq  
FSEQ-ON  
NDSEQ-OFF  
FEDBSEQ-AUTO  
$WAIT-TRACK  
$SCAN-START  
  
PHASECAL 0157+747 pcal.fsq  |  $SCAN-STOP  
FSEQ-OFF  
SUBARRAY1 ant1 ant7  
$MK_TABLES pcal_tab #1  
FSEQ-FILE #2  
FSEQ-ON  
TRACKTABLE pcal_tab.radec  
NDSEQ-OFF  
FEDBSEQ-OFF  
FEDB 0  
TRACK  
$WAIT-TRACK  
$SCAN-START  
  
SOLPNTCAL solpnt.fsq solpnt.trj solpnt.nsq  |  $SCAN-STOP  
SUBARRAY1 ant1 ant7 ant14  
$MK_TABLES sun_tab SUN  
TRACKTABLE sun_tab.radec  
TRACK  
FSEQ-FILE #1  
FSEQ-ON  
NDSEQ-FILE #3  
FEDBSEQ-AUTO  
$WAIT-TRACK  
TRAJ-FILE #2  
TRAJ-ON  
$SCAN-START  
  
ROACHDLACAL  |  $SCAN-STOP  
SUBARRAY1 1-15  
$MK_TABLES xm_tab XMSAT  
TRACKTABLE xm_tab.trk  
TRACK  
FSEQ-FILE xm.fsq  
FSEQ-ON  
NDSEQ-OFF  
FEDBSEQ-AUTO  
$WAIT-TRACK  
$ROACH-DLA  
  
## EOVSA Recovery Commands

This section describes a set of emergency commands that may be sent to the ACC via TCP/IP to attempt recovery from some run-time errors. 
    
    Commands sent via TCP/IP to acc.solar.pvt at port TCP.schedule.port 

### SYNC [<subarray1>] [subarray2>] [<antlist>]

This command stops and restarts all or part of the cRIO stateframe servers in order to synchronize with the ACC stateframe server. 

### RESTART [<subarray1>] [subarray2>] [<antlist>]

This command reboots all or part of cRIO modules to recover from a fatal error. 
    
    Commands sent via TCP/IP to acc.solar.pvt at port TCP.master.port 

NOTE: These commands must be sent via TCP/IP at a predefined port (_TCP.master.port_ ) that is different from the Schedule server port (_TCP.schedule.port_ ). Both ports may be retrieved via anonymous ftp from the c:\ni-rt\startup\acc.ini file. 

### RESET

Reinitialize the startup procedure of the ACC without rebooting the target. At startup, or after issuing this command, the ACC restarts all service loops and executes the initial sets of command located in the **c:\n-rt\startup\startup.ini** file. The **startup.ini** file may contain a sequence of Schedule commands need to bring the system a predefined state. An example of such file is provided below: 
    
    LO1A-WRITE *RST
    FSEQ-INIT subarray1
    FSEQ-FILE subarray1 solar.fsq
    SYNC

NOTE: Although the setup.ini file contains a SYNC command, the fault system may need to issue SYNC command after startup if the initialization fails. 

### REBOOT

This command reboots the ACC and follows the same steps that would follow a RESET command.. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Control_Commands&oldid=363](http://ovsa.njit.edu//wiki/index.php?title=Control_Commands&oldid=363)"
