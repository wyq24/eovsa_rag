# Pointing Calibration - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Pointing_Calibration
**Scraped:** 2025-08-05 09:13:01

# Pointing Calibration

From EOVSA Wiki

Jump to navigation Jump to search

## General Introduction

To obtain the best possible gain calibration, it is important that the individual antennas point accurately to the positions they are commanded to. Because of the different types and sensitivities of the EOVSA antennas, there are several different ways of measuring and correcting for pointing errors. Despite the different antenna designs used in the EOVSA system, some attempt is made to make the pointing corrections work in the same manner to the extent possible. 

The AzEl mounted antennas (Ants 1-8, and 12) use a 9-parameter pointing model in which parameter P6 is unused, and is hence kept to be zero. The EQ mounted antennas (Ants 9-11, 13 and 14) also use a 9-parameter pointing model, in which parameter P9 is unused. In all cases, the main offsets are parameters P1 and P7, where P1 is either Azimuth or Hour Angle offset, and P7 is either Elevation or Declination offset. Note that these offsets apply to the axis readout, hence the magnitude of P1 varies in the sky relative to the magnitude of P7. For many purposes, it is better to measure offsets in "sky" units, i.e. Cross-elevation (XEL) or Cross-declination (XDEC), both of which are obtained by multiplying by the cosine of the relevant angle. Thus, XEL = AZ*cos(EL), and XDEC = HA*cos(DEC). 

## Star Pointing

## Solar Pointing (SOLPNT)

## Interferometric Pointing (CALPNT)

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Pointing_Calibration&oldid=651](http://ovsa.njit.edu//wiki/index.php?title=Pointing_Calibration&oldid=651)"
