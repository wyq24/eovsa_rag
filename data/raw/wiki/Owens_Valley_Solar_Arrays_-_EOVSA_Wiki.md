# Owens Valley Solar Arrays - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Owens_Valley_Solar_Arrays#EOVSA_Documentation
**Scraped:** 2025-08-05 09:12:31

# Owens Valley Solar Arrays

From EOVSA Wiki

Jump to navigation Jump to search

[![Eovsa1.png](/wiki/images/1/1f/Eovsa1.png)](/wiki/index.php/File:Eovsa1.png)

[EOVSA](http://ovsa.njit.edu/) (Expanded Owens Valley Solar Array) is a solar-dedicated radio interferometer operated by the New Jersey Institute of Technology and serving as a **National Science Foundation Geospace Facility**. [![NSF.jpg](/wiki/images/a/a6/NSF.jpg)](/wiki/index.php/File:NSF.jpg)
    
    Operation of EOVSA is supported by the National Science Foundation under Grant No. AGS-2130832. Any opinions, findings, and conclusions or  recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science  Foundation. 

This wiki serves as the site for EOVSA documentation. 

[![OVRO-LWA1.png](/wiki/images/d/d8/OVRO-LWA1.png)](/wiki/index.php/File:OVRO-LWA1.png)

OVRO-LWA (Owens Valley Radio Observatory Long Wavelength Array) is an all-sky imager that has a new solar-dedicated spectroscopic imaging mode. OVRO-LWA is a multi-institutional collaboration led by Caltech. NJIT Solar Radio Group is leading its solar-mode development and science. At the bottom of this page are new links for that facility. 

## Latest OVSA Science Highlights

[OVSA Science Highlight No. 1: Microwave Precursor of a Major Solar Eruption](/wiki/index.php/OVSA_Science_Highlight_No._1:_Microwave_Precursor_of_a_Major_Solar_Eruption "OVSA Science Highlight No. 1: Microwave Precursor of a Major Solar Eruption")

[![Solar eruption nasa.jpeg](/wiki/images/d/d1/Solar_eruption_nasa.jpeg)](/wiki/index.php/File:Solar_eruption_nasa.jpeg)

A study by [Kou et al.](https://iopscience.iop.org/article/10.3847/2041-8213/adf063) presents the first spatially resolved microwave imaging spectroscopy of the precursor phase of a major solar eruption. The findings reveal that thermal electron emissions dominate during the slow-rise phase, supporting a scenario of moderate magnetic reconnection prior to the flare’s impulsive onset. [Contributed by Yuankun Kou (Nanjing Univeristy); Edited by B. Chen. Posted on August 2, 2025.] 

We welcome contributions at all times. Please refer to the [OVSA Science Highlights](/wiki/index.php/OVSA_Science_Highlights "OVSA Science Highlights") page for guidelines and a complete list of highlights. 

## OVSA Publications

Our collection of publications that utilize OVSA data is available at [this NASA/ADS Library](https://ui.adsabs.harvard.edu/public-libraries/eQ7HfPkySqydu-B8BCt6QQ). If you have a paper that is missing from this library, please email Bin Chen (bin.chen [at] njit.edu). 

## EOVSA Flare List

  * [Query EOVSA Flare list](https://ovsa.njit.edu/flarelist)
  * List of EOVSA flares in separate years: [2025](/wiki/index.php/2025 "2025"), [2024](/wiki/index.php/2024 "2024"), [2023](/wiki/index.php/2023 "2023"), [2022](/wiki/index.php/2022 "2022"), [2021](/wiki/index.php/2021 "2021"), [2020](/wiki/index.php/2020 "2020"), [2019](/wiki/index.php/2019 "2019"), [2017](/wiki/index.php/2017 "2017")

## Using OVSA Data

  * [EOVSA Data Products](/wiki/index.php/EOVSA_Data_Products "EOVSA Data Products"): An introduction to standard EOVSA spectrogram and spectral image products with example scripts for reading and plotting.
  * [EOVSA Data Policy](/wiki/index.php/EOVSA_Data_Policy "EOVSA Data Policy"): Policy for using EOVSA data products.
  * Analysis Software: These are for in-depth use of EOVSA data (from calibrated visibilities) and tools for quantitative analysis. 
    * [SunCASA](https://github.com/suncasa/suncasa) A wrapper around [CASA (the Common Astronomy Software Applications package)](https://casa.nrao.edu/) for synthesis imaging and visualizing solar spectral imaging data. CASA is one of the leading software tool for "supporting the data post-processing needs of the next generation of radio astronomical telescopes such as ALMA and VLA", an international effort led by the [National Radio Astronomy Observatory](https://public.nrao.edu/). The current version of CASA uses Python (2.7) interface. More information about CASA can be found on [NRAO's CASA website ](https://casa.nrao.edu/). Note, CASA is available ONLY on UNIX-BASED PLATFORMS (and therefore, so is SunCASA).
    * [GSFIT](https://github.com/Gelu-Nita/GSFIT) A IDL-widget(GUI)-based spectral fitting package called gsfit, which provides a user-friendly display of EOVSA image cubes and an interface to fast fitting codes (via platform-dependent shared-object libraries).
    * [pyGSFIT](https://github.com/suncasa/pygsfit) A Python-widget(pyQT)-based spectral fitting package, which provides a user-friendly display of EOVSA image cubes, spatially resolved spectra, and an interface to scipy-based fitting codes.
    * [Spectrogram Software](/wiki/index.php/Spectrogram_Software "Spectrogram Software")
    * [Mapping Software](/wiki/index.php/Mapping_Software "Mapping Software")
  * Data Analysis Guides (for those who start from raw data) 
    * [Tohban Guide to Self Calibration and Imaging for EOVSA](/wiki/index.php/Tohban_Guide_to_Self_Calibration_and_Imaging_for_EOVSA "Tohban Guide to Self Calibration and Imaging for EOVSA") Step-to-step guide for manually making images from raw visibility data.
    * [EOVSA flare pipeline](/wiki/index.php/EOVSA_flare_pipeline "EOVSA flare pipeline") Description of the EOVSA flare pipeline and tutorial for running it to produce quicklook images.

  * EOVSA Modeling Guide
    * [GX Simulator](/wiki/index.php/GX_Simulator "GX Simulator")

  * Other helpful links 
    * [CASA Guides](https://casaguides.nrao.edu)
    * [SolarSoft IDL](http://www.lmsal.com/solarsoft/)
    * [Miriad Guides](http://www.atnf.csiro.au/computing/software/miriad/userguide/userhtml.html)
    * [Fast Gyrosynchrotron Codes (Alexey Kuznetsov's website)](https://sites.google.com/site/fgscodes/)
    * [Basic GitHub Tutorial](/wiki/index.php/Basic_GitHub_Tutorial "Basic GitHub Tutorial")

  * [Full Disk Simulations](/wiki/index.php/Full_Disk_Simulations "Full Disk Simulations")
  * [All-Day Synthesis Issues](/wiki/index.php/All-Day_Synthesis_Issues "All-Day Synthesis Issues")
  * [Analyzing Pre-2017 Data](/wiki/index.php/Analyzing_Pre-2017_Data "Analyzing Pre-2017 Data")
  * [Fixing Pipeline Problems pre-2021-Feb-07](/wiki/index.php/Fixing_Pipeline_Problems_pre-2021-Feb-07 "Fixing Pipeline Problems pre-2021-Feb-07")

## EOVSA Documentation

  * General
    * [Downconversion and Frequency Tuning](/wiki/index.php/Downconversion_and_Frequency_Tuning "Downconversion and Frequency Tuning")
    * [Dealing with Radio Frequency Interference](/wiki/index.php/Dealing_with_Radio_Frequency_Interference "Dealing with Radio Frequency Interference")
    * [Switching between 200 MHz and 300 MHz Correlator](/wiki/index.php/Switching_between_200_MHz_and_300_MHz_Correlator "Switching between 200 MHz and 300 MHz Correlator")
    * [Observing in "Fast" Mode](/wiki/index.php/Observing_in_%22Fast%22_Mode "Observing in "Fast" Mode")

  * Computer-Network
    * [Computing Systems](/wiki/index.php/Computing_Systems "Computing Systems")
    * [Network](/wiki/index.php/Network "Network")

  * Control System
    * [27-m Antenna Commands](/wiki/index.php/27-m_Antenna_Commands "27-m Antenna Commands")
    * [Schedule Commands](/wiki/index.php/Schedule_Commands "Schedule Commands")
    * [Control Commands](/wiki/index.php/Control_Commands "Control Commands")
    * [Attenuation and Level Control](/wiki/index.php/Attenuation_and_Level_Control "Attenuation and Level Control")

  * Hardware
    * [Hardware Overview](/wiki/index.php/Hardware_Overview "Hardware Overview")
    * [2.1-m Antennas](/wiki/index.php/2.1-m_Antennas "2.1-m Antennas")
    * [27-m Antennas](/wiki/index.php/27-m_Antennas "27-m Antennas")

  * System Software
    * [Calibration Database](/wiki/index.php/Calibration_Database "Calibration Database")
    * [Stateframe Database](/wiki/index.php/Stateframe_Database "Stateframe Database")
    * [Database Maintenance](/wiki/index.php/Database_Maintenance "Database Maintenance")
    * [Create CASA measurement sets](/wiki/index.php/Create_CASA_measurement_sets "Create CASA measurement sets")

  * Calibration
    * [Calibration Overview](/wiki/index.php/Calibration_Overview "Calibration Overview")
    * [Pointing Calibration](/wiki/index.php/Pointing_Calibration "Pointing Calibration")
    * [Total Power Calibration](/wiki/index.php/Total_Power_Calibration "Total Power Calibration")
    * [System Gain Calibration](/wiki/index.php/System_Gain_Calibration "System Gain Calibration")
    * [Antenna Position](/wiki/index.php/Antenna_Position "Antenna Position") (Baseline Calibration)
    * [Reference Gain Calibration](/wiki/index.php/Reference_Gain_Calibration "Reference Gain Calibration")
    * [Daily Gain Calibration](/wiki/index.php/Daily_Gain_Calibration "Daily Gain Calibration")
    * [Delay Calibration](/wiki/index.php/Delay_Calibration "Delay Calibration")
    * [Bandpass Calibration](/wiki/index.php?title=Bandpass_Calibration&action=edit&redlink=1 "Bandpass Calibration \(page does not exist\)")
    * [Polarization Calibration](/wiki/index.php/Polarization_Calibration "Polarization Calibration")
    * [Calibrator Survey](/wiki/index.php/Calibrator_Survey "Calibrator Survey")
    * [Practical Calibration Tutorial](/wiki/index.php/Practical_Calibration_Tutorial "Practical Calibration Tutorial")

  * [Starburst](/wiki/index.php/Starburst "Starburst")

## EOVSA System Software

  * LabVIEW software
  * Python code [Github repository](https://github.com/dgary50/eovsa)
  * [Python3 Code Installation](/wiki/index.php/Python3_Code_Installation "Python3 Code Installation")

## Using OVRO-LWA data

  * [OVRO-LWA Data Products](/wiki/index.php/OVRO-LWA_Data_Products "OVRO-LWA Data Products"): An introduction to standard OVRO-LWA spectrogram and spectral image products with example scripts for reading and plotting.
  * [OVRO-LWA Data Policy](/wiki/index.php?title=OVRO-LWA_Data_Policy&action=edit&redlink=1 "OVRO-LWA Data Policy \(page does not exist\)"): Policy for using OVRO-LWA data products.

## EOVSA Observing Log

[2016 November](/wiki/index.php/2016_November "2016 November"); [ December](/wiki/index.php/2016_December "2016 December")

[2017 January](/wiki/index.php/2017_January "2017 January"); [ February](/wiki/index.php/2017_February "2017 February"); [ March](/wiki/index.php/2017_March "2017 March"); [ April](/wiki/index.php/2017_April "2017 April"); [ May](/wiki/index.php/2017_May "2017 May"); [ June](/wiki/index.php/2017_June "2017 June"); [ July](/wiki/index.php/2017_July "2017 July"); [ August](/wiki/index.php/2017_August "2017 August"); [ September](/wiki/index.php/2017_September "2017 September"); [ October](/wiki/index.php/2017_October "2017 October"); [ November](/wiki/index.php/2017_November "2017 November"); [ December](/wiki/index.php/2017_December "2017 December")

[2018 January](/wiki/index.php/2018_January "2018 January"); [ February](/wiki/index.php/2018_February "2018 February"); [ March](/wiki/index.php/2018_March "2018 March"); [ April](/wiki/index.php/2018_April "2018 April"); [ May](/wiki/index.php?title=2018_May&action=edit&redlink=1 "2018 May \(page does not exist\)"); [ June](/wiki/index.php?title=2018_June&action=edit&redlink=1 "2018 June \(page does not exist\)"); [ July](/wiki/index.php/2018_July "2018 July"); [ August](/wiki/index.php?title=2018_August&action=edit&redlink=1 "2018 August \(page does not exist\)"); [ September](/wiki/index.php?title=2018_September&action=edit&redlink=1 "2018 September \(page does not exist\)"); [ October](/wiki/index.php?title=2018_October&action=edit&redlink=1 "2018 October \(page does not exist\)"); [ November](/wiki/index.php?title=2018_November&action=edit&redlink=1 "2018 November \(page does not exist\)"); [ December](/wiki/index.php?title=2018_December&action=edit&redlink=1 "2018 December \(page does not exist\)")

[2019 January](/wiki/index.php?title=2019_January&action=edit&redlink=1 "2019 January \(page does not exist\)"); [ February](/wiki/index.php?title=2019_February&action=edit&redlink=1 "2019 February \(page does not exist\)"); [ March](/wiki/index.php/2019_March "2019 March"); [ April](/wiki/index.php/2019_April "2019 April"); [ May](/wiki/index.php/2019_May "2019 May"); [ June](/wiki/index.php/2019_June "2019 June"); [ July](/wiki/index.php/2019_July "2019 July"); [ August](/wiki/index.php?title=2019_August&action=edit&redlink=1 "2019 August \(page does not exist\)"); [ September](/wiki/index.php?title=2019_September&action=edit&redlink=1 "2019 September \(page does not exist\)"); [ October](/wiki/index.php?title=2019_October&action=edit&redlink=1 "2019 October \(page does not exist\)"); [ November](/wiki/index.php/2019_November "2019 November"); [ December](/wiki/index.php/2019_December "2019 December")

[2020 January](/wiki/index.php/2020_January "2020 January"); [ February](/wiki/index.php?title=2020_February&action=edit&redlink=1 "2020 February \(page does not exist\)"); [ March](/wiki/index.php/2020_March "2020 March"); [ April](/wiki/index.php?title=2020_April&action=edit&redlink=1 "2020 April \(page does not exist\)"); [ May](/wiki/index.php?title=2020_May&action=edit&redlink=1 "2020 May \(page does not exist\)"); [ June](/wiki/index.php?title=2020_June&action=edit&redlink=1 "2020 June \(page does not exist\)"); [ July](/wiki/index.php?title=2020_July&action=edit&redlink=1 "2020 July \(page does not exist\)"); [ August](/wiki/index.php/2020_August "2020 August"); [ September](/wiki/index.php?title=2020_September&action=edit&redlink=1 "2020 September \(page does not exist\)"); [ October](/wiki/index.php?title=2020_October&action=edit&redlink=1 "2020 October \(page does not exist\)"); [ November](/wiki/index.php/2020_November "2020 November"); [ December](/wiki/index.php/2020_December "2020 December")

[2021 January](/wiki/index.php?title=2021_January&action=edit&redlink=1 "2021 January \(page does not exist\)"); [ February](/wiki/index.php/2021_February "2021 February"); [ March](/wiki/index.php?title=2021_March&action=edit&redlink=1 "2021 March \(page does not exist\)"); [ April](/wiki/index.php?title=2021_April&action=edit&redlink=1 "2021 April \(page does not exist\)"); [ May](/wiki/index.php/2021_May "2021 May"); [ June](/wiki/index.php/2021_June "2021 June"); [ July](/wiki/index.php/2021_July "2021 July"); [ August](/wiki/index.php?title=2021_August&action=edit&redlink=1 "2021 August \(page does not exist\)"); [ September](/wiki/index.php?title=2021_September&action=edit&redlink=1 "2021 September \(page does not exist\)"); [ October](/wiki/index.php?title=2021_October&action=edit&redlink=1 "2021 October \(page does not exist\)"); [ November](/wiki/index.php?title=2021_November&action=edit&redlink=1 "2021 November \(page does not exist\)"); [ December](/wiki/index.php?title=2021_December&action=edit&redlink=1 "2021 December \(page does not exist\)")

[2022 SQL Outage](/wiki/index.php/2022_SQL_Outage "2022 SQL Outage")

[2023 January](/wiki/index.php/2023_January "2023 January"); [ February](/wiki/index.php/2023_February "2023 February"); [ March](/wiki/index.php?title=2023_March&action=edit&redlink=1 "2023 March \(page does not exist\)"); [ April](/wiki/index.php?title=2023_April&action=edit&redlink=1 "2023 April \(page does not exist\)"); [ May](/wiki/index.php/2023_May "2023 May"); [ June](/wiki/index.php/2023_June "2023 June"); [ July](/wiki/index.php/2023_July "2023 July"); [ August](/wiki/index.php/2023_August "2023 August"); [ September](/wiki/index.php/2023_September "2023 September"); [ October](/wiki/index.php/2023_October "2023 October"); [ November](/wiki/index.php/2023_November "2023 November"); [ December](/wiki/index.php/2023_December "2023 December")

[2024 January](/wiki/index.php/2024_January "2024 January"); [ February](/wiki/index.php/2024_February "2024 February"); [ March](/wiki/index.php/2024_March "2024 March"); [ April](/wiki/index.php/2024_April "2024 April"); [May](/wiki/index.php/2024_May "2024 May"); [ June](/wiki/index.php/2024_June "2024 June"); [ July](/wiki/index.php/2024_July "2024 July"); [ August](/wiki/index.php/2024_August "2024 August"); [ September](/wiki/index.php/2024_September "2024 September"); [ October](/wiki/index.php/2024_October "2024 October"); [ November](/wiki/index.php/2024_November "2024 November"); [ December](/wiki/index.php/2024_December "2024 December")

[2025 January](/wiki/index.php/2025_January "2025 January"); [ February](/wiki/index.php/2025_February "2025 February"); [ March](/wiki/index.php/2025_March "2025 March"); [ April](/wiki/index.php/2025_April "2025 April"); [May](/wiki/index.php/2025_May "2025 May"); [ June](/wiki/index.php/2025_June "2025 June"); [ July](/wiki/index.php/2025_July "2025 July"); [ August](/wiki/index.php?title=2025_August&action=edit&redlink=1 "2025 August \(page does not exist\)"); [ September](/wiki/index.php?title=2025_September&action=edit&redlink=1 "2025 September \(page does not exist\)"); [ October](/wiki/index.php?title=2025_October&action=edit&redlink=1 "2025 October \(page does not exist\)"); [ November](/wiki/index.php?title=2025_November&action=edit&redlink=1 "2025 November \(page does not exist\)"); [ December](/wiki/index.php?title=2025_December&action=edit&redlink=1 "2025 December \(page does not exist\)")

## OVSA Scientist on Duty

  * Scientist on Duty (SoD): OVSA team members take turns and serve as a SoD to work with our onsite observatory staff on day-to-day observing. They are also responsible for monitoring solar activities and ensuring that the data we collect is of high quality.
  * SoD observing logs ([directory to all logs](https://drive.google.com/drive/folders/1q6-0Z9B0CPFutuTqzmeheEUSJM3tEL2o?usp=drive_link)): 
    * 2024: [May (and before that)](https://docs.google.com/document/d/1QDWw5y4HpcE7CSpzXwftMqQT4FDgNJj-6fRrgWrqdug/edit?usp=sharing), [June](https://docs.google.com/document/d/1Rh2gYBV2E454xVYEv8jx5IXKd1N2Z05ns4dhI2XCE08/edit?usp=sharing), [July](https://docs.google.com/document/d/1beUpp6rgwjqSxKbuHzXIR9hhPrGyi0j-SjtEIeav9Vg/edit?usp=sharing), [August](https://docs.google.com/document/d/1pSzUXW5gd-4cZAR-gglTUVM_J2UHMa4wYJ2AzD4cdEo/edit?usp=sharing), [September](https://docs.google.com/document/d/18pArAP0kRDhXHbty_y3TtrygmWkC2oLn-UD7njIpRIo/edit?usp=sharing), [October](https://docs.google.com/document/d/1Qt6vhrqPAOG7W5Y_tLiod_QgNR1FDyzRxQcg6_oJQd4/edit?usp=sharing), [November](https://docs.google.com/document/d/1pv9-Wne80FCrg0J5BkjOafmof_s3jlnc9HwyzWkIBfU/edit?usp=sharing), [December](https://docs.google.com/document/d/1O5svOVwQZbUON1GMR_8nBR5LAL0M8RM2_zWW4oeBiLk/edit?usp=sharing)
    * 2025: [January](https://docs.google.com/document/d/1pUdSRyWgQa2py1PSLa3CKs_DDqL_SOgx6MMIp4cPnpk/edit?usp=sharing),[February](https://docs.google.com/document/d/18cnIAaeM8UBiYPtsQn7g6TM8mjr57blSoY9l-6ShhwQ/edit?usp=sharing), [March](https://docs.google.com/document/d/1k60i7nabWltnU38I7fGS2uq2-FUe5TMAKcM1BeLIRdY/edit?usp=sharing), [April](https://docs.google.com/document/d/1CMaXBtA1ULNFbzuawYirP913A6dTa68cbYk2a7knirI/edit?usp=sharing), [May](https://docs.google.com/document/d/13Kr8lYfFN9bzgFvCJi6nBUxbQHa3_eTgfjwaCUn3vCs/edit?tab=t.0), [June](https://docs.google.com/document/d/1ptGvQiB6SPgzJ-I6IgJ4bKK-3GPK-4LBpq7BG6sFPSg/edit?usp=sharing), [July](https://docs.google.com/document/d/1XrOonOdwrkSDSWT2CwvzIaw7aRxBA4Sba1GCMRmkDZk/edit?usp=sharing)
  * SoD instructions: 
    * Daily routines: see [SoD Routines](https://docs.google.com/document/d/1_iGnMRRrvb85Z0vT8-LzgQmCOKDSATEuQ0vTsn2C-dc/edit?usp=sharing) for detailed instructions.
    * Instructions for [making quick-look flare spectrograms and movies](/wiki/index.php/Making_quick-look_flare_spectrograms_and_movies "Making quick-look flare spectrograms and movies")

## OVRO-LWA Solar-Dedicated Spectroscopic Imager

The OVRO-LWA (Owens Valley Radio Observatory Long Wavelength Array) has recently been upgraded to include a solar-dedicated beam and two solar imaging modes (slow visibilities of 352 antennas with a 10-s cadence, and fast visibilities of 48 antennas with a 0.1-s cadence). The large collecting area and excellent calibration provide unprecedented high-sensitivity imaging of the quiet Sun and bursts. The array is currently in commissioning and observations are not yet continuous, but they are becoming more so. See the daily realtime data at <http://ovsa.njit.edu/status.php> for **real-time display of the spectrogram and a selection of images** , both updated on a 1-min cadence. 

### Solar-Dedicated Modes

  * Beamformer: the beamformer uses the 256 core antennas to form a synthesized beam of more than 1 degree in size that tracks the Sun from sunrise to sunset. This permits a continuous record of the full-Stokes total flux (without spatial resolution) of the Sun (a dynamic spectrum) with 24 kHz frequency resolution (3072 frequencies from 15-90 MHz) and as low as 1 ms time resolution.

  * Slow Visibility Imaging: in this mode, the entire 352-element array is interferometrically correlated to provide visibilities for imaging at all 3072 frequencies at 10-s time resolution. This is ideal for imaging quiet Sun and slowly-varying emission such as coronal mass ejections and active region variability.

  * Fast Visibility Imaging: in this mode, a subset of 48 antennas (chosen to include mainly outer antennas to maintain good spatial resolution) is interferometrically correlated to provide visibilities for imaging at 768 frequencies (96 kHz frequency resolution) at 0.1-s time resolution. This is ideal for imaging rapidly varying emission such as type II and type III bursts as well as many other solar spectral fine structures.

### Inital Data Access

In its current commissioning state, we try to run the beamformer and imaging pipeline every day in real-time since November 2023 (no latency for beamforming spectrograms and 5-10 min latency for images). Quicklook real-time spectrograms/images can be accessed from <http://ovsa.njit.edu/status.php>. To access data from previous days, use the following links (replace yyyymmdd with the date you desire): 

  * Quicklook beamformer total-power spectrograms: <http://ovsa.njit.edu/lwa-data/1min_spectra/yyyymmdd/>. Check this link for additional daily plots [Daily OVRO-LWA Beamformer Data](/wiki/index.php/Daily_OVRO-LWA_Beamformer_Data "Daily OVRO-LWA Beamformer Data").
  * Quicklook multi-frequency movies at 1-min cadence: <http://ovsa.njit.edu/lwa-data/1min_images/yyyymmdd/movie_yyyy-mm-dd.html>

Note our pipeline processing development is still in the early phase. For example, absolute flux calibrations have not been done for the beamformer spectrograms. Also, artificial effects (including ionospheric refraction effects) are present in the images that cause distortions/shifts. We caution interested users only to consider them for quick-look purposes at this point. Please contact the EOVSA PIs (Dale Gary, Bin Chen) if you intend to use them for science. 

### OVRO-LWA Operation Notes

[OVRO-LWA Operation Notes](/wiki/index.php/OVRO-LWA_Operation_Notes "OVRO-LWA Operation Notes")

## Tohbans

[Trouble Shooting Guide](/wiki/index.php/Trouble_Shooting_Guide "Trouble Shooting Guide")

[Tohban Records](/wiki/index.php/Tohban_Records "Tohban Records")

[Owen's Notes](/wiki/index.php/Owen%27s_Notes "Owen's Notes")

[Caius' Notes](/wiki/index.php/Caius%27_Notes "Caius' Notes")

[Tohban EOVSA Imaging Tutorial A-Z](/wiki/index.php/Tohban_EOVSA_Imaging_Tutorial_A-Z "Tohban EOVSA Imaging Tutorial A-Z")

[Tohban OVRO-LWA Imaging Tutorial](/wiki/index.php/Tohban_OVRO-LWA_Imaging_Tutorial "Tohban OVRO-LWA Imaging Tutorial")

[Tohban Guide to Self Calibration and Imaging for EOVSA](/wiki/index.php/Tohban_Guide_to_Self_Calibration_and_Imaging_for_EOVSA "Tohban Guide to Self Calibration and Imaging for EOVSA")

[Guide to Upgrade SolarSoft(SSW)](/wiki/index.php/Guide_to_Upgrade_SolarSoft\(SSW\) "Guide to Upgrade SolarSoft\(SSW\)")

[Star Pointing Notes](/wiki/index.php/Star_Pointing_Notes "Star Pointing Notes")

## VLA Flare List and Publications

See [this link](http://www.ovsa.njit.edu/wiki/index.php/VLA_Data_Survey#List_of_Jansky_VLA_Solar_Observations) for a list of flare observations made by the [Karl G. Jansky Very Large Array](https://science.nrao.edu/facilities/vla/) (VLA). Below is a partial list of publications that utilize VLA solar data (see also [this NASA/ADS Library](https://ui.adsabs.harvard.edu/public-libraries/ZwbjpLo9RS-viufWEoQ95Q)). 

  * [Luo et al. (2022), ApJ, 940, 137](https://ui.adsabs.harvard.edu/abs/2022ApJ...940..137L/abstract) _Multiple Regions of Nonthermal Quasiperiodic Pulsations during the Impulsive Phase of a Solar Flare_
  * [Battaglia et al. (2021), ApJ, 922, 134](https://ui.adsabs.harvard.edu/abs/2021ApJ...922..134B/abstract) _Multiple Electron Acceleration Instances during a Series of Solar Microflares Observed Simultaneously at X-Rays and Microwaves_
  * [Luo et al. (2021), ApJ, 911, 4](https://ui.adsabs.harvard.edu/abs/2021ApJ...911....4L/abstract) _Radio Spectral Imaging of an M8.4 Eruptive Solar Flare: Possible Evidence of a Termination Shock_
  * [Zhang et al. (2021), ApJ, 910, 40](https://ui.adsabs.harvard.edu/abs/2021ApJ...910...40Z/abstract) _Multiwavelength Observations of the Formation and Eruption of a Complex Filament_
  * [Sharma et al. (2020), ApJ, 904, 94](https://ui.adsabs.harvard.edu/abs/2020ApJ...904...94S/abstract) _Radio and X-Ray Observations of Short-lived Episodes of Electron Acceleration in a Solar Microflare_
  * [Chen et al. (2019), ApJ, 884, 63](https://ui.adsabs.harvard.edu/abs/2019ApJ...884...63C/abstract) _Radio Spectroscopic Imaging of a Solar Flare Termination Shock: Split-band Feature as Evidence for Shock Compression_
  * [Yu & Chen (2019), ApJ, 872, 71](https://ui.adsabs.harvard.edu/abs/2019ApJ...872...71Y/abstract) _Possible Detection of Subsecond-period Propagating Magnetohydrodynamics Waves in Post-reconnection Magnetic Loops during a Two-ribbon Solar Flare_
  * [Chen et al. (2018), ApJ, 866, 62](https://ui.adsabs.harvard.edu/abs/2018ApJ...866...62C/abstract) _Magnetic Reconnection Null Points as the Origin of Semirelativistic Electron Beams in a Solar Jet_

__

  * [Wang et al. (2016), ApJ, 848, 77](https://ui.adsabs.harvard.edu/abs/2017ApJ...848...77W/abstract) _Dynamic Spectral Imaging of Decimetric Fiber Bursts in an Eruptive Solar Flare_
  * [Chen et al. (2015), Science, 350, 1238](https://ui.adsabs.harvard.edu/abs/2015Sci...350.1238C/abstract) _Particle acceleration by a solar flare termination shock_
  * [Chen et al. (2014), ApJ, 794, 149](https://ui.adsabs.harvard.edu/abs/2014ApJ...794..149C/abstract) _Direct Evidence of an Eruptive, Filament-hosting Magnetic Flux Rope Leading to a Fast Solar Coronal Mass Ejection_
  * [Chen et al. (2013), ApJL, 763, 21](https://ui.adsabs.harvard.edu/abs/2013ApJ...763L..21C/abstract) _Tracing Electron Beams in the Sun's Corona with Radio Dynamic Imaging Spectroscopy_

## Radio Data from Around The Heliosphere

  * [_Radio Data_](http://ovsa.njit.edu//wiki/index.php/Radio_Data_from_Around_the_World#Radio_Data_Access)

## Radio Astronomy Lecture Notes

Here is a link to the [Radio Astronomy Lecture Notes](/wiki/index.php/Radio_Astronomy_Lecture_Notes "Radio Astronomy Lecture Notes") adapted from the Phys728: Radio Astronomy graduate-level course Prof. Dale Gary taught at NJIT until Spring 2019. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Owens_Valley_Solar_Arrays&oldid=12786](http://ovsa.njit.edu//wiki/index.php?title=Owens_Valley_Solar_Arrays&oldid=12786)"
