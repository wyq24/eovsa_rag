# EOVSA Data Products - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/EOVSA_Data_Products
**Scraped:** 2025-08-05 09:12:29

# EOVSA Data Products

From EOVSA Wiki

Jump to navigation Jump to search

# Introduction

EOVSA observes the full disk of the Sun at all times when the Sun is >10 degrees above the local horizon (season dependent and ranges from 7-12 hours duration centered on 20 UT). EOVSA records data at 451 science frequency channels each second, in four polarization products, as well as additional total flux measurements from each individual antenna. Figure 1 summarizes the different levels of data we produce. The later sections will give a more detailed description and usage examples. 

[![EOVSA pipeline block diagram/flow chart](/wiki/images/6/68/Pipeline_flowchart.jpg)](/wiki/index.php/File:Pipeline_flowchart.jpg "EOVSA pipeline block diagram/flow chart")

# Level 0 - Raw visibility data from the instrument

As outlined in Figure 1, EOVSA creates raw data products in the left-hand column (labeled Level 0). This includes observations of cosmic sources for phase calibration, and gain and pointing observations required for total power calibration. 

## Raw "Interim" Database (IDB) visibility data

Full-resolution raw "Interim" Database (IDB) visibility data. They are stored in Miriad format, and hence may not be that useful for most people. Be patient after clicking the link--this is a very long list of directories, one for each available date. Recent data (latest few months) can be retrieved from the following page: 

<https://www.ovsa.njit.edu/fits/IDB/>

For older data, visit the UC/Berkeley hosting page: 

<https://research.ssl.berkeley.edu/data/eovsa/IDB/>

## Raw 1-min-averaged visibility data

This is the same as for the IDB data, except with 1-minute time integration applied. This is typically not useful for flares, but is perfectly fine for imaging active regions and full Sun. These data can be retrieved from the following page: 

<http://www.ovsa.njit.edu/fits/UDB/>

# Level 0.5 - Calibrated visibility data

