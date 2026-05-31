# Attenuation and Level Control - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Attenuation_and_Level_Control
**Scraped:** 2025-08-05 09:12:51

# Attenuation and Level Control

From EOVSA Wiki

Jump to navigation Jump to search

## Introduction

The setting of attenuation and scale factors in the EOVSA system is critical for several competing criteria: 

  * Keeping components within a safe operating range in order to avoid damage to components
  * Keeping the various amplifier stages in both the frontend module (FEM) and downconverter module (DCM) within a linear operating range
  * Keeping the two polarization channels (H and V) matched and balanced
  * Keeping the optical link within a linear range
  * Keeping the 8-bit digitizer from clipping
  * Keeping the power and power-squared products output by the correlator in a range appropriate to correct spectral kurtosis calculation
  * Keeping the pre-correlation power levels in the appropriate range for 4-bit down-sampling

This memo examines each of these issues in turn, and offers explicit guidelines for attenuation and level control, based on experience with the prototype system. The control system must incorporate these guidelines in a manner that both meets the above criteria and also allows a reasonable scheme for calibration that is as simple and practical as possible. 

## Keeping Components Safe

When the prototype system was designed, we had little information about the RFI environment, and hence were working with a range of likely 1-18 GHz RF signal strengths without consideration of RFI. Tests with the prototype (see the recent “EOVSA RFI Environment and Polarization” memo) indicate that the signal levels are dominated by the H-polarized PCS signal near 1.9 GHz, which varies greatly with direction of the antenna. The prototype was also constructed with considerably more gain than it was designed for, which has exacerbated the problem of potential damage to components. We have since modified the prototypes to bring the overall gain down closer to design levels, but there still exists the potential for RFI-related damage to components with certain combinations of attenuation. Of course, there is also the possibility of greatly enhanced signals during strong solar flares. 

