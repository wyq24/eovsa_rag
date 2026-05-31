# Calibrator Survey - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Calibrator_Survey
**Scraped:** 2025-08-05 09:13:33

# Calibrator Survey

From EOVSA Wiki

Jump to navigation Jump to search

The purpose is to do a survey of calibrators listed in the [VLA Calibrator Manual](http://www.aoc.nrao.edu/~gtaylor/csource.html) in the EOVSA frequency range (2.5-18 GHz) to determine their spectral shapes. The results are very useful to determine whether or not a phase calibrator in question is suitable for the entire EOVSA bandwidth or is only usable for a fraction of the bandwidth. It is also valuable to test the sensitivity limit of EOVSA's 27-m + 2-m baseline within a reasonable amount of integration time (10 minutes). The best calibrator sources are those 1) bright enough over the entire band (within ~10 min of integration), and 2) show a rather flat visibility vs. UV distance curve (point source). 

[![](/wiki/images/2/23/Cal_src_vis.png)](/wiki/index.php/File:Cal_src_vis.png)

[](/wiki/index.php/File:Cal_src_vis.png "Enlarge")

**Fig. 1:** The plot produced by dg_src_visibility.py for the time frame 2016-10-14 15:10 UT to 2016-10-15 15:10 UT, showing sources with minflux = 4.0 (Jy).

## Observing Sequence

Bin wrote a routine named "eovsa_src_visibility.py" on helios. Dale upgraded it with more user-friendly features named "dg_src_visibility.py". They display the visibility of all VLA calibrators by the 27-m antenna above a certain flux density threshold (defined by parameter "minflux") in C band for a given time and duration. An example of this plot is shown in **Fig. 1**. 

To produce this plot, give the following commands in helios.solar.pvt terminal on MobaXterm: 
    
    ipython --pylab
    import dg_src_visibility as sv
    from util import Time
    t=Time('2016-10-14 15:10')
    sv.plot_src(minflux=4., starttime=t, dur=24.)
    
When the network is slow, Bin's original routine may be useful. Just change "dg_src_visibility" to "eovsa_src_visibility". 

**03/27/2017: The routine's name has been changed to "whatup" since Nov. 2016, and many changes have been made since then. Therefore, it is recommended to use whatup.py instead of the above routines. Just do:**
    
    import whatup as wu
    wu.whatup(minflux=4.,t=t,dur=24.) *Note the change of variable name "starttime" to "t"
    
From this plot, the observer is asked to create the observing schedule that covers as many calibrator sources as possible, according to some criteria such as the followings: 

1\. -29d < Declination < 45d 

2\. Altitude > 10 deg 

3\. At least 10 ~ 20 deg (altitude) away from the Sun 

4\. If multiple sources are visible within the same time interval, try choosing brighter one, especially for the first source in the schedule (you will have to check the phase plot - see [2.3](http://www.ovsa.njit.edu/wiki/index.php/Calibrator_Survey#During_the_observation_-_how_to_check_the_phase_data_of_your_first_file)) 

5\. Do **NOT** include: 0319+415 (mysterious amplitude modulation), 1256-057 (in geosynchronous satellite orbit, ~5.9d) 

If you click on any line, it will show you the source name, intensity, and the position information.The observer is advised to include at least one? coverage of the sources 3c286 (1331+305) and 3c48 (0137+331) during the observing schedule. The observing schedule created from this plot on this date, using the low frequency receiver, looked like the following: 
    
    2016-10-14 15:10:00 PHASECAL 1229+020 pcal_lo.fsq
    2016-10-14 16:20:00 PHASECAL 1130-148 pcal_lo.fsq
    2016-10-14 17:30:00 PHASECAL 1331+305 pcal_lo.fsq
    2016-10-14 18:40:00 PHASECAL 0927+390 pcal_lo.fsq
    2016-10-14 19:50:00 PHASECAL 1642+398 pcal_lo.fsq
    2016-10-14 21:00:00 PHASECAL 1331+305 pcal_lo.fsq
    2016-10-14 22:10:00 PHASECAL 1733-130 pcal_lo.fsq
    2016-10-14 23:20:00 PHASECAL 2007+404 pcal_lo.fsq
    2016-10-15 00:30:00 PHASECAL 2123+055 pcal_lo.fsq
    2016-10-15 01:40:00 PHASECAL 2202+422 pcal_lo.fsq
    2016-10-15 02:50:00 PHASECAL 2136+006 pcal_lo.fsq
    2016-10-15 04:00:00 PHASECAL 2232+117 pcal_lo.fsq
    2016-10-15 05:10:00 PHASECAL 0137+331 pcal_lo.fsq
    2016-10-15 06:20:00 PHASECAL 0319+415 pcal_lo.fsq
    2016-10-15 07:30:00 PHASECAL 0137+331 pcal_lo.fsq
    2016-10-15 08:40:00 REWIND
    
Save the schedule with .scd extension, and put it in "/home/sched/Dropbox/PythonCode/Current" folder on helios server. Make sure that there is no blank line after REWIND, since it will be read as another time slot to be filled when loaded to the Schedule window later on. 

## What to look before/during the observation

### Before the schedule start - CryoRX tab

1\. Make sure that the first and the second rows (FEMA Outlets and FEMA Receiver) show "ON" and non-zero values. If they aren't, it means that the control system for receiver has died. One way to make it come back is to execute "ctlgo" in a terminal window on helios in VNC Viewer (you may have to stop the schedule). "DrainVoltage" should all be 1.20. 

2\. RFSwitch: ON - if using high frequency receiver (pcal.fsq), OFF - if using low frequency receiver (pcal_lo.fsq) 

3\. RXSelect & ZFocus (bottom of FEMA Receiver): "Position" should be [RXSelect,ZFocus] ~[???,7.5?] for the observation using high frequency receiver (pcal.fsq), and ~[103?,28.5?] for the observation using low frequency receiver (pcal_lo.fsq). If you want to change between receiver settings, use "rx-select lo/hi ant14" (change between lo and hi) in Raw Command window. If this command does not switch RXSelect and ZFocus values to the values mentioned earlier, then use "frm-abs-x [target RXSelect position value] ant14" and "frm-abs-z [target ZFocus position value] ant14" for manually setting RXselect & ZFocus position values, respectively. Each target position values should be close to the values mentioned earlier. 

### Problems expected at the schedule start

#### Frequency Tuning is not "Sweeping"

1\. Try "STOP" and "GO" the schedule 

2\. If #1 does not work, type "loa1-reboot" in Raw command window 

#### Ant 14(13A) is showing Elevation Permit (the "second column" permit in red)

1\. "reboot 1 ant14" - wait 30 seconds until it comes back 

2\. If you don't want to stop the observation that has already been started, then execute "tracktable pcal_tab.radec ant14" and "track atn14" in Row command window. (change "pcak_tab.radec" part depending on how your schedule is set up accordingly.) 

#### Attenuation

1\. Make sure dBm values for both H and V Channels are around 2~3 dB. If not, adjust the attenuation. See [Natsuha's write-up about how to change attenuation](http://www.ovsa.njit.edu/wiki/index.php/Trouble_Shooting_Guide#hpol.2Fvpol_plot_.28Savelist.29_is_showing_unusual_oscillating_behavior) for how to do it. However, if the source you're observing is weak then the dB values may not reach 2~3 even if attenuation are zeroes. In this case, just leave it. (This might happen for ant 1 and 11.)

2\. Ant 14's backend attenuation have to be both 24. For other antennas, the values have to be changing (not every second, but slowly). 

### During the observation - how to check the phase data of your first file

You can check the phase plots from the files that are stored in DPP right after the first file is created (i.e. 10 minutes after the start of the observation of your first source) to check if things are going okay. It is recommended, though, to check with the source with moderate brightness, which should show good phase data if the observation is going well (e.g. 2136+006, 9.9 Jy).

To check the phase plots, do the following 

1\. Connect to user@pipeline.solar.pvt (PW is the same for DPP server). 

2\. Start ipython --pylab. 

3\. Enter the following commands: 
    
    import read_idb as ri
    out = ri.read_idb(['/dppdata1/IDB/IDB20161209115019'], navg=60)                   #Change beyond /dppdata1/IDB/
    bl2ord = ri.p.bl_list()
    f,ax3 = subplots(4,10)                                                            #10 = number of working antennas
    for k,i in enumerate([0,1,2,3,4,8,9,10,11,12]):                                   #Indices of working antennas: 1-5,9-13
        for j in range(4):
            ax3[j,k].plot(angle(out['x'][bl2ord[i,13],0,j]),'.')
            ax3[j,k].set_ylim(-4,4)

[![](/wiki/images/5/58/Phase_ex.png)](/wiki/index.php/File:Phase_ex.png)

[](/wiki/index.php/File:Phase_ex.png "Enlarge")

**Figure 2:** Example of the phase plots produced by the commands, taken during the 10-min interval of the observation of 1229+020 (30.0 Jy source) on 2016-12-09. Each columns are different antennas. X-axis is time and y-axis is the phase values (-pi to pi). Notice that most antennas are showing constant phase values over time (each point is 60s average), except for the second from the last, which was ant12 that was down during this observation.

4\. If there's nothing going wrong with the observation or its setup, then you should see your phase plots being relatively straight over time, like in **Figure 2**. If not, there could be something wrong, or you could wait another 10 minutes to read the next file to see if it gets better or not. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Calibrator_Survey&oldid=928](http://ovsa.njit.edu//wiki/index.php?title=Calibrator_Survey&oldid=928)"