After applying calibration and other preliminary processing to the raw (level 0) data, we create the CASA ms’s in the second column in Figure 1 (labeled "level 0.5"). These visibility data are in the Fourier domain of the true images in the plane of the sky and are not immediately ready for spectral imaging analysis yet. However, they have all of the required content to produce images and spectrogram data in standard FITS format (level 1.0). We provide a set of standard ms’s for each day (red boxes in Figure 1), for use by researchers who know how to deal with visibility data. These data are more suitable for experienced users to exploit the full potential of EOVSA data, such as spatially resolved spectral analysis. Processing these data requires CASA or sunCASA (<https://github.com/suncasa/suncasa-src>). Please refer to our tutorial at [EOVSA_Data_Analysis_Tutorial](/wiki/index.php/EOVSA_Data_Analysis_Tutorial "EOVSA Data Analysis Tutorial"). 

## Calibrated full-resolution visibility data for flare events

Calibrated and self-calibrated visibility data for flare events (purple boxes in Figure 1) will typically be available within 7 days after they are taken. They will be released at our flare list site soon: <https://ovsa.njit.edu/flarelist>

## Self-calibrated 1-min-averaged visibility data

EOVSA 1-min averaged visibility data in CASA ms format can be retrieved from the following page: 

<http://www.ovsa.njit.edu/fits/UDBms_slfcaled>

# Level 1.0 - Images and spectrogram data in standard FITS format

Level 1.0 data are for users who prefer to work with spectrogram (frequency-time) and image data directly, which are also outputs of the pipeline system shown in Figure 1 (orange boxes). They are perfectly suitable to be used as context data for comparison with other multi-wavelength observations but are not (yet) intended for quantitative spatially resolved spectral analysis. 

Spectrograms are provided as standard FITS tables containing the frequency list, list of times, and data in both total power (TP) and a sum of amplitudes over intermediate-length baselines (cross power or XP). Likewise, image data products are in FITS format with standard keywords and are converted into the Helioprojective Cartesian coordinate system compatible with the World Coordinate System (WCS) convention, along with correct registration for the spatial, spectral, and temporal coordinates. Both the spectrogram and image data products are calibrated and have physical radio intensity units (sfu for spectrograms and brightness temperature for radio images). 

We provide the following level 1 data products: 

  * Synoptic products: 
    * **All-day spectrograms** : Full-day total-power (TP) and cross-power (XP) spectrograms (i.e., no spatial resolution) at full spectral and time resolution in FITS format. One file per day.
    * **All-day synoptic images** : Full disk images at 7 selected frequency bands centered at 1.4, 3.0, 4.5, 6.8, 10.2, 13.9 and 17.0 GHz are produced once per day utilizing the earth-rotation synthesis, calibrated in brightness temperature. This is because EOVSA has a limited number of baselines and we need a long integration to fill up the uv domain in order to make full-disk images.
  * Event-based products: 
    * **Flare spectrograms** : These are full time and frequency resolution spectrograms produced from the median of calibrated cross-power visibilities in FITS format, cropped to cover the flare duration. Preflare background is also subtracted. Since mid-October 2024, we offer both total- and cross-power spectrograms for flare events. Cross-power spectrograms, compared to total-power spectrograms, have the advantage of revealing details of the flare evolution by "filtering out" the large-scale, continuous background from the visibilities. Note that for certain flares that have a large source size, the flux can be lower than its true values (as a fraction of the flux will be "resolved out").
    * **Pipeline-produced spectral images** : We also have a semi-automated flare imaging pipeline to produce calibrated (and self-calibrated) images at 12-s cadence at up to 10 frequency bands. They are saved in standard FITS format and have been registered into Helioprojective coordinates. They can be read by SSWIDL or astropy/sunpy. These data have already been calibrated to physical units and are usually good to be compared with context data. But please be cautious when using them for quantitative spectral analysis.

Summary of EOVSA Level 1 Data Products  Category  | Data Product  | Naming Convention  | Download Link   
---|---|---|---  
Synoptic Spectrograms  | All-day TP Spectrograms  | EOVSA_TPall_yyyymmdd.fts  | <https://ovsa.njit.edu/browser>  
All-day XP Spectrograms  | EOVSA_XPall_yyyymmdd.fts   
Synoptic Images  | Synoptic 1.4 GHz images  | eovsa_yyyymmdd.spw00-01.tb.disk.fits   
Synoptic 3.0 GHz images  | eovsa_yyyymmdd.spw02-05.tb.disk.fits   
Synoptic 4.5 GHz images  | eovsa_yyyymmdd.spw06-10.tb.disk.fits   
Synoptic 6.8 GHz images  | eovsa_yyyymmdd.spw11-20.tb.disk.fits   
Synoptic 10.2 GHz images  | eovsa_yyyymmdd.spw21-30.tb.disk.fits   
Synoptic 13.9 GHz images  | eovsa_yyyymmdd.spw31-43.tb.disk.fits   
Synoptic 17.0 GHz images  | eovsa_yyyymmdd.spw44-49.tb.disk.fits   
Flare Spectrograms  | Flare TP Spectrogram  | eovsa.spec_tp.flare_id_YYYYMMDDHHMM.fits  | <https://ovsa.njit.edu/flarelist>  
Flare XP Spectrogram  | eovsa.spec_xp.flare_id_YYYYMMDDHHMM.fits   
Flare Spectral Images  | Pipeline-produced spectral images  | eovsa.lev1_mbd_12s.YYYY-MM-DDTHHMMSSZ.image.fits   
  
## Browsing and Downloading level 1 data

[![](/wiki/images/8/82/Eovsa_browser.jpg)](/wiki/index.php/File:Eovsa_browser.jpg)

[](/wiki/index.php/File:Eovsa_browser.jpg "Enlarge")

EOVSA Browser

[![](/wiki/images/6/6c/EOVSA_flarelist.jpg)](/wiki/index.php/File:EOVSA_flarelist.jpg)

[](/wiki/index.php/File:EOVSA_flarelist.jpg "Enlarge")

EOVSA Flare List

### Synoptic level 1 data

EOVSA Level 1 synoptic data products can be retrieved with the following steps: 

  * Go to [EOVSA browser](http://ovsa.njit.edu/browser/) page.
  * Browse to the date of interest.
  * Click "synoptic fits" button next to the calendar tool.
  * Select the data product based on the names listed in the table above.

### Flare level 1 data

EOVSA flare list with spectrograms and spectral images can be queried and downloaded at <https://ovsa.njit.edu/flarelist>. Users can use the top box to select a time range of interest and query our flare list. The results are displayed in the dropdown box. An interactive plot of the flare light curves will be shown at the bottom of the page once an event is highlighted (by clicking on the flare ID). Quicklook plots and FITS files of the spectrograms and flare movies can be accessed by clicking the icons in each flare record. 

## Reading and Using level 1 data

### Introduction

All our level 1 data products are in FITS format. All the images have standard, WCS-compatible coordinates. Users can use their favorite method to read these files. In the following, we provide minimal examples to read them with Astropy and Sunpy. 

### Synoptic Data Products

#### Python Users

An example of how to read and plot the flare spectrograms and images in Python (with [Astropy](https://www.astropy.org/), [SunPy](https://sunpy.org/), and optionally, [radiospectra](https://docs.sunpy.org/projects/radiospectra/en/latest/)) can be accessed at [this Google Colab Jupyter notebook](https://colab.research.google.com/drive/1bF_WjKRk51Hb3h10EzcGaBCw9QFjWwqW?usp=sharing). 

#### SSWIDL Users

For IDL users, here is an example of using SSWIDL's "[mrdfits](https://hesperia.gsfc.nasa.gov/ssw/gen/idl/fits/mrdfits.pro)" to read the total-power FITS file and the "[spectrogram](https://hesperia.gsfc.nasa.gov/ssw/gen/idl/objects/spectrogram.pro)" function to visualize it. We use the 2021 Oct 28 X1 flare as example, downloaded from [the browser](https://ovsa.njit.edu/browser/?suntoday_date=2021-10-28). 
    
    ; Read the FITS file using mrdfits
    filename = 'EOVSA_TPall_20211028.fts'
    spec = mrdfits(filename,0) ;(Array of amplitudes in SFU, of size [number of times, number of frequencies])
    freq = mrdfits(filename,1) ;(A structure array of frequency information, of size [number of frequencies])
    time = mrdfits(filename,2) ;(Array of UT times in SSWIDL anytim format, of size [number of times])
    fghz = freq.sfreq  ;center frequencies in GHz
    timeut = anytim(time) ;convert the time into anytim format
    
    ntime = n_elements(timeut) ; number of times
    nfreq = n_elements(fghz) ; number of frequencies
    
    ; Convert the information into a spectrogram object.
    s = spectrogram(spec, timeut, fghz)
    
    ; Do a simple plot
    window,/free,xsiz=1024,ysiz=600
    ; Find min and max of data from 5% to 95% of sorted array (eliminates outliers)
    sarr = sort(spec)
    dlim = minmax(spec[sarr[n_elements(sarr)*0.05:n_elements(sarr)*0.95]])
    ; Set drange with margin factor of 2 on low end and 5 on high end
    s.set,drange=dlim*[0.5,5]
    loadct,5
    s.plot,/log,timerange=['2021-10-28T15:15:00','2021-10-28T16:00:00'],/xsty,/ysty,ytitle='Frequency [GHz]',charsize=1.5
    
[![IDL synop tp 20211028.jpg](/wiki/images/5/54/IDL_synop_tp_20211028.jpg)](/wiki/index.php/File:IDL_synop_tp_20211028.jpg)
    
    ; If you wish to do a pre-flare background subtraction and bring out more details of the flare
    timebkg = ['2021-10-28T15:15', '2021-10-28T15:20'] ; selecting a background window
    dt0 = min(abs(timeut - anytim(timebkg[0])), bkg_i0)
    dt1 = min(abs(timeut - anytim(timebkg[1])), bkg_i1)
    spec_bkg = mean(spec[bkg_i0:bkg_i1,*], dimension=1) ; this is the average background
    spec_sub = spec - rebin(reform(spec_bkg, 1, nfreq), ntime, nfreq) ;do the subtraction
    ; Recreate the spectrogram and do the plotting
    s = spectrogram(spec_sub, timeut, fghz)
    window,/free,xsiz=1024,ysiz=600
    s->set,drange=dlim*[0.01,2]
    loadct,5
    s.plot,/linear,timerange=['2021-10-28T15:15:00','2021-10-28T16:00:00'],/xsty,/ysty,ytitle='Frequency [GHz]',charsize=1.5
    
[![IDL synop tp 20211028 bkgsub.jpg](/wiki/images/1/12/IDL_synop_tp_20211028_bkgsub.jpg)](/wiki/index.php/File:IDL_synop_tp_20211028_bkgsub.jpg)
    
    ; One can also load the object into plotman and visualize it interactively. See the snapshot below for an example.
    ; The widget allows a convenient way to explore the light curves by selecting "plot_Control" -> "Image or Spectrogram Profiles" -> "Rows or Columns") 
    s->set,timerange = ['2021-10-28T15:15:00','2021-10-28T16:00:00']
    s->plotman
    
[![IDL synop tp 20211028 bkgsub plotman.jpg](/wiki/images/e/ed/IDL_synop_tp_20211028_bkgsub_plotman.jpg)](/wiki/index.php/File:IDL_synop_tp_20211028_bkgsub_plotman.jpg)

For synoptic images: 
    
    read_sdo,'eovsa_20191225.spw11-20.tb.disk.fits',header,data,/UNCOMP_DELETE
    index2map,header,data,eomap
    plot_map,eomap
    
[![Eovsa 20191225 image sswidl.jpg](/wiki/images/8/89/Eovsa_20191225_image_sswidl.jpg)](/wiki/index.php/File:Eovsa_20191225_image_sswidl.jpg)

### Event-Based Data Products

#### Python Users

An example of how to read and plot the flare spectrograms and images in Python (with [Astropy](https://www.astropy.org/) and [SunPy](https://sunpy.org/)) can be accessed at [this Google Colab Jupyter notebook](https://colab.research.google.com/drive/1wMvuxuNip5cJJHMoTOLT6u_OdWobpBY0?usp=sharing). 

#### SSWIDL Users

For event-based data products, the only difference is in how the time array is read and converted. In these FITS files, the time array is provided in Julian Date (JD), not in SSWIDL anytim format. Use the following function to convert JD to SSWIDL “anytim” seconds, then proceed with the same spectrogram analysis and plotting steps as in the synoptic example above. Note that for most event-based spectrograms, background-subtraction has already been performed. 
    
    ; Function to convert Julian Date (JD) to SSWIDL "anytim" seconds (since 1979-01-01 00:00:00 UTC)
    function jd2anytim, jd
      jd0 = 2443874.5           ; JD of 1979-01-01 00:00:00
      sec_per_day = 86400.0
      return, (jd - jd0) * sec_per_day
    end
    
    ; Read the event-based FITS file
    filename = 'eovsa.spec.flare_id_20211028152600.fits'
    spec = mrdfits(filename, 0)      ; [ntime, nfreq] array of amplitudes in SFU
    freq = mrdfits(filename, 1)      ; Structure array of frequency info (length nfreq)
    time = mrdfits(filename, 2)      ; Structure array with field 'time' (JD, length ntime)
    
    fghz = freq.fghz                 ; Center frequencies [GHz]
    timeut = jd2anytim(time.time)    ; Convert JD to SSWIDL "anytim" seconds
    
    ; The rest of your workflow (creating the spectrogram and plotting)
    ; is identical to the synoptic example above.
    
**Tip:** After `timeut = jd2anytim(time.time)`, you can continue with the code from the synoptic data section—creating the spectrogram, plotting, background subtraction, and interactive exploration with `plotman`—using the same commands. 

# Requesting EOVSA Data or Analysis Assistance

The pipeline-processed synoptic and flare event data (level 1.0) are science-ready and usually sufficient for many purposes. However, the list may not be complete, and the pipeline-processed data do not have the full-time and frequency resolution necessary for certain in-depth quantitative spectral analyses. If you are interested in (1) working on events that are not currently included in our level 1.0 database and/or (2) needing assistance from an EOVSA team member in detailed or quantitative analysis that requires EOVSA data processing beyond that offered by the level 1.0 products, please use the following Data Request Form to submit such requests. 

[EOVSA data request form](https://forms.gle/xPo7G3fwGwQhEmdLA)

We will normally respond to your request within 2-3 working days. Note that for (1), standard acknowledgments and reference citations would be sufficient. For (2), the EOVSA team member who helped with the data analysis/interpretation needs to be included as a co-author for publications that utilize the relevant EOVSA data. Please refer to <https://ovsa.njit.edu//wiki/index.php/EOVSA_Data_Policy> for details of our data policy. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=EOVSA_Data_Products&oldid=12492](http://ovsa.njit.edu//wiki/index.php?title=EOVSA_Data_Products&oldid=12492)"
