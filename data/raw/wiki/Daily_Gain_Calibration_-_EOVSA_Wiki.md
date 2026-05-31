# Daily Gain Calibration - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Daily_Gain_Calibration
**Scraped:** 2025-08-05 09:13:25

# Daily Gain Calibration

From EOVSA Wiki

Jump to navigation Jump to search

Similar as reference complex gain calibration, daily gain calibration refers to tuning the "system" amplitude and phase as a function of IF band at a finer level. Typically, daily gain calibration would be carried out three times between two reference gain calibrations every day. We have a routine to retrieve and analyze the daily gain calibration data, named phacal_anal.py. Start from a timestamp **(Note: The time of day is important! Make sure to set it to somewhere in the middle of the day, e.g. 15:00 UT)**
    
    import phacal_anal as pa
    from util import Time
    t = Time('2017-07-03 15:00')
    pa.phacal_anal(t)
    
phacal_anal will find all daily gain calibrations occurred during that natural day (CA local time). 

# Commands for calibrating the eclipse [temporary]

## 15:00 UT

First run the refcal analysis for the day (can be done by 15:00 UT): 
    
    from util import Time
    import refcal_anal as ra
    import cal_header as ch
    out = ra.rd_refcal(Time(['2017-08-21 11:00','2017-08-21 14:00'))
    out_corr = ra.unrot_refcal(out)
    refcal = ra.refcal_anal(out)
    ch.refcal2sql(refcal)
    
## 19:20 UT

Next, as soon as the solar (eclipse) UDB file appears (around 19:20 UT) run the pipeline processing. Change directory to the one where the final eclipse files will be, /data1/dgary/solar/eclipse. **Note: the <tab> will complete the filename, but delete the trailing /.**: 
    
    from util import Time
    import pipeline_cal as pc
    filename = '/data1/eovsa/fits/UDB/2017/UDB20170821155<tab>'
    pc.udb_corr(filename)
    
## 20:00 UT

Run the phasecal analysis, answering y to questions about plots and accepting: 
    
    from util import Time
    import phacal_anal as pa
    pa.phacal_anal(Time('2017-08-21 19:00'))
    
Immediately after that, exit ipython, cd to /data1/dgary/solar/eclipse and get into CASA, then do 
    
    default importeovsa
    idbfiles = 'UDB20170821<tab>'
    go
    from suncasa.tasks import task_calibeovsa as tc
    tc.calibeovsa('UDB2017081915<tab>',doimage=True,stokes='I')
    
This will generate the first eclipse map, but it will be a single image of the entire eclipse! There may be some visible indication of the Moon in the image, but perhaps not. To make better images, it will be necessary to run clean on restricted time ranges. 
    
    tget clean
    <set parameters>
    go
    
Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Daily_Gain_Calibration&oldid=1803](http://ovsa.njit.edu//wiki/index.php?title=Daily_Gain_Calibration&oldid=1803)"
