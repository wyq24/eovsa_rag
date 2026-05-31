# Create CASA measurement sets - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Create_CASA_measurement_sets
**Scraped:** 2025-08-05 09:12:59

# Create CASA measurement sets

From EOVSA Wiki

Jump to navigation Jump to search

## Import visibilities from MIRIAD

The data EOVSA are stored in MIRIAD data format. To use CASA to process the data, one will need to import MIRIAD visibilities to be converted to a CASA Measurement Set (MS). 

## Using the _importeovsa_ task

We have written a CASA task named _importeovsa_. The task _importeovsa_ allows one to import visibilities in MIRIAD data format (IDB/UDB) to create MS file(s). The inputs are: 
    
    #  importeovsa :: Import EOVSA idb file(s) to a measurement set or multiple measurement set
    idbfiles            =         ''        #  Name of input EOVSA idb file(s) or observation time range.
    timebin             =       '0s'        #  Bin width for time averaging
    width               =          1        #  Width of output channel relative to MS channel (# to average)
    visprefix           =         ''        #  Prefix of vis names (may include the path).
    nocreatms           =      False        #  If setting nocreatms True, will simulate a model measurement set for the first idb file and copy the model for the rest of idl files in list. If False, will
                                            #   simulate a new measurement set for every idbfile in list.
    doconcat            =      False        #  If concatenate multi casa measurement sets to one file.
    modelms             =         ''        #  Name of input model measurement set file. If modelms is assigned, no simulation will start.
    
**This webpage is to be finished ......**

Imports an arbitrary number of EOVSA idb-format data sets into a casa measurement set. If more than one band is present, they will be put in the same measurement set but in a separate spectral window. 

Detailed Keyword arguments: 

idbfiles -- Name of input EOVSA idb file(s) or observation time range 
    
       default: none.  Must be supplied
       example: idbfiles = 'IDB20160524000518'
       example: idbfiles=['IDB20160524000518','IDB20160524000528']
       example: idbfiles=['2016-08-09 12:10:00','2016-08-09 12:50:00']
    
visprefix -- Prefix of vis names (may include the path) default: none; example: visprefix='sun/'] 

\--- Data Selection --- 

nocreatms -- If copying a new MS file instead of create one from MS simulator. default: False 

modelms -- Name of the standard Measurement Set. IF modelms is not provided, use '/home/user/sjyu/20160531/ms/sun/SUN/SUN_20160531T142234-10m.1s.ms' as a standard MS. 

doconcat -- If outputing one single MS file 

\--- Channel averaging parameter --- 

width -- Number of input channels to average to create an output channel. If a list is given, each bin will apply to one spw in the selection. default: 1 => no channel averaging. options: (int) or [int] 

example: chanbin=[2,3] => average 2 channels of 1st selected spectral window and 3 in the second one. 

\--- Time averaging parameters --- 

timebin -- Bin width for time averaging. When timebin is greater than 0s, the task will average data in time. Flagged data will be included in the average calculation, unless the parameter keepflags is set to False. In this case only partially flagged rows will be used in the average. default: '0s' 

    #  pimporteovsa :: Parallelized import EOVSA idb file(s) to a measurement set or multiple measurement set
    idbfiles            =         ''        #  Name of input EOVSA idb file(s) or observation time range.
    ncpu                =          8        #  Number of cpu cores to use
    timebin             =       '0s'        #  Bin width for time averaging
    width               =          1        #  Width of output channel relative to MS channel (# to average)
    visprefix           =         ''        #  Prefix of vis names (may include the path).
    nocreatms           =      False        #  If setting nocreatms True, will simulate a model measurement set for the first idb file and copy the model for the rest of idl files in list. If False, will
                                            #   simulate a new measurement set for every idbfile in list.
    doconcat            =      False        #  If concatenate multi casa measurement sets to one file.
    modelms             =         ''        #  Name of input model measurement set file. If modelms is assigned, no simulation will start.
    
Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Create_CASA_measurement_sets&oldid=849](http://ovsa.njit.edu//wiki/index.php?title=Create_CASA_measurement_sets&oldid=849)"
