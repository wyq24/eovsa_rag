# Calibration Database - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Calibration_Database
**Scraped:** 2025-08-05 09:12:56

# Calibration Database

From EOVSA Wiki

Jump to navigation Jump to search

## Description and Use of the EOVSA Calibration Database

### Background

We have created a general-purpose table in the SQL-Server database _eOVSA06_ , named _abin_ , which is used to hold binary calibration data in a general format given by an XML format string in the same table. The table is meant to be extendable to any calibration type, although it remains to be seen whether it is general enough to handle all use cases. This document describes the scheme, the format of the _abin_ entries, and the list of currently defined binary types (this will have to be updated on a regular basis as new definitions are added). 

### Description of the General Scheme

The general idea is to create entries into the _abin_ table that are self-describing and completely general. 

The table columns are: 
    
    ['Bin';, 'Timestamp', 'Version', 'Id', 'Description']

The _Id_ number is auto-incremented to be unique to each record, and is never set by the user. Each type definition will appear in the table with an _n_.0 _Version_ number (float), and whenever it is updated, a new n.0 record is written with the current _Timestamp_. This provides a history, with the corresponding _Timestamp_ giving the start timerange of applicability (actually regretting that this key is called _Version_ , since its purpose could more accurately be referred to as the calibration _Type_). To distinguish between this key and the true versions given within the type definition record, the latter is referred as the “internal version.” The _Bin_ column contains an XML data description that is to be used to decode the data. The _Version_ (type) number _n_ will be unique for each calibration type, so that records with _Version_ = 1.0, for example, will always contain the latest definition for a particular type of data defined as type 1 (the type of calibration data is further described in the _Description_ column). The type definitions, as well as helper routines for creating, reading, and writing records is found in the Python module **cal_header.py**. 

The XML data itself, found in the _Bin_ column of a _Version n_.0 record, contains an internal version variable that gives a further record of the version of the XML format. As a concrete example, the latest _Version_ 4.0 (delay centers) calibration will contain an XML string that includes its own internal version variable, say its value is 2.1, that would distinguish it from an earlier type 4.0 version. This internal version number is used by the `send_xml2sql()` to determine whether a definition defined in **cal_header.py** has changed and needs to be written to the _abin_ table. 

After (never before) the defining _n_.0 record is written, subsequent records of that type can be written containing the binary calibration data, which will be decoded using the defining XML string. Thus, after writing the latest _Version_ 4.0 format record, subsequent records with Version 4.1 (type 4, with internal version 1.0) can be written that will be decoded using that latest 4.0 XML string. Other versions, e.g. 4.2 (internal version 2.0) etc., could in principle be written, although it is not clear why that would be needed (perhaps an important change to the contents, but without a corresponding change to the format, could be indicated with a new 4.x version number). Thus, the latest `delay_centers` entry can be read with a query like: 
    
    SELECT TOP 1 * FROM abin WHERE Version > 4.0 AND Version < 5.0 ORDER BY Timestamp DESC

while the `delay_centers` entry for a given _Timestamp tstamp_ can be read with a query like: 
    
    SELECT TOP 1 * FROM abin WHERE Version > 4.0 AND Version < 5.0 AND Timestamp <= tstamp ORDER BY Timestamp DESC

In testing this, it was discovered that binary records returned by such a query are limited in length to 4096. To get an arbitrarily long record, one must prepend the string “SET TEXTSIZE 2147483647” to the query. Note that such details are already handled by the helper routine `read_cal()` in **cal_header.py**. As new calibration types are created, their definitions will be added to **cal_header.py** , both by updating the `cal_types()` routine to add the new type’s _Version_ number and _Description_ , and by adding a two writing routines—one called `type>2xml()` routine that returns the XML description of the data (later written into the database by `send_xml2sql()`), and one called `<type>2sql()` that converts the calibration data to a binary buffer and writes it into the database, where `<ype>` is a hopefully rational name for the new type. As new formats for an existing type are created, it should be fine to simply update the `cal_types()` routine to change the description (if needed) and update the format embodied in the `<type>2xml()` and `<type>2sql()` routines. It should not be necessary to keep the old format, since the database itself already forms a history. Of course, any previous versions of the **cal_header.py** file will also be kept in the **github** versioning system. 

### Currently-Defined Types

This section will hopefully be updated whenever new types are added, to provide a list of currently-defined calibration data types. However, it is probably wise to consult the **cal_header.py** file to verify the current definitions. Here is the verbatim return statement from `cal_types()`: 
    
    return {1:['Total power calibration (output of SOLPNTCAL)','proto_tpcal2xml',1.0],
    
            2:['DCM master base attenuation table [units=dB]','dcm_master_table2xml',1.0],
    
            3:['DCM base attenuation table [units=dB]','dcm_table2xml',1.0],
    
            4:['Delay centers [units=ns]','dlacen2xml',1.0]}
    
