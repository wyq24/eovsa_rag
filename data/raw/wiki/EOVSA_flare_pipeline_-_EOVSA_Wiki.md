# EOVSA flare pipeline - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/EOVSA_flare_pipeline
**Scraped:** 2025-08-05 09:12:36

# EOVSA flare pipeline

From EOVSA Wiki

Jump to navigation Jump to search

The frequency of observing calibrator sources during EOVSA solar observations is much less than that one typically would like to observe to properly take into account the instrumental gain variations. Hence self-calibration is often needed to calibrate the data to a level of satisfaction. A self-calibration pipeline suitable for generating calibrated dataset and quicklook images have been developed. Here we explain the various inputs of that pipeline and discuss various factors that is needed to be considered before supplying the input values. We also provide the steps for running the code on the pipeline machine. 

**Format of the pipeline**

The pipeline for now consists of an input file and two codes. The input file is named as _inputs.py_ . The other two codes are _gen_IDB_MS.py_ and _IDB_selfcal_pipeline_version.py_. The code _gen_IDB_MS.py_ is used to generate the measurement set (MS) from the raw files and calibrate the data using the gaintables derived from the calibrator observations. The second script is where the self-calibration happens. The main reason for having two separate codes is that "gen_IDB_MS.py" uses SUNCASA which for now runs on CASA versions<=5.4 . However, _IDB_selfcal_pipeline_version.py_ requires CASA >=5.6. Hence for now the user needs to run the codes using the appropriate CASA versions. 

**Description of the inputs**

An example inputs file in given below. 
    
    ## Task handlers ###
    cal_disk = 0 ## apply calibration tables from full disc imaging
    identify_data_gap=1  ### identify data gaps
    doslfcal = 1  # main cycle of doing selfcalibration
    doapply = 0  # apply the results
    
    # ============ declaring the working directories ============
    ### remember / is necessary in all the folder names
    
    workpath = '/data1/testing/20211101/'
    slfcaldir = workpath+ 'slfcal_v3/'  # place to put all selfcalibration products
    imagedir = slfcaldir + 'images/'  # place to put all selfcalibration images
    caltbdir = slfcaldir+'caltables/'  # place to put calibration tables
    slfdisktbdir = slfcaldir + 'slfdisktb/'
    
    # ============= time to image =================
    starttime='2017-08-20 19:20:00'   ### has strict formating rules
    endtime='2017-08-20 19:48:00'
    
    # ============ selfcal parameters ===============
    refantenna = '0'
    calc_cell=True ### If set to False use the value in beam given below
    cell=[10]  ### size needs to be same as the number of spw listed in selfcal_spw
    calc_imsize=True   ### is False uses the value given below
    imsize=42  ### in solar radius, the full image size at the first frequency. Other frequencies, the value will be scaled.
               ### The default value of 42 solar radius is for ~1 GHz
    
    max_frac_freq_avg=0.5  ### I will average at most this much fractional bandwidth
    
    maxiter=10  ### maximum selfcal iterations
    uvlim=25
    avg_spw_max=5
    flag_antennas = '' ###anything except 13~15. Those antennas are always flagged. 
    phasecenter=''
    
    # ========== end of input parameters =================
    
