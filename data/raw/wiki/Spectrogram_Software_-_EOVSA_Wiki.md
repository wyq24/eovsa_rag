# Spectrogram Software - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Spectrogram_Software
**Scraped:** 2025-08-05 09:12:32

# Spectrogram Software

From EOVSA Wiki

Jump to navigation Jump to search

## EOVSA Python Spectrogram Object (v0.1)

The module spectrogram.py defines a Spectrogram class that allows the creation of an object for reading, displaying, and gaining access to the EOVSA total power data from the “interim” Miriad data files. Because the object directly accesses these files, it will work only when logged in and running from the dpp computer, although this may change with further development of the code. 

## Minimal Use of Object

As a short example of the use the module from the dpp, start ipython and at the prompt type: 
    
    import spectrogram as sp
    from util import Time
    trange = Time(['2015-05-05 22:00:00','2015-05-05 22:30:00'])
    s = sp.Spectrogram(trange)
    s.explore()

This will find the files corresponding to the half-hour period indicated by the timerange trange, read the data, apply calibration and background subtraction, and display the data in three separate panels: as a spectrogram (dynamic spectrum), instantaneous spectrum, and lightcurve for a single frequency. By clicking and dragging the mouse in the dynamic spectrum panel, one can control which frequency is displayed in the lightcurve panel, and which time is displayed in the spectrum panel. One can use the usual plot control icons to zoom, pan, select, print, etc. In the instantaneous spectrum panel, a fit of the Stähli function is overplotted on the spectral points. Figure 1 shows the result of the above commands. 

[![](/wiki/images/0/04/Spectrogram.png)](/wiki/index.php/File:Spectrogram.png)

Figure 1: Screenshot of the result of the s.explore() command for the X-flare of 2015 May 05.

In this example the default settings are used, which includes performing total power calibration, background subtraction, and taking the median over all antennas and the two polarizations. It also defaults to displaying the entire time range, and only the frequencies between 2.5 and 18 GHz (frequency indexes 116:448). Each of these is controlled by setting the corresponding values as follows: 

  * s.docal = True (apply calibration)
  * s.bidx = [0, 100] (develop background spectrum as median over range 0:100 – default)
  * s.dosub = True (perform background subtraction over range specified in s.bidx)
  * s.showants = range(nants) (display/select data for this list of antennas)
  * s.domedian = True (calculate median over all antennas in s.showants list)

Once the spectrogram has been displayed, 

  * s.ax (handle to matplotlib axis on which the plot is displayed)

can be used to manipulate the plot, e.g. for adding text (s.ax.set_text()) or plot labels (s.ax.set_xlabel()), etc. 

## Selecting Data for Plotting/Retrieving

Different contiguous ranges of the data can be selected for displaying or retrieving, by use of the index range settings: 

  * s.fidx = [116, 448] (select data only over these frequency indexes)
  * s.tidx = [0, ntimes] (select data only over these time indexes)
  * s.showants = range(nants) (select data for antennas in this list, numbered 0 to nants-1)

Any of these values can be changed after creation of the spectrogram object (s in this example). After the object has been created, it can be used to retrieve and/or display the spectrogram. Display routines are s.show() – create a dynamic spectrum display; and s.explore() – create the interactive display as in Fig. 1, above. In either of these display modes, set s.cbar = True or False to display or not display the colorbar. Set the two-element variable s.drange (default is s.drange = [1, max(data)]) before plotting to limit the upper and lower range of data. Set s.dolog = True to resample the spectrogram on a logarithmic scale in frequency, otherwise the data are resampled on a linear scale. 

## Retrieving Data from the Object

Once created, the data contained in the object can be retrieved directly, or with several functions: 

  * s.xdata (actual, uncalibrated, unselected data for X polarization)
  * s.ydata (actual, uncalibrated, unselected data for Y polarization)
  * s.time (actual, unselected range of times as a Time() object)
  * s.fghz (actual, unselected range of frequencies in GHz)
  * s.calfac (raw calibration factors as read from calibration file)
  * s.offsun (raw off-Sun values as read from calibration file)
  * s.get_cal_data() (return xtsys and ytsys after selection as above, and with calibration applied, but no background subtraction [ignores both s.docal and s.dosub settings])
  * s.get_bgsub_data() (return xtsys and ytsys after selection as above, optionally with calibration applied [if s.docal is True], but force background subtraction over indexes in s.bidx [ignores s.dosub setting])
  * s.getbg() (get single background spectrum after selection, developed over range of indexes in s.bidx, optionally with calibration applied [if s.docal is True])
  * s.get_median_data() (return tsys, stdtsys after selection, which are median over all antennas and polarizations, and corresponding standard deviation over antennas in s.showants, optionally applying calibration and performing background subtraction)

## Getting Calibrated Data

If the procedure above for creating the spectrogram object results in a warning message “Calibration file not found for date 2015-06-07 22:00:00.000” (the date will change according to the date in trange), this indicates that a total power calibration file has not yet been created. The total power calibration is based on SOLPNTCAL observations that are typically taken twice per day (requires 5 minutes of observation), but the analysis of the observations to create the calibration file is not automatically done. In order to create a calibration file for a particular date, it is necessary to know the end time of the SOLPNTCAL observation. If a SOLPNT observation has been done from 21:30 – 21:35 UT, it can be analyzed by typing in a terminal console (not within an ipython session): 
    
     python /common/python/current/calibration.py ‘2015-06-07 21:36’ 

Note that the time given is 6 minutes after the start of the SOLPNT scan, or 1 minute after its end. This command will automatically generate the appropriate calibration file in the directory /data1/TPCAL. There is no user interaction for this command—it either works or does not. If for some reason you are not satisfied with the calibration, there is often a second scan on the same day. Analyzing either scan should give the same result. In any case, once an appropriate calibration file exists, it will be automatically read on creation of the spectrogram object [ created with s = sp.Spectrogram(trange)]. You can then retrieve calibrated data from the object by 
    
     xtsys, ytsys = s.get_cal_data(), 

where xtsys and ytsys are arrays of size [nt,nf,nant], for polarization channels X and Y, respectively. To get calibrated data with background subtraction, instead use 
    
     xtsys, ytsys = s.get_bgsub_data(), 

ensuring that s.docal is True (the default). In case you want a single spectrogram representing the median of all antennas and polarizations, use 
    
     tsys, stdtsys = s.get_data(), 

where tsys is an array of size [nf,nt] containing the median data, and stdtsys is an array of the same size containing the standard deviation of the 16 measurements (8 antennas and 2 polarizations) at each frequency and time. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Spectrogram_Software&oldid=343](http://ovsa.njit.edu//wiki/index.php?title=Spectrogram_Software&oldid=343)"
