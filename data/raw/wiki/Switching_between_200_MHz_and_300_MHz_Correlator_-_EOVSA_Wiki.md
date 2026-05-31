# Switching between 200 MHz and 300 MHz Correlator - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Switching_between_200_MHz_and_300_MHz_Correlator
**Scraped:** 2025-08-05 09:12:43

# Switching between 200 MHz and 300 MHz Correlator

From EOVSA Wiki

Jump to navigation Jump to search

# Update (2019 Feb 20)

**This page was describing an interim procedure that is no longer relevant. We have now made changes to the system to fix the problems/limitations with the 200 MHz correlator, and so we are using that exclusively and no longer need to run the 300 MHz (test) correlator that had been under development. This 300 MHz correlator never worked properly...**

# Procedure

Note that after switching correlators, or even rebooting ROACHes for a given correlator design, one must determine new delays for each antenna. For unknown reasons, the delays can actually change a LOT on a reboot -- more than just a few steps as expected from the way the ADC works. To get the delays in the ballpark, or at least determine the sign of the delay, observations on CIEL-2 with band23.fsq are extremely helpful. After that, observe a strong phase calibrator for up to 1/2 hour and use delay_widget.py to determine and set the delays. 

## Switching from 200 MHz to 300 MHz Correlator

Follow these steps, in this order, to switch from a currently running 200 MHz correlator design to a 300 MHz one: 

  * Point eovsa_corr.bof to currently desired 300 MHz correlator design 
    * Log in to ovsa.njit.edu, and cd to folder /test

       sudo rm eovsa_corr.bof
       sudo ln -s eovsa_corr_300mhz_<date>.bof eovsa_corr.bof

  * FTP sched@helios:/home/sched/Dropbox/PythonCode/Current/eovsa_corr.ini to /parm folder to ACC

       ftp ACC <enter user/password>
       cd /parm 
       put eovsa_corr1200.ini eovsa_corr.ini
       bye

  * Edit roach.py to swap comments in two places, **#val =** , and **#mcstart =** and save to BOTH folders sched@helios:/home/sched/Dropbox/PythonCode/Current AND /common/python/current.
  * Edit chan_util_bc.py to swap single comment **#ifbw =** and save to /common/python/current.
  * Edit delay_widget.py to swap signs (comment out line **ch.dla_update2sql(delays,-xydelays)** and uncomment the following line) and save to /common/python/current.
  * **Physically change the clock speed to 1200 MHz** , 0 dBm (requires Kjell or someone at OVRO to make this change)
  * Edit user@dpp:/home/user/test_svn/Miriad/dpp/DPPparameters.f90 to swap single comment for **correlator_clock** parameter
  * Edit user@dpp:/home/user/test_svn/Miriad/dpp/DPP_PROCESS_SPECTRAL_FRAME.f90 to swap single comment for **pshift(jp) =**
  * Close the schedule program on helios
  * From ipython on helios, load the 300 MHz design

       ipython --pylab
       import roach as r
       ro = ['roach'+str(i+1) for i in range(8)]
       r.reload(ro)

  * Open the schedule program and restart the schedule, which should now run in 300 MHz mode.

## Switching from 300 MHz to 200 MHz Correlator

Follow these (nearly the same) steps, in this order, to switch from a currently running 300 MHz correlator design to a 200 MHz one: 

  * Point eovsa_corr.bof to currently desired 200 MHz correlator design 
    * Log in to ovsa.njit.edu, and cd to folder /test

       sudo rm eovsa_corr.bof
       sudo ln -s eovsa_corr_2016_May_11_1053.bof eovsa_corr.bof 

  * FTP sched@helios:/home/sched/Dropbox/PythonCode/Current/eovsa_corr.ini to /parm folder to ACC

       ftp ACC <enter user/password>
       cd /parm
       put eovsa_corr.ini
       bye

  * Edit roach.py to swap comments in two places, **#val =** , and **#mcstart =** and save to BOTH folders sched@helios:/home/sched/Dropbox/PythonCode/Current AND /common/python/current.
  * Edit chan_util_bc.py to swap single comment **#ifbw =** and save to /common/python/current.
  * Edit delay_widget.py to swap signs (uncomment line **ch.dla_update2sql(delays,-xydelays)** and comment the following line) and save to /common/python/current.
  * **Physically change the clock speed to 800 MHz** , 0 dBm (requires Kjell or someone at OVRO to make this change)
  * Edit user@dpp:/home/user/test_svn/Miriad/dpp/DPPparameters.f90 to swap single comment for **correlator_clock** parameter
  * Edit user@dpp:/home/user/test_svn/Miriad/dpp/DPP_PROCESS_SPECTRAL_FRAME.f90 to swap single comment for **pshift(jp) =**
  * Close the schedule program on helios
  * From ipython on helios, load the 200 MHz design

       ipython --pylab
       import roach as r
       ro = ['roach'+str(i+1) for i in range(8)]
       r.reload(ro)

  * Open the schedule program and restart the schedule, which should now run in 200 MHz mode.

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Switching_between_200_MHz_and_300_MHz_Correlator&oldid=3603](http://ovsa.njit.edu//wiki/index.php?title=Switching_between_200_MHz_and_300_MHz_Correlator&oldid=3603)"
