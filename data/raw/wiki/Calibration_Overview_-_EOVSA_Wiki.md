# Calibration Overview - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Calibration_Overview
**Scraped:** 2025-08-05 09:13:00

# Calibration Overview

From EOVSA Wiki

Jump to navigation Jump to search

## Introduction

This document provides an overview on how calibrations will be performed with EOVSA, and what the implications are for monitor, control, pipeline and analysis software. Here is a summary table (Table 1), followed by more detailed discussions. 

Table 1: Summary of EOVSA Calibrations†  
---  
Calibration Type  | Calibration Item  | When Calibrated  | Reference Source  | Analysis Type  | Solution Type  | Applied by  | Criticality   
Pointing Calibration | Antenna pointing errors | Occasional | Sun, sat,   
brgt cosmic src | Offline | Per ant | Control System | High   
System Gain Calibration | Attenuator gain variation | Occasional | ND, Sun | Realtime | Per ant, poln | DPP Stage-2 | High   
Total power response | Occasional | ND, Sun | Offline | Per ant, poln | DPP Stage-2 | High   
System non-linearity | Occasional | ND, Sun? | Offline | Per ant, poln | DPP Stage-2 | Normal   
Spectral similarity | Precalculated | Sat? | Offline | Per ant, poln? | DPP Stage-2 | High?   
Delay Calibration | Fine delay | Precalculated | N/A | Offline | Per ant, poln, IF | Correlator | High   
Delay center | Occasional | Sat, Brgt cosmic src | Offline | Per ant, poln | Correlator | High   
Residual delay | Daily-weekly | Brgt cosmic src | Pipeline | Per ant, poln, IF | Pipeline | High   
Bandpass calibration | System bandpass pattern | Daily-weekly | Brgt cosmic src | Pipeline | Per ant, poln, chan | Pipeline | High   
Reference Gain Calibration | System complex gain   
w.r.t. point source | Daily-weekly | Brgt cosmic src | Pipeline | Per ant, poln, IF | Pipeline | High   
Daily Gain Calibration | Time-dependent   
complex gain   
w.r.t. point source | ~Hourly | cosmic src   
near Sun | Pipeline | Per ant, poln, IF | Pipeline | High   
Polarization calibration | Differential feed rotation | Occasional | Brgt cosmic src | Realtime | Per ant | Correlator | High   
D-term and R-L angle | Occasional | Brgt cosmic src, sat? | Offline | Per ant | Correlator | Normal   
Baseline correction | Antenna position error | Occasional | Multiple cosmic srcs, sats | Offline | Per ant | Correlator | High   
  
†Modified from Gordon Hurford’s list of calibrations (v2010-Nov-16) -- BC, 2016-Sep-24 

## Pointing Calibration

Pointing calibration is antenna-based (has to be done separately for each antenna), and entails an initial determination of pointing errors to create a set of pointing correction coefficients, followed by periodic checks of pointing and possible updating of coefficients as necessary. For KSRBL, initial pointing determination was done optically by mounting an 80 mm optical telescope and small CCD camera on the dish, and doing a single 1-night set of measurements of star fields. This provided excellent determination of correction coefficients around the sky, leaving a simple az-el offset to be determined by solar pointing (because the optical and radio axes were not guaranteed to be parallel). The analysis of the set of optical measurements was complicated, but could and should be automated. However, the assumption is that this only has to be done once during initial commissioning of an antenna. The determination of the az-el offset is then accomplished by a single determination of the solar radio disk position. Note that there will be differences in the radio beam position vs. frequency, so any determination of solar disk position will vary with frequency and must be optimized in some way, probably weighted to the highest frequencies, which have the smaller beam. 

Once the pointing coefficients and offset are determined, they can be optimized and updated periodically by a pointing calibration, and it is that calibration that is further described here. There are several options: (1) determination of the offsets of the solar radio disk (requires the Sun, and may be skewed by active regions—also limited to a single declination), (2) determination of the position of other bright objects such as satellites (valid only at discrete frequencies where such satellites are broadcasting), and (3) interferometric pointing on cosmic sources or planets using one or both of the 27-m dishes. Each of these has merits, and all will likely be implemented. 

### Solar Pointing Calibration

