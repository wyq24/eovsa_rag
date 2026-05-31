# Mapping Software - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Mapping_Software
**Scraped:** 2025-08-05 09:12:33

# Mapping Software

From EOVSA Wiki

Jump to navigation Jump to search

# Port of IDL Mapping routines (by Dominic Zarro) to Python

## Getting the Software

Simply go to [this github repository](https://github.com/dgary50/mapping) to download the software. 

## Philosophy

Although the Sunpy Python package already exists for doing analysis of solar data, it has a significant learning curve and lacks the generality of the Mapping routines written by Dominic Zarro for the IDL-based Solarsoft (SSW). Perhaps having the IDL Mapping routines available in Python may help those IDL users who have been avoiding learning Python. The mapping routines **work equally well in both Python 2.7 and Python 3**. 

## Similarities and Differences

To the extent possible, the routine names and general approach of the IDL routines have been kept, so that those familiar with the IDL routines will find it familiar and easy to use. The routines for multi-panel plots, overlaying the solar grid, contour plots, map sub-regions, rotations, translations, and differential solar rotation are all available. Importantly, the plotting system works similar to IDL direct graphics behavior as follows: 

  * Issuing multiple plot calls will use the same window.
  * For multi-panel plots, each new plot call will advance to the next panel, but after the last panel has been used the next plot call will reuse the first panel.
  * To plot to a new window, simply specify a window number. If that window does not exist, it will be created. If it does exist it will be reused.
  * Once a window is plotted to, subsequent plots will go to that window if no window is specified.
  * Contour overlays automatically go to the last-used window/panel.

However, unlike IDL direct graphics, once a plot is created one can zoom, pan, print in multiple formats, etc. 

Some differences could not be eliminated, however. Unlike IDL, Python does not have a procedure syntax, switch parameters, nor can it return output in parameters to a call. Therefore, everything is a function, and when multiple results are to be returned they are returned as either tuples or in dictionaries. Here are a couple of examples to illustrate: 

### IDL fits2map syntax example:
    
    fits2map,'aia304.fits',aiamap,header=h
    
### Python form of the same command:
    
    aiamap, h = fits2map('aia304.fits',header=True)
    
In the above, if header is not set to True, fits2map returns only aiamap, while if header is True then fits2map returns a tuple of items--the map and the header. 

### IDL plot_map syntax example:
    
    plot_map,aiamap,grid=10,/limb,center=[-400,400],fov=[3,3]
    
### Python form of the same command:
    
    plot_map(aiamap, grid=10, limb=True, center=[-400,400], fov=[3,3])
    
In the above, the action of the /limb switch in IDL is accomplished by setting limb=True. 

Please see [this link](http://www.ovsa.njit.edu/mapping/mapping_test.html) for further examples. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Mapping_Software&oldid=4961](http://ovsa.njit.edu//wiki/index.php?title=Mapping_Software&oldid=4961)"
