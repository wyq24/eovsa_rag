# Hardware Overview - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Hardware_Overview
**Scraped:** 2025-08-05 09:12:52

# Hardware Overview

From EOVSA Wiki

Jump to navigation Jump to search

## Frontend System

[![](/wiki/images/9/98/Feed_package.png)](/wiki/index.php/File:Feed_package.png)

[](/wiki/index.php/File:Feed_package.png "Enlarge")

**Figure 1:** Two perspective views of the 2.1-m antenna front end feed package

The front end system (**Figure 1**) consists of a broadband (1-18 GHz) dual-polarization log-periodic crossed-dipole feed, and a thermally-controlled RF box (called the FEM, or Front End Module) that houses the amplifiers, calibration noise source (noise diode), attenuators, and optical transmitters needed to control the gain of the system and supply the two RF signals multiplexed onto a single optical fiber output. 

[![](/wiki/images/c/c3/Eovsa_front_end_block_diagram.png)](/wiki/index.php/File:Eovsa_front_end_block_diagram.png)

[](/wiki/index.php/File:Eovsa_front_end_block_diagram.png "Enlarge")

**Figure 2:** The complete block diagram for the Front End Module (FEM) housed in the RF box

The block diagram for the FEM is shown in **Figure 2**. 

## Downconverter System

[![](/wiki/images/8/8f/Eovsa_down_converter_block_diagram.png)](/wiki/index.php/File:Eovsa_down_converter_block_diagram.png)

[](/wiki/index.php/File:Eovsa_down_converter_block_diagram.png "Enlarge")

**Figure 3:** The complete block diagram for the Downconverter Module (DCM)

## Digital Correlator

[![](/wiki/images/a/aa/Eovsa_correlator_block.png)](/wiki/index.php/File:Eovsa_correlator_block.png)

[](/wiki/index.php/File:Eovsa_correlator_block.png "Enlarge")

Digital Correlator

### Equalizer Coefficients

Because the correlator down-samples the 18-bits of real and imaginary power from each antenna to 4-bits, prior to correlation, it is necessary to control which bits are sampled in order to maintain maximum dynamic range. Let's consider that the top four bits of power are sampled. If the power level is too high, it will saturate in the ADCs, or in the butterfly stages of the FFT. To avoid this, we want the power level to fill as much of the 18 bits as possible, but without danger of overflowing, hence in practice it fills less than 18 bits. In order to ensure that the optimum 4 bits of these 18-bit numbers are selected, the correlator has an equalizer stage that applies a multiplicative factor to the power before selecting the top 4 bits. Each ROACH has a set of four registers named 'eq_x0_coeffs', 'eq_x1_coeffs', 'eq_x2_coeffs', and 'eq_x3_coeffs' that provide the multiplicative factors. The 'x0' and 'x1' coefficients correspond to the first antenna's X and Y polarization, respectively, while the 'x2' and 'x3' coefficients correspond to the second antenna. I will refer to each of these as one of the ROACH's four IF **channels,** two for each antenna. The correlator can tune successively to different 500 MHz IF **bands,** and each is divided into 4096 **subchannels.** A final bit of terminology is that the tuning sequence can be in any order, and each tuning covers 20 ms, or 1 of 50 **slots** during a second. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Hardware_Overview&oldid=972](http://ovsa.njit.edu//wiki/index.php?title=Hardware_Overview&oldid=972)"
