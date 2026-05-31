# Caius' Notes - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Caius%27_Notes
**Scraped:** 2025-08-05 09:13:39

# Caius' Notes

From EOVSA Wiki

Jump to navigation Jump to search

## EOVSA flare spectrograms

### Checking the possible EOVSA

Verify the possible flares on the daily EOVSA Solar Dynamic Spectrogram, for example: 

<http://ovsa.njit.edu/browser/?suntoday_date=2024-05-07>

[![Daily spec 20240507.png](/wiki/images/8/84/Daily_spec_20240507.png)](/wiki/index.php/File:Daily_spec_20240507.png)

[](/wiki/index.php/File:Daily_spec_20240507.png "Enlarge")

In this example, we are going to analyze the M8.2 flare that happened after 16:00 UT. 

For a better flare time precision, a Dynamic spectrogram with short time range at: 

<http://ovsa.njit.edu/flaremon/>

[![XSP20240507153014.png](/wiki/images/7/78/XSP20240507153014.png)](/wiki/index.php/File:XSP20240507153014.png)

[](/wiki/index.php/File:XSP20240507153014.png "Enlarge")

Since 2024-May-05, the Real Time Flare detection figure and its list are also available: 

<http://ovsa.njit.edu/flaremon/FLM20240507.png> <http://ovsa.njit.edu/flaremon/flarelist/flarelist_2024-05-07.txt>

[![FLM20240507.png](/wiki/images/6/68/FLM20240507.png)](/wiki/index.php/File:FLM20240507.png)

[](/wiki/index.php/File:FLM20240507.png "Enlarge")

### Using Python 3.8

Login into pipeline machine as user: 
    
    ssh -X user@pipeline 

To verify the antennas that were working, check the observing log <http://ovsa.njit.edu/wiki/index.php/2024_May>, 

or consult the TPCAL log file, e.g. more /dppdata1/TPCAL/LOG/TPCyyyymmdd.log 

Create the flare directory at /data1/dgary/solar/, e.g: 
    
    mkdir 20240507_M8flare 
    cd 20240507_M8flare

Load the Python 3.8 environment: 
    
    bash 
    loadpyenv3.8
    ipython --pylab

In Python, enter the following: 
    
    from eovsapy import flare_spec as fs 
    from eovsapy.util import Time 

To download the IDB directories form the SQL cloud, enter the flare interval as: 
    
    files = fs.calIDB(Time(['2024-05-07 16:20','2024-05-07 16:35'])) 

If the IDB already exist, they can be read as: 
    
    files = ['IDB20240507162024','IDB20240507163024'] 

Or all the IDB files can be read as: 
    
    import glob
    files = sorted(glob.glob('IDB*')) 

When all the antennas were fine, enter the following: 
    
    out, spec = fs.inspect(files) 

But, if one or more antennas weren't working, enter the list of the good ones as: 
    
     out, spec = fs.inspect(files, ant_str='ant1-6 ant8-9 ant11-13') 

[![Out spec.png](/wiki/images/1/1b/Out_spec.png)](/wiki/index.php/File:Out_spec.png)

[](/wiki/index.php/File:Out_spec.png "Enlarge")

To better see the flare, you can change the spec vmax as: 
    
     imshow(spec,vmax=30,vmin=-1) 

[![Out spec2.png](/wiki/images/f/fd/Out_spec2.png)](/wiki/index.php/File:Out_spec2.png)

[](/wiki/index.php/File:Out_spec2.png "Enlarge")

Use the figure above to choose the background interval (bgidx), the maximum intensity and the frequencies. 

The tpk (Time of the peak) determines the name of the resulting files (.png and .fits), and also determines the flare_id. 

It's better to keep the formate of tpk as tpk='yyyy-mm-dd hh:mm:00' and add the flare time on wiki in the format of "hh:mm": 
    
     f, ax0, ax1 = fs.make_plot(out,bgidx=[200,210],vmin=0.1, vmax=110, lcfreqs=[120,190,270,350],ant_str='ant1-6 ant8-9 ant11-13', tpk='2024-05-07 16:30:00') 

[![Eovsa.spec.flare id 20240507163000.png](/wiki/images/2/29/Eovsa.spec.flare_id_20240507163000.png)](/wiki/index.php/File:Eovsa.spec.flare_id_20240507163000.png)

[](/wiki/index.php/File:Eovsa.spec.flare_id_20240507163000.png "Enlarge")

A second background interval can be defined right after the first one, e.g., bg2idx=[1000,1010] 

In this example, the output files are eovsa.spec.flare_id_20240507163000.fits and eovsa.spec.flare_id_20240507163000.fits. 

At the end, copy the .fits file to /common/webplots/events/2024: 
    
     cp eovsa.spec.flare_id_20240507163000.fits /common/webplots/events/2024 

and include the flare in the wiki Flare List: 

<http://ovsa.njit.edu/wiki/index.php/2024>

The flare position have been copied from the <https://solarmonitor.org/>

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Caius%27_Notes&oldid=10009](http://ovsa.njit.edu//wiki/index.php?title=Caius%27_Notes&oldid=10009)"
