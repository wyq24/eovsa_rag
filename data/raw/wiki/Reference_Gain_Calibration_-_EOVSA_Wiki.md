# Reference Gain Calibration - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Reference_Gain_Calibration
**Scraped:** 2025-08-05 09:13:24

# Reference Gain Calibration

From EOVSA Wiki

Jump to navigation Jump to search

## Procedure for Analysis

Reference complex gain calibration refers to determining the "system" amplitude and phase with high precision as a function of IF band (i.e. integrated over each 500 MHz IF band). A typical reference calibration would cover 34 bands, 2 polarizations, and 13 antennas. The routines (on pipeline machine) to retrieve and analyze the data are in the module refcal_anal.py. Start from a time range during which the reference calibration observation occurred (check the [phasecal results](http://ovsa.njit.edu/phasecal/) to see which 1-hr scan had stable phases) 
    
    import refcal_anal as ra
    from util import Time
    #example time range of the refcal scan that took place BEFORE the observation
    trange=Time(['2017-04-08T14:00','2017-04-08T15:00'])
    
Now read the data from that timerange 
    
    out=ra.rd_refcal(trange)
    
Note that there are optional arguments that can be given, such as projid='PHASECAL' (the default) and srcid='1229+060', but these are generally not needed. 

To correct for differential feed rotation (for refcal data after 05:00 UT on 2017-Jul-01), you can use: 
    
    out_corr = ra.unrot_refcal(out)
    
Take a look at the phases (averaged over each band): 
    
    ra.graph(out_corr)
    
By default it displays only bands 5, 11, 17, 23 and polarization XX. To change the bands and polarization to display, use the "bandplt" and 'pol' parameters (better to check more bands). 
    
    ra.graph(out_corr, bandplt=[5,13,19,25], pol=1)
    
Observations within this time range will be used for averaging to get the reference phases/amplitudes. Data will be flagged if the SNR is less than minsnr, which can be supplied. The default minsnr is set to 1.0. We can further determine a finer selection of time range within this scan that has clean and stable phases if needed, by setting the new timerange in "trange" below. 
    
    refcal=ra.refcal_anal(out_corr,timerange=trange,scanidx=[0])
    
It will generate four plots. First and second are phases and amplitudes of the data similar as those produced by ra.graph(), but with the selected time range for averaging highlighted (one can use "bandplt" and "pol" to choose bands and polarization to display as well). The 3rd plot is the averaged phase vs. frequency and the 4th is the averaged amplitude vs. frequency. Those data will be our "analyzed" reference calibration data saved in the returned dictionary (named "refcal" here). The dictionary contains the actual complex values (refcal['refcal']), a flag array with the same shape (refcal['flag']), and some timestamps, e.g., refcal['t_mid'] is the middle of the time range used for averaging. Both refcal['refcal'] and refcal['flag'] have a shape of (15, 2, 34) -- which corresponds to # of antennas, # of polarizations, and # of bands. 

If you determine some antenna, band, polarization need to be flagged/unflagged, they have to be manually changed in the returned refcal['flag'] array. In this example, Antenna 12 was not tracking, and the algorithm did not pick up all of them, so we have to do this manually -- setting refcal['flag'][11, :, :]=1 
    
    refcal['flag'][11]=1
    
If satisfied with the results (by looking at the plots), we can go ahead and send them to the SQL database 
    
    import cal_header as ch
    ch.refcal2sql(refcal)
    
To retrieve the refcal data back from SQL database based on, e.g., a solar data one wish to calibrate. We can provide a time: 
    
    t=Time('2017-04-07T19:40')
    refcal=ra.sql2refcal(t)
    
The resulted refcal have three keys: 'amp' (15 x 2 x 34 array), 'pha' (15 x 2 x 34 array), and 'timestamp' (in jd). The refcal data found will be the closest one PRIOR to the supplied observation time. 

## Updating the Reference Calibrations Table

The table below lists the known good reference calibrations. To facilitate adding entries to this table, do the following, where the time is after the desired refcal, but before any later refcal: 
    
    t=Time('2017-06-23T19:40')  # retrieves the refcal at 13:07 UT on that day
    refcal=ra.sql2refcal(t)
    ra.graph_results(refcal, savefigs=True)
    
This will create summary plots of the amplitude and phase, will write the two corresponding *.png files into the /common/webplots/refcal folder, and will print as a text string the lines needed to add an entry. Just cut from the terminal and paste into the wiki editor at the appropriate place to preserve time order. 

## Getting Band 4 Phase (2017-Dec-24)

[![](/wiki/images/2/2b/Band4_phase_diff.png)](/wiki/index.php/File:Band4_phase_diff.png)

[](/wiki/index.php/File:Band4_phase_diff.png "Enlarge")

**Figure 1:** LoRX - HiRX phase differences 2017-12-24. The blue points are the phase differences for common frequencies between pcal_lo_all.fsq and pcal_hi_all.fsq, for parallel feeds (XX and YY), and the orange points are the same for the crossed feeds (XY and YX). Note that the XX and XY points are identical (except at high frequencies where noise is greater), while the YY and YX points differ by what looks like a frequency-independent constant. The green curves are quadratic fits to the blue points. The phase differences, and their fits, are nearly identical on each of the 13 antennas, which was not necessarily expected. Most of the slope here is a delay difference of about 5.9 ns.

Because the refcals have up to now been done with the high-frequency receiver (HiRX) on Antenna 14, we are only measuring the reference phase on bands 5-34, even though band 4 has been present in the solar data. However, the shape of the phase vs. frequency is very regular, suggesting that if we know this shape (which could change over time, so it should be remeasured from time to time) then we can predict the Band 4 phase based on the phases of the higher bands. 

To do this, we measure the phase differences between the low-frequency receiver (LoRX) and HiRx for those frequencies that are in common. It happens that there are many frequencies in common, since the LoRX covers 1-6 GHz and the HiRX covers 3-18 GHz. In fact, the pcal_lo_all.fsq frequency sequence measures bands 1-12 (1-7 GHz) and the phases seem to be coherent from 6-7 GHz. This provides 38 frequencies in common between LoRX and HiRX, from which to determine the phase differences. 

The procedure, then, is to measure the LoRX and HiRX phases near the meridian passage of a strong calibrator (so that all of the feeds are approximately parallel and no feed-rotation-correction is needed). We first observe the source with the LoRX receiver using pcal_lo_all.fsq, and then observe the source with the HiRX receiver using pcal_hi_all.fsq. This is part of another procedure where we then rotate the Ant 14 feed by 90 degrees so that it is crossed with respect to the others. It seems that the XX and YY phases of the parallel feeds should be the same as the XY and YX phases of the crossed feeds, and therefore we should get the same phase differences in the two cases. Here is an example of obtaining the phases of such observations and plotting the phase differences, with corresponding parabolic fits: 
    
    npzfiles = ['/common/webplots/phasecal/20171224131548_1229+020.npz','/common/webplots/phasecal/20171224135049_1229+020.npz',
                '/common/webplots/phasecal/20171224142048_1229+020.npz','/common/webplots/phasecal/20171224145148_1229+020.npz']  # LoRX, HiRX, HiRX, LoRX
    import read_idb as ri
    import numpy as np
    import matplotlib.pylab as plt
    from util import common_val_idx, lobe
    outlo1 = ri.read_npz([npzfiles[0]])  # Parallel feed LoRX
    outhi1 = ri.read_npz([npzfiles[1]])  # Parallel feed HiRX
    outhi2 = ri.read_npz([npzfiles[2]])  # Crossed feed HiRX
    outlo2 = ri.read_npz([npzfiles[3]])  # Crossed feed LoRX
    phlo1 = np.angle(np.sum(outlo1['x'][ri.bl2ord[13,0:13]],3)) # Parallel LoRX phases averaged over time
    phhi1 = np.angle(np.sum(outhi1['x'][ri.bl2ord[13,0:13]],3)) # Parallel HiRx phases averaged over time
    phlo2 = np.angle(np.sum(outlo2['x'][ri.bl2ord[13,0:13]],3)) # Crossed LoRX phases averaged over time
    phhi2 = np.angle(np.sum(outhi2['x'][ri.bl2ord[13,0:13]],3)) # Crossed HiRx phases averaged over time
    idx1,idx2 = common_val_idx(outlo1['fghz'],outhi1['fghz'])  # Find common frequency indexes
    pdif1 = np.unwrap(lobe(phlo1[:,:,idx1] - phhi1[:,:,idx2]))  # Parallel phase differences at common frequencies
    pdif2 = np.unwrap(lobe(phlo2[:,:,idx1] - phhi2[:,:,idx2]))  # Crossed phase differences
    fcom = outlo1['fghz'][idx1]          # Common frequencies
    band4_fghz = outlo1['fghz'][23:31]   # Band 4 frequencies
    ps = []
    f, ax = plt.subplots(2,13)
    for i in range(13):
        for j in range(2):
            ax[j,i].cla()
            ax[j,i].plot(fcom,pdif1[i,j],'.')     # Plot parallel XX, YY phase differences
            ax[j,i].plot(fcom,pdif2[i,j+2],'.')   # Plot crossed XY, YX phase differences
            ax[j,i].set_ylim(-1,11)
            ps.append(np.polyfit(fcom,pdif1[i,j],2))
            ax[j,i].plot(fcom,np.polyval(ps[-1],fcom),'-')
    
The resulting plot is shown in **Figure 1** above. Curiously, the XX and YY phase differences (blue points) differ by about -0.5 radians, while the XX and YX phase differences (blue in top row vs. orange in bottom row) differ by +0.5 radians. Meanwhile, the XX and XY phase differences are essentially identical. This relates to the X vs. Y delays in some manner that has yet to be understood. 

The phase differences can be extrapolated to the band4 phases by 
    
    for p in np.array(ps)[::2]:
        print ('{:8.2f}'*8).format(*np.polyval(p,band4_fghz))
    
    for p in np.array(ps)[1::2]:
        print ('{:8.2f}'*8).format(*np.polyval(p,band4_fghz))
    
which results in the following tables (I put the headings in by hand): 
    
     XX Phase Differences for Band 4
        2.87    2.89    2.90    2.92    2.94    2.96    2.97    3.00
       ------  ------  ------  ------  ------  ------  ------  ------
    1  -0.596  -0.562  -0.528  -0.494  -0.460  -0.426  -0.392  -0.358
    2  -0.574  -0.541  -0.508  -0.475  -0.442  -0.408  -0.375  -0.341
    3  -0.567  -0.535  -0.502  -0.469  -0.436  -0.403  -0.370  -0.337
    4  -0.617  -0.583  -0.549  -0.514  -0.479  -0.444  -0.409  -0.374
    5  -0.664  -0.629  -0.594  -0.559  -0.523  -0.488  -0.452  -0.416
    6  -0.653  -0.619  -0.584  -0.549  -0.514  -0.479  -0.444  -0.409
    7  -0.593  -0.558  -0.524  -0.489  -0.454  -0.419  -0.384  -0.349
    8  -0.565  -0.532  -0.499  -0.466  -0.433  -0.399  -0.366  -0.332
    9  -0.720  -0.686  -0.651  -0.617  -0.582  -0.548  -0.513  -0.478
    10 -0.542  -0.510  -0.478  -0.446  -0.413  -0.381  -0.348  -0.315
    11 -0.660  -0.626  -0.591  -0.557  -0.522  -0.487  -0.452  -0.417
    12 -0.521  -0.490  -0.460  -0.429  -0.397  -0.366  -0.335  -0.303
    13 -0.793  -0.753  -0.714  -0.674  -0.634  -0.595  -0.555  -0.515
    
     YY Phase Differences for Band 4
        2.87    2.89    2.90    2.92    2.94    2.96    2.97    3.00
       ------  ------  ------  ------  ------  ------  ------  ------
    1  -1.016  -0.980  -0.944  -0.909  -0.873  -0.837  -0.801  -0.765
    2  -0.988  -0.952  -0.916  -0.880  -0.844  -0.808  -0.772  -0.736
    3  -1.012  -0.977  -0.942  -0.906  -0.871  -0.836  -0.800  -0.765
    4  -1.008  -0.973  -0.939  -0.904  -0.869  -0.834  -0.799  -0.764
    5  -1.065  -1.027  -0.990  -0.953  -0.916  -0.878  -0.841  -0.803
    6  -0.924  -0.890  -0.856  -0.823  -0.789  -0.755  -0.721  -0.687
    7  -0.584  -0.561  -0.538  -0.515  -0.492  -0.468  -0.444  -0.420
    8  -1.038  -1.003  -0.967  -0.931  -0.895  -0.859  -0.823  -0.787
    9  -1.079  -1.045  -1.010  -0.975  -0.939  -0.904  -0.869  -0.834
    10 -1.155  -1.117  -1.079  -1.041  -1.003  -0.964  -0.926  -0.888
    11 -1.046  -1.010  -0.975  -0.939  -0.903  -0.867  -0.831  -0.795
    12 -0.781  -0.750  -0.719  -0.688  -0.657  -0.625  -0.594  -0.562
    13 -1.163  -1.123  -1.082  -1.042  -1.001  -0.960  -0.919  -0.879
    
### Implementation in refcal_anal.py (2018-Mar-05)

[![](/wiki/images/a/a1/Delay_curve.png)](/wiki/index.php/File:Delay_curve.png)

[](/wiki/index.php/File:Delay_curve.png "Enlarge")

**Figure 2:** The band-averaged phase differences in high-frequency bands between 2018-02-05 and 2018-02-07 (reference day). The orange line is a linear fit to the points, forced to pass through (0,0). The green points are the fit values for band 4, which are used to estimate this day's (2018-02-05) band 4 phases. Note that the scatter in ant 6 was because it was not tracking that day.

The refcal_anal.py routine has been updated to include the band-averaged band 4 phase calibration. This implementation has the following two components. 

    **1.** On the day we take the measurements with the above-mentioned LoRX-HiRX observation sequence: It calculates the phase differences between low-frequency and high-frequency measurements over bands 5 - 10, extrapolate it to band 4, and subtract this extrapolated difference from the actual band 4 phases measured by low-frequency receiver to obtain the "reference band 4 phases" as if they were measured by high-frequency receiver. This have to be saved in the SQL database with the special keyword **lohi=True**.

    **2.** On regular days when we do NOT take measurements with LoRX: It calculates the "estimated band 4 phases" using the closest earlier reference band 4 phases calculated in step #1. First, it calculates the phase differences in high-frequency bands between the target day and the reference day (a "delay curve"). This should be fit with a linear curve passing through zeros like in **Figure 2**. We use this fit to obtain the phase difference in band 4 between the target day and the reference day. Knowing the "reference band 4 phases" from #1, we estimate the band 4 phases on arbitrary day.

To do the first task of saving reference refcal, follow the example lines of code below (in pipeline): 
    
    from util import Time
    import refcal_anal as ra
    trange = Time(['2018-03-06T09:30','2018-03-06T10:30']) #has to contain LoRX and HiRX scans
    out = ra.rd_refcal(trange)
    out_corr = ra.unrot_refcal(out)
    refcal = ra.refcal_anal(out_corr, timerange=Time(['2018-03-06 09:30','2018-03-06 10:00']), lohi=True) #timerange has to specify **only HiRX scan**
    import cal_header as ch
    ch.refcal2sql(refcal, lohi=True) #save to SQL
    
The last plot created will have the calculated band 4 phases added to the usual refcal phase summary plot. There is no special keyword needed for the second task - the routine now automatically calculates the estimated band 4 phases for every refcal, and produces a new plot showing the delay curve like Figure 2, calculated with respect to the most recent reference refcal. If this delay curve starts to show large scatters, it is likely that we need a new LoHi scan to obtain the new reference refcal. It is also important to note that the new reference refcal is needed **after every delay center reset** , since resetting the delay center introduces some offsets in delay curves and therefore causes the band 4 estimation algorithm to fail. 

The estimated band 4 phase errors from this algorithm is currently ~20 degrees. We also would like to eventually obtain the phases at every frequencies instead of band-averaged values. 

#### List of Saved Reference Refcals
    
    2017-12-24 14:06:50.000
    2018-02-07 11:00:48.000
    2018-02-22 10:46:51.000
    2018-03-06 09:46:48.000
    2018-03-07 20:04:50.000
    
## List of Analyzed Reference Calibrations

}  Date | Timestamp | Source | Obs Trange | Scan Idx | Avg Trange | Bands | Phase Plot | Amp Plot | Comments   
---|---|---|---|---|---|---|---|---|---  
2017/04/02 | 06:36:50 | 3c273 | 04:20~11:00 | All | 05:47~07:26 | 5, 7, 9, 11, 13, 15, 17, 19, 21, 23 | [Phase](/wiki/index.php/File:20170402_refcal_pha.png "File:20170402 refcal pha.png") | [Amp](/wiki/index.php/File:20170402_refcal_amp.png "File:20170402 refcal amp.png") | Ant 12 was not tracking. Delay center change at 11:38:17.   
2017/04/04 | 09:32:50 | 3c273 | 04:43~10:57 | All | 08:46~10:19 | 5, 7, 9, 11, 13, 15, 17, 19, 21, 23 | [Phase](/wiki/index.php/File:20170404_refcal_pha.png "File:20170404 refcal pha.png") | [Amp](/wiki/index.php/File:20170404_refcal_amp.png "File:20170404 refcal amp.png") | Ant 12 was not tracking. Delay center change at 16:43:51.   
2017/04/05 | 06:44:10 | 3c273 | 04:17~10:30 | All | 04:27~09:34 | 5, 7, 9, 11, 13, 15, 17, 19, 21, 23 | [Phase](/wiki/index.php/File:20170405_refcal_pha.png "File:20170405 refcal pha.png") | [Amp](/wiki/index.php/File:20170405_refcal_amp.png "File:20170405 refcal amp.png") | Ant 12 was not tracking.   
2017/04/06 | 09:54:50 | 3c273 | 04:14~10:49 | All | 05:39~08:11 | 5, 7, 9, 11, 13, 15, 17, 19, 21, 23 | [Phase](/wiki/index.php/File:20170406_refcal_pha.png "File:20170406 refcal pha.png") | [Amp](/wiki/index.php/File:20170406_refcal_amp.png "File:20170406 refcal amp.png") | Ant 12 was not tracking.   
2017/04/07 | 08:30:51 | 3c273 | 04:00~10:30 | 1, 3, 5, 7, 9, 11, 13, 15, 17 | 07:53~09:10 | 5~34 | [Phase](/wiki/index.php/File:20170407_refcal_pha.png "File:20170407 refcal pha.png") | [Amp](/wiki/index.php/File:20170407_refcal_amp.png "File:20170407 refcal amp.png") | Ant 12 was not tracking.   
2017/04/08 | 06:14:51 | 3c273 | 05:00~10:30 | 1, 3, 5, 7, 9, 11, 13 | 05:00~07:00 | 5~34 | [Phase](/wiki/index.php/File:20170408_refcal_pha.png "File:20170408 refcal pha.png") | [Amp](/wiki/index.php/File:20170408_refcal_amp.png "File:20170408 refcal amp.png") | Ant 12 was not tracking. Ant 13 not working. Delay center change at 2017-04-08T03:12:26. Another refcal record is added at 2017-04-09T06:14:45.   
2017/04/10 | 06:57:10 | 3c273 | 04:30~10:30 | 2, 6, 8 |  | 5~34 | [Phase](/wiki/index.php/File:20170410_refcal_pha.png "File:20170410 refcal pha.png") | [Amp](/wiki/index.php/File:20170410_refcal_amp.png "File:20170410 refcal amp.png") | Ant 12 was not tracking. Delay center change at 2017-04-08 13:20:39.   
2017/04/13 | 13:48:39 | 2136+006 |  | 0 |  | 5~23 | [Phase](http://ovsa.njit.edu/refcal/20170413_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170413_refcal_amp.png) |   
2017/04/16 | 06:36:48 | 3c273 | 03:00~11:00 |  | 05:55~07:20 | 5~34 | [Phase](/wiki/index.php/File:20170416_refcal_pha.png "File:20170416 refcal pha.png") | [Amp](/wiki/index.php/File:20170416_refcal_amp.png "File:20170416 refcal amp.png") | Ant 12 was not tracking.   
2017/04/17 | 06:41:51 | 3c273 | 03:29~10:07 | All | 05:55~07:29 | 5~34 | [Phase](/wiki/index.php/File:20170417_refcal_pha.png "File:20170417 refcal pha.png") | [Amp](/wiki/index.php/File:20170417_refcal_amp.png "File:20170417 refcal amp.png") | Ant 12 was not tracking. Delay center change at 19:12:58.   
2017/04/26 | 08:06:52 | 3c273 | 02:50~09:28 | All | 07:21~08:57 | 5~34 | [Phase](/wiki/index.php/File:20170426_refcal_pha.png "File:20170426 refcal pha.png") | [Amp](/wiki/index.php/File:20170426_refcal_amp.png "File:20170426 refcal amp.png") | Ant 12 was not tracking. Delay center change at 04:37:28 and 11:51:26.   
2017/06/11 | 12:56:22 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170611_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170611_refcal_amp.png) | No calibration for: Ant 12   
2017/06/14 | 02:33:19 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170614_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170614_refcal_amp.png) | No calibration for: Ant 8 Ant 12   
2017/06/14 | 13:01:19 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170614_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170614_refcal_amp.png) | No calibration for: Ant 12   
2017/06/15 | 13:05:48 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170615_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170615_refcal_amp.png) | No calibration for: Ant 12   
2017/06/16 | 13:05:48 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170616_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170616_refcal_amp.png) | No calibration for: Ant 12   
2017/06/20 | 13:06:26 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170620_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170620_refcal_amp.png) | No calibration for: Ant 1 Ant 12   
2017/06/21 | 13:06:38 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170621_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170621_refcal_amp.png) | No calibration for: Ant 12   
2017/06/22 | 13:06:53 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170622_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170622_refcal_amp.png) | No calibration for: Ant 12   
2017/06/23 | 13:07:09 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170623_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170623_refcal_amp.png) | No calibration for: Ant 12   
2017/06/24 | 02:25:49 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170624_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170624_refcal_amp.png) | No calibration for: Ant 12   
2017/06/24 | 13:07:25 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170624_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170624_refcal_amp.png) | No calibration for: Ant 12   
2017/06/25 | 13:07:43 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170625_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170625_refcal_amp.png) | No calibration for: Ant 10 Ant 12   
2017/06/26 | 13:15:47 |  |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170626_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170626_refcal_amp.png) | No calibration for: Ant 10 Ant 12   
2017/06/27 | 13:02:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170627_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170627_refcal_amp.png) | No calibration for: Ant 12   
2017/06/30 | 02:47:50 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170630_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170630_refcal_amp.png) | No calibration for: Ant 12   
2017/07/01 | 02:44:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170701_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170701_refcal_amp.png) | No calibration for: Ant 12   
2017/07/02 | 03:01:20 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170702_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170702_refcal_amp.png) |   
2017/07/03 | 02:47:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170703_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170703_refcal_amp.png) | No calibration for: Ant 10   
2017/07/04 | 02:47:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170704_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170704_refcal_amp.png) |   
2017/07/05 | 02:55:19 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170705_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170705_refcal_amp.png) |   
2017/07/06 | 02:47:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170706_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170706_refcal_amp.png) |   
2017/07/07 | 13:12:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170707_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170707_refcal_amp.png) |   
2017/07/09 | 02:35:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170709_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170709_refcal_amp.png) |   
2017/07/09 | 13:16:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170709_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170709_refcal_amp.png) |   
2017/07/10 | 13:14:17 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170710_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170710_refcal_amp.png) |   
2017/07/11 | 13:14:18 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170711_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170711_refcal_amp.png) |   
2017/07/12 | 13:14:24 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170712_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170712_refcal_amp.png) |   
2017/07/13 | 13:14:59 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170713_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170713_refcal_amp.png) |   
2017/07/14 | 13:15:35 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170714_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170714_refcal_amp.png) |   
2017/07/16 | 02:48:33 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170716_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170716_refcal_amp.png) |   
2017/07/16 | 13:16:48 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170716_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170716_refcal_amp.png) |   
2017/07/17 | 13:14:54 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170717_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170717_refcal_amp.png) |   
2017/07/18 | 13:15:31 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170718_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170718_refcal_amp.png) |   
2017/07/19 | 13:16:16 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170719_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170719_refcal_amp.png) |   
2017/07/20 | 13:16:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170720_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170720_refcal_amp.png) | No calibration for: Ant 10   
2017/07/21 | 13:20:57 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170721_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170721_refcal_amp.png) |   
2017/07/22 | 13:21:36 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170722_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170722_refcal_amp.png) |   
2017/07/23 | 13:34:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170723_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170723_refcal_amp.png) |   
2017/07/24 | 13:22:58 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170724_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170724_refcal_amp.png) |   
2017/07/25 | 13:23:38 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170725_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170725_refcal_amp.png) |   
2017/07/26 | 18:00:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170726_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170726_refcal_amp.png) |   
2017/07/28 | 02:42:36 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170728_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170728_refcal_amp.png) |   
2017/07/29 | 13:37:40 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170729_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170729_refcal_amp.png) |   
2017/07/31 | 13:27:05 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170731_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170731_refcal_amp.png) |   
2017/08/01 | 13:28:30 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170801_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170801_refcal_amp.png) |   
2017/08/02 | 13:29:13 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170802_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170802_refcal_amp.png) |   
2017/08/03 | 13:29:59 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170803_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170803_refcal_amp.png) |   
2017/08/05 | 02:35:58 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170805_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170805_refcal_amp.png) |   
2017/08/05 | 13:31:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170805_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170805_refcal_amp.png) |   
2017/08/06 | 13:32:06 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170806_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170806_refcal_amp.png) |   
2017/08/07 | 13:32:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170807_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170807_refcal_amp.png) |   
2017/08/08 | 13:33:33 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170808_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170808_refcal_amp.png) |   
2017/08/11 | 12:47:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170811_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170811_refcal_amp.png) |   
2017/08/12 | 12:43:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170812_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170812_refcal_amp.png) | No calibration for: Ant 9   
2017/08/13 | 12:39:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170813_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170813_refcal_amp.png) |   
2017/08/14 | 12:34:19 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170814_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170814_refcal_amp.png) |   
2017/08/15 | 12:31:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170815_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170815_refcal_amp.png) |   
2017/08/16 | 12:27:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170816_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170816_refcal_amp.png) |   
2017/08/17 | 12:23:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170817_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170817_refcal_amp.png) |   
2017/08/18 | 12:19:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170818_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170818_refcal_amp.png) |   
2017/08/19 | 12:15:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170819_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170819_refcal_amp.png) |   
2017/08/21 | 12:07:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170821_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170821_refcal_amp.png) |   
2017/08/22 | 12:03:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170822_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170822_refcal_amp.png) |   
2017/08/23 | 12:14:51 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170823_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170823_refcal_amp.png) |   
2017/08/24 | 11:55:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170824_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170824_refcal_amp.png) |   
2017/08/25 | 14:01:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170825_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170825_refcal_amp.png) |   
2017/08/26 | 13:57:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170826_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170826_refcal_amp.png) |   
2017/08/28 | 01:03:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170828_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170828_refcal_amp.png) |   
2017/08/29 | 00:59:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170829_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170829_refcal_amp.png) |   
2017/08/29 | 13:49:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170829_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170829_refcal_amp.png) |   
2017/08/30 | 13:49:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170830_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170830_refcal_amp.png) |   
2017/08/31 | 13:50:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170831_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170831_refcal_amp.png) |   
2017/09/01 | 13:51:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170901_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170901_refcal_amp.png) |   
2017/09/02 | 13:52:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170902_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170902_refcal_amp.png) |   
2017/09/03 | 13:53:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170903_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170903_refcal_amp.png) |   
2017/09/04 | 13:54:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170904_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170904_refcal_amp.png) |   
2017/09/05 | 13:54:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170905_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170905_refcal_amp.png) |   
2017/09/06 | 13:55:58 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170906_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170906_refcal_amp.png) |   
2017/09/07 | 13:56:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170907_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170907_refcal_amp.png) |   
2017/09/08 | 13:56:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170908_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170908_refcal_amp.png) |   
2017/09/10 | 00:01:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170910_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170910_refcal_amp.png) |   
2017/09/10 | 13:57:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170910_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170910_refcal_amp.png) |   
2017/09/11 | 13:58:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170911_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170911_refcal_amp.png) |   
2017/09/12 | 14:00:11 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170912_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170912_refcal_amp.png) |   
2017/09/14 | 04:15:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170914_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170914_refcal_amp.png) | Refcal at around 14 UT is also good.   
2017/09/14 | 14:01:48 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170914_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170914_refcal_amp.png) |   
2017/09/15 | 14:39:27 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170915_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170915_refcal_amp.png) |   
2017/09/16 | 13:46:56 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170916_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170916_refcal_amp.png) |   
2017/09/17 | 13:47:46 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170917_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170917_refcal_amp.png) |   
2017/09/18 | 14:05:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170918_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170918_refcal_amp.png) |   
2017/09/19 | 14:06:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170919_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170919_refcal_amp.png) |   
2017/09/22 | 14:08:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170922_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170922_refcal_amp.png) |   
2017/09/23 | 14:09:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170923_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170923_refcal_amp.png) |   
2017/09/24 | 14:10:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170924_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170924_refcal_amp.png) |   
2017/09/25 | 14:17:33 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170925_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170925_refcal_amp.png) |   
2017/09/26 | 14:10:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170926_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170926_refcal_amp.png) |   
2017/09/27 | 14:06:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170927_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170927_refcal_amp.png) |   
2017/09/28 | 14:02:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170928_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170928_refcal_amp.png) |   
2017/09/29 | 14:01:20 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170929_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170929_refcal_amp.png) |   
2017/09/30 | 13:54:50 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20170930_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20170930_refcal_amp.png) |   
2017/10/01 | 13:50:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171001_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171001_refcal_amp.png) |   
2017/10/02 | 13:47:28 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171002_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171002_refcal_amp.png) |   
2017/10/03 | 13:43:25 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171003_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171003_refcal_amp.png) |   
2017/10/04 | 13:40:52 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171004_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171004_refcal_amp.png) | No calibration for: Ant 10   
2017/10/06 | 02:42:39 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171006_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171006_refcal_amp.png) |   
2017/10/06 | 13:32:53 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171006_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171006_refcal_amp.png) |   
2017/10/07 | 13:30:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171007_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171007_refcal_amp.png) |   
2017/10/08 | 13:26:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171008_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171008_refcal_amp.png) |   
2017/10/10 | 02:31:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171010_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171010_refcal_amp.png) |   
2017/10/11 | 02:23:50 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171011_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171011_refcal_amp.png) | No calibration for: Ant 12   
2017/10/12 | 02:19:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171012_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171012_refcal_amp.png) | No calibration for: Ant 12   
2017/10/13 | 02:15:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171013_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171013_refcal_amp.png) | No calibration for: Ant 12   
2017/10/13 | 12:54:23 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171013_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171013_refcal_amp.png) | No calibration for: Ant 12   
2017/10/14 | 12:50:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171014_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171014_refcal_amp.png) | No calibration for: Ant 12   
2017/10/16 | 02:07:50 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171016_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171016_refcal_amp.png) | No calibration for: Ant 12   
2017/10/18 | 01:59:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171018_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171018_refcal_amp.png) | No calibration for: Ant 12   
2017/10/19 | 12:30:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171019_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171019_refcal_amp.png) | No calibration for: Ant 12   
2017/10/20 | 12:22:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171021_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171021_refcal_amp.png) |   
2017/10/21 | 12:22:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171021_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171021_refcal_amp.png) |   
2017/10/22 | 12:18:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171022_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171022_refcal_amp.png) |   
2017/10/24 | 12:10:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171024_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171024_refcal_amp.png) | Few frequencies have unusually high amplitudes.   
2017/10/24 | 01:35:50 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171024_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171024_refcal_amp.png) |   
2017/10/25 | 01:31:50 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171025_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171025_refcal_amp.png) |   
2017/10/26 | 12:02:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171026_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171026_refcal_amp.png) |   
2017/10/27 | 11:58:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171027_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171027_refcal_amp.png) |   
2017/10/28 | 11:54:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171028_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171028_refcal_amp.png) |   
2017/10/29 | 11:50:22 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171029_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171029_refcal_amp.png) | Ant 8 was down.   
2017/11/02 | 14:50:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171102_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171102_refcal_amp.png) | No calibration for: Ant 3   
2017/11/03 | 14:52:20 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171103_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171103_refcal_amp.png) | No calibration for: Ant 3   
2017/11/04 | 14:53:51 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171104_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171104_refcal_amp.png) | No calibration for: Ant 3   
2017/11/05 | 14:54:50 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171105_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171105_refcal_amp.png) | Ant 3 was down. No calibration for: Ant 3   
2017/11/07 | 00:39:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171107_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171107_00_refcal_amp.png) |   
2017/11/07 | 14:56:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171107_14_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171107_14_refcal_amp.png) | No calibration for: Ant 3   
2017/11/08 | 14:57:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171108_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171108_refcal_amp.png) | No calibration for: Ant 3   
2017/11/09 | 14:58:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171109_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171109_refcal_amp.png) | No calibration for: Ant 3   
2017/11/10 | 15:00:50 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171110_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171110_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/12 | 00:22:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171112_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171112_00_refcal_amp.png) | No calibration for: Ant 3   
2017/11/12 | 15:02:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171112_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171112_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/15 | 00:12:50 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171115_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171115_00_refcal_amp.png) | No calibration for: Ant 3   
2017/11/15 | 15:07:00 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171115_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171115_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/16 | 15:08:14 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171116_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171116_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/17 | 15:09:29 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171117_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171117_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/19 | 00:13:26 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171119_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171119_00_refcal_amp.png) | No calibration for: Ant 3   
2017/11/19 | 15:11:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171119_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171119_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/21 | 00:11:50 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171121_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171121_00_refcal_amp.png) | No calibration for: Ant 3   
2017/11/22 | 00:10:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171122_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171122_00_refcal_amp.png) | No calibration for: Ant 3   
2017/11/22 | 15:15:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171122_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171122_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/23 | 15:16:50 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171123_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171123_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/24 | 15:18:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171124_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171124_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/25 | 15:19:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171125_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171125_15_refcal_amp.png) | No calibration for: Ant 3   
2017/11/26 | 15:20:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171126_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171126_15_refcal_amp.png) | No calibration for: Ant 3   
2017/12/03 | 00:05:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171203_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171203_00_refcal_amp.png) |   
2017/12/04 | 15:29:13 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171204_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171204_15_refcal_amp.png) | No calibration on Ant 3 and 6   
2017/12/06 | 00:05:14 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171206_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171206_00_refcal_amp.png) | First refcal on 2017-12-05 is bad. No Ant3 calibration.   
2017/12/07 | 00:05:06 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171207_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171207_00_refcal_amp.png) | First refcal on 2017-12-06 had Windscram. No Ant3 calibration.   
2017/12/07 | 15:32:07 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171207_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171207_15_refcal_amp.png) | No Ant 3 calibration.   
2017/12/08 | 15:33:05 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171208_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171208_15_refcal_amp.png) | No Ant3 calibration.   
2017/12/13 | 15:37:19 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171213_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171213_15_refcal_amp.png) |   
2017/12/18 | 00:06:26 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171218_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171218_00_refcal_amp.png) | No calibration for: Ant 4   
2017/12/18 | 15:40:50 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171218_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171218_15_refcal_amp.png) | No calibration for: Ant 4 Ant 6   
2017/12/19 | 23:57:49 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171219_23_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171219_23_refcal_amp.png) |   
2017/12/22 | 15:27:55 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171222_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171222_15_refcal_amp.png) |   
2017/12/23 | 15:43:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171223_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171223_15_refcal_amp.png) |   
2017/12/24 | 15:42:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171224_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171224_15_refcal_amp.png) |   
2017/12/25 | 15:44:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171225_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171225_15_refcal_amp.png) |   
2017/12/27 | 00:10:50 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171227_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171227_00_refcal_amp.png) |   
2017/12/27 | 15:44:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171227_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171227_15_refcal_amp.png) |   
2017/12/28 | 15:44:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171228_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171228_15_refcal_amp.png) |   
2017/12/29 | 15:45:50 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171229_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171229_15_refcal_amp.png) |   
2017/12/30 | 15:44:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171230_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171230_15_refcal_amp.png) |   
2017/12/31 | 15:45:50 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20171231_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20171231_15_refcal_amp.png) |   
2018/01/01 | 15:45:32 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180101_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180101_15_refcal_amp.png) | No calibration on Ant 6   
2018/01/02 | 15:45:32 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180102_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180102_15_refcal_amp.png) |   
2018/01/04 | 00:17:48 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180104_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180104_00_refcal_amp.png) |   
2018/01/04 | 15:45:31 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180104_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180104_15_refcal_amp.png) |   
2018/01/06 | 00:19:45 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180106_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180106_00_refcal_amp.png) |   
2018/01/07 | 15:45:08 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180107_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180107_15_refcal_amp.png) |   
2018/01/08 | 15:44:57 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180108_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180108_15_refcal_amp.png) |   
2018/01/10 | 00:23:57 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180110_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180110_00_refcal_amp.png) |   
2018/01/15 | 15:42:19 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180115_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180115_15_refcal_amp.png) |   
2018/01/16 | 15:41:49 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180116_15_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180116_15_refcal_amp.png) |   
2018/01/24 | 00:34:04 | 2253+161 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180124_00_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180124_00_refcal_amp.png) |   
2018/02/13 | 01:04:49 | 0319+415 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180213_01_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180213_01_refcal_amp.png) |   
2018/02/13 | 14:07:50 | 1229+020 |  | 0 |  | 5~34 | [Phase](http://ovsa.njit.edu/refcal/20180213_14_refcal_pha.png) | [Amp](http://ovsa.njit.edu/refcal/20180213_14_refcal_amp.png) |   
  
Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Reference_Gain_Calibration&oldid=2337](http://ovsa.njit.edu//wiki/index.php?title=Reference_Gain_Calibration&oldid=2337)"
