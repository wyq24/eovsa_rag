# Stateframe Database - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Stateframe_Database
**Scraped:** 2025-08-05 09:12:57

# Stateframe Database

From EOVSA Wiki

Jump to navigation Jump to search

## Setup and Initial Test of Python Access to Existing Database

### Introduction

This document describes the initial setup and access of the EOVSA Stateframe database from Python. The original version of this document described the case of a database called “eOVSA05” that existed on a machine named “GARY-FY13NB” (laptop). That connection string for connecting from the laptop was: 
    
    cnxn = pyodbc.connect(“DRIVER={SQL Server}; SERVER=GARY-FY13NB; DATABASE=eOVSA05;Trusted_connection=yes;")
    
However, some adjustments were needed to allow connection to the actual server machine (EOVSASQL), using an IP address and “SQL Authentication.” The trick was to create a user on the server in the SQL Server Management Studio (user name is `‘aaa’`, password provided to those who need it), and then use the server IP address (currently ‘128.235.89.168’) on port 1433. This port had to be opened in the server’s Windows Firewall. The new connection string is: 
    
    cnxn = pyodbc.connect("DRIVER={SQL Server}; SERVER=128.235.89.168,1433; DATABASE=eOVSA06;UID=aaa;PWD=<password>;")
    
The other commands have been updated for the current situation, also. As of 2014-Sep-30, the SQL Server has been set up at OVRO and the connection string from Helios is: 
    
    cnxn = pyodbc.connect("DRIVER={FreeTDS}; SERVER=192.168.24.106,1433; DATABASE=eOVSA06;UID=aaa;PWD=<password>;")
    
### Initial setup of database access software

The Python library to access Microsoft SQL Server is called pyodbc. This describes downloading the library and integrating it with an existing **python2.76** installation, making a first connection to the database, and executing a query. The query assumes that database “eOVSA06” has a populated table “fV26_vD15.” 

1\. First install **pyodbc** ([[1]](https://pypi.org/project/pyodbc/)). 2\. Start **ipython** and type 
    
    import pyodbc

3\. Connect to database with 
    
    cnxn = pyodbc.connect("DRIVER={SQL Server}; SERVER=128.235.89.168,1433; DATABASE=eOVSA06; UID=aaa; PWD=<password>;")

4\. Get a 'cursor' to the database: 
    
    cursor = cnxn.cursor()

5\. Send an SQL query: 
    
    cursor.execute("select top 16 * from fV26_vD15 order by Timestamp")

6\. Fetch the data returned by the query 
    
    rows = cursor.fetchall()

7\. rows now contains a list of 16 rows. 

Note that setup on Linux (Ubuntu) is quite a bit more complicated. Here are the steps: 

1\. Download **pyodbc-3.0.7.zip** from the above link (or copy from **helios.solar.pvt**). 

2\. Install unixODBC and FreeTDS packages: 
    
    sudo apt-get install unixodbc freetds-dev freetds-bin tdsodbc

3\. Edit **/etc/freetds/freetds.conf** (or copy from helios) to change the last 4 lines to 
    
            [sqlserver]
    	host = sqlserver.solar.pvt
    	port = 1433
    	tds version = 11.0
    
4\. Edit file **/etc/odbc.ini** (or copy from helios) to contain: 
    
            [sql]
            Driver = FreeTDS
    	Description = ODBC connection via FreeTDS
    	Trace = No
    	Servername = sqlserver.solar.pvt
    	Database = eOVSA06
    
5\. Edit file **/etc/odbcinst.ini** (or copy from helios) to contain: 
    
            [FreeTDS]
    	Description     = TDS driver (Sybase/MS SQL)
    	Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
    	Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
    	CPTimeout       =
    	CPReuse         =
    	FileUsage       = 1
    
6\. [These are old instructions--just follow the pypi instructions at the above link.] Unzip the zip file in step 1, cd to the directory **pyodbc-3.0.7** , and type: 
    
            python setup.py build
    	sudo python setup.py install
    
From there, use the connection string for Linux shown in the introduction section, and proceed from there. 

### Examples of returned queries
    
    cursor.execute(“select top 2 * from fV26_vD1 order by Timestamp”)
    rows = cursor.fetchall()
    
Returns the entire “dimension-1” data for the first two entries in the table, ordered by _Timestamp_. The contents can be accessed one row at a time (`rows[0]` and `rows[1]` in this case), and the entry names can be listed with `rows[0].cursor_description`. One can access the value of, say, the current temperature via `rows[0].Sche_Data_Weat_Temperature`: 
    
    cursor.execute(“””select top 20 * from fV26_vD15 a where (a.[I15] % 15) = 0 order by Timestamp”””)
    rows = cursor.fetchall()
    
Returns the first 20 rows for Antenna 1 [via (`a.[Index] % 15) = 0`] of the dimension-15 table, ordered by _Timestamp_. One can check that these are all for the same antenna, for example, by checking one of the pointing coefficients using the Python code: 
    
    for row in rows: print row.Ante_Cont_PointingCoefficient2

### Create a new StateFrameDef Table entry

Whenever a new version of the stateframe is created due to some change in the content of the stateframe, a new StateFrameDef table entry must be created. This is accomplished via a set of SQL commands, like: 
    
    cursor.execute(“insert into StateFrameDef (Status, Version, Dimension, DataType,  FieldBytes,  DimOffset,  StartByte,  FieldNum,  FieldName) 
                        values ( 0, 15, 15, 'u16', 2, 28, 759, 1, 'DCM_Slot')”)
    
and so on for the entire new table. Once all of the rows of the table are entered, the command to create the tables for that version is: 
    
    cursor.execute(“update StateFrameDef set status=1 where Version=’15’”) 

NB: Once a stateframedef entry is entered, it cannot be entered again within causing unrecoverable errors in the table. See below for description of procedure to clear all of the tables and start ove 

### Complete process of inserting a new binary record

The structure of binary data for a given stateframe version is encoded in its XML file with the name ‘stateframe_vxx.00.xml’, where xx is the version number, i.e. 26. The binary data has to be rearranged via a routine in **stateframedef.py** called `transmogrify()`. A complete recipe for reading and inserting data from a stateframe log file (‘sf_20140205_v26.0.log’ in this example), is as follows: 
    
    import stateframedef as sfd
    import pyodbc
    sf, version = sfd.rxml.xml_ptrs(‘stateframe_v26.00.xml’)
    brange, outlist = sfd.sfdef(sf)
    f = open(‘sf_20140205_v26.0.log’,’rb’)
    buf = f.read(32)
    recsize = sfd.struct.unpack_from(‘i’, buf, 16)[0]
    f.close()
    cnxn = pyodbc.connect("DRIVER={SQL Server};SERVER=128.235.89.168,1433; 
    DATABASE=eOVSA06;UID=aaa;PWD=<password>;")
    cursor = cnxn.cursor()
    with open(‘sf_20140205_v26.0.log’, ‘rb’) as f:
        bufin = f.read(recsize)
        bufout = sfd.transmogrify(bufin, brange)
        try:
            cursor.execute(‘insert into fBin (Bin) values (?)’,  
            pyodbc.Binary(bufout))
        except:
                  pass
    cnxn.commit()
    
The execute line may return an error and fail, of course, especially if the data have previously been inserted, so it is enclosed in a try: except: clause so that everything does not immediately stop. Error checking would go into the except: clause. 

### Procedure to create the information for a new stateframedef table

The Python code in **stateframedef.py** does all of the manipulation related to creating StateFrameDef (and also ScanHeaderDef) tables as well as converting stateframe (or scanheader) binary data to the database data. For various reasons involving the internals of SQL, it is necessary to reorder certain data (two-dimensional arrays) in the stateframe and scanheader before they can be saved in the SQL database. These special cases are handled in the bowels of **stateframedef.py** ’s `walk_keys()` routine. To create a stateframedef table from a new stateframe xml file, e.g. stateframe_v32.00.xml, do: 
    
    import stateframedef as sfd
    sf, version = sfd.rxml.xml_ptrs(‘stateframe_v32.00.xml’)
    brange, outlist = sfd.sfdef(sf)
    sfd.startbyte(outlist)
    tbl = sfd.outlist2table(outlist,version)
    
This last line prints the table to the screen and also creates the contents of the table as commands for input to SQL. To upload the table in SQL and activate it, the commands are: 
    
    for line in tbl:
    cursor.execute(line)
    cursor.execute(“update StateFrameDef set status=1 where Version=’” +  
                    str(int(version)) + ”’”)
    
### To close a connection

Once a connection cxnx has been created, and a cursor has been defined, do the following to release them: 
    
    cursor.close()
    del cursor
    cnxn.close()
    
### To clear all tables and start from scratch

The SQL tables that describe each version of the stateframe or scanheader are called (case-insensitive) StateFrameDef and ScanHeaderDef. If somehow these get confused (as in entering a line that is already in the table), any previously backed-up tables can be restored using: 
    
    cursor.execute(“ov_fTEST_DefRestore”) 

However, if no appropriate backup exists, the tables need to be cleared and reloaded. This is a very quick process, luckily. To empty the “definition” tables, execute the following: 
    
    cursor.execute(“ov_fTEST_DefTruncate”)

To reload them, it is intended to have a single function (not available yet): 
    
    reload_deftables(),

which will clear the tables and reload them automatically. Right now, there is a routine that does this for one file: 
    
    flag = load_deftable(xml_file),

which returns True if successful, or False if an error. If a definition for the specified version already exists in the table, a warning is generated and the table is not redefined, but the routine returns True. This avoids trying to redefine the table and thus messing it up. The `reload_deftables()` routine will just clear the tables, and then take all xml files in a directory and repeatedly call `load_deftable()`. 

### Getting data across version boundaries

The data for each version of the stateframe appears in unique tables, so that the information for one period of time may be in, for example, fV32_vD15, while for the next adjacent time it is in fV35_vD15 (no data were recorded for versions 33-34). If one wants to get data that spans these two tables, one would use the following query (this example is for Ante_Cont_Elevation1): 
    
    cursor.execute(“””select Timestamp, Ante_Cont_Elevation1 
                      from fV32_vD15 a where (a.[i15] % 15) = 0 
                      union all 
                      select Timestamp, Ante_Cont_Elevation1 
                      from fV35_vD15 b where (b.[i15] % 15) = 0 
                                           order by TimeStamp”””)
    
Note that it is necessary to include in the select list the column (TimeStamp in this case) that is to be used for ordering the data. Otherwise one gets a cryptic error message [42000] ORDER BY items must appear in the select list if the statement contains a UNION, INTERSECT or EXCEPT operator. Once the data are selected, the following lines will plot them: 
    
    rows = cursor.fetchall()
    elev = zeros(len(rows),'float')
    times = zeros(len(rows),'float')
    for i,x in enumerate(rows):
        times[i], elev[i] = x
    plot(times-times[0],elev/10000.,'.')
    
### New python code for accessing the database

There is a module called dbutil that contains (and will further be developed) routines to access the database. The two current routines are: 

  * `cursor = get_cursor()` Opens the database and returns a cursor for access to it.
  * `mydict = get_dbrecs(cursor, version, dimension, timestamp, nrecs)` Takes as input an open cursor and version, dimension, timestamp and nrecs, and returns a dictionary from the table indicated by the version and dimension, starting at timestamp, and having nrecs entries. The data in each mydict key has dimensions of dimension x nrecs.

## Useful Tricks

### Get a List of Tables

To get the list of the tables names from the database, do this: 
    
    import dbutil as db
    cursor = db.get_cursor()
    query = "select table_name from information_schema.tables where table_type = 'base table' order by table_name"
    data, msg = db.do_query(cursor, query) 

If successful, msg will be the string 'Success' and data will be a dictionary with a single key, table_name. To get the latest records, choose the table with the highest version number. 

### Get Column Names from a Table

To get a list of the column names from the table fV66_vD15, do this: 
    
    import dbutil as db
    cursor = db.get_cursor()
    query = "select column_name from information_schema.columns where table_name = 'fV66_vD15'"
    data, msg = db.do_query(cursor, query) 

If successful, msg will be the string 'Success' and data will be a dictionary with key column_name. 

### Get Every Nth Entry

To get every Nth entry, for example, one data point each hour, use the modulo (%) function. For example, this gets the VPol power for Ant 14 [**(I15 % 15) = 13**] once an hour [**(cast(Timestamp as bigint) % 3600) = 0**]: 
    
    import dbutil as db
    cursor = db.get_cursor()
    query = 'select Timestamp,Ante_Fron_FEM_VPol_Power from fV66_vD15 where (I15 % 15) = 13 and 
    Timestamp between '+t0+' and '+t1+' and (cast(Timestamp as bigint) % 3600) = 0 order by Timestamp'
    data, msg = db.do_query(cursor, query)

where t0 is the start Labview timestamp as a string, and t1 is the end Labview timestamp as a string. Note the need to convert Timestamp (a float) to a big integer first. If successful, msg will be the string 'Success' and data will be a dictionary with keys Timestamp and Ante_Fron_FEM_VPol_Power. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Stateframe_Database&oldid=6077](http://ovsa.njit.edu//wiki/index.php?title=Stateframe_Database&oldid=6077)"
