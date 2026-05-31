# Computing Systems - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Computing_Systems
**Scraped:** 2025-08-05 09:12:46

# Computing Systems

From EOVSA Wiki

Jump to navigation Jump to search

## Overview of EOVSA Computing Systems

The computing infrastructure for EOVSA has been developed largely according to the initial plan, which calls for multiple computers dedicated to specific tasks. This document describes the computing hardware specifications and capabilities, role of each computer in the system, and interdependences among them. A schematic summary is shown in Figure 1. 

[![Figure 1](/wiki/images/8/84/Figure_1.png)](/wiki/index.php/File:Figure_1.png "Figure 1")

## Specifications of Each System

In this section we detail the system specifications, for reference purposes. The systems are listed alphabetically by name. 

### acc.solar.pvt (192.168.24.10)

The Array Control Computer (ACC) is a National Instruments (NI) PXIe-1071 4-slot chassis with three units installed: NI PXIe-8133 real-time controller, NI PXI-6682H timing module, and NI PXI-8431 RS485 module. The relevant features of acc are: 

  * Real-Time PharLap operating system running Labview RT
  * Quad-core i7-820QM, 1.73 GHz processor with 4 GB RAM
  * High-bandwidth PXI express embedded controller
  * Two 10/100/1000BASE-TX (gigabit) Ethernet – one port is connected to the LAN, and the other is dedicated to the Hitite synthesizer.
  * 4 hi-speed USB, GPIB, RS-232 serial, 120 GB HDD
  * Rackmount 4U Chassis

### dpp.solar.pvt (192.168.24.100)

The Data Packaging Processor (DPP) is a Silicon Mechanics Rackform nServ A331.v3 computer with 32 cores. The main features of dpp are: 

  * Two Opteron 6276 CPUs (2.3 GHz, 16-core, G34, 16 MB L3 Cache)
  * 64 GB RAM, 1600 MHz
  * Intel 82576 dual-port Gigabit ethernet controller
  * Two 2-TB Seagate Constellation SATA HDD
  * Myricom 10G-PCIE2-8B-2S dual-port 10-GB Ethernet controller with SFP+ interface
  * Ubuntu 18.04 LTS (long-term support) 64-bit operating system (updated 22 October 2018)
  * Rackmount 1U Chassis

### helios.solar.pvt (192.168.24.103)

The Scheduling and Fault System computer is a Dell Precision T3600 computer. The main features of helios are: 

  * Intel Xeon E5-1603 CPU (4-core, 2.8 GHz, 10 MB L3 Cache)
  * 8 GB RAM, 1600 MHz
  * Two 2-TB SATA HDD
  * 512 MB NVidia Quadro NVS 310 dual-monitor graphics adapter
  * Dell Ultrasharp U2312H 23-inch monitor
  * 16xDVD+/-RW optical DVD drive
  * Integrated gigabit Ethernet controller
  * Ubuntu 18.04 LTS (long-term support) 64-bit operating system (updated 2018 Sep 18)
  * Free-standing Tower Chassis

### ovsa.njit.edu (192.100.16.206)

The Gateway/Web Server is an older machine (ordered 1/12/2011). The DELL service tag number is FHDD8P1. The main features of ovsa are: 

  * Intel Xeon W3505 (2.53 GHz, dual-core, 8 MB L3 Cache)
  * 4 GB RAM, 1333 MHz
  * 250 GB SATA HDD (operating system) + 250 GB data disk + 500 GB archive disk
  * 512 MB Nvidia Quadro FX580 dual-monitor graphics adapter
  * Dell U2211H 21.5-inch monitor
  * 16X DVD+/-RW optical DVD drive
  * Broadcom NetXtreme 57xx Gigabit Ethernet controller
  * Ubuntu 16.04 LTS (long-term support) 32-bit operating system (updated 2018 Sep 18)
  * Free-standing Tower Chassis

### pipeline.solar.pvt (192.168.24.104)

The Pipeline Computer is a Silicon Mechanics Storform iServ R513.v4 computer with 20 cores. Pipeline is the most powerful of the EOVSA computers, and is meant to handle the real-time creation of data products. The main features of pipeline are: 

  * Two Intel Xeon E5-2660v2 CPUs (2.2 GHz, 10-core, 25 MB L3 Cache)
  * 128 GB RAM, 1600 MHz
  * Integrated dual-port Gigabit Ethernet controller
  * LP PCIe 3.0 x16 SAS/SATA controller
  * Twelve 4-TB Seagate Constellation SATA HDD configured as RAID 6 with hot spare (36 TB usable)
  * Ubuntu 18.04 LTS (long-term support) Server Edition 64-bit operating system (updated 2018 Sep 18)
  * Rackmount 2U Chassis

### roach{n}.solar.pvt (192.168.24.12{n})

The eight ROACH2 boards each have a Power-PC CPU, with hostnames are roach1.solar.pvt, roach2.solar.pvt, … roach8.solar.pvt. The receive their operating systems via NFS netboot from the Gateway/Web Server computer ovsa.njit.edu. The CPUs on the roaches are mainly for interacting with the on-board FPGAs, which are programmed to run the correlator design. 

### tawa.solar.pvt (192.168.24.105)

The Analysis Computer is essentially a clone of the DPP Computer, a Silicon Mechanics Rackform nServ A331.v4 computer with 32 cores. The main features of tawa are: 

  * Two Opteron 6276 CPUs (2.3 GHz, 16-core, G34, 16 MB L3 Cache)
  * 64 GB RAM, 1600 MHz
  * Intel 82576 dual-port Gigabit ethernet controller
  * Two 2-TB Seagate Constellation SATA HDD, in a RAID1 configuration.
  * DVD+/-RW optical DVD drive
  * Ubuntu 12.04 LTS (long-term support) Server Edition 64-bit operating system
  * Rackmount 1U Chassis

### sqlserver.solar.pvt (192.168.24.106)

The RDBMS computer is a Dell PowerEdge R520. It records the main monitor database, which can be queried using standard SQL queries. The computer was installed on 9/25/2014, and runs the Windows Server 2008 R2 Standard operating system. The main features of sqlserver are: 

  * Intel Xeon E5-2420 CPU (1.9 GHz, 6-core, 15MB Cache)
  * 32 GB RAM, 1600 MHz
  * Broadcom 5720 Quad-port Gigabit Ethernet controller
  * Four 4-TB SAS Western Digital WD-4001FYYG HDD, in a RAID5 configuration (12 TB usable)
  * iDRAC remote management card (IP address 192.168.24.108)
  * Read-only optical DVD drive
  * SQL Server 2012 Developer software

