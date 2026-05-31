# Starburst - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Starburst
**Scraped:** 2025-08-05 09:13:35

# Starburst

From EOVSA Wiki

Jump to navigation Jump to search

## Hardware

The starburst hardware was designed partly by Ryan Monroe (the LO distribution, downconverter modules (DCM) and ROACH-2 firmware), and by James Lamb/Mark Hodges (He-cooled receiver). James created a block diagram of the full system dated ..., but the system has evolved somewhat since then, so some details may be updated in Ryan's version of the block diagram. At the time that the starburst program was stopped (due to problems with the 27-m antennas), the hardware was largely, but not completely assembled. Here is a fairly complete link to the documents up to that time: [[Starburst Technical Documents](https://www.ovro.caltech.edu/ovro-technical/projects/eovsa-starburst/eovsa-starburst.html)] Some marked up drawings are included below to indicate what parts are either missing or not installed. 

### Receiver and Focus Box

The receiver is shared between the EOVSA and Starburst projects, and hence has some characteristics designed for one or the other program. The receiver is designed to cover the entire 1-18 GHz frequency range, but since this is difficult to do with a single receiver system, the receiver package actually houses two separate, switch selectable receivers with their own feeds, the Lo (1-6 GHz) receiver and the Hi (3-18 GHz) receiver. There is a rather complex "focus rotation mechanism" (FRM) that has three motion axes. 

  * The Z axis is an in-and-out motion to move the feeds into the best focus (the focus position is different for the two feeds).
  * The X axis is a translation horizontally to move the selected receiver into position at the focus.
  * The position angle (PA) axis is a rotational motion to orient the selected feed to different position angles, both to align the feeds with the Alt-Az-mounted dishes (correcting for the differential parallactic angle) during a typical calibration observation, and also to characterize the polarization properties of the array feeds over a shorter time.

A diagram that includes the block diagram for the receiver is here (see also Fig. 1). [File:Starburst system diagram.pdf](/wiki/index.php/File:Starburst_system_diagram.pdf "File:Starburst system diagram.pdf")

[![](/wiki/images/e/ee/EOVSA_27-m_Receiver_Block_Diagram.JPG)](/wiki/index.php/File:EOVSA_27-m_Receiver_Block_Diagram.JPG)

[](/wiki/index.php/File:EOVSA_27-m_Receiver_Block_Diagram.JPG "Enlarge")

Fig. 1: Block diagram for the EOVSA/Starburst He-cooled front-end receiver. The items in color are within the dewar, while the other components are in the external Auxiliarly Box. Additional notch filters (not shown) have been placed in the 1-6 GHz RF chain just before the receiver selection switch.

### LO Distribution Module

### Downconverter Module (DCM)

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Starburst&oldid=84](http://ovsa.njit.edu//wiki/index.php?title=Starburst&oldid=84)"