To add a new type, simply add another entry to this dictionary, with a unique type number, and a three-element list whose first element is the _Description_ string, second element is the string name of the routine to call to create the XML definition (returns a binary buffer ready for writing to the _abin_ table), and third element is the version number. Then add the corresponding `type>2xml()` routine defining the format of the binary data, and the `<type>2sql()` routine that converts the calibration data to a corresponding binary buffer. The **cal_header.py** module includes a routine `send_xml2sql()`, which can be called at any time and checks the latest version of each calibration type in the _abin_ table, and updates any that have changed (i.e. has a different version number than the latest one in the table). The return statement of each `<type>2sql()` routine should call `write_cal()` to actually write the binary buffer to the database, so that a single call to the routine does everything. It is anticipated that routines that create the calibration data will call the corresponding `<type>2sql()` routine directly. 

To change an existing type, change the description in the cal_types() routine, if desired, and change the corresponding `<type>2xml()` and `<type>2sql()` routines to create the new definition. It should not be strictly necessary to increment the version number that will be written into the XML description, unless two active versions are needed at the same time. It is up to the programmer to decide whether to increment the version’s minor (fractional) or major (integer) part of the version number, since only its uniqueness is required. 

### Reading Back Data for a given Calibration Type

If the above scheme is followed, it should be possible to use a single, general routine to find and successfully read the binary calibration data for a given time. The `read_cal()` routine in the **cal_header.py** module does this, returning a Python dictionary and the binary buffer. The dictionary contains key, value pairs defining the variable names (keys) and the types and start location (values) in the binary buffer. To use these returned entities, one employs the `extract()` routine defined in the **stateframe.py** module, e.g. to read the total power (type 1) calibration factors for antenna 5 on April 3, 2016 as of 20:00 UT: 
    
    import stateframe, util
    
    tp, buf = read_cal(1, t=util.Time(‘2016-04- 03 20:00’))
    
    calfac = stateframe.extract(buf,tp[‘Antenna’][4][‘Calfac’])
    
Here the index for antenna 5 is 4, since it is a zero-based index. Note that to read the values for the current time, the input _t_ can be omitted. 

## Reading and Writing Delay Center Tables

### Quick Start

  * Run roachcal.scd to create three packet-capture files on the DPP,

        **/data1/PRT/PRT** _yyyymmddhhmmss_**adc.dat** 
        **/data1/PRT/PRT** _yyyymmddhhmmss_**ndon.dat** 
        **/data1/PRT/PRT** _yyyymmddhhmmss_**ciel.dat**
    
  * Read the latter two packet capture files into ipython (reading each file takes awhile--1 GB each)

        import pcapture2 as p
        outxy = p.rd_jspec(_ndon_file_)
        outxxyy = p.rd_jspec(_ciel_file_)
    
  * Analyze the data

        import roachcal as rc
        xxyy = rc.getphasecor(outxxyy['x'],'ant1-14',[0],[700,3800],pplot=True)
        xy = rc.getphasecor(outxy['a'],'ant1-14',[2],[700,3800],pplot=True)
    
  * Check the plots and the output arrays. If okay, update the delay-center table

        import cal_header as ch
        ch.dla_update2sql(xxyy,xy)
    
  * Send the new delay-center table to the ACC

        ch.dla_censql2table()
    
### Explanation

Whenever a new delay center measurement is made, it can be easily written to the database using the following procedure. To create a brand new table, start with a delay_centers.txt file, which is simply a human-readable text file of a specific format patterned after the one originally made by hand. The ability to see a text file of the delay centers is useful to ensure that everything looks sensible. Also, such a table is read from the ACC /parm folder by the dppxmp program. To create a text table from the current database contents, simply run: 
    
    import cal_header as ch
    ch.dla_censql2table(acc=False)
    
By default, acc=True, which means to write the table to the ACC. In either case, the equivalent table is also written to /tmp/delay_centers.txt, on whatever machine the command is run from. This table can be changed by hand, if desired, and written back to the database by 
    
    ch.dla_centable2sql(filename='/tmp/delay_centers.txt')
    
but note that these updates will not be reflected in the ACC file until you run 
    
    ch.dla_censql2table(acc=True)
    
where the acc=True is the default, so could be omitted. 

In the more usual case, rather than start with a new table, the delay center values will simply be updated by measuring changes to the delays relative to the current one. To update the SQL database for new delay centers AND write them to the ACC, let's assume that the delay offsets, in units of delay steps, have been measured for baselines wrt antenna 1, i.e. 1-2, 1-3, 1-4, ... 1-14, and also on the auto-correlations for each antenna 1 through 14. The former are in a 14-element array _dla_update_ , and the latter are in a 14-element array _xy_delay_ , with zeros for any missing or otherwise not measured antennas. Such measurements can be done using the roachcal.scd schedule file, and analyzed with routines in the roachcal.py module. After obtaining these two arrays, run: 
    
    ch.dla_update2sql(dla_update,xy_delay)
    
to automatically read the current delay table from the SQL database, update it, and create a new table with the update. After 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Calibration_Database&oldid=854](http://ovsa.njit.edu//wiki/index.php?title=Calibration_Database&oldid=854)"