### win1.solar.pvt (192.168.24.101)

The Windows PC is a clone of the Gateway/Web Server, purchased around the same time (ordered 5/19/2011), but runs the Windows 7 operating system, mainly for the purpose of running Windows-only utilities including monitoring the ACC and the antennas. The DELL service tag number is C303GQ1. The main features of win1 are: 

  * Intel Xeon W3530 (2.8 GHz, dual-core, 8 MB L3 Cache)
  * 4 GB RAM, 1333 MHz
  * Two 500 GB SATA HDD
  * 512 MB Nvidia Quadro FX580 dual-monitor graphics adapter
  * Dell U2211H 21.5-inch monitor
  * 16X DVD+/-RW optical DVD drive
  * Broadcom NetXtreme 57xx Gigabit Ethernet controller
  * Windows 7, 32-bit operating system
  * Free-standing Tower Chassis

## Function/Purpose of Computers

In the cases of the acc, dpp, pipeline, and sqlserver, the system host name is suggestive of the main purpose of the computer, while helios and tawa are the names of mythological Sun gods. This section gives a somewhat detailed description of the function of each system. 

### ovsa.njit.edu

This is the web server and gateway computer, which is the only one that is on the Wide-Area-Network (WAN). It has no other function in the overall system except to permit outside users to connect to the private network (LAN) by tunneling. To gain access to machines on the private network, it is necessary to log in to ovsa via ssh, at the same time declaring a tunnel that specifically opens a relevant port through to the desired machine on the LAN. The protocol is to issue a command like:  

    ssh -L <local port>:<host>.solar.pvt:<desired port> <user>@ovsa.njit.edu
    
where <host> is the host name of the machine to tunnel to, on the solar.pvt LAN, <desired port> is the port you wish to reach, and <user> is the name of a user account on ovsa.njit.edu that you will use to log in and create the tunnel. The <local port> is the port you will connect to from your local machine. Once you have issued the above command and logged in, you must open a second connection to localhost:<local port>. As a concrete example, say I wish to log in to helios as user sched via ssh. I would issue the command  

    ssh –L 22:helios.solar.pvt:22 dgary@ovsa.njit.edu
    
where 22 is the usual ssh port. I would then (in a second window) issue the command  

    ssh sched@localhost
    
which defaults to port 22 since I am using ssh. Another example is to set up for a VNC connection to helios. For that, I would issue the command  

    ssh –L 5902:helios.solar.pvt:20000 dgary@ovsa.njit.edu
    
