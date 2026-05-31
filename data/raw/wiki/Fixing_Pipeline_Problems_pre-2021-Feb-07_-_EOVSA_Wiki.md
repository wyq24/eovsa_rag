# Fixing Pipeline Problems pre-2021-Feb-07 - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Fixing_Pipeline_Problems_pre-2021-Feb-07
**Scraped:** 2025-08-05 09:12:40

# Fixing Pipeline Problems pre-2021-Feb-07

From EOVSA Wiki

Jump to navigation Jump to search

# Pipeline Processing Errors Pre-2021-Feb-07

In early February it was realized that the auto-correlations out of the correlator have saturation, but that the nature of the saturation is such that it is fully correctable. One result of the saturation is that front-end attenuation correction was not working well, but after rerunning the pipeline analysis to remove the saturation the attenuation correction works fine. Unfortunately, there are some important issues that have to be fixed for all data prior to 2021-Feb-10 or so. These are: 

  * The total power calibration has to be rerun for all data, and inserted into the SQL database prior to any analysis.
  * The UDB files have to be recreated by the real-time pipeline system.
  * The CASA ms file corresponding to the UDB files have to be recreated from them.

If you are interested in analyzing a flare, only the first is needed since the flare analysis uses the IDB files, not the UDB files. However, if you are interested in analyzing an active region or full disk data, for which you will be using UDB files, you will need to do all of them. Note, the first two steps are independent, i.e. the order you do them in does not matter. However, the last step has to be done last after **both** of the other two are done. 

## Recalibrating the total power

To redo the total power calibration, the easiest approach is to simply issue this command at the system prompt on the pipeline machine at OVRO (this example is for the date 2020 Jun 8): 
    
    python /common/python/current/calibration.py "2020-06-08 21:36"
    
Note that the time given is 6 minutes after the actual time of the calibration, which was done at 21:30 UT. Two calibrations are done each day, and normally the second one is the one used for the calibration. You can check the calibration times by looking at the quick look spectra in the [EOVSA browser](http://ovsa.njit.edu/browser). Normally the calibrations are done at 18:30 and 21:30 UT, but beware that on some days the times may be different. Again, in the above command specify a time 6 minutes after the start time of the calibration. 

## Reprocessing the UDB data

It is more involved to reprocess the UDB data. First, check that this is needed by checking the creation date of the UDB files for the date you are interested in--someone may have already reprocessed that date for you. To check the creation date, at the system prompt enter (this example is for the date 2020 Jun 8): 
    
    ls -ld /data1/eovsa/fits/UDB/2020/UDB20200608*
    
and if the creation dates are after Feb 10 2021 then you can expect that the reprocessing is already done for you. 

If not, the reprocessing is done by editing the file /home/user/test_svn/python/udb_reprocess.py to give the date to be reprocessed. In the line 
    
    pipeline.udb_reprocess_days('2020-06-08 13:00:00','2020-06-08 23:00:00')
    
simply change the date to the one you want to reprocess. Do not change the times--udb_reprocess has a rather complicated idea of the timerange, but the range 1300-2300 UT will do the entire day, not only this timerange. 

After the file had been edited, run it by issuing the following commands (you can just cut and paste them from here...): 
    
    cd /home/user/workdir
    setenv datestr `date +%Y%m%d`
    if ! (-d /data1/eovsa/fits/images/${datestr} ) then
       mkdir /data1/eovsa/fits/images/${datestr}
    endif
    set line="$datestr"
    /usr/bin/python /home/user/test_svn/python/udb_reprocess.py >> /data1/processing/LOG/udb_reprocess_log.txt_$line
    
The reprocessing is a rather lengthy process, and can take many hours. You can check the progress by looking at the log file, which if I run it today (2021 Apr 22) will have the name /data1/processing/LOG/udb_reprocess_log.txt_20210422. 

At the end of this process, when you check the creation date of the appropriate folder, e.g. 
    
    ls -ld /data1/eovsa/fits/UDB/2020/UDB20200608*
    
you should see that they are all for the current date. The final step is to rerun the pipeline processing that creates the UDB ms file. 

## Creating the CASA ms File from the UDB Files

You **must** do both of the previous two steps prior to doing this one. This last pipeline procedure is a three-step procedure, (1) create the CASA UDB ms files and image FITS files, (2) create the jpg images for the browser, and (3) compress the FITS files for the browser images so they take up less space. The essential part is step 1, which you do by issuing the following command (this example for 2020 Jun 8): 
    
    /bin/tcsh /common/python/suncasa/shellScript/pipeline.csh -c 1 2020 06 08 > /tmp/pipeline_tmp.log
    
This also is a lengthy process taking a couple of hours. You can view the progress by looking at the log file. You can change the log file name to whatever you want. If you want to continue with creating the images and compressing the FITS files, enter these two commands (these are relatively quick): 
    
    /bin/bash /common/python/suncasa/shellScript/pipeline_plt.bash -n 1 -e 1 2020 06 08
    /common/python/suncasa/shellScript/pipeline_compress.bash -n 1 -O 1 2020 06 08
    
After the above rather lengthy process, you should have all of the files reprocessed and up to date. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Fixing_Pipeline_Problems_pre-2021-Feb-07&oldid=5543](http://ovsa.njit.edu//wiki/index.php?title=Fixing_Pipeline_Problems_pre-2021-Feb-07&oldid=5543)"
