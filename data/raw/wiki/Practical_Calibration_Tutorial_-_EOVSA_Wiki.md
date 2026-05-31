# Practical Calibration Tutorial - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Practical_Calibration_Tutorial
**Scraped:** 2025-08-05 09:13:34

# Practical Calibration Tutorial

From EOVSA Wiki

Jump to navigation Jump to search

This page is a practical tutorial for calibrating EOVSA data. Note currently the calibration processes can only be done on EOVSA site machines (such as pipeline), as the calibration SQL database is only available there. 

## Preparation

First, identify whether or not EOVSA had the observation for the time range of the event (e.g., a flare). There are many ways to do this, but a nice way is to use the [RHESSI Browser](http://sprg.ssl.berkeley.edu/~tohban/browser/) and check "EOVSA Radio Data" on the upper left. Use the time you identified to find the corresponding IDB file(s) under /data1/eovsa/fits/IDB/yyyymmdd/. *Typically*, each IDB data file has a 10-minute duration. Then, on pipeline, it is advised to go to your own directory and work under there. Note, **never, NEVER, work directly on the IDB data in the original data directory!** Here I use a 10-min duration data on 2017 Aug 21 (which has a C flare) as an example. 

## Check Status of Calibration Products

Check [the calibration status page](http://ovsa.njit.edu/EOVSA/cal_status.php) for status of the calibration products. Navigate to the date of interest and check the numbers under "r" (reference phase), "p" (daily phase calibration), and "tp" (total-power and attenuation calibration). "1" means the respective calibration product already exists. "0" means otherwise. 

## Reference Calibration and Phase Calibration

If the calibration does not exist for a particular day (i.e., "0"), and if you know what you are doing, run the following line on pipeline: 
    
    python /common/python/current/calwidget.py &
    
Here are some instructions (more will be added with graphics) The calibration widget allows combining the low frequency receiver (1-6 GHz) with the high frequency receiver (3-18), so every morning and evening we first do a 20-min scan with low and then 60-min with high receiver. 

\- To create a single refcal from these, select each of one pair separately and do any flagging they need. 

\- To do time flagging, point to the time plot you want to flag and use key “a” to start an interval, “b” to end it. You can select two independent intervals. If you want to change a line you just made, use key “x” to erase it. To kill an entire band for one antenna, set the interval to cover the whole time range. You can also apply a given interval to all antennas for a given band, or all bands for a given antenna, by selecting the appropriate check box. 

\- Once the data are flagged, the sigma map will update and hopefully turn blue for that box. Keep going until all boxes are blue if possible. 

\- Finally, select one of the pair of refcal scans you have flagged and select “set as refcal.” That will cause the “extend selection” button to be available. Click that and then highlight the other of the hi-low pair. The “set as refcal” button will change to “set as extended refcal.” Click that, and the pair will be merged (you’ll see the sigma map update to show all bands, although we do not observe bands 3 & 4, so they will remain yellow). Finally, click the save to SQL button. 

\- Use the morning refcal if possible, but if it is not good then use the evening one. You only need one. If you do use the evening one, say yes when the “save to SQL” asks about changing the time, and then save it to an early time, like 13:00 UT. 

\- After that is done, analyze each of the other scans as phasecal, including the unused refcal. To see how “good” the phasecal is, select the “sum phase” tab. Good antennas will show a nice linear fit. When the data are noisy, the phase unwrap doesn’t work well. To fix that, one has to identify the band of the bad point and flag all times for that antenna and band. Sometimes one has to kill several points, which is fine. When each phasecal is okay, save it to SQL. Generally doing this would not hurt anything, because this just writes records to the SQL database, which can be replaced or updated by reanalyzing. 

## Total-Power and Attenuation Calibration

[![](/wiki/images/d/d9/Fig-tp_calqual.png)](/wiki/index.php/File:Fig-tp_calqual.png)

[](/wiki/index.php/File:Fig-tp_calqual.png "Enlarge")

Checking total-power calibration quality

As introduced in [ this page](/wiki/index.php/Total_Power_Calibration "Total Power Calibration"), the total-power and absolute flux calibration is done by comparing with RSTN daily radio flux density measurements. It is always a good idea to check the quality of the calibration. To do that, first, start IPython in your working directory. Here I am loading all pylab modules (I know this is not a good way, but simple). 
    
    ipython --pylab
    
Check the quality of the absolute flux (total power) calibration for the particular day 
    
    from util import Time
    import daily_xsp
    daily_xsp.cal_qual(Time('2017-08-21'))
    
This command will apply attenuation calibration and feed rotation from the database to total-power gain calibration data, and display a figure on the right showing the calibrated total-power spectrum on all antennas and all polarizations. The first scan on the figure is done with the array dwelling on the Sun and stepping through different attenuator levels. The second and third scans are done by moving across the solar disk. A perfect calibration would achieve something similar to the RSTN flux for all antennas and all polarizations. This is not always the case, however. But it helps us to evaluate the quality of the absolute gain calibration. 

If the calibration is deemed not satisfactory, one could go back and re-generate the attenuator gain calibration (perhaps it was not generated in the first place). This can be done by running the following command on pipeline (you need to change the date for your desired data) 
    
    python /common/python/current/calibration.py '2017-08-21 21:36'
    
Note the time used here (21:36). Typically, two calibrations are done on 17:30/18:30 and 21:30. Each calibration takes about 5 min. The time selection indicates that we use the second calibration, and make sure that we wait until the second calibration is done. 

## Apply All Calibrations to Visibility Data

Start CASA in your working directory (e.g., /data1/bchen/). To start CASA, use: 
    
    casa
    
### importeovsa

The level 0 visilibity data is in Miriad format (IDB). We should import IDB data into CASA Measurement Set so that we can process the data in CASA. By default, we apply the total power and attenuation calibrations at this stage (via keyword "udb_corr = True"). Multiprocessing can be enabled by setting ncpu = [a number > 1 but < # of available threads]. 
    
    from astropy.time import Time
    import os
    trange = Time(['2017-08-21 20:15:00', '2017-08-21 20:25:00'])
    #### (Optional) change output path, default current directory "./" #####
    outpath = './msdata/'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    ######################################################
    msfiles = importeovsa(idbfiles=trange, ncpu=1[, visprefix=outpath])
    
As a result of moving the online data files to a different location, the following commands can be used to identify where the files are based on the date and run importeovsa on them: 
    
    from suncasa.tasks import task_calibeovsa as calibeovsa
    from suncasa.tasks import task_importeovsa as timporteovsa
    from split_cli import split_cli as split
    import dump_tsys as dt
    from util import Time
    import numpy as np
    import os
    from glob import glob
    from eovsapy import util
    
    trange = Time(['2020-06-07 21:35:00', '2020-06-07 21:55:00'])
    idbdir = util.get_idbdir(trange[0])
    
    info = dt.rd_fdb(trange[0])
    sidx = np.where(
        np.logical_and(info['SOURCEID'] == 'Sun', info['PROJECTID'] == 'NormalObserving') & np.logical_and(
            info['ST_TS'].astype(np.float) >= trange[0].lv,
            info['ST_TS'].astype(np.float) <= trange[
                1].lv))
    filelist = info['FILE'][sidx]
    
    outpath = './msdata/'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    inpath = idbdir + '{}/'.format(trange[0].datetime.strftime("%Y%m%d"))
    ncpu = 1
    
    msfiles = timporteovsa.importeovsa(idbfiles=[inpath + ll for ll in filelist], ncpu=ncpu, timebin="0s", width=1,
                                       visprefix=outpath,
                                       nocreatms=False, doconcat=False,
                                       modelms="", doscaling=False, keep_nsclms=False, udb_corr=True)
    
### calibeovsa

SunCASA task "calibeovsa" applies the reference phase and daily phase calibrations to the visibility data (as a measurement set). After that, the measurement set is calibrated. Calibeovsa also allows to concatenate multiple measurement sets (e.g., several 10-min duration solar files) into a single measurement set. 
    
    # This is to set the path/name for the concatenated files
    concatvis = os.path.basename(msfiles[0])[:11] + '_concat.ms'
    vis = calibeovsa(msfiles, doconcat=True, concatvis=concatvis[, msoutdir=outpath])
    
Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Practical_Calibration_Tutorial&oldid=5538](http://ovsa.njit.edu//wiki/index.php?title=Practical_Calibration_Tutorial&oldid=5538)"
