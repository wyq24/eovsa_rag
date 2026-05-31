# Trouble Shooting Guide - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Trouble_Shooting_Guide
**Scraped:** 2025-08-05 09:13:37

# Trouble Shooting Guide

From EOVSA Wiki

Jump to navigation Jump to search

This is a trouble shooting guide for tohbans monitoring EOVSA remotely using MobaXterm and VNC Viewer. 

**< General checklist for solar observation>**

1\. Check [Antenna Status Page](http://ovsa.njit.edu/EOVSA/ant_status.php) to see if any antenna is under work. 

2\. If the schedule widow is not open refer to <http://www.ovsa.njit.edu/wiki/index.php/Trouble_Shooting_Guide#1.1_I_accidentally_closed_the_schedule> . In the Schedule window, click "Today", and then "Go". 

3\. **Antenna Tracking** \- are all antenna tracking (in white color)? 

4\. **Frequency Tuning** \- LO1A Sweep Status = "Sweeping", FSeqFile = FSEQ-FILE on the schedule, ErrorMsg = "No error" 

5\. **Phase Tracking** \- "ON" 

6\. **Power and Attenuation** \- Are all dBm on both H- and V- Channels within the second and third numbers shown in "AGC" on the schedule window? You can also see **SaveList** hpol and vpol to check this. 

7\. **Temps** \- no fluctuation? 

8\. **CryoRX** \- this is for antenna 14 control system. If it is down (Eg: FEMA Outlets & Receiver Voltage/Current values are zero and status is OFF), then issue the command 'ctlgo' in the terminal. 

9\. Make sure that [EOVSA Observing Status Page](http://ovsa.njit.edu/EOVSA/status.php) is being updated and that the data is being recorded. You can check if the data is recorded by typing "ls /data1/IDB |tail" in DPP terminal too. 

10\. Antennas 9 to 13 should automatically stow at the end of the observation. If needed see [possible problem with Ant 10](http://www.ovsa.njit.edu/wiki/index.php/Trouble_Shooting_Guide#Antenna_does_not_stow_.28Ant_10.29). Antenna 11 does not stow automatically. Follow the steps below to stow Ant 11; 

stop ant11

stow ant11

11\. Checking the PHASECAL plots [PHASECAL plot page](http://ovsa.njit.edu/phasecal/), if you notice any unusual noisy data on ants 9, 10, 11 or 13, generally it means the antenna did not stow properly on a previous occasion, so you should issue the commands (for example with ant 13): step 1: stop ant13 

step 2: stow ant13 (wait for it to completely stow--repeat steps 1 and 2 if it seems like it is not stowing after 5 minutes or so) 

step 3: track ant13 

New!  12\. After the day's observation is over, take a look at the results of all PHASECAL by going to [PHASECAL plot page](http://ovsa.njit.edu/phasecal/). Note any scan that didn't go well **without** the effect of WINDSCRAM (if it was under WINDSCRAM then the data points would appear in red). Record your comments on them in tohban log at [EOVSA tohban log page](http://ovsa.njit.edu/dev/tohban/). Log other activities during your duty. 

New!  13\. Do the reference gain calibration analysis by following the procedures explained in [Reference Gain Calibration](http://www.ovsa.njit.edu/wiki/index.php/Reference_Gain_Calibration) **by 1 pm on the next day**. 

## Schedule window

### 1.1 I accidentally closed the schedule

From a helios terminal enter the following commands: 

1\. cd ~/Dropbox/PythonCode/Current

2\. screen

3\. python /common/python/current/schedule.py &

4\. Press <CRTL>AD to exit from screen. 

5\. Click on "Today" and then "GO". 

### “Error: Could not write stateframe to SQL”

1\. Hit STOP on the schedule 

2\. Type $scan-stop in Raw Command window (to stop the data recording) 

3\. Close the schedule (exit out of it) 

4\. cd ~/Dropbox/PythonCode/Current

5\. screen

6\. python /common/python/current/schedule.py &

7\. Press <CRTL>AD to exit from screen. 

8\. Click on "Today" and then "GO". 

### Schedule window is frozen

1\. From helios, type the command ps -elf | grep schedule.py and note the PID # (the number is at the fourth column from the left). 

1\. Close the old one using command kill -9 # where # is the PID # from above. 

3\. cd ~/Dropbox/PythonCode/Current

4\. screen

5\. python /common/python/current/schedule.py &

6\. Press <CRTL>AD to exit from screen. 

7\. Click on "Today" and then "GO". 

8\. Double-check everything in the system, and that data files are created. 

## Stateframe

### Stateframe is frozen

1\. Close the old one using command 'kill -2 #', where # is the number followed by My PID on the right corner of the StateFrame, in the terminal of sched@helios. If you have accidentally closed the StateFrame without noting the PID, you can get it by typing **ps -elf | grep sf_display** in sched@helios, and looking at the number indicated in the **fourth column from the left** on the line that ends with "python /common/python/current/sf_display.py". 

2\. Open a new Stateframe from the menu on the left ('sf_display') 

3\. Check the log box of the new stateframe 

### “ACC down?”

1\. Open pdudigital.solar.pvt on web browser 

2\. Go to “Actions” 

3\. Go to “Loads” (on the left) 

4\. Click item 14 (ACC) 

5\. Hit “Cycle” and “Ok” when prompted 

After rebooting, if Stateframe hangs up & does not respond, open a new Stateframe and give "kill ##" (## = “My PID” on the upper right corner of frozen Stateframe) command to sched@helios.solar.pvt server. 

### ACC Restart

After the above procedure, or any time the ACC reboots, it loads from its own disk and this appears to cause glitches in the recorded data due to some synchronization problem. For some reason not understood, the glitches go away when the ACC is loaded from the win computer. To do this, 

  * Start LabVIEW on the win computer if it is not already open, and click on EOVSA-LabVIEW 2015.lvproj (this may already be open).
  * In the new Project Explorer window, under Targets, expand the acc item and right click on acc, then choose Connect from the drop down menu.
  * After connecting, click on ACC Master.vi and select Apply.
  * Now under the Startup folder in the Project Explorer, right-click ACC Master.vi and select Run.
  * In the window that pops up, start it (by selecting the white arrow at the top of the window)
  * After it starts successfully, right click on acc in the Project Explorer and choose Disconnect.
  * Now you can close the ACC Master.vi window

Note: Rebooting the ACC kills the dppxmp program, so you need to rmlock on the DPP to allow it to run again. It also kills the sf_display, see above. 

### CryoRX tab - Status are OFF, all values are zeroes (Checklist #7 is false)

What you should be seeing is that FEMA Outlets and Receiver Voltages/Currents are all zeroes, and Status are all OFF (except for Noise Diode, and RFSwitch when using low frequency receiver). This means that the control system for receiver has died. You would still see that antennas are tracking fine and data is recorded, and it doesn't mean that these data are "wrong" or "unusable". They have to be ON and non-zeroes whenever you want to change receiver setting or modify attenuation setting, which sometimes happens during the observation. 

~~To reboot, execute "starburstControl start" in antctl@feanta server (ssh connect from helios, if disconnected).~~

<12/18/2016> To reboot, just type "ctlgo" in a terminal window on helios in VNC Viewer (you may have to stop the schedule). If for any reason you want to stop the control system, type "ctlstop". 

### Antenna(s) down

**Don’t forget to check the[Antenna Status page](http://ovsa.njit.edu/EOVSA/ant_status.php) before considering to “fix” any of the antennas!!**

Symptoms: Not tracking, showing ‘AT STOW’ or other unwanted coordinates, both AZ and EL permits ON or only EL permit ON, or Axis Lock is ON 

Please be noted that the old antennas don't have power controller so $pcycle command won't work on them. 

1\. Ant 9, 10, 11, 13 could be in this state early in the schedule because they just can't move to commanded position (out of declination limit). In this case, you just have to wait a while (~few hours?) 

2\. In cold morning, large spike in the current may cause large position error in AT STOW state. 

3\. Proceed if neither #1 nor #2 is the case. If only AZ permit is ON (the first column), try "reboot 1 ant2" for rebooting ant2, for example. 

4\. If both AZ and EL permit is ON (the second column) or only EL permit is ON, then give command "$pcycle ant2" for resetting antenna 2. This switches OFF the power to antenna for 15 seconds and switches ON. In Communication tab, Ant 2 line will go red. Wait till it becomes white. If it does not become white, then try "sync ant2". If cRIO does not respond to this, it may be in “safe mode”, in which case you can type "$pcycle crio ant2" and it will cycle the power on the cRIO. Note that cRIO takes at least 2 minutes to reboot and come back online. If this sequence does not work, you may try $pcycle again, but keep in mind that this command in general should only be used when needed (i.e. discouraged if it can be avoided), to save wear and tear on the components.

5\. Give "tracktable [the current tracktable ***.radec] ant2" and "track ant2" to initiate the tracking. If this does not work, look for temperature to raise (if temperature is low). 

6\. If any antenna's communication is down (pwr shows off in communication), you can issue "$pcycle crio ant#" in raw command, then follow the routine described in 4 and 5. 

### Ant14's cRIO's "Ant" value (last column) is showing negative value

What you may see is that ant14's cRIO's "Ant" value (the very last column) showing negative value (not necessarily the extremely large value like you see for some antennas that are down, but some random number with negative sign). When you observe this, go to "ant14.solar.pvt" on web browser and see if it says in red "Slot1 - Maths error" on the left side. It is believed to occur when the controller is interpolating coordinates for the last-entered track table, and the calculation blows up (i.e. pcal_tab.radec file would have had a day change in it when it was not supposed to). 

This should not happen beyond 12/18/2016, but if you observe it beyond this date, **report to Dr. Gary** , and proceed to do the followings:

1\. In "ant14.solar.pvt", go to "Log-in" and log-in (if you need ID/PW, ask Dr. Gary or Natsuha.) 

2\. Click "Parameters", then select "#10 - Status And Trips". 

3\. Choose "#10.00". 

4\. Enter "1070" to "Update values", and hit "change". 

5\. Go to 'parameter drop down' tab under the 'menu' tab, and choose "#38 - User Trip". 

6\. Enter "100" to "Update values", and hit "change". 

This is supposed to reset the controller. Watch for cRIO's Ant value changes to positive values. Take note on the time you did this procedure, and report it to Dr. Gary.

### BRIGHTSCRAM

Find out which antenna is experiencing this by looking at [FITS image files](http://ovsa.njit.edu/fits/images/). BRIGHTSCRAM should appear as data-gap like features on the dynamics spectra. If more than two antennas are having BRIGHTSCRAM, then ALL antennas show BRIGHTSCRAM.

Wait for a while (~10 min) to see if it automatically goes away. After it goes away, give "tracktable [the current tracktable ***.radec] ant#" and "track ant#" to initiate the tracking. 

### Frequency Tuning's Sweep Status is “stopped” or "Queue overflow"

1\. Try "Stop" and "Go" the schedule. 

2\. If #1 does not work, try "lo1a-reboot" in Raw command window 

3\. After the previous command, enter the following raw commands, or simply stop and restart the schedule (which will send the commands for you): 
    
    fseq-off
    fseq-init
    fseq-file [the current frequency receiver setting ***.fsq] (should be in the right side of the schedule window, like solarhi.fsq)
    fseq-on
    
### Temperature is fluctuating too much

Try rebooting the temperature controller by typing "tec$bc ant2" for ant2, for example (tec => Thermo-Electric Controller). 

### nd-on is on (Attenuation)

Send "nd-off ant#" raw command to turn off the local noise diode. 

[![](/wiki/images/d/df/2016-04-13_hpol.png)](/wiki/index.php/File:2016-04-13_hpol.png)

[](/wiki/index.php/File:2016-04-13_hpol.png "Enlarge")

**Figure 1:** Example of the oscillation from unbalanced attenuation for ant 12 (orange).

[![](/wiki/images/b/b8/2016-04-15_hpol.png)](/wiki/index.php/File:2016-04-15_hpol.png)

[](/wiki/index.php/File:2016-04-15_hpol.png "Enlarge")

**Figure 2:** Example of the oscillation from unbalanced attenuation for ant 2 (red) and 5 (cyan).

### hpol/vpol plot (Savelist) is showing unusual oscillating behavior

What you should see is the dBm values of the antenna fluctuating very violently like in **Figure 1** and **2**. Notice that the amplitude of the fluctuation is ~3 dB, which was one FEMATTN step (at this date). This happens when hattn/vattn settings of the antenna get changed somehow and two polarizations get very unbalanced. The result is that the automatic gain control is not being able to find a happy level for both at the same time, and went into an oscillation. To calm it down, first issue the commands: 
    
    femauto-off ant#
    hattn 0 0 ant#
    vattn 0 0 ant#

which turns off the automatic gain control. **If the antenna is on the Sun, temporarily move it off the Sun using**
    
    radecoff 0 10 ant#
    
With the antenna off the Sun, set the hattn and vattn settings until both power levels are around 3 dB, i.e.: 
    
    hattn 0 12 ant#
    vattn 0 11 ant#
    
where the choice of attenuations (12 and 11 in this example) are those that set the power level close to 3 dB. Finally, turn the gain control back on, with 
    
    femauto-on ant#
    
**If you issued the radecoff command, be sure to remove it with**
    
    radecoff 0 0 ant#
    
If the fluctuation is within one FEMATTN step (2 dB as of 12/12/16, check [Schedule Command - FEMATTN level](http://www.ovsa.njit.edu/wiki/index.php/Schedule_Commands#FEMATTN_level_.5Bantennalist.5D)), the cause might be just interference. In this case, leave it for a while and see if the oscillation goes away.

### Antenna does not stow (Ant 10)

This mostly seems to happen on Ant 10 (as of ~July 2017). The symptom is that Ant 10 keeps staying at "TO STOW" status while all other (old) antennas are AT STOW already at the end of the observation. You might have tried the command "stow ant10", but it did not change the status. If this continues for more than a minute or so, it is likely that the antenna is running into a limit, and cannot be stowed properly with just "stow ant10" command (you also cannot trust if it does go to STOW by itself much later). To properly stow the antenna, **issue "stop ant10" first** , then do "stow ant10". You may need to do this multiple times. If you don't properly stow the antenna this way, it may not start tracking automatically next morning, and you will miss the data from this antenna. 

### Antenna tab is blank and an attempt to switch to it causes the Stateframe to freeze

This occurred around early June of 2017. The cause turned out to be a change in numpy behavior. Dr. Gary updated the numpy at some point and a subtle difference caused it. This means that we should think about software upgrade as one of the causes of malfunctions of our system sometimes. 

### Antenna shows (Lo or Hi) Hard limit and does not track

If a hard limit of any azel antenna (1-8 or 12) is ON, follow this procedure into the Raw Command window of the schedule (with no typos). 

1\. Make sure that other antennas are tracking a source and that no source changes are coming up within the next minute or so. 

2\. Put antenna in velocity mode with 
    
    runmode 2 ant#  (e.g for antenna 6, use "runmode 2 ant6")   
    
Be sure to specify the antenna, otherwise ALL antennas will move. 

3\. Drive the antenna OFF the limit in velocity mode. 
    
    <axis>velocity <speed> ant# 
    
Examples 
    
    azimuthvelocity 5000 ant6    # Ant 6 (on low hard azimuth limit) begins to move in positive azimuth at 0.5 deg/s
    elevationvelocity -5000 ant3 # Ant 3 (on high hard elevation limit) begins to move in negative elevation at 0.5 deg/s
    
Speed units are 1/10000th degree/second, so 5000 means 0.5 degrees/s. If the limit is on the azimuth axis, set <axis>velocity as "azimuthvelocity". If the limit is on the elevation axis, set <axis>velocity as "elevationvelocity". To drive off a low limit, use a positive velocity 5000. To drive off a high limit, use a negative velocity -5000. 

4\. After the limit is off, set the velocity back to zero. 

Wait for up to ~10-30 s, until the Hard Limit indicator goes OFF (on the antenna tab). 
    
    <axis>velocity 0 ant# (e.g "azimuthvelocity 0 ant6" for which antenna 6 stops moving) 
    
5\. Bring antenna to track. 
    
    track ant# (e.g "track ant6" for which antenna 6 resumes normal slew to target and starts tracking)
    
If the Lo Hard Limit indicator does not go OFF after 30 s, go ahead with commands 4 and 5 (although tracking will not work) and let Dr. Gary know about it. 

### Control Room Temp row is red (temp above 85 F)

This information tells you what the temperature of the EOVSA control room (where all hardwares are) is. When this becomes higher than 85 F, this row becomes red, and we must let Owen and Dr. Gary know and shut down the system to protect our hardware. It only happened once before, but when it happens it is critical, so you must act immediately. 

Note that this should not happen any more. The cause was the air conditioner solenoid getting stuck on 'heat'. The solenoid has now been bypassed so the air conditioner can only cool. If this occurs it is likely that the air conditioner has completely failed. 

Note that, when the row is grey, it is only because the "Pressure" information is zero, which means that we're not getting weather information. So this is not related to the control room temperature. 

### Front End Temperature shows 0

If front end temperature shows all 0 and the attenuation tab gives 'nan' for a certain antenna, you can cycle the front end power by issuing following command in raw command window: '$pcycle fem ant#', where ant# is the antenna that having the problem. 

### Ant 14 receiver does not switch between lo/hi

This information is relevant since ~ 2018 March, when we started to have low-frequency receiver of Ant 14 working for calibration purposes. The schedule should have HISELECT and LOSELECT during the morning and evening reference calibration scans. During HISELECT/LOSELECT, check **CryoRX** window, and make sure that the following setting is achieved (see **Figure 3** and **4**): 

[![](/wiki/images/7/72/HISELECT.png)](/wiki/index.php/File:HISELECT.png)

[](/wiki/index.php/File:HISELECT.png "Enlarge")

**Figure 3:** How CryoRX window should look like after HISELECT schedule has run.

[![](/wiki/images/6/65/LOSELECT.png)](/wiki/index.php/File:LOSELECT.png)

[](/wiki/index.php/File:LOSELECT.png "Enlarge")

**Figure 4:** How CryoRX window should look like after LOSELECT schedule has run.

**HISELECT scan:**

RFSwitch = ON 

Selected RS = High Freq RX 

[RXSelect, Position] = ~510 

[ZFocus, Position] = ~8 

**LOSELECT scan:**

RFSwitch = OFF 

Selected RS = Low Freq RX 

[RXSelect, Position] = ~103 

[ZFocus, Position] = ~70 

If for some reason this state is not achieved (e.g., the receiver state does not switch from low-frequency mode to high-frequency mode during HISELECT, the RXSelect or ZFocus position stops at some values and do not approach to the desired values), issue **rx-select hi ant 14** or **rx-select lo ant14** , to switch the state manually to high-frequency mode and low-frequency mode, respectively. 

### Antenna 13 shows 'position' in AZ and 'Lo Hard Limit' in EL

Stow the certain antenna and then TRACK may solve the problem. 

## Data recording (DPP)

### Data recording has stopped (ls /data1/IDB |tail does not return the most recent file)

You need to delete dpplock.txt file. Follow these steps: 

1\. Enter "top" into user@dpp.solar.pvt command line (if user@dpp.solar.pvt is not there, open a new terminal/terminal tab in VNC viewer & type “ssh -X user@dpp.solar.pvt). 

2\. Look for "dppxmp” under “command” column. **If it is there, do NOT delete dpplock.txt.** If it’s not there, then quit top by hitting “q” and proceed. 

3\. Type “rmlock" on DPP terminal. Check if the data recording has recovered by sending "ls /data1/IDB |tail". 

## Network

### x11vnc with 20000 port

To permit connections via VNC, first check if the x11vnc server is running by giving this command in Helios terminal through Mobaxterm or SSH. 
    
    ps -ef | grep -v grep | grep /usr/local/bin/x11vnc
    
or 
    
    x11vnc
    
which should display a line indicating that it is running (it will not be, on a new reboot). If not, type 
    
    x11go
    
to start it. 

### Cannot open VNC Viewer, or VNC Viewer's response is too slow

Open the “local” raw command window and Stateframe window by following these steps: 

1\. Type "cd /common/python/current" in helios.solar.pvt terminal of MobaXterm 

2\. Type "./sched_commands.py" for raw command window 

3\. Type "./sf_display.py" for Stateframe window (add “ &” in the end if you want to keep typing the command in the same helios window) -- note that this Stateframe window may take a while (~5 min or more) to load. 

## Others

[![](/wiki/images/4/45/FLM20151005.png)](/wiki/index.php/File:FLM20151005.png)

[](/wiki/index.php/File:FLM20151005.png "Enlarge")

**Figure 3:** Geosynchronous satellite signals seen in flare monitor.

### Strong interference in flare monitor

Twice per year (for 1-2 weeks centered around Mar. 5 and Oct. 5), the Sun enters in geosynchronous satellite belt. In this case, we see strong signals on flare monitor, like in **Figure 3** (blue line). These are radio signals from man-made satellites, which will not harm the system and cannot be avoided, so don't be alarmed. 

### The “streak” in the lowest frequency of the dynamic spectrum

If you are seeing this at the beginning or at the end of the day, this is the Sun! See **Figure 4** and **Figure 5** for sample images. When the baseline is foreshortened (as in near sunrise or sunset), the response is quite strong to the solar disk. As the Sun rises, the intensity goes down because the baselines start to get longer. You will actually see the reverse trend in the afternoon, although often the RFI is stronger so the color scale is more blue than in the morning. 

[![](/wiki/images/8/8d/XSP20151202160136.png)](/wiki/index.php/File:XSP20151202160136.png)

[](/wiki/index.php/File:XSP20151202160136.png "Enlarge")

**Figure 4:** The solar signal at the beginning of 2015-12-02 observation period. Notice that the low frequency intensity is decreasing as the Sun rises.

[![](/wiki/images/3/3e/XSP20151202213507.png)](/wiki/index.php/File:XSP20151202213507.png)

[](/wiki/index.php/File:XSP20151202213507.png "Enlarge")

**Figure 5:** The solar signal at the end of 2015-12-02 observation period. Notice the reverse effect compared to **Figure 4**.

### dpp.fix_packets() reads 0.0 output

dpp.fix_packets runs at all times and should show an output similar to: 

2018-10-25 17:21:59.001 153544.0 153513.0 

2018-10-25 17:22:59.002 153555.0 153529.0 

2018-10-25 17:23:29.001 Packet loss detected! 153603.0 115873.0 Resetting interfaces 

2018-10-25 17:23:59.002 153545.0 153511.0 

2018-10-25 17:24:59.002 153676.0 153654.0 

(example output from dpp.fix_packets) 

If at some point the output reads 0.0, the tohban must change the cpu assignments by following the steps below: 

1\. Press CTRL+C to interrupt the process and exit out of python. 

2\. To change the cpu assignment, edit the shell script by using this command on the terminal 

**vim /home/user/test_svn/shell_scripts/SMP_AFFINITY.sh**

The file includes three pairs of cpu assignments, two pairs of which are commented out. Edit the file to move the commented lines (uncomment the pair you want to use, and comment the old pair), and save the file. 

3\. run the script simply by typing 

**/home/user/test_svn/shell_scripts/SMP_AFFINITY.sh**

into the terminal, then type **rmlock**

4\. To run the actual command, type 
    
     $>   ipython --pylab
     [1]> import dpp_plot_packets as dpp
     [2]> dpp.fix_packets(cpu=[22,23])    
    
Here 22,23 are the new cpu assignments. These numbers will vary depending upon which cpu pair is uncommented in the script. This should start the process again and read out a non-zero number for packets. 

5\. In the event that changing cpu assignments does not solve the problem, try changing it to yet another pair. If that fails as well, then the DPP will need a reboot. Contact Owen or Dale to reboot the DPP. 

## Refcal calibration

To run the daily reference and phase calibration follow these steps. 

On pipeline terminal, 
    
    python /common/python/current/calwidget.py
    
which opens the calwidget window. Select the desired date of calibration in date tab by entering it or by using up and down arrows. Click enter to display all the calibration scans on that day. There are two reference calibrations placed in the start and end of the schedule with both HI and LO frequency receiver modes. After selecting click 'Analyse as Refcal' button. Please wait till the status displayed in the bottom of the window shows 'Analysis complete'. 

1\. Select the LO receiver scan by clicking on it and check the Fix Phase Drift check box. 

2\. Analyze the LO receiver as refcal. 

3\. Do any flagging needed to improve the solution. 

4\. Select the Hi receiver scan (leave the Fix Phase Drift box checked). 

5\. Analyze the HI receiver as refcal (takes awhile) and do flagging. 

6\. Select the LO receiver refcal and select Set as Refcal. The extend selection check box becomes available. 

7\. Check the check box, then select the HI receiver refcal. 

8\. The button changes to Set as Extended Refcal. Click that button, and if all goes well the line with the HI receiver scan will have an asterisk added, and the Sigma Map will be updated to include the merged scans. 

9\. Leave the HI receiver scan selected, and click Save to SQL. 

## Old Possibly Outdated Instructions for review

These instructions are left here as an archive. After review they will be removed. Please let Dale Gary or Owen Giersch know if they are still valid instructions and should be reinstated. 

### Old General Checklist

1\. Check [Antenna Status Page](http://ovsa.njit.edu/EOVSA/ant_status.php) to see if any antenna is under work. 

2\. In Schedule window, click "Today", "File", choose "Save" (overwrite if prompted), and "Go". 

**Since Feb. 2017, the schedule setup is slightly different.** Do the following:

2.1. Load 'solar.scd' and hit Today. Save it (overwrite if prompted).

2.2. Open 'solar_plus3c84_Feb2017.scd' in Texteditor (in ~/Dropbox/PythonCode/Current folder).

2.3. Update the sunrise and the sunset time according to the solar.scd file that you just updated.

2.4. Update the PHASECAL (and refcal, which is 1-hr PHASECAL, if necessary) times by **subtracting** 4 minutes from each scan (to account for the day-to-day sidereal time shift of each calibrator source). Shift the times of previous and next lines (usually ACQUIRE and SUN) accordingly.

2.5. Save the updated 'solar_plus3c84_Feb2017.scd'. Don't forget to update the DATE as well.

2.6. Load the updated 'solar_plus3c84_Feb2017.scd' and hit Go.

3\. **Antenna Tracking** \- are all antenna tracking (in white color)? 

4\. **Frequency Tuning** \- LO1A Sweep Status = "Sweeping", FSeqFile = FSEQ-FILE on the schedule, ErrorMsg = "No error" 

5\. **Phase Tracking** \- "ON" 

6\. **Power and Attenuation** \- Are all dBm on both H- and V- Channels within the second and third numbers shown in "AGC" on the schedule window? You can also see **SaveList** hpol and vpol to check this. 

7\. **Temps** \- no fluctuation? 

8\. **CryoRX** \- this is for antenna 14 control system. If it is down (Eg: FEMA Outlets & Receiver Voltage/Current values are zero and status is OFF), then issue the command 'ctlgo' in the terminal. 

9\. Make sure that [EOVSA Observing Status Page](http://ovsa.njit.edu/EOVSA/status.php) is being updated and that the data is being recorded. You can check if the data is recorded by typing "ls /data1/IDB |tail" in DPP terminal too. 

10\. STOW antennas at the end of the observation, if needed (see [possible problem with Ant 10](http://www.ovsa.njit.edu/wiki/index.php/Trouble_Shooting_Guide#Antenna_does_not_stow_.28Ant_10.29)) 

11\. Checking the PHASECAL plots [PHASECAL plot page](http://ovsa.njit.edu/phasecal/), if you notice any unusual noisy data on ants 9, 10, 11 or 13, generally it means the antenna did not stow properly on a previous occasion, so you should issue the commands (for example with ant 13): step 1: stop ant13 

step 2: stow ant13 (wait for it to completely stow--repeat steps 1 and 2 if it seems like it is not stowing after 5 minutes or so) 

step 3: track ant13 

New!  12\. After the day's observation is over, take a look at the results of all PHASECAL by going to [PHASECAL plot page](http://ovsa.njit.edu/phasecal/). Note any scan that didn't go well **without** the effect of WINDSCRAM (if it was under WINDSCRAM then the data points would appear in red). Record your comments on them in tohban log at [EOVSA tohban log page](http://ovsa.njit.edu/dev/tohban/). Log other activities during your duty. 

New!  13\. Do the reference gain calibration analysis by following the procedures explained in [Reference Gain Calibration](http://www.ovsa.njit.edu/wiki/index.php/Reference_Gain_Calibration) **by 1 pm on the next day**. 

### 1.1 I accidentally closed the schedule

1\. Click "Schedule" (on the left task bar) just once. 

2\. Click "Today". 

### “Error: Could not write stateframe to SQL”

1\. hit STOP on the schedule 

2\. type $scan-stop in Raw Command window (to stop the data recording) 

3\. close the schedule (exit out of it) 

4\. restart the program (by clicking on the icon at the left) 

5\. hit GO to start the observation again 

### Schedule window is frozen

1\. Close the old one using command 'kill -9 #', where # is the number found by typing **ps -elf | grep schedule.py** in sched@helios (the number is at the fourth column from the left). 

2\. Click "Schedule" (on the left task bar) **just once**. 

3\. Make sure you load the correct schedule and hit "Go". Double-check everything in the system, and that data files are created. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Trouble_Shooting_Guide&oldid=5465](http://ovsa.njit.edu//wiki/index.php?title=Trouble_Shooting_Guide&oldid=5465)"