This is based primarily on the scheme developed for KSRBL ([Dou et al. 2009, PASP, 121, 512](http://adsabs.harvard.edu/abs/2009PASP..121..512D)). The pointing offsets for all antennas can be determined simultaneously, and as a function of frequency, by offsetting each antenna in a cross pattern and measuring the total power spectrum. This provides multiple useful parameters: (i) frequency-dependent pointing offsets, which can be surprisingly large, and are necessary for primary beam corrections to all interferometer amplitudes, (ii) direct measurement of the primary beam size and shape, and (iii) a check on overall total power gain calibration relative to that determined interferometrically on cosmic sources. 

This type of pointing can be done quickly (in less than 20 minutes for KSRBL, possibly much faster if we can devise an antenna control scheme that provides accurate scans) and may even be done daily. It does take time from solar observing. Note that an alternative is to take an antenna out of the array and do the pointing scan in a separate subarray while the rest of the array continues observing. A special antenna control sequence (trajectory) would be implemented, along with standard analysis software independent of the pipeline (since it is only total power). The analysis could be part of the monitor/control system, or offline, depending on how regularly it is done and how integral the results are to the overall calibration. This is TBD. 

### Satellite Pointing Calibration

It is possible to track satellites across the sky and apply offsets relative to the tracked position in order to do total power pointing measurements. This unfortunately can be done only at a few spot frequencies, and may be too limiting to be useful. Communication satellites are good for this purpose, but are largely geostationary and often too close together, which severely limits their usefulness. Navigation satellites such as GPS have excellent sky coverage, but GPS operates only at very low frequencies where the primary beam is large, so it remains to be seen whether pointing measurements at such low frequencies can be done precisely enough to be useful. There may be a few other satellites that broadcast at higher frequencies. Given the limited resources, it seems wise to defer consideration of this type of calibration unless and until it becomes clear that it is actually needed. 

### Interferometric Pointing Calibration

Should it be necessary to obtain radio-measured pointing coefficients over the whole sky, only interferometric calibration can work given the lack of sufficiently bright sources for total power calibration. Interferometric calibration will require at least one baseline with a 27-m antenna and a 2-m antenna, and is done by pointing the 27-m antenna at a strong cosmic or planetary source and then pointing the 2-m antenna is a cross pattern similar to the technique used in solar pointing calibration. The phase center tracks the source, and the position of the peak of the interferometer amplitude will provide the pointing offsets. In contrast with solar pointing, which can be done with individual frequency sub-channels, it is likely that the sensitivity of the measurement will limit the measurement to integrated 500 MHz bands. Thus, interferometric calibration will not be very useful for frequency-dependent pointing measurements like the solar pointing, but will be useful for determining some average offset as a function of position over the sky, which is all that is needed for determining the pointing coefficients. This has the advantages of (i) not requiring the Sun, so does not impact time on the Sun, and (ii) obtains pointing offsets over the entire sky rather than being limited to a single declination. Because it uses interferometric results, it will have to come through the correlator and DPP. The analysis would have to be part of the pipeline, or else be done offline. 

Table 2: Summary of Pointing Calibration Options   
---  
Calibration Type  | Impacts Solar Observing?  | Products  | Uses  | Control Requirements  | Analysis Requirements  | Priority   
Solar pointing | Yes | (i) Pointing offset spectrum   
(ii) Primary beam size   
(iii) Solar total power spectrum | (i) Determine pointing corrections at single declination; also amplitude gain coefficients   
(ii) Amplitude gain   
(iii) Solar flux calibration | Antenna trajectory control | Total power analysis could be offline | Essential   
\- best way to get total power gain vs. frequency   
Satellite pointing | No | Pointing offset at a few frequencies | All sky pointing Correction | Antenna trajectory control | Total power analysis in small range of relevant frequencies | Defer   
Interferometric pointing | No | Pointing offset spectrum at 500 MHz resolution | All sky pointing correction | Antenna trajectory control | Pipeline or offline interferometry | Desirable/Needed   
  
## System Gain Calibration (incomplete)

This refers to the periodic (daily?) determination of several system parameters affecting the total power gain: (i) Attenuator nominal values, (ii) noise diode increment, (iii) total power non-linearity. These are simultaneously determined by cycling through all attenuator settings, once with noise diode off and again with noise diode on, and recording the total power level (separately for each antenna). The exact scheme to be followed depends on the system design. This figure summarizes all the gain control "knobs" in the analogue and digital system. 

[![](/wiki/images/1/1a/Eovsa_gain_controls.png)](/wiki/index.php/File:Eovsa_gain_controls.png)

[](/wiki/index.php/File:Eovsa_gain_controls.png "Enlarge")

EOVSA Gain Control "Knobs"

This attenuation scheme uses the Day/Night calibrator as a single setting, while the others are variable in 1 dB steps. The Day/Night attenuator difference of 17 dB is probably too much. The solar variation attenuator in the front end applies to the entire 1-18 GHz RF band, and sets the overall power level to keep the optical link in its linear range. Note that strong fluctuations in a narrow band (e.g. spike bursts) will have less effect when integrated over the entire RF band, so changes to this attenuator should normally be slow and steady during solar bursts. In the back end, the attenuation is applied in the IF (650-1150 MHz) chain. The first attenuator is for leveling the receiver in the absence of bursts. Once leveled, the settings for each receiver will vary with IF band, but will be fixed in time. The second attenuator is for maintaining the output level during solar bursts, and it is this attenuator that will need to be controlled on a relatively fast timescale. Each attenuator will need to have each of its steps calibrated. The two back end attenuators will be in a single integrated assembly, and are best measured offline using test equipment. Assuming adequate temperature control, they should be stable, and changes would indicate a failure of the assembly. Thus, a maintenance test can be conducted periodically to check their values, but it should not be necessary to have a daily gain calibration procedure that checks every IF attenuation setting. 

We therefore assume that only the two front-end attenuators will be checked, through a gain calibration procedure, on a regular basis. Will it be necessary to do the procedure in different IF bands, to check for frequency-dependent variations in attenuation? If such variations can be characterized once in the lab, it may be possible to do the measurement in a single, RFI-free band chosen as the standard one for the measurement. 

### Observational Procedure

In the current OVSA gain calibration scheme, the antennas are pointed at blank sky and the RF attenuation is switched to each setting in turn, switching the noise diode on and off during the measurement. Each IF band is also measured, but the results are combined to give a single attenuation value for each setting, i.e. no frequency-dependent variations are considered. Note that for the current OVSA it is possible to insert so much attenuation (55 dB) that the front-end signal can be assumed to be zero, allowing for receiver offsets to be determined. The maximum attenuation in Fig. 2 is only 36 dB (less if the Day/Night attenuator is reduced). 

## Delay Center Calibration

Delay center calibration involves sweeping the delays around their nominal value while observing a strong source interferometrically, in order to determine the optimum setting for the delays. For OVSA, the optimum delay is determined by a peak in the amplitude on a particular baseline, whereas for EOVSA it will more likely be done by flattening the phase response across the bandpass. For EOVSA, the current plan is to implement delays in the correlator, so sweeping the delays would be implemented there. 

### Delay Tracking

It is useful to look at some issues related to delay tracking (ref. the A. R. Thompson FASR memo, “FASR_Delay_Fringe_Phsw.pdf”). For the currently considered design, the ADCs will operate at a clock rate of 1200 MHz, or sample time τs = 0.833 ns, so coarse delays of that step-size will be trivial to implement using a shift register. In tracking the delay, we would change the delay when the delay error is, say, +1/2 τs, making it then -1/2 τs, so this is the maximum delay error. It is interesting that the bandwidth and the sample time are not independent, but rather obey the Nyquist criterion 1/τs = 2Δν, so that Δντs = 1/2. Assuming that the IF band ranges from 0 to Δν (600 MHz in our case) the maximum phase slope across the band, for delay error τ, is Δφ = 2πτΔν = π/2, where τ=1/2τs was used. Therefore, the highest IF frequency channel’s phase will vary linearly with time between -π/2 and +π/2. The rate of delay obeys the equation 

d τ d t = Ω B cos ⁡ ( h ) / c {\displaystyle {\frac {d\tau }{dt}}=\Omega B\cos(h)/c} ![{\\displaystyle {\\frac {d\\tau }{dt}}=\\Omega B\\cos\(h\)/c}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7ae35eb9607bcd1527da7bd6f3796283d2b3e984)

where Ω = 7.27×10-5 rad/s is the rotation rate of the Earth, B is the baseline length (maximum about 1.5 km), and h is the hour angle. The maximum rate is then about 0.364 ns/s, so for sample time τs = 0.833 ns we would have to step the delay once every 2.29 s for the worst case. To keep the phase of the highest channel within 1 degree, the phase correction must be updated every 2.29 s/90 = 25 ms. It appears that this worst case can be adequately handled by correcting the phase at the output of the correlator, after the 20 ms accumulation. Note also that inserting the delays in the IF causes fringe rotation (natural fringes) at a maximum fringe rate νf = (0.364 ns/s)(18 GHz) = 6.6 Hz. Averaging over a time τav = 20 ms results in an amplitude given by sinc(νfτav) = 0.97 in the worst case (18 GHz, at noon, on the longest baseline). This suggests that we might get away with applying fringe stopping at the output of the correlator as well, with a possible small amplitude correction applied. UPDATE: The correlator coarse delays will be set only on a 1 s tick, therefore the delay can be an extra ½ s early or late, giving an error in the worst case of ±0.598 ns (this is ±0.416 ns ± (½ s) (0.364 ns/s), or ±0.72τs). 

### Observational Procedure

The procedure for taking delay center calibration data is to track any strong interferometric point source and sweep the coarse delays in a TBD manner (i.e. track the geometric delay and apply a delay offset, and sweep the offset over some window Δτ, from – Δτ/2 to +Δτ/2) so that the phase slope across an IF band (after the corrections described above for nominal phase slope and fringe rotation) can be obtained. The delay that results in the flattest slope is the correct one. An alternative is to vector average the data over the IF band and maximize the amplitude, which would be a more sensitive measure, but could be adversely affected by RFI. This works for any band, so it should be possible to find an RFI-free band where the chosen point source is strongest. Note that the delays are antenna-based, so they have to be swept differentially (it is the difference in delay between antennas that matters). When using a cosmic source, it is enough to set one of the 27-m antennas as the reference antenna and sweep the delays of each of the others simultaneously, but an alternative is to sweep the two 27-m delays in opposite directions so that all large-small baselines can be examined separately. It is probably worthwhile to check the delays on an isolated solar active region, when available, so that small-small baseline delays can be examined. No doubt there is a clever algorithm to make sweeping of delays most efficient, so that multiple delay centers can be determined simultaneously. The duration of the calibration observation will be set by the integration time needed for an acceptable RMS deviation for the individual measurements at each delay step, and the number of steps over which the delay is swept. The delay center should be very stable, and once determined only changes to hardware or physical cables should occasion the need for remeasuring the delays. UPDATE: We have learned that on restarting a ROACH board it comes up with an indeterminate 4τs ambiguity in delay due to the sampling (ADC) clock being 4 times the FPGA clock. This means that WHENEVER A ROACH IS REBOOTED a new delay calibration is needed. A suggested methodology is to go to the Sirius XM Blues geosynchronous satellite at 115 W longitude and observe its S band (2332.5-2345.0 MHz) transmission, to determine the optimum delay by minimizing the phase slope. It will not be necessary to sweep the delay for this, however. The phase slope over 12.5 MHz will be 3.75Δn degrees, where Δn (ranging from -3 to 3 in units of τs) is the number of steps by which the delay center has changed since the previous measurement. A special pipeline procedure would be created to do the analysis and update the delay center tables. [BC 9/25/2016: We can also use strong cosmic calibrators to obtain the delay solutions.] 

### Analysis Procedure

In the case of delay calibration on a cosmic source with the 27-m antennas, a full delay calibration will result in 2(N - 2) + 1 measurements (27 for N = 15) to determine N - 1 (14 for N = 15) delays (one reference antenna is set to zero delay). The set of over-determined measurements can be used to find a least-squares solution. If only one delay needs to be determined (due, for example, to a hardware change affecting only one antenna), then a subarray with the one 2-m antenna and two 27-m antennas can be used, and only the affected antenna needs to be swept, resulting in 2 measurements to determine one delay. Nevertheless, it is probably good practice to measure all of the delays on some periodic schedule. In the case of delay calibration on a solar active region, with no 27-m antennas, both the delay control and analysis are more complicated. [BC 9/25/2016: Now that we only have one 27-m antenna, so our measurements are no longer over-determined: 13 measurements to determine 13 delays (it would be convenient to just set the 27-m antenna to zero delay). In practice, we can still yield plausible solutions based on observation of a strong cosmic source (e.g., 3C84).]

Table 3: Summary of Delay Calibration   
---  
Calibration Type  | Impacts Solar Observing?  | Products  | Uses  | Control Requirements  | Analysis Requirements  | Priority   
Full array delay calibration on cosmic source | No | Delay pattern for each large- small baseline over an IF band | Determine optimum delay centers | Control 27-m delays in correlator (separately from geometric delay tracking) | Special analysis routine to find/solve for optimum delay solution | Essential   
Single antenna delay calibration on cosmic source | No | Delay pattern for baselines A- n and B-n,* where n is the small antenna | Determine optimum delay center for one antenna | Control 27-m delays in correlator (separately from geometric delay tracking) | Simple analysis routine to find optimum delay | Needed, could be deferred   
Full solar array delay calibration on solar active region | Yes | Delay pattern for each small- small baseline over an IF band | Verify delay centers on small-small baselines | Control all delays in correlator (separately from geometric delay tracking) | Special analysis routine to find/solve for optimum delay solution | Good to have, can be deferred   
  
## Bandpass Calibration

Bandpass calibration refers to determining the relative complex gain and offset (system noise) as a function of subchannel across an IF band. It is measured on each large-small baseline interferometrically by observing a bright point source and integrating to obtain suitable signal-to-noise for a reliable measurement. We note that measuring the bandpass using small-small baselines is out of the question due to the low sensitivity on those baselines. The data are then analyzed to determine the resulting antenna-based complex gains. Offsets are determined by inserting full attenuation off-source, and could be considered a separate calibration, although it should be performed at the time of the bandpass calibration. Note that bandpass calibration must be measured separately for each IF band. Things that affect the bandpass are gain slopes due to frequency-dependent components/cables, higher-order ripples due to standing waves, and IF bandpass filter shape. If standard science bandwidths are used, the bandpass calibration could be done by integrating over the science subbands, to improve signal-to-noise and shorten the required duration of the observation. To maximize signal-to-noise, only large-small baselines (those with one 27-m antenna and one 2-m antenna) will be used. 

### Observational Procedure

The entire array tracks a bright cosmic source, one IF band at a time, integrating on each band until good signal-to-noise is achieved. The procedure is repeated for each of the 34 bands. 

The sensitivity per polarization of a single baseline is given by 

σ i j = 4.97 T s y s , i T s y s , j D i D j Δ t s Δ ν M H z J y {\displaystyle \sigma _{ij}={\frac {4.97{\sqrt {T_{\rm {sys,i}}T_{\rm {sys,j}}}}}{D_{i}D_{j}{\sqrt {\Delta t_{\rm {s}}\Delta \nu _{\rm {MHz}}}}}}~{\rm {Jy}}} ![{\\displaystyle \\sigma _{ij}={\\frac {4.97{\\sqrt {T_{\\rm {sys,i}}T_{\\rm {sys,j}}}}}{D_{i}D_{j}{\\sqrt {\\Delta t_{\\rm {s}}\\Delta \\nu _{\\rm {MHz}}}}}}~{\\rm {Jy}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e912afcea48e26fa11103b2c7d9252f569019be1),

where  T s y s , i {\displaystyle T_{\rm {sys,i}}} ![{\\displaystyle T_{\\rm {sys,i}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/070b21923f5d7a8c9129a9abc72e60f31fa1ea8b) and  D i {\displaystyle D_{i}} ![{\\displaystyle D_{i}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/9f07b53d3212e08ca316a536c8aac0bbefa79ee1) are the system temperature (K) and diameter (m) of the ith element, and an antenna efficiency of 0.5 has been assumed. If the system temperature of the cooled 27-m receivers is 30 K, and that of the 2-m receivers is 400 K, the sensitivity on baselines between a 27m-2m pair is: 

σ l , s = 9.6 Δ t s Δ ν M H z J y {\displaystyle \sigma _{l,s}={\frac {9.6}{\sqrt {\Delta t_{\rm {s}}\Delta \nu _{\rm {MHz}}}}}~{\rm {Jy}}} ![{\\displaystyle \\sigma _{l,s}={\\frac {9.6}{\\sqrt {\\Delta t_{\\rm {s}}\\Delta \\nu _{\\rm {MHz}}}}}~{\\rm {Jy}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/3c92b0cca98d231c0009826dfb45b5ef33fbcd02),

it will take about 23 s with 10:1 signal to noise ratio on 3C84 on each 1-MHz-wide channel (assuming ~20 Jy flux density). Probably the higher frequency bands will have lower signal to noise, so will take longer, but these are also the bands with the wider science bandwidths. A 50:1 signal to noise ratio measurement (rms phase error about 1.1 degree) on all 34 bands can be done in 6 hours. 

### Analysis Procedure

The Data are calibrated to correct for pointing offsets vs. frequency (obtained from Pointing Calibration, see 1 above), and the set of amplitudes and phases on each large-small baseline are obtained. Denoting the large antennas as a, b, and the nth small antenna as n, the antenna-based bandpass amplitude as a function of subchannel k for antenna n is 

A n ( k ) = A a n 2 ( k ) A b n 2 ( k ) A a b 2 ( k ) {\displaystyle A_{n}(k)={\sqrt {\frac {A_{an}^{2}(k)A_{bn}^{2}(k)}{A_{ab}^{2}(k)}}}} ![{\\displaystyle A_{n}\(k\)={\\sqrt {\\frac {A_{an}^{2}\(k\)A_{bn}^{2}\(k\)}{A_{ab}^{2}\(k\)}}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/cc6ae8ad9b8a8b9d0e69d3c2c6bb8d5a5b3e3a22)

where  A i j 2 = A i j A i j ∗ {\displaystyle A_{ij}^{2}=A_{ij}A_{ij}^{*}} ![{\\displaystyle A_{ij}^{2}=A_{ij}A_{ij}^{*}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f7c98df61ec701ccdb0e7957f8389d7c473ff893) is the square of the amplitude measured on baseline i, j. There appears to be no way to measure the bandpass of the large dishes separately (without small-small baselines), but perhaps they are never needed. 

Assuming we take one of the large antennas (denoted antenna a) as the reference antenna, which we can do without loss of generality, the antenna-based bandpass phase is just that measured on the a-n baseline,  ϕ n ( k ) = ϕ a n ( k ) {\displaystyle \phi _{n}(k)=\phi _{an}(k)} ![{\\displaystyle \\phi _{n}\(k\)=\\phi _{an}\(k\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/af7c8312d732f6fe359b8f7b494a56c964cec37d). Note that  ϕ b n ( k ) {\displaystyle \phi _{bn}(k)} ![{\\displaystyle \\phi _{bn}\(k\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0293ddae1f7807d93179a4500193045ebf2c3635) is useful primarily to verify phase closure. The deviation from closure phase  δ ϕ c l ( k ) = ϕ a b ( k ) + ϕ b n ( k ) − ϕ a n ( k ) {\displaystyle \delta \phi _{cl}(k)=\phi _{ab}(k)+\phi _{bn}(k)-\phi _{an}(k)} ![{\\displaystyle \\delta \\phi _{cl}\(k\)=\\phi _{ab}\(k\)+\\phi _{bn}\(k\)-\\phi _{an}\(k\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/53c9916e995b45d4ecdd1f08f394e9d476b250b0) would be used as a measure of the uncertainty in  ϕ n ( k ) {\displaystyle \phi _{n}(k)} ![{\\displaystyle \\phi _{n}\(k\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e7355a8aeb12b7160497e326d9164f91d27a76cf). Given sufficient signal to noise, the bandpass amplitude and phase can be determined for each subchannel k, but if that is not possible, it is sufficient to determine this calibration for each science subband. The product of this analysis is the normalized shape and relative phase variation across the band, which should change slowly (assuming thermal variations of standing waves is well controlled). The overall complex gain will be determined by more frequent measurements integrated over each entire IF band (both reference and daily gain calibration). Note that the Miriad task mfcal performs the required analysis, but no doubt assumes data for all baselines, whereas we have only a small subset of baselines. It is worthwhile to try mfcal on simulated data with some very noisy baselines to see if it comes up with a correct solution. Note also that the total power bandpass response for each antenna, obtained from section 1, could be relevant to compare with the amplitude bandpass response. [BC 2016-Sep-26: CASA's bandpass task may work on a subset of baselines. Need to be tested for only using baselines of one antenna, though.]

[BC 2016-Sep-26: Now that we only have one 27-m antenna. It means that we need to solve for the complex gain for each channel on each 2-m antenna, totaling 13 x nch solutions (where nch is # of spectral channels), from 13 x nch measurements of complex visibilities on all 13 small-large baselines. The measured visibilities can be described as: 

G a n ( k ) = G a ( k ) G n ∗ ( k ) = A a ( k ) A n ( k ) A a n ( k ) e i ( ϕ n ( k ) − ϕ a ( k ) + ϕ a n ( k ) ) {\displaystyle G_{an}(k)=G_{a}(k)G_{n}^{*}(k)=A_{a}(k)A_{n}(k)A_{an}(k)e^{i(\phi _{n}(k)-\phi _{a}(k)+\phi _{an}(k))}} ![{\\displaystyle G_{an}\(k\)=G_{a}\(k\)G_{n}^{*}\(k\)=A_{a}\(k\)A_{n}\(k\)A_{an}\(k\)e^{i\(\\phi _{n}\(k\)-\\phi _{a}\(k\)+\\phi _{an}\(k\)\)}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/3edce3b39f9912afd74841a2eb6478c0292ccdec)

where  A i ( k ) {\displaystyle A_{i}(k)} ![{\\displaystyle A_{i}\(k\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/207d39cabed002b9ff7b4502e5bb135bd5c6d5e2) and  ϕ i ( k ) {\displaystyle \phi _{i}(k)} ![{\\displaystyle \\phi _{i}\(k\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/185b043ed4c5bc0efaa1a190366c6e90270a3873) are amplitude and phase of each antenna at a given spectral channel k, and  A a n ( k ) {\displaystyle A_{an}(k)} ![{\\displaystyle A_{an}\(k\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/109ce0abe2b20a59b46afe869f791af8bdbfd47c) and  ϕ a n ( k ) {\displaystyle \phi _{an}(k)} ![{\\displaystyle \\phi _{an}\(k\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/eaf8f3bcb17666270cc240d8975fa2e9b81f0422) are the corresponding baseline error, or closure error. There is no over-determined measurements, unfortunately, so we have to assume no closure error and solve for the antenna-based amplitudes and phases. We also need to use the 27-m antenna as the reference and set its amplitude to unity and phase to zero for all channels.]

Table 4: Summary of Bandpass Calibration   
---  
Calibration Type  | Impacts Solar Observing?  | Products  | Uses  | Control Requirements  | Analysis Requirements  | Priority   
Full spectrum bandpass calibration | No | Amplitude and phase on each large-small baseline over each spectral channel | Determine the antenna-based complex gain variations across each IF band | Relatively longer integration time on each IF band to obtain adequate SNR | Miriad task mfcal may work, CASA task bandpass may work | Needed for detailed science investigations, could be deferred   
  
## Reference Gain Calibration

Reference complex gain calibration refers to determining the "system" amplitude and phase with high precision as a function of IF band (i.e. integrated over each 500 MHz IF band). The idea is that an observation of a calibrator for phase calibration, when corrected by the reference phase calibration, will yield a linear phase slope as a function of frequency, so that only the phase slope measurement is required for the calibration solution. 

### Observational Procedure

Given the speed with which a bandpass calibration (section 5) can be obtained, and the basic similarity between that and the reference calibration, the same basic observational approach can be taken, and only the analysis differs in some details. For integration over 500 MHz, the entire reference calibration can be done on 3C84 in 34 bands, at 50:1 signal to noise ratio, in less than 60 s on large-small baselines (c.f., sensitivity equations in section 5). However, it is wise to measure the reference complex gain on all baselines and seek a traditional gain solution. [BC 9/24/2016: However, optimum delay and bandpass corrections should be applied prior to averaging over these channels.] 

For small-small (2m-2m) baselines, it becomes: 

σ s , s = 451 Δ t s Δ ν M H z J y {\displaystyle \sigma _{s,s}={\frac {451}{\sqrt {\Delta t_{\rm {s}}\Delta \nu _{\rm {MHz}}}}}~{\rm {Jy}}} ![{\\displaystyle \\sigma _{s,s}={\\frac {451}{\\sqrt {\\Delta t_{\\rm {s}}\\Delta \\nu _{\\rm {MHz}}}}}~{\\rm {Jy}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/759ac10015c893953799fe08488b06375a92f384),

In principle, this permits a 10:1 signal to noise measurement on 3C84, integrated over the 500 MHz IF band, in about 100 s. [BC 9/24/2016: Again, we need perfect delay/bandpass solutions to flatten the phases before combining the channels. In reality, we would need considerably longer time to achieve this].  A one-hour reference calibration would yield a 50:1 signal to noise measurement on small-small baselines [BC: This is an ideal scenario]. Note that the 3C84 flux density spectrum has to be calibrated by reference to a calibrator standard, either 3C286 or 3C48. Both are weaker than 3C84, but only the large-small baselines are needed, so determining the 3C84 spectrum can be done in a very short time, of order 10 minutes. 

### Analysis Procedure

It would be fruitful to analyze separately the large-small baselines (as in section 3.2, above) to get a reference gain calibration, and the small-small baselines to get an independent calibration by traditional means, and compare. If the two are identical, then the time-consuming measurement of the small-small baselines can be abandoned except as a check on system performance. Reasons they may be different would be related to the correlation efficiency and correlator malfunction, or possibly software errors in the DPP. 

Table 5: Summary of Reference Gain Calibration   
---  
Calibration Type  | Affect Solar Observing?  | Products  | Uses  | Control Requirements  | Analysis Requirements  | Priority   
Band-by-band reference gain solution  | No  | Amplitude and phase on each small-small baseline, integrated over each 500 MHz IF band  | (i) Determinetheantenna- based complex gain integrated over each IF band   
(ii) Compare large-small gain solution with small-small gain solution  | 27-m antenna required  | Standard Miriad/CASA task for antenna-based gain solution  | Essential   
  
## Daily Gain Calibration

This refers to the periodic measurements of gain calibrators during the day, and needs to be done only on the large-small baselines. A calibrator is chosen relatively nearby to the Sun, so that the local sky conditions are sampled. After correcting for the reference calibration, the phases should form a linear phase slope with frequency [BC 9/24/2016: This implies a residual multi-band delay. What is the source of this residual delay? Are we confident enough on this linearity?]. The task of the daily calibration is to obtain this phase slope as a function of time in order to permit two-point interpolation of the phase correction for intervening solar data. Note that it should not be necessary to obtain the phase in every band, unless the phase slope proves to be nonlinear. [BC 9/24/2016: But it is probably a good idea to do this for every band in the first place.]. Therefore, the phase slope can be determined over a relatively restricted range of frequencies, to avoid the problem of the widely different primary beam vs. frequency. With OVSA we observe between about 2.8 – 10 GHz. [BC 9/24/2016: How does a varying primary beam vs. frequency affect phases from a point-source calibrator?

### Observational Procedure

A cosmic point source nearby to the Sun will be chosen by some automated means, and once per hour or so the array will automatically slew to the source, take data for a set amount of time sufficient for good signal to noise on selected bands, and then go back to the Sun. The distance to slew will vary depending on what frequency range is chosen for calibration, and the nearness of a suitable calibrator. Point source calibrators brighter than 4 Jy are shown in Fig. 1, from Stephen White’s FASR memo on source counts. 

[![](/wiki/images/f/f4/Eovsa_calib_sources.jpg)](/wiki/index.php/File:Eovsa_calib_sources.jpg)

[](/wiki/index.php/File:Eovsa_calib_sources.jpg "Enlarge")

Figure 1: Positions in the sky of point source calibrators > 4 Jy at 4.5 GHz (left) and 8.0 GHz (right). The path of the Sun +/- 20 degrees is shown. At all times there are suitable calibrators within 45 degrees of the Sun.

It appears that there are plenty of sources available, with worst case slew distances of about 45 degrees. With a slew speed of 30 degrees per minute, the time off Sun is maximum 3 minutes + time on source. With a 500 MHz bandwidth, it is possible to obtain 20:1 signal to noise in each of 10 IF bands in <50 s. We also note that, although the spec of the 27-m dishes is only 18 degrees/minute, it should be possible to have them tracking the calibrator continuously. Thus, we can make a 20:1 measurement in about 5 minutes, which should permit calibrations every hour if needed. 

### Analysis Procedure

This calibration observation will require a specially written routine, or perhaps a script, that will average the data over the relevant 500 MHz IF bands (say 10 different bands between 2.5 and 10 GHz) on the large-small baselines, apply the reference calibration, and fit phase slopes to all of the “phase spectra.” [BC 9/24/2016: Before doing this, we should test it and see if this is really the case.]. For large antennas designated a, b and small antenna n, the phases should close, i.e. , and certainly the phase slope should be forced to close. Assuming 27-m antenna a is the reference antenna, the phase slope to apply to antenna n is that fitted to the a-n baseline. The calibration should be analyzed by the pipeline immediately after the calibration is finished, so that its results can be applied immediately during the following solar scan. 

[BC 9/24/2016: Shall we solve for the amplitude (per antenna, per IF) as well? Although we have corrected most of the system amplitude during reference gain calibration, there is likely time-dependent amplitude fluctuation as well.]

Table 6: Summary of Daily Gain Calibration   
---  
Calibration Type  | Affect Solar Observing?  | Products  | Uses  | Control Requirements  | Analysis Requirements  | Priority   
Daily phase calibration in 10 (or so) IF bands  | Yes  | Phase in each IF band on each large- small baseline, integrated over each 500 MHz IF band  | Determine the linear phase difference since the last reference calibration  | 27-m antenna required; Possibly requires subarray coordination if 27- m are to track cal source continuously  | Special routine or script  | Essential   
  
Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Calibration_Overview&oldid=297](http://ovsa.njit.edu//wiki/index.php?title=Calibration_Overview&oldid=297)"
