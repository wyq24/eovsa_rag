# Analyzing Pre-2017 Data - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Analyzing_Pre-2017_Data
**Scraped:** 2025-08-05 09:12:39

# Analyzing Pre-2017 Data

From EOVSA Wiki

Jump to navigation Jump to search

# Analyzing Pre-2017 Data

Prior to April 2017, the EOVSA correlator was not fully working and so imaging is not possible. However, EOVSA still offers some unique total power measurements and even some limited baseline data, albeit without proper calibration. This page describes how to proceed with that analysis on the Pipeline machine. 

## Accessing Analysis Software

As a matter of keeping the software up to date, at some point the current software could no longer work with older data. This was solved on the Pipeline machine by creating a Python virtual environment containing the older software. To activate a terminal session on Pipeline that is using the appropriate Python environment, issue the following command: 
    
    source ~/.virtualenvss/astropy-dev/bin/activate.csh
    
which will result in a new prompt: 
    
    [astropy-dev] pipeline:~>
    
You can now use the commands on the remainder of this page, some of which will NOT work in the standard environment. 

To exit this special environment, issue this command: 
    
    deactivate
    
## Total Power Analysis

The total power can be read from IDB files using the dump_tsys module, which has the rd_miriad_tsys() routine. The call is of this form 
    
    out = dump_tsys.rd_miriad_tsys(trange)
    
which will result in 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Analyzing_Pre-2017_Data&oldid=4505](http://ovsa.njit.edu//wiki/index.php?title=Analyzing_Pre-2017_Data&oldid=4505)"
