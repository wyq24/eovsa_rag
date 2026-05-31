# Star Pointing Notes - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Star_Pointing_Notes
**Scraped:** 2025-08-05 09:13:42

# Star Pointing Notes

From EOVSA Wiki

Jump to navigation Jump to search

# Star Pointing Appending note

Following the steps in [Owen's Notes](/wiki/index.php/Owen%27s_Notes "Owen's Notes")

First do pointing select 
    
    import readbsc as bsc
    
    bsc.do_stars(y,m,d,h,m, npts=60)
    
Then ftp to ACC (admin) 

get /parm/starttracktable.radec 

Then create(edit) a control file: nano STARS.ctl 

Then edit the schedule file starpointing.scd 

(may have CRIO problem) reboot CRIO 

then SYNC ANT* then 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Star_Pointing_Notes&oldid=12257](http://ovsa.njit.edu//wiki/index.php?title=Star_Pointing_Notes&oldid=12257)"