and then open a VNC connection to localhost:2 (VNC defaults to adding 5900 to the port number, hence this would connect via port 5902). For users of the Windows operating system, I suggest the use of the excellent MobaXterm (<http://mobaxterm.mobatek.net/>), which allows such tunnels to be set up and saved, then executed as a one-click operation. 

### acc.solar.pvt

As its name implies, this is the Array Control Computer (ACC), which runs the supervisory LabVIEW code to communicate with the cRIO computer systems in each antenna, and to assemble and serve the 1-s stateframe. It provides a dedicated TCP/IP port (6341) from which each subsystem can connect and read stateframes of various “age” from the history buffer, from 0-9 seconds old. Stateframe 0 is the incomplete one being filled for the current second. It also supplies ports for the ACC to receive stateframe information from the schedule (port 6340) and the DPP (port 6344) for adding to the stateframe. In addition to talking to the cRIOs, it also controls the Hittite LO system, the subarray switches in the LO Distribution Module (LODM), and the downconverter modules (DCMs). 

### helios.solar.pvt

This machine has several functions. It is the computer that runs the schedule (for definiteness, only one schedule is allowed to run at a time), and as such it also must control the ROACHes at several time cadences. It initializes them on startup, it sends information about the frequency sequence once per scan, and it sends integer delays once per second. It also creates the scan_header data file to the ACC, which is read by the DPP at the start of each scan. And it creates and sends schedule information, including the exact delays, to the ACC for inclusion in the stateframe. The schedule is meant to run the same general sequence of commands every day automatically, so that unless some special configuration of the system is needed (such as for non-regular calibrations or system tests) it will continue to run for multiple days without intervention. It also must support all scheduling of calibration observations, but at least for now this is expected to be done semi-manually. The schedule may also eventually play a role in the monitor RDBMS, but this has not been fully defined as yet.  
Another important function of helios is to run the fault system supervisory program. As of this writing, the fault system has not been implemented, but when functional it will examine the contents of the stateframe and create a parallel array of flags indicating problems, which various systems can examine and decide whether to alert the operator or take some corrective action.  
Finally, helios also runs a version of the operator display (called sf_display for stateframe display), which can also run additional copies as desired on other machines. It currently works fine on external machines running either Linux or Windows, when they are properly set up for tunneling through ovsa.njit.edu.  
It is anticipated that helios will have only a single user account, called sched. 

### dpp.solar.pvt

As the name implies, this is the Data Packaging Processor (DPP), which receives the raw 10-GBe UDP data packets from the ROACHes, processes them, and outputs the “interim database” Miriad files. It has a total of 4 TB of hard disk, which is sufficient for about 1 month of interim data under full EOVSA operation. If the interim data are to be kept, they will have to be transferred to the pipeline machine, and eventually to NJIT. The DPP sends its subsystem information to the ACC, which adds it to the stateframe. The DPP also reads the stateframe as well as the scan_header file and various calibration files residing on the ACC, in order to do the correct processing of the data into Miriad files. Once the interim data have been produced (each file containing roughly 2 minutes of data), control should pass to the Pipeline machine (pipeline.solar.pvt) for further processing into archival data bases as well as real-time data products. It will be necessary to use nfs to mount the dpp.solar.pvt disks on pipeline.solar.pvt. We should avoid nfs-mounting pipeline disks on dpp, however, so that the data-taking is not compromised when pipeline is down for some reason.  
It is anticipated that dpp will have only a single user account, called user. 

### sqlserver.solar.pvt

This is the RDBMS computer responsible for recording and serving the monitor database (scan header and stateframe information). Its programming allows it to adapt seamlessly to multiple versions of the stateframe. Explicit methods of accessing, storing and querying data from Python are documented in Python_Access_to_Database.pdf. The main purpose of the database is to provide historical information about the state of the system for engineering purposes, and tracking down problems in the system. It is anticipated that certain summary web pages will be created that perform standard queries to provide an overview of the state of the system. 

### pipeline.solar.pvt

This is the Pipeline computer responsible for real-time processing of the interim data, which has several purposes: (1) To provide a continuous indication of the quality of the data and the state of solar activity by permitting display of light-curves, spectra, and images. These data-quality indicators should be put directly onto the web for public access, as well as for use as an operator console. (2) To generate the metadata and near-real-time data products, including ultimately coronal magnetic field maps and other parameters. These data products will go into a searchable database accessible via Dominic Zarro’s system. (3) To process certain daily calibration observations in an automatic way so that the results are available to the DPP for applying to the next scan’s interim data. (4) To process and/or reprocess the interim database into final archival databases, which will form the standard uv data to be used by scientists to create and analyze their own (non-real-time) data products. (5) In the case that the archival database calibration is somehow better than that available for the real-time processing, off-line reprocessing and recreation of the real-time data products will be done for archival purposes.  
The 32 TB of RAID disk storage that are available on pipeline.solar.pvt should provide enough space for at least a year of interim data, and several years of archival data, depending on the as yet unknown data volume of the metadata and data products. A second copy of the archival data will be kept at NJIT, and possibly other sites.  
Pipeline currently has only one user account, called user. It may have additional accounts for a few individuals who are responsible for developing pipeline’s software, such as Jim McTiernan and Stephen White. 

### tawa.solar.pvt

This is a general-purpose analysis machine, meant to provide for analysis capability that is off the critical data path. It should have access to pipeline’s disks via nfs, and should be capable of doing all of the Pipeline analysis as well as other tasks.   
Tawa, as a general-purpose machine can have multiple user accounts. It may ultimately have a general guest account so that outside users can process limited jobs locally without having the full suite of software on their own computer. 

## Interdependencies of the EOVSA Computers

In order for the various computers in the system to do their jobs effectively, there are certain interdependencies that are built in to the infrastructure. It is important to clarify these and make sure that they are as limited as possible in order to allow the system to function when non-critical infrastructure is down for maintenance or repair.  

[![Figure 2.png](/wiki/images/7/76/Figure_2.png)](/wiki/index.php/File:Figure_2.png)

The above table summarizes the interdependencies of the computers in the EOVSA system. The critical computers for control of the system are acc, helios and dpp. Basic control and data-taking are not possible without these three machines being operational. Still important, but not critical, computers (i.e. not single-point failures) are the cRIOs in the antennas, the antenna controllers themselves, and the ROACH boards. In general, the system should be capable of operating without one or more of these systems. Note that losing a ROACH board means that the two antennas input to that board are lost, and additionally all frequency channels (1/8th of each 500-MHz band) handled by that board’s X-engine are also lost. In terms of impact, then, an individual ROACH board is more critical than an individual cRIO or antenna controller. Next in importance is pipeline, which has a role not only in real-time data products and interim-to-archival processing, but also in certain near-real-time calibration processing. Although the interim database can be created without pipeline, the quality of the interim database may be compromised. Finally, tawa is off the critical path and should not generally affect any aspect of data-taking or data-processing. The gateway/web server, ovsa, could be critical in providing access to the private network from outside, although in case of ovsa failure tawa could be pressed into service by merely plugging it into the WAN and possibly making some changes in the DHCP/firewall settings at the site. It may be worthwhile to put into place preparations (and advance testing) to make this option as quick and easy as possible.  
Certain disks should be accessible via nfs from multiple machines, but care should be taken with nfs to avoid loss of a non-critical machine causing problems with a critical one. Therefore, unless otherwise required, the cross-mounting should be limited to pipeline having r/o access to dpp, and tawa having r/o access to dpp and pipeline. 

## Troubleshooting Tips

We have had problems when replacing computers or motherboards, but using existing boot disks from the old machine. The new machine does not configure its network, due to a file that is on the existing boot disk. Here is a statement of the problem: 
    
    On ubuntu, /etc/udev/rules.d/70-persistent-net.rules maps mac addresses to ethernet interface names.  
    It will be created if it doesn't exist or appended to if it does exist.  If it gets appended to then 
    you end up with ethN where N is the number of ethernet interfaces on the machine from whence the disk 
    came.  Renaming the file to have a ".old" extension and rebooting will cause it to be recreated 
    starting with eth0. 

All that is needed is to rename this file so that a file of that name does not exist, then reboot. The system will automatically create the file correctly, and all will be well. 

### Problems with SQL Server

The SQLserver machine is a Dell PowerEdge, with a large number of differences from the kind of Windows PC I am used to. I will attempt to note a few important things I have learned due to the recent failure of the RAID system (and the SQL database) on that system. 

The first thing is that there is a remote administration device on the machine with a system called iDRAC7. It had very old firmware, but today I downloaded and installed new firmware from 2020. That version of iDRAC is no longer supported, but at least I was able to load the firmware and get a newer version working. To access it via the GUI (web interface), enter the URL <http://192.168.24.108/console>. The first problem is that the certificate has expired so only older versions of web browsers allow you to go there. There is also an ssh CLI interface, and you get there by 
    
    ssh root@192.168.24.108    (or sqlidrac.solar.pvt)
    
The commands from there are very esoteric. 

#### To Get the SQL Server Monitor Screen to Work

We had a terrible time because we could not see the boot up process or interact with it. I then stumbled upon a procedure for turning it on! Apparently it was set not to display anything. To check the status connect via ssh and type: 
    
    racadm getconfig -g cfgRacTuning -o cfgRacTuneLocalServerVideo
    
If it returns 0, that means the video is turned off. To turn it on type: 
    
    racadm config -g cfgRacTuning -o cfgRacTuneLocalServerVideo 1
    
#### To Get Into the RAID Configuration Utility

Once the monitor screen is working and showing the boot process, at some point the PERC controller information will be displayed with a notice to hit Ctrl-R to enter the configuration utility. Type 
    
    Ctrl-R
    
to enter the configuration. 

What you do there depends on the issue, see the Dell PowerEdge RAID Controller documentation in the Dropbox/OVSA Expansion/Design/Documentation folder for details. The specific problem we had is that the Virtual Disk setup was lost (when disks are popped out and put back in, they are marked Foreign and their configuration has to be "imported"). In fact, the four RAID disks were marked "Failed" in the PD (physical disk) menu. However, by popping out and reinserting the disks, they came back as good, but Foreign. Once all four were marked good, a Foreign View menu appeared, from which one highlights the line at the top, hits F2, and then one can Import the configuration. At that point, one of the disks was marked as Rebuild and a rebuild of the array was started. However, on reboot during the rebuild the disks again came up as Failed, and the whole process had to be restarted. I am now letting the rebuild complete without rebooting, to see if that helps. My surmise is that the disk in slot 5 (the four disks are in slots 1, 3, 5, 7) is flakey and the one in slot 3 has to be rebuilt. On reboot the one in slot 5 fails and because the one in slot 3 hasn't yet been rebuilt the whole thing comes crashing down. Hopefully when the disk in slot 3 is rebuilt the system will tolerate a failure of the slot 5 disk. 

## Rebooting the Computers

For all of the Linux computers running Ubuntu, the command to reboot is 
    
    sudo reboot now
    
which will immediately start the reboot process. After a few seconds, your remote connection will be interrupted and you will have to wait for the boot process to complete (up to 5 minutes) before reconnecting. 

If multiple machines are to be rebooted, the computers should be rebooted in the following order: _Helios_ , _DPP_ , _Pipeline_ , _Tawa_ , _Ovsa_. This ensures that the remote-mounted disk connections will be reestablished. 

When some systems are rebooted, they do not necessarily restart all required software (although they should, and the problems should be researched and fixed). Currently, the following exceptions are needed: 

### Helios

Whenever Helios is rebooted, the sched dropbox server does not automatically restart. To restart it, type the following at a terminal command prompt: 
    
    python /home/sched/Downloads/dropbox.py start
    
After a reboot, the schedule has been seen to act strangely (time not updating smoothly). This was traced to the chronyd (time) service not starting correctly. To check it, type 
    
    chronyc sourcestats
    
which should return something like this: 
    
    210 Number of sources = 6
    Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
    ==============================================================================
    ntp1.solar.pvt              4   3     6     +1.491     45.171    +12us  6424ns
    ntp1.cm.pvt                 0   0     0     +0.000   2000.000     +0ns  4000ms
    chilipepper.canonical.com   4   3     7   +474.809   6872.249  -4302us  1104us
    pugot.canonical.com         4   3     7    -88.119  12753.910  -8834us  2163us
    golem.canonical.com         4   4     7   -453.965   9604.132    -14ms  1207us
    alphyn.canonical.com        4   3     7    +18.198     24.140  -2128us  3812ns
    
If not, then start it with the command 
    
    sudo systemctl restart chrony.service
    
and reissue the command 
    
    chronyc sourcestats
    
to check that it is running correctly. 

Finally, after a reboot the schedule and sf_display programs have to be restarted. To do that, simply log on via VNC as usual, and then click once on their icons in the left taskbar (hover over them with the mouse if you are unsure which is which). 

To permit connections via vnc, first check if the x11vnc server is running by 
    
    ps -ef | grep -v grep | grep x11vnc
    
which should display a line that indicates that it is running (it will not be, on a new reboot). If not, type 
    
    x11go
    
to start it. 

Definition of x11go is 
    
    alias x11go="x11vnc -shared -display :0 -forever -clip 1920x1200+0+0 -bg -o /var/log/x11vnc.log -usepw -rfbport 20000 -auth /home/sched/.Xauthority"
    
### DPP

First, check that the 10 Gb ethernet interfaces are present, by typing the command 
    
    ifconfig
    
which should show a list of interfaces including enp5s0 and enp7s0. If these are NOT present, type 
    
    sudo modprobe myri10ge
    
to start the device driver. Then check again that these interfaces are present. 

When the DPP is rebooted, its interrupt priority needs to be reconfigured. This is done via the following, typed at a terminal command prompt: 
    
    sudo /home/user/test_svn/shell_scripts/SMP_AFFINITY.sh
    
If the dppxmp program was running at the time of the reboot, then after the reboot it will also be necessary to delete the lock file: 
    
    rm /home/user/test_svn/Miriad/dpp/DPPlock.txt
    
or just issue the equivalent alias 
    
    rmlock
    
#### NB:

**Note also that if the DPP reboots it is likely necessary to mount its disk on Pipeline, otherwise the pipeline task will fail.** To check, log in to Pipeline and type **df**. The following shows its output when the DPP data1 disk is NOT present: 
    
    pipeline:~> df
    Filesystem               1K-blocks        Used  Available Use% Mounted on
    udev                      65964708           0   65964708   0% /dev
    tmpfs                     13198988        2096   13196892   1% /run
    /dev/sda3                100676016    66240196   29298668  70% /
    tmpfs                     65994932           0   65994932   0% /dev/shm
    tmpfs                         5120           0       5120   0% /run/lock
    tmpfs                     65994932           0   65994932   0% /sys/fs/cgroup
    /dev/loop0                   13312       13312          0 100% /snap/gnome-characters/124
    /dev/loop3                    2304        2304          0 100% /snap/gnome-calculator/238
    /dev/loop4                   14848       14848          0 100% /snap/gnome-logs/43
    /dev/loop6                    3840        3840          0 100% /snap/gnome-system-monitor/57
    /dev/loop1                   90112       90112          0 100% /snap/core/5328
    /dev/loop2                  144384      144384          0 100% /snap/gnome-3-26-1604/70
    /dev/loop5                   43264       43264          0 100% /snap/gtk-common-themes/701
    /dev/sda1                   463844      205889     229488  48% /boot
    /dev/sdb1              35051283456 25353337932 9697945524  73% /data1
    cgmfs                          100           0        100   0% /run/cgmanager/fs
    192.168.24.103:/common  1914515456   302341120 1514899456  17% /common
    tmpfs                     13198984          28   13198956   1% /run/user/111
    tmpfs                     13198984          32   13198952   1% /run/user/1000
    /dev/loop7                   89984       89984          0 100% /snap/core/5548
    /dev/loop8                   14976       14976          0 100% /snap/gnome-logs/45
    /dev/loop9                   89984       89984          0 100% /snap/core/5662
    /dev/loop10                 144128      144128          0 100% /snap/gnome-3-26-1604/74
    
If so, type **sudo mount -a** on Pipeline, then the **df** command will show the same thing, but with the additional line 
    
    pipeline:~> df
    Filesystem               1K-blocks        Used   Available Use% Mounted on
    .
    .
    . 
    192.168.24.100:/data1   1922728960   569949184 1255088128  32% /dppdata1
    .
    .
    .
    
where /dppdata1 is the DPP data1 disk. 

### Correlator (ROACH boards)

If the number of packets coming from the correlator, as seen by the command (the part before the $ is the dpp prompt) 
    
    user@dpp:~$ python dpp_eth_mon.py
    
is considerably less than 155000 on each interface, the ROACH boards may need to be rebooted. Note that if the number of packets is close, like 148000 or so, it may be that the above SMP_AFFINITY_20160511.sh script needs to be run. In any case, if the correlator needs to be rebooted, do the following commands in ipython: 
    
    import roach as r
    ro = ['roach' + str(i+1) for i in range(8)]
    r.reload(ro)
    
This will result in quite a bit of output as the 8 ROACH boards reboot (takes several minutes). Near the end of the process, all boards should show success, the sync value should be 1, and the mcount should be within 2-3 of the predicted value. After that, you can close the ipython session and recheck the presence of the packets, which should now be 155000 or so. 

### LNA14

The LNA14 computer is the Beaglebone embedded system computer in the 27-m receiver AUX box. It controls the power to the low-noise amplifiers (LNAs) in the frontend. If that is rebooted, some software has to be started manually, using these commands (the first kills any running python tasks): 
    
    killAll python
    python ccat_bitbang_chips-master/boards/ccat_bias_board/bbServer.py -p 50002 &
    
### ACC

For now (2018 Jan 20) we cannot let the ACC reboot by itself, but rather we need to start it from the Win computer. See the instructions [HERE.](http://www.ovsa.njit.edu/wiki/index.php/Trouble_Shooting_Guide#ACC_Restart)

## RAID System on Pipeline

The hardware controller on Pipeline is an LSI 9271-series SAS controller, the MegaRAID SAS 9271-8i 6Gb/s SAS controller card. The current web pages seem to be from a company Avago Technologies. In order to control the card, one needs to use one of several software approaches available, as detailed in the User Guide, which I have put in the Dropbox under 
    
      Dropbox/OVSA Expansion/Design/InstrumentationDocs/Pipeline_51530_00_RevP_MegaRAID_SAS_SW_UserGd.pdf.
    
I spent a lot of time trying to gain access to the various software control, and succeeded in two of them, as follows: 

### WebBIOS

The WebBIOS configuration utility is discussed in Chapter 4 of the above document. To get into it, one must first connect a monitor, keyboard and mouse to Pipeline and then reboot the machine. During the reboot process, when the screen shows the LSI page, hit ^H (ctrl-H) and after awhile the WebBIOS configuration utility wll appear. 

The specific problem I was trying to address is that I had popped one of the drives out while the computer was running (since I thought this would not cause a problem—I was wrong!). It began beeping 1 s on, 1 s off, which means the configuration is in a “warning” state in RAID 6. Since one disk is redundant, this was a warning rather than critical. 

To fix the problem, once I booted into the WebBIOS utility I found that by listing the drive properties I could see that the disk in slot 10 (the one I removed) was listed as “unconfigured bad,” which is indeed the expected behavior for a disk being removed while active. I was able to select the disk and change its state to “unconfigured good,” at which point it was indicated as “FOREIGN.” I then marked it for rebuild, but had to import its configuration (apparently this is metadata contained on the drive) before I could do the rebuild. The rebuild appeared to start automatically (and is VERY slow—it is still working after many hours). Note that I had also removed the “Hot Swap” drive, and it also showed “unconfigured bad,” which I was able to set to “unconfigured good.” However, I tried to mark it as a hot swap drive and it gave an error saying the configuration failed. I ended up having to ignore it. 

The problem I find with the WebBIOS utility is that although one can stop the beeping via a mouse click, to exit the utility one has to reboot. The reboot then starts the beeping again! I would also like to see the progress of the rebuild, but there seems to be no way except to boot into the utility again, which seems overkill. 

### MegaCLI

There is a command-line utility provided by LSI called MegaCLI, and after a lot of work I finally was able to get it installed. I had previously tried to install another utility called StorCLI, but ultimately determined that it does not work with the series of controller we have. **Note that the installation procedure below is for documentation purposes, but should not be needed again now that MegaCLI has been installed.**

#### installation

To install MegaCLI, I first found it on the Avago Technologies website (it was not obvious, but when I entered the product number and then typed megacli in the search, it did come up. I downloaded MegaCLI_5.5, in the form of a zip file, and unzipped it, which created a bunch of directories including Linux. In that subdirectory, I found MegaCli-8.07.14-1.noarch.rpm. In order to install it on an Ubuntu system, I had to install alien, e.g. 
    
    sudo apt-get install alien
    
and then type 
    
    alien –scripts MegaCli-8.07.14-1.noarch.rpm
    
This resulting in the creation of a file 
    
    megacli_8.07_14-2_all.deb
    
I then installed this with the command 
    
    sudo dpkg –i megacli_8.07_14-2_all.deb
    
The end result was to create the file (and associated library) 
    
    /opt/MegaRAID/MegaCli/MegaCli64
    
#### some useful commands

One can run this routine with the –h switch to get a list of commands (it is very extensive). The use of the command is described in Chapter 7 of the pdf document mentioned earlier. One important thing I discovered is that the dash in front of all the elements of a command are NOT necessary—the same command works fine without them. Here are some commands I used: 
    
    sudo /opt/MegaRAID/MegaCli/MegaCli64 adpsetprop alarmdsbl a0
    
disables the damn alarm while rebuilding is in progress. Enter 
    
    sudo /opt/MegaRAID/MegaCli/MegaCli64 adpsetprop alarmenbl a0
    
to reenable it after the rebuild is done. 
    
    sudo /opt/MegaRAID/MegaCli/MegaCli64 ldpdinfo a0
    
lists a whole lot of information for each drive in the array. In particular, use with grep Firmware to find out the state of the drive: 
    
    sudo /opt/MegaRAID/MegaCli/MegaCli64 ldpdinfo a0 | grep Firmware
    
which when rebuilding will show the drives that are currently rebuilding. There are clearly some other useful things, like event log management (section 7.15.1) that I need to read about and take advantage of. I was able to print the “info” events by 
    
    sudo /opt/MegaRAID/MegaCli/MegaCli64 adpeventlog getevents info –f junk.txt a0
    
which gave me all >2000 info events in the event log. 

#### Events of 2022 Feb 25

On 2022 Feb 17 a fire began north of the observatory and swept down the valley under 40-mph winds. It burned all along the river, including on the observatory grounds, but through heroic efforts by the fire-fighters none of the OVRO infrastructure was damaged. However, the power was down for several days and was restored only on 2022 Feb 22. We had problems with disks on Helios and the SQL server, but Pipeline seemed to be fine until 2022 Feb 25. On that date it suddenly began beeping to signal a disk failure. The above command to turn off the beeping was used successfully. To diagnose the problem, I successfully ran the above command to generate the text file of the event log (again named junk.txt). With the help of the command 
    
    tail -55000 junk.txt | grep -B5 State
    
I was able to list the times and description of all state changes as follows (some uninteresting lines of output have been removed): 
    
    Time: Fri Feb 25 18:14:19 2022
    Event Description: State change on PD 0c(e0x08/s4) from ONLINE(18) to FAILED(11)
    --
    Time: Fri Feb 25 18:14:19 2022
    Event Description: State change on VD 00/0 from OPTIMAL(3) to PARTIALLY DEGRADED(1)
    --
    Time: Fri Feb 25 18:14:19 2022
    Event Description: State change on VD 01/1 from OPTIMAL(3) to PARTIALLY DEGRADED(1)
    --
    Time: Fri Feb 25 18:14:19 2022
    Event Description: State change on PD 0c(e0x08/s4) from FAILED(11) to UNCONFIGURED_BAD(1)
    --
    Time: Fri Feb 25 18:14:29 2022
    Event Description: State change on PD 14(e0x08/s11) from UNCONFIGURED_GOOD(0) to REBUILD(14)
    --
    seqNum: 0x00011431
    Seconds since last reboot: 46
    Event Description: State change on PD 14(e0x08/s11) from REBUILD(14) to OFFLINE(10)
    --
    seqNum: 0x00011433
    Seconds since last reboot: 46
    Event Description: State change on PD 14(e0x08/s11) from OFFLINE(10) to REBUILD(14)
    --
    seqNum: 0x0001146e
    Seconds since last reboot: 30
    Event Description: State change on PD 14(e0x08/s11) from REBUILD(14) to OFFLINE(10)
    --
    seqNum: 0x00011470
    Seconds since last reboot: 30
    Event Description: State change on PD 14(e0x08/s11) from OFFLINE(10) to REBUILD(14)
    --
    seqNum: 0x000114a0
    Seconds since last reboot: 30
    Event Description: State change on PD 14(e0x08/s11) from REBUILD(14) to OFFLINE(10)
    --
    seqNum: 0x000114a2
    Seconds since last reboot: 30
    Event Description: State change on PD 14(e0x08/s11) from OFFLINE(10) to REBUILD(14)
    
My understanding from this sequence is that 

  * Physical Drive (PD) 0c failed at 18:14:19 UT
  * The two virtual volumes were then marked as partially degraded
  * The failed drive was marked "unconfigured_bad"
  * The Physical Drive 14 (a hot-swap drive) was automatically called into service (moved from "unconfigured_good")
  * A rebuild was initiated 10 s later.

There were several pairs of state changes from REBUILD to OFFLINE and back to REBUILD, which I believe happened later due to several reboots Owen did while trying to figure out what was wrong. 

We can assume from this that we have one failed disk (PD 0c in slot 4) and the system was working on rebuilding PD 14 in slot 11. The virtual drive state is currently optimal at --[Dgary](/wiki/index.php?title=User:Dgary&action=edit&redlink=1 "User:Dgary \(page does not exist\)") ([talk](/wiki/index.php?title=User_talk:Dgary&action=edit&redlink=1 "User talk:Dgary \(page does not exist\)")) 16:16, 27 February 2022 (UTC), and the command 
    
    sudo /opt/MegaRAID/MegaCli/MegaCli64 ldpdinfo a0 | grep Slot
    
lists the slot numbers as 0-3, then 11, then 5-10, so indeed slot 4 is skipped. We need to replace the bad disk ASAP. 

## Network Attached Storage

### Synology

We have added two larger Network Attached Storage (NAS) systems from Synology, one with six 10 TB disks and one with five 12 TB disks. This provide 50 TB and 45 TB, respectively, of RAID-5 disk space. The second Synology NAS has a lot of empty bays so I think we can extend it easily by buying more disks. 

The one purchased in 2021 (nas3) is a Synology DS3018xs 6bay NAS DiskStation (not rack mounted). 

The one purchased in 2022 (nas4) is a Synology RS2421RP+ 12bay NAS RackStation with dual power supplies. We have 7 empty bays so we can expand although I'm not sure it can be done for an existing file system--we may have to create a second filesystem that uses the other drives. 

For setup, I issued the Windows 
    
    arp -a
    
command, which gave the results 
    
    IP Address         Mac Address
    192.168.24.140     00-11-32-c4-60-4b
    192.168.24.212     90-09-d0-09-20-87
    
These are on the 1 GbE interface, and the IP address was assigned via DHCP. There are 4 possible 1 GbE interfaces, and this one is LAN 4. The other LANs have some random addresses. I do not see the 10 GbE LAN, however. It seems that the "TrendNet" card we purchased may not be compatible and we will need to purchase a compatible card. For now, we will use the LAN 4 1 GbE interface. 

Once connected to the local network (solar.pvt), I was able to run the Synology WebAssistant by going to find.synology.com in a web browser. After connecting initially, I ran the setup/update routine, which took about 10 min and involved some internal setting up of the disks. After that, a web page ccomes up with 
    
    Create your administrator account
    
asking for server name, username, and to create a new password. 

Since we already have nas1 and nas2, I use nas3 and nas4 for the server names. For nas3 I used the same username and password as for the other nas devices (see /home/user/.nascredentials on pipeline). For nas4, Big Brother thinks the username/password are too simple and required different and more complex ones (see /home/user/.nas4credentials on pipeline). 

I skipped the step asking to create a QuickConnect ID. 

After the admin user was logged in on nas3, 

  * Click the "Main Menu" icon in the upper left, then select Storage Manager.
  * Under Storage Pool click Create and drag all disks to Storage Pool 1.
  * Then under Volume click Create and select the RAID type (RAID 5), File System (ext4), and select how much capacity to use (all of it!). This created the volume with RAID 5 utilizing all of the disks. The resulting storage capacity is 45.28 TB.
  * Then in Control Panel under Shared Folder, click Create and set up a Share named nas3.

On nas4, I selected the btrfs file system, and of course I created the share name as nas4. 

In Ubuntu (18.04) on Pipeline, I created a mount point /nas3 and added the following lines to /etc/fstab 
    
    //192.168.24.140/nas3 /nas3 cifs uid=1000,gid=1000,credentials=/home/user/.nascredentials,vers=2.0,iocharset=utf8 0 0
    //192.168.24.212/nas4 /nas4 cifs uid=1000,gid=1000,credentials=/home/user/.nas4credentials,vers=2.0,iocharset=utf8 0 0
    
It turns out to be important to provide uid and gid of the "user" account, and to specify vers=2.0 (gave a cifs error 95 otherwise). 

The resulting shares /nas3 and /nas4 are then available for writing by user, but not by other users. However, it should be readable by anyone. 

### MyCloud

Due to the need for additional storage space, we have added (at this time --[Dgary](/wiki/index.php?title=User:Dgary&action=edit&redlink=1 "User:Dgary \(page does not exist\)") ([talk](/wiki/index.php?title=User_talk:Dgary&action=edit&redlink=1 "User talk:Dgary \(page does not exist\)")) 19:12, 30 October 2019 (UTC)) two MyCloud devices of 12 TB each. Both are running in RAID 1 mode, hence each provides 6 TB of storage. This documents setup and use of these devices. To interact with the two currently existing devices for setup purposes, go to their web pages (accessible only from a computer on the local solar.pvt network): 
    
    <http://192.168.24.222/>  (nas1)
    <http://192.168.24.130/>  (nas2)
    
### MyCloud Setup

To find the MyCloud on the network from the Win1 computer, open a command prompt and type 
    
    arp -a
    
This lists IP addresses and MAC addresses on the network. The two MyCloud devices are given an address automatically (DHCP) and currently are as follows: 
    
    IP Address         MAC Address         Mounted as
    192.168.24.222    00-00-c0-1d-4a-53     NAS1
    192.168.24.130    00-00-c0-1f-1f-6d     NAS2
    
When first connecting to the device webpage (e.g. <http://192.168.24.222/>), you will be asked to set an admin user. Both devices have the same password as the crios. 

The NAS2 device required a firmware update after first installation, which is accomplished simply by clicking on "update firmware." It required a couple of minutes and then automatically rebooted the device, which takes several minutes longer. 

The first thing to do is turn on NSF Service. Go to Settings/Network, scroll down to Network Services, and turn on NSF Service. Next, add a network share. From the Shares icon a screen will show a list of shares and has a folder+ button to add a new share. Click that the enter a name for the share (e.g. nas2). Then click on the new share name and turn off Public. We also want to turn on NFS Access for this share (requires the above step to turn on NSF Service, first). At the very bottom of this share's page, click the read/write icon to enable admin access. 

The final step is to mount the new share on pipeline so that it is accessible. To do this, a file ~/.nascredentials was created with the admin username and password, and an appropriate root folder was created (e.g. sudo mkdir /nas2). Then the new share mount point is appended to the /etc/fstab file, which as of this time is shown below: 
    
    # /etc/fstab: static file system information.
    #
    # Use 'blkid' to print the universally unique identifier for a
    # device; this may be used with UUID= as a more robust way to name devices
    # that works even if disks are added and removed. See fstab(5).
    #
    # <file system> <mount point>   <type>  <options>       <dump>  <pass>
    proc            /proc           proc    nodev,noexec,nosuid 0       0
    # / was on /dev/sda3 during installation
    UUID=353296c1-ec0e-4aae-9642-37cdf9c62d0e /               ext4    errors=remount-ro 0       1
    # /boot was on /dev/sda1 during installation
    UUID=d4bc9199-7ed0-4b8d-8fc1-85b0f35ad52c /boot           ext4    defaults        0       2
    # /data1 was on /dev/sdb1 during installation
    UUID=4e4fb507-76b8-42d7-a682-2a1aee3b5c7f /data1          xfs     defaults        0       2
    # swap was on /dev/sda2 during installation
    UUID=437b4082-29bd-4632-8728-be731e19c721 none            swap    sw              0       0
    /data1          /export/data1   none    bind            0       0
    # Mount dpp data disk
    192.168.24.100:/data1   /dppdata1  nfs     auto            0       0
    # Mount helios common area
    192.168.24.103:/common  /common nfs     auto            0       0
    # Mount Network Attached Storage disk
    //192.168.24.222/nas1 /nas1 cifs credentials=/home/user/.nascredentials,iocharset=utf8 0 0
    //192.168.24.130/nas2 /nas2 cifs credentials=/home/user/.nascredentials,iocharset=utf8 0 0
    
The last two lines are the ones for mounting the nas1 and nas2 shares. The command 
    
    sudo mount -a
    
will mount the shares, and of course they will also be mounted properly on each reboot. The new disk is now accessible at mount points /nas1 or /nas2. 

### Moving files to the NAS shares

Up to now, we have simply moving the older (pre-2017) raw IDB files to the NAS disks. The command to move an entire month of files, for Oct 2016 in the example below, is 
    
    sudo mv /data1/eovsa/fits/IDB/201610?? /nas2
    
This should probably be done from the screen utility since moving an entire month of files takes a long time (more than one hour?). Note that the resulting files after the move will be owned by root, but can be read by anyone. Still, if a particular day's data is to be accessed for an extended time, it is recommended to copy (not move) the files from the NAS to the standard location /data1/eovsa/fits/IDB/ and delete them when done. 

## Backing up the Computers

At present, we have not pursued a rigorous backup protocol for the computers on the site. However, we need to pay more attention to this, and we can use this link: [[1]](https://help.ubuntu.com/community/BackupYourSystem) to develop a protocol. More will be written here as that is developed. \--[Dgary](/wiki/index.php?title=User:Dgary&action=edit&redlink=1 "User:Dgary \(page does not exist\)") ([talk](/wiki/index.php?title=User_talk:Dgary&action=edit&redlink=1 "User talk:Dgary \(page does not exist\)")) 19:39, 30 November 2016 (UTC) 

Here is a useful link explaining how to backup ubuntu system with rsync [[2]](https://wiki.archlinux.org/index.php/full_system_backup_with_rsync). For this moment we use the following command to backup ovsa.njit.edu machine. 
    
    # rsync -aAXv --exclude={"/common/*","/archive/*","/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"} / /path/to/backup/folder

If any error shows up, we need to find out what wasn't copied. 
    
    # rsync -anq --exclude={"/common/*","/archive/*","/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"} / /path/to/backup/folder

Add the parameter -n to compare source and destination directories without transfering. 

Here is another useful link: [[3]](https://blog.sleeplessbeastie.eu/2012/05/08/how-to-mount-software-raid1-member-using-mdadm/) on how to mount a raid-1-member disk without its mirror. This is not really related to backups, but was needed when tawa was down and we needed access to its boot disk. 

## Steps to setup Helios

### Setup the Python environment

Install anaconda2 to /common/anaconda2. See [anaconda website](https://www.anaconda.com/download/#linux). Once having anaconda installed, add the installation path to .bashrc. 
    
    export PATH="/common/anaconda2/bin:$PATH" 
    
To link the eovsapy package to /common/python/current, a symbolic link did not work. Instead two changes were made: 
    
    mkdir /common/python/current
    sudo mount --bind /home/sched/Dropbox/PythonCode/pycode /current
    
Then add the path to .bashrc. 
    
    export PYTHONPATH="/common/python/current/:$PYTHONPATH"
    
To make this bind mount visible on nfs, add crossmnt to the /etc/exportfs file: 
    
    /common      192.168.24.90/24(rw,sync,no_root_squash,no_subtree_check,crossmnt)
    
### Install required packages with conda

Install as many requirements as possible with conda, then use pip. See [Using Pip in a Conda Environment ](https://www.anaconda.com/blog/developer-blog/using-pip-in-a-conda-environment/) for a reference. 
    
    conda install -c anaconda pip
    
### Install the rest of the required packages with pip

Use pip to install **aipy _,_**_corr'_ , and **construct'** to helios. 
    
    pip install --target=/common/python/packages/helios aipy
    pip install --target=/common/python/packages/helios corr
    pip install --target=/common/python/packages/helios --upgrade construct==2.5.0
    
If you got into an error similar to "gcc: error trying to exec 'cc1plus': execvp: No such file or directory", restall 'build-essential'. Otherwise, skip this step. 
    
    sudo apt-get update
    sudo apt-get install --reinstall build-essential
    
Add the path to .bashrc 
    
    export PYTHONPATH="/common/python/packages/helios/:$PYTHONPATH"
    
### Setup NFS (Network File System)

This step is to make the folder /common accessiable from other machines. Define the exported directory in /etc/exports, 
    
    /common      192.168.24.90/24(rw,sync,no_root_squash,no_subtree_check,crossmnt)
    /common      192.100.16.206/0(rw,sync,no_root_squash,no_subtree_check,crossmnt)
    
To mount the "pycode" permanently on "current" across the reboots, add an entry to /etc/fstab 
    
    /home/sched/Dropbox/PythonCode/pycode /common/python/current none defaults,bind 0 0
    
## Steps to setup pipeline

### Setup the Python environment

Assume that we have install anaconda2 to /common/anaconda2. Add the installation path to .bashrc. 
    
    export PATH="/common/anaconda2/bin:$PATH" 
    
Then add the eovsapy path to .bashrc. 
    
    export PYTHONPATH="/common/python/current/:$PYTHONPATH"
    
### Install the rest of the required packages with pip
    
    pip install --target=/common/python/packages/pipeline aipy
    pip install --target=/common/python/packages/pipeline sunpy==0.7.9
    pip install --target=/common/python/packages/pipeline pyodbc
    
Add the path to .bashrc 
    
    export PYTHONPATH="/common/python/packages/pipeline:$PYTHONPATH"
    
Modify the aipy package for EOVSA configuration. 
    
    cd /data1/dgary/aipy_new folder
    python setup.py install
    
Add the path to ~/.casa/init.py 
    
    sys.path.append('/common/python/packages/pipeline')
    
### Update the dependencies package in CASA

CASA ships with a few thrid party packages (NumPy, SciPy, Matplotlib). However, some essential packages in EOVSAPY and SUNCASA, e.g., aipy and SunPy, require dependencies package with a higher version. 
    
    numpy>=1.14.0. ## was 1.11.3, required by aipy
    dateutil>=2.5.0  ## was 1.5.0, required by SunPy
    
This step is to update those package to appropriate versions. In CASA prompt, 
    
    try:
        from pip import main as pipmain
    except:
        from pip._internal import main as pipmain
    pipmain(['install', '--target=/common/casa/casa-release-5.4.1-31.el6/lib/python2.7/site-packages', '--upgrade', 'numpy==1.14.3'])
    pipmain(['install', '--target=/common/casa/casa-release-5.4.1-31.el6/lib/python2.7/site-packages', '--upgrade', 'python-dateutil==2.7.5'])
    
## Steps to setup the correlator (ROACH boards)

The ROACH boards (roach1.solar.pvt, etc.) get their boot information from the ovsa.njit.edu web/gateway server. If the boards are not booting, one must first ascertain where the problem is. To communicate at the lowest level with a roach board, follow these steps: 

### Low-level Communication with a ROACH board

The boot process of a ROACH board can be monitored by connecting a serial USB cable from a USB port on the DPP to one of the ROACHes (from the USB-A connector on the DPP to the USB-B connector on the ROACH). When this is done, devices ttyUSB0 - ttyUSB3 will appear in the DPP /dev directory. To connect to a powered-on ROACH, use the command 
    
    sudo screen /dev/ttyUSB2 115200
    
but note that this will return immediately if the ROACH is powered off. This is annoying, because the boot process begins immediately upon powering the ROACH, so one must turn on the ROACH board and then issue the above command very quickly in order to see the entire boot process. To exit the screen when you are done, type ^A-k to kill the session. 

If successful, one will see the boot process begin with this: 
    
    Waiting for PHY auto negotiation to complete... done
    ENET Speed is 1000 Mbps - FULL duplex connection (EMAC0)
    BOOTP broadcast 1
    DHCP client bound to address 192.168.24.121
    Using ppc_4xx_eth0 device
    TFTP from server 192.100.16.206; our IP address is 192.168.24.121; sending through gateway 192.168.24.1
    Filename 'uImage-roach2'.
    Load address: 0x4000000
    Loading: *
    
From there, watch for error messages and deal with them accordingly. The boot information is found in the ovsa.njit.edu:/srv/tftp/ folder. Configuration information for the TFTP server is in the file ovsa.njit.edu:/etc/xinetd.d/tftp. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Computing_Systems&oldid=6605](http://ovsa.njit.edu//wiki/index.php?title=Computing_Systems&oldid=6605)"