In the regions of the sky with the minimum RFI, our tests indicate that the input power, Pin, is about -62 dBm (based on Christian Holmstedt’s spreadsheet “EOVSA FE Simplified Power Levels and Noise,” i.e., more than a factor of 10 higher than our minimum design expectation of -74 dBm. This is no doubt due to the residual RFI that is present even at this minimum level. At places where the RFI is maximum, the power Pin is at least 10 times higher, or of order -50 dBm. According to Christian’s spreadsheet, damage to the prototypes can occur when Pin = -48 dBm, if both attenuators in the FEM are set to zero. Thus, from this perspective alone the optical link can become damaged at any time by pointing the antennas at the “wrong” location in the sky. At this same setting, the 3rd stage amplifier is overdriven at as low as Pin = -64 dBm (i.e. over the entire sky), while the 2nd stage amplifier is overdriven at Pin = -50 dBm. The situation is slightly worse for the production system. This implies that the attenuation state with both attenuators set to zero must be avoided at all times, and the control system needs to explicitly prevent this. In the absence of solar flares, it is safe for the 2nd stage amplifier and optical transmitter to set the 1st FEM attenuator to 9 dB, so it is recommended that this be the minimum allowed setting. If the 2nd FEM attenuator is set to 0 dB, there is a potential to overdrive the 3rd amplifier in the region of strongest RFI, but not to a damaging level. Still, it is safest to use a non-zero setting at any time the antennas are slewing from one source to another. 

For safety reasons also, the frontend attenuation should be under active control at any time the antennas are pointed at the Sun, so that large flares do not occur that can damage the frontend components. 

As for damage to the components in the DCM, or further down the chain, we know that this is possible since we actually did damage the digitizer boards in the correlator due to excess IF power. However, this was due to misunderstanding the nature of the 20 dB amplifier on the digitizer boards, and for the prototype systems new fixed attenuators have been added between the DCMs and digitizers that should eliminate the potential for damage. Provided the frontend systems are properly in range, it is not expected that it will be possible to damage any component in the DCM or digitizer boards, regardless of the setting of the DCM attenuator. However, this should be checked for the case of tuning to band 2 (the band with the 1.9 GHz PCS signal). For the production systems (and the prototype systems will also be retrofitted), the final IF amplifier will be eliminated so that the fixed attenuation can be removed without causing damage to the digitizers. 

## Keeping the Amplifiers in their Linear Range

This criterion is more stringent than the above case of damage, and it is best to actually devise a measurement method for linearity of each stage (not yet done). However, at least for the FEM it is possible to get some idea of linearity based on manufacturer’s specifications, as implemented in Christian Holmstedt’s spreadsheet “EOVSA FE Simplified Power Levels and Noise.” If the minimum 1st attenuation setting is 9, as suggested in the previous section, then the salient points are that the 2nd-stage amplifier remains linear until Pin = -42 dBm, while the 3rd-stage amplifier is linear at least 10 dB above the optimum setting for Pout = 3 dBm to the optical transmitter. So as long as the 2nd attenuator is set to maintain optimum Pout, there is a margin of 10 dB before the 1 dB compression point. Likewise, if the 1st attenuator is set to 18 dB, the 2nd-stage amplifier will remain linear at all likely values of Pin, and the 3rd-stage amplifier will remain linear with the same 10 dB margin. 

In the DCM, there are no adjustments relative to the input, except for the IF attenuator at the very output of the DCM, so as long as the FEM is in range, the DCM should not experience nonlinearity internally. 

## Keeping the H and V Polarizations Matched and Balanced

As discussed in the recent “EOVSA RFI Environment and Polarization” memo, it is important that after balancing the power levels, the attenuations applied at every point in the chain must be the same in H and V channels. In other words, if a 3 dB step is put into the H channel, the same 3 dB step must be put into V. For this reason, this memo anticipates that the attenuators will first be set in the system to maintain power balance at the minimum Pin state (i.e. in a region of the sky with the minimum RFI), and then all further adjustments of attenuator state will be done simultaneously in the two polarization channels. This means that if for some region of the sky the two channels differ in power level, the one with maximum power must drive the choice of attenuation. As the polarization memo describes, we have found that the RFI affecting the power level is H-polarized, hence H and V polarization levels do NOT have the same behavior over the sky. However, we are contemplating reorienting the feed by rotating it by 45 degrees so that both hands respond in the same way to the RFI in most regions of the sky. This memo assumes that has been done, in which case the power in the two channels should vary together except when the antenna is pointed near the zenith. In any case, it remains true that the attenuation settings should be chosen based on the polarization channel with the highest power. 

## Keeping the Optical Link in its Linear Range

By doing some measurements with CW signals at various frequencies, Christian Holmstedt has determined that the FEM output power (Pout) setting that gives the most linear response in the optical link increases with frequency, but at each frequency is linear in a range roughly 6 dB wide. The most critical frequency band for linearity is at low frequencies, where the bulk of the RFI occurs, since the most deleterious effect of nonlinearity is to produce harmonics of strong signals. Therefore, it makes sense to maintain the FEM output power near the optimum value for low frequencies, which has been determined to be Pout = 3 dBm. At 18 GHz, the optimum Pout ~ 8 dBm. With the prototype system, this corresponds to a detector voltage level of about 0.5 V. The conversion from detector voltage to corresponding output power in dBm will vary from one detector to another, and must be obtained from calibration, but it is about 0.065 V / dBm. Note that if the power is set to 3 dBm, and we use 3 dB attenuation steps, then the output power will range from 1.5 dBm to 4.5 dBm, i.e. when the power falls below 1.5 dBm then 3 dB will be removed and the power will rise to 4.5 dBm, and likewise when the power exceeds 4.5 dBm then 3 dB will be inserted. The main function of the attenuation control in the FEM will be to keep Pout in this range. 

The overall attenuation state has been conceived to be represented by a single number, which is an index into a lookup table of possible attenuations involving both FEM attenuators and the DCM attenuator. While convenient as a lookup device, the different character of the various attenuations suggests the following: a “fixed” table of attenuation states will represent the leveling of each channel in the minimum RFI state. This table is “fixed” in the sense that it will change only when a new leveling calibration suggests that it is necessary. It is hoped that the stability of the system will be such that this leveling only rarely needs to be updated. There will be such a table for each of the H and V polarizations in the FEM, and likewise for each channel in the DCM. All calibrations will be done with these attenuations set (plus any required additional attenuation steps). Table 1 shows the FEM settings for Antennas 1 and 7 (the only two active antennas at the moment). There will also be a DCM level setting table, which will have entries for each of the 34(35) IF bands, but this cannot be determined until we get the KATADC boards repaired and reinstalled. For now, we will use a fixed DCM attenuation level of 2 dB, which has been arrived at by examining the digitizer overflow values in the correlator packet header. 

Table 1: Frontend Level-Setting Attenuation   
---  
Antenna   
Number  | H Attn (dB)  | V Attn (dB)   
First Attn  | Second Attn  | First Attn  | Second Attn   
1  | 9  | 1  | 9  | 2   
7  | 9  | 1  | 9  | 2   
  
There will then be a table of 3 dB attenuation steps for the FEM that is common to both H and V, so that after leveling, all attenuations are applied equally to H and V, and only in 3 dB steps, and likewise there is a table of 2 dB steps in the DCM. A suggested definition of these tables is shown in Table 2 for FEM, which assumes the minimum “fixed” attenuation is around (9,1) as in Table 1, and Table 3 for DCM. Since both tables have only 16 states, the indexes can be combined into a single 8-bit index by FEM-index * 16 + DCM-index. 
    
        Table 2: Frontend Adjustments Relative to Level Settings 
      (All adjustments apply to both Hpol and Vpol simultaneously)
    FE Index Number    First Attn    Second Attn     Total Added Attn
    
         0                 0             0                0
         1                 0             3                3
         2                 0             6                6
         3                 0             9                9
         4                 0             12               12
         5                 0             15               15
         6                 0             18               18
         7                 9             12               21
         8                 9             15               24
         9                 9             18               27
         10                9             21               30
         11                9             24               33 
         12                9             27               36      
         13                18            21               39    
         14                18            24               42      
         15                31            31               62
    Minimum level setting is expected to be around (9, 1).  For this setting, most non-
    flaring observations will involve indexes 0-3.  Large flares will involve 4-9. Values 
    above 9 are unused except index 15 (used for zero-input-signal calibration).
    
        Table 3: Backend Adjustments Relative to Level Settings 
     (All adjustments apply to both Hpol and Vpol simultaneously)
          BE Index Number                    Attenuation (dB)
                  0                                 0
                  1                                 2
                  2                                 4
                  3                                 6
                  4                                 8
                  5                                 10
                  6                                 12
                  7                                 14
                  8                                 16
                  9                                 18
                  10                                20
                  11                                22
                  12                                24
                  13                                26
                  14                                28
                  15                                30
    
It will be the job of the cRIOs in each antenna to read the detector voltages in each channel and, based on the highest voltage, report to the ACC whether to step the attenuation one step up or down according to the FE Index in Table 2. If the cRIO detects that two or more upward steps are needed, it should implement the adjustment itself (for safety reasons), otherwise the ACC will determine whether all antennas should be stepped or not. In normal operation, all antennas should step simultaneously under the control of the ACC, at a maximum rate of 1 step/s. 

## Keeping the 8-Bit Digitizer from Clipping

It will be the job of the DPP to examine the power levels reported by the correlator and determine what DCM attenuation changes are needed as a function of IF band. The DPP will then instruct the ACC to implement any needed 2 dB attenuation steps up or down. In addition, the fault system will examine the overflow count of the digitizers, as provided by the correlator packet headers, and report that information to the ACC, which will make the decision whether to override the DPP. This should never happen, but is implemented as a safety measure. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Attenuation_and_Level_Control&oldid=333](http://ovsa.njit.edu//wiki/index.php?title=Attenuation_and_Level_Control&oldid=333)"
