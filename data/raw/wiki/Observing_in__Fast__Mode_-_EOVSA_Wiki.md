# Observing in "Fast" Mode - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Observing_in_%22Fast%22_Mode
**Scraped:** 2025-08-05 09:12:45

# Observing in "Fast" Mode

From EOVSA Wiki

Jump to navigation Jump to search

# Purpose

The normal operating mode of EOVSA is to tune across the entire 1-18 GHz band (50 tunings) each second, which means taking data in a given frequency band for 20 ms (actually 19 ms after 1 ms of settling time) per second. Some solar phenomena, especially coherent emission, varies on a much shorter timescale, making it of interest to have an observing mode that repeats a given frequency with higher time resolution. Luckily, the frequency-agile nature of EOVSA allows this. 

Additionally, coherent emission can vary on much smaller frequency scales as well, making finer frequency resolution desirable when in fast mode, so this is also implemented. 

# Implementation

We have implemented a mode that we call "Fast Mode" where the system dwells on one or more bands for a larger fraction of a second and records data at a 20 ms rate during that dwell time. This is subject to the system requirement of a 1-s repetition rate, but is otherwise quite unrestricted. For example, it is possible to sit on one band for 0.8 s and then tune to 10 other bands at a 0.02 s rate to finish out the 1-s cycle, with this cycle repeating every second. Many other combinations are possible. 

## Hittite LO Command File

The first requirement of the system is the local oscillator (LO) tuning itself, which is performed by a Hittite 40 GHz signal generator. An example control file (called a frequency sequence file, or FSEQ file, which is a text file with extention .fsq) is shown below: 

    LIST:DWELL  

    0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,  

    0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,**0.8** ,  

    0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,  

    0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,  

    0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,0.01975,  

    0.01975,0.01975  

    LIST:SEQUENCE 1, 2, 5, 6, 9, 13, 19, 20, 26, 37, 51  

The first command, LIST:DWELL, gives a list of 52 durations, one for each of our possible tuning bands. Most bands have a duration of 19.75 ms, slightly less than the target 20 ms in order to account for some overhead in tuning. Note that the 20th band has a duration of 0.8 s (I have highlighted it in bold). In the actual file, the LIST:DWELL command is on a single line, but here I have broken it into lines of 10 numbers each for clarity. The second command, LIST:SEQUENCE, specifies the bands to be used in the sequence, here a roughly logarithmically spaced set of bands over the whole range, but with band 20 (the dwell band) inserted. Note that the sum of durations for these 11 bands must add to 1 s (or slightly less due to the overhead). 

## Dwell Sequence Creator

To create such DWELL sequences, a helper routine has been written in Python called make_flare_fsq() in the file make_fsq.py. The call sequence is 
    
    make_flare_fsq(dwellband, bandlist=None, acc=True, check=True, verbose=False)
    
where dwellband is the band number to dwell on and bandlist is a list of additional bands to sample. There is a default list of bands [5,6,8,11,14,18,24,31,40,52] that will be used if bandlist is None. A couple of examples follow: 
    
    make_flare_fsq(20)
    
is the simplest way to call the function, which will use the sequence [5,6,8,11,14,18,20,24,31,40,52] where band 20 is inserted into the list, and band 20 will be the DWELL band. A different set of sampling frequencies can be specified using the bandlist parameter. If fewer or greater than 10 frequencies are given in the bandlist parameter, the DWELL duration on the dwellband will be increased or decreased accordingly to make the total duration 1 s. It is possible to use only one frequency, e.g., 
    
    make_flare_fsq(20,[20])
    
would make a DWELL file with no frequency switching, remaining on band 20 for the entire 1 s duration. 

It is important to note that the name of the DWELL frequency sequence file is automatically generated with the string `DWELL` followed by the dwell band, a `+` symbol, and the number of additional frequencies in the sequence. Thus, the make_flare_seq(20) command would generate a file named DWELL20+10.fsq, written to the current directory. The FSEQ file **must** begin with the string `DWELL` or it will not trigger additional requirements discussed below. If the `acc` parameter is True (default), the file will also be automatically transferred to the ACC for use by the system. It is a good idea to set `check=True`, which checks the total number of "science channels" to be recorded does not exceed 512 (more on this below). Note that no distinction is made in the filename between one set of additional (non-dwell) frequencies and another, so if you create a sequence with DWELL band 20 and 10 other frequencies that is different from a previous one, the new file will overwrite the old one. 