The _task handlers_ listed in the _inputs.py_ controls what functions will be performed by the _IDB_selfcal_pipeline_version.py_. A value of _0_ means that functionality will be run. Please give _1_ as input if the said task is desired. The next group of inputs are the _working directories_. After that, the time duration of interest should be provided. Please note that the format used when providing the _starttime_ and _endtime_ should be followed exactly as given in the above example. The next group of inputs are those which control different imaging and calibration parameters. _refantenna_ is the index of the reference antenna which is used during the calibration. The user has the choice to either provide the cell size and manually, or the code can calculate it based on the maximum uv value. Please set the parameter _calc_cell_ to _True_ if automatic setting of parameter value is desired. If set to _False_ , the user must provide the cell size for all the spws. Please note that the unit of the cell size is in arcseconds. Current the parameters _calc_imsize_ and _imsize_ are not used. The _imsize_ is always set to 4096, which means that the total area imaged is equal to _4096_ x _cell size_. _maxiter_ is the maximum number of selfcal iterations which can happen. During the self-calibration step, we use uv values above a cutoff. The cutoff is controlled by the parameter _uvlim_. The value of this parameter is in units of  λ {\displaystyle \lambda } ![{\\displaystyle \\lambda }](https://wikimedia.org/api/rest_v1/media/math/render/svg/b43d0ea3c9c025af1be9128e62a18fa74bedda2a) and corresponds to the value at spw 0. For other spws, the value is scaled with the corresponding frequency. During the self-calibration process, often spws are averaged to make an image. The two parameters named _max_frac_freq_avg_ and _avg_spw_max_ controls the maximum bandwidth over which this averaging can happen. _max_frac_freq_avg_ is equal to the fractional bandwidth and is given by  ( f u − f l ) ∗ 2 / ( f u + f l ) {\displaystyle (f_{u}-f_{l})*2/(f_{u}+f_{l})} ![{\\displaystyle \(f_{u}-f_{l}\)*2/\(f_{u}+f_{l}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e7ae40648f9e337885682df0c53280ba82219b25), where  f u , f l {\displaystyle f_{u},f_{l}} ![{\\displaystyle f_{u},f_{l}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/d1234de13f1d5338ed7da76c6294659f3b7f186f) are the lower and upper edges of the band to be averaged. _avg_spw_max_ is the maximum number of spws which can be averaged. During averaging both these parameters are calculated and the averaging stops when one of them is satisfied. If the user wants an antenna to be flagged other than antennas 13~15, that list should be supplied in _flag_antennas_ . The image phasecenter is often shifted close to the location of the flare, so as to make a smaller image. Hence a custom phasecenter is used. The user has the option to provide the desired phasecenter in the input _phasecenter_ or if left blank, the code will try to calculate it automatically. 

**Important steps in pipeline**

  * _Find time of self-calibration_ : The flare times are first detected, because the self-calibration is performed only once by the pipeline for a dataset. If the user intends to perform self-calibration at multiple times, the dataset should be split around the times of interest. For each spw, the auto-correlations are extracted and the median and median absolute deviation of the timeseries are calculated. The times at which the auto-correlation value exceeds the threshold are noted down. The longest time interval for which the value is higher than the threshold is identified with the flare duration. A time interval of length duration/3 around the peak is chosen for self-calibration. The minimum time interval is chosen to be 10s and the maximum is chosen to be 1 minute. If no value is found above the threshold, we choose 1 minute around the peak for self-calibration. These times are identified as _quiet times_ and other times are identified as _flaring times_.

## Updates

## Introduction

The EOVSA flare pipeline (eovsa_flare_pipeline.py) consists of three main steps: 

  * Use the calibrated MS file as input, generated by eovsa_flare_calib.py, which imports (via importeovsa.py) and calibrates IDB data (with calibeovsa.py) based on the provided time range.
  * Create a mask and perform self-calibration (selfcal).
  * Generate FITS files and movies containing images at multiple frequencies, along with the dynamic spectrum. The resulting FITS, movie, MS, and self-calibrated MS files will be uploaded to the EOVSA data website.

## Self-calibrations

## Producing EOVSA flare Level 1 data products

It may take several hours to generate flare movies, as the process depends on calibration and self-calibration steps. For example, producing a 3-minute movie with a 12-second cadence could take around 5 hours. It's recommended to use a script and run it in a screen session for efficiency. 

  * Input from calibrated MS file:

    from suncasa.eovsa import eovsa_flare_pipeline
    fp = eovsa_flare_pipeline.FlareSelfCalib(vis='IDB20201207_1600-1900.ms')
    fp.slfcal_pipeline(doselfcal=True, doimaging=True)

  * Input a timerange:

    from suncasa.eovsa import eovsa_flare_pipeline
    from eovsapy.util import Time
    fp = eovsa_flare_pipeline.FlareSelfCalib(vis=Time(['2021-05-07 19:01:00', '2021-05-07 19:03:00']))
    fp.slfcal_pipeline(doselfcal=True, doimaging=True)

  * For SoDs, it will fetch flare data from the flare list wiki URL and save it to a CSV file in the current directory, which will be a supply for flare pipeline:

    from suncasa.eovsa import eovsa_flarelist as ef
    flarelist_csv = ef.get_eoflarelist(timerange=["2024-10-01 22:00:00", "2024-10-01 23:00:00"])
    ef.run_eoflare_pipeline(flarelist_csv=flarelist_csv, to_web=True)

## EOVSA flare Level 1 data products

Data products: 

  * {Flare_ID}.calibrated.ms.tar.gz: Calibrated MS file
  * {Flare_ID}.selfcalibrated.ms.tar.gz: Self-calibrated MS file across multiple SPWs
  * {Flare_ID}.caltables.tar.gz: Self-calibration tables associated with the self-calibrated MS file
  * eovsa.lev1_mbd_12s.YYYY-MM-DDTHHMMSSZ.image.fits: images at several spws, with 12s time cadence
  * eovsa.spec.flare_id_YYYYMMDDHHMMSS.fits
  * eovsa.lev1_mbd_12s.flare_id_YYYYMMDDHHMMSS.mp4

Web Links: 

  * Spectrogram image and data: <http://ovsa.njit.edu/events/YYYY/>
  * Image data: <https://ovsa.njit.edu/fits/flares/YYYY/MM/DD/{Flare_ID}/>
  * Flare movies: <https://ovsa.njit.edu/SynopticImg/eovsamedia/eovsa-browser/YYYY/MM/DD/>"

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=EOVSA_flare_pipeline&oldid=10700](http://ovsa.njit.edu//wiki/index.php?title=EOVSA_flare_pipeline&oldid=10700)"