It is also possible to hand modify a file to dwell on 2 bands. In the above listed file, for example, could be modified to change 0.8 for band 20 to 0.4 and the 0.01975 to 0.4 for band 2, and the system will dwell for 0.4 s on both bands 2 and 20. (This should be verified.) 

## Initiating Fast Mode

Once the sequence file exists on the ACC (in the /parm directory), it can be called from the schedule in the usual way. For example, the `FLARE.ctl` contains commands to observe the Sun and set the frequency sequence to the filename specified after the word FLARE. To use it in the schedule, adding a line 
    
    2023-05-13 20:00:00 FLARE dwell20+10.fsq
    
to solar schedule (solar.scd) would invoke that frequency sequence in Fast Mode, triggered by the leading `DWELL` string (not case sensitive). Note that the default action of the recording software is to add repeated measurements of a band, so if the same frequency sequence as above were given in a filename with a different leading string than `DWELL`, it would result in accumulating the band 20 data over 0.8 s and writing out a single set of science channels for that band, NOT the individual measurements made every 20 ms. 

## Science Channels Used in Fast Mode

The second requirement of the system is to generate a set of science channels. Each of these is accumulated over a range of subchannels among the 4096 fine subchannels available within each band. There is a standard set of science channels defined for each band, with finer spacing for bands 1-9, but a minimum set of 8 science channels for all bands above band 9. The standard set of science channels, totaled over the 50 bands, results in 451 science channels. The system can accommodate a maximum of 512 science channels numbered 0-511. To signify a channel that should be recorded in DWELL mode (i.e. should not be accumulated over repeated measurements in 1 s), 512 is added to the channel number, which makes the range 512 to 1023. In order to add channels numbered above 512, channels numbered below 512 will in general have to be reduced so as not to exceed a total of 512. That happens rather naturally as long as the dwell duration on the dwell band(s) is relatively long, thus reducing the number of additional bands that would fit in a 1-s period. 

In order to provide finer frequency resolution than normal in the dwell band, we have experimented with the system and found that the recording can keep up as long as the number of science channels in the dwell band does not exceed around 200. The default, then, is to average 16 subchannels to create one science channel, which results in 208 science channels per dwell band. That means there are only 512-208 = 304 channels available for other bands. Using two dwell bands would leave only 96 available channels. It is easily possible to create a dwell sequence that would exceed these limits, which is why the `check=True` in the call to make_flare_fsq() is a good idea, but note that editing the sequence file by hand to add a second dwell band requires some thought. 

When a sequence filename starting with `DWELL` is specified, then, the system automatically generates a corresponding set of science channels with the 208 dwell channels numbered above 511 and the standard set of non-dwell channels numbered below 512 as usual. 

## Data Recording in Fast Mode

The data recording program **dppxmp** normally creates an output measurement set in Miriad format named IDB<yyyymmddhhmmss> that is 10 min in duration and around 700 MB in size. When the program detects channel numbers higher than 511, however, it triggers the creation of a second output measurement set named XDB<yyyymmddhhmmss> that is several times larger in volume over the same 10 min duration. The output directories are /data1/IDB/ and /data1/XDB/ on the DPP computer. 

It should be noted that the dwell band channels are written to both the IDB and XDB files, i.e. channels numbered 512-1023 are simultaneously written with 20 ms resolution in the XDB file and, after subtraction of 512 from each channel number, are written to the IDB file as normal channels accumulated over all samples measured in 1 s. 

# Additional Considerations

Although we have verified that the system can successfully write the IDB and XDB files simultaneously, we have not worked out a scheme for calibrating the XDB data. A correct calibration scheme would be to observe a calibrator in the same mode as the mode used for the Sun, i.e. observe a calibrator with the same DWELL frequency sequence. It remains to be tested whether such an observation will give enough signal to get a good phase calibration, since the fine frequency channels will reduce the signal-to-noise ratio. In addition, an amplitude calibration is needed by doing a SOLPNTCAL observation on the Sun with the fast mode, and no doubt new software will be needed to properly analyze those data. Even once such calibrations are done, new ways to saving the calibration data and applying it would be needed (e.g. new SQL record types, etc.). 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Observing_in_%22Fast%22_Mode&oldid=6941](http://ovsa.njit.edu//wiki/index.php?title=Observing_in_%22Fast%22_Mode&oldid=6941)"
