# Database Maintenance - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Database_Maintenance
**Scraped:** 2025-08-05 09:12:58

# Database Maintenance

From EOVSA Wiki

Jump to navigation Jump to search

# Description of Databases

Initially we had a single database, eOVSA06, with many tables holding varioius system monitoring information at a 1-s cadence, tables with scan header information at a several-per-day cadence, and the calibration table (abin) with descriptors and data for various calibration types. However, that database, operating on the SQLserver Windows operating system, has grown too large and unwieldy (7.5 TB as of early 2022), and is impossible to use at other sites. The power outage associated with the Feb 2022 brush fire caused a major scare when the SQLserver machine could not be rebooted. We have largely recovered the database, but it is clearly dangerous to have only the one copy of this critical data. 

In response, I have created a new database called eOVSA in the MySQL open standard, which contains only those columns from the 1-s stateframe needed for calibration (much smaller, at about 120 GB as of early 2022), and those columns needed from the scanheader, as well as the entire abin calibration database. This 125 GB database can be easily copied to other sites so that calibration of raw data can be done from anywhere. In concert with this, I have transitioned the EOVSA control and calibration software to Python3, creating two packages: eovsapy (routines that can be run from anywhere, and will form the main package for sharing with the world) and eovsactl (routines that are strictly for control of the EOVSA system and should only be run from the OVRO site). One issue, of course, is that this smaller database has to be kept up to date as more data are taken. 

This wiki page is a convenient location for the specific commands needed to create and maintain these additional databases, as well as some documentation of how to back up the core part of the SQLserver (full) database. 

# SQLserver

The single eOVSA06 database has some disk errors that cause problems when trying to do a full backup, which is quite annoying. However, the way the complex table structure is filled out is to simply transmit binary data to three tables, abin, fbin, and hbin (calibration, stateframe, and scanheader tables, respectively). There are a number of "stored procedures" and "scalar-valued functions" (SPs and SVFs) that parse these binary records into the many other tables (and views) used in the database, but for saving the raw data it is enough to simply save these binary files and the corresponding code for the SPs and SVFs. The latter have been saved on the NAS4 RAID system under the folder /nas4/Gil/SP_and_SVF_code. The table structure has also been saved in the folder /nas4/Gil/Table_Structure. These binary files take about half the space of the full database. I have created a new database named test (not very original) in /nas4/SQL_LOG to which I have copies all of the recoverable abin, hbin, and fbin records through 2022-Feb-16 when the data stopped being recorded to the SQL database. This can serve as an emergency backup, but of course will need to be kept up to date as well. 

## Saved "Backup" Files

Contents of **/nas4/SQL_LOG** (backup "test" database containing tables abin, fbin, hbin) 
    
    -rwxr-xr-x 1 sched helios     117506048 Mar  3 00:09 eOVSA_xfer_2_GilInNJ
    -rwxr-xr-x 1 sched helios  285778903040 Mar 17 00:20 test_log.ldf
    -rwxr-xr-x 1 sched helios 3681028145152 Mar 17 00:20 test.mdf
    
Contents of **/nas4/Gil/SP_and_SVF_code** (stored procedures and single-valued functions needed to recreate database) 
    
    -rwxr-xr-x 1 sched helios   1179 Mar 13 06:13 SPs_AllOfEm.sql
    -rwxr-xr-x 1 sched helios 527572 Mar 13 06:11 SPs_AllOfEm.txt
    -rwxr-xr-x 1 sched helios   1503 Mar 14 04:46 SVFs_AllOfEm.sql
    -rwxr-xr-x 1 sched helios   6173 Mar 14 04:45 SVFs_AllOfEm.txt
    
Contents of **/nas4/Gil/Table_Structure** (SQL script for recreating the tables) 
    
    -rwxr-xr-x 1 sched helios   8589 Mar 14 16:34 Tables_AllOfEm.sql
    -rwxr-xr-x 1 sched helios 234161 Mar 14 16:32 Tables_AllOfEm.txt
    
## Keeping "test" Up-to-Date

The "test" database was created by copying all hbin, fbin, and abin records from the original database through about 2022-Feb-16 when the SQL system stopped being updated. While copying these records we ran into a small number of read errors (3?) in copying individual fbin records. The way the copy was done is to create the tables from scripts generated from the SQLserver eOVSA06 database, and then run the following script from the SQLserver SSMS (SQL Server Management Studio): 
    
    USE [test]
    DECLARE @cnt BIGINT = -2147483646
    DECLARE @msg VARCHAR(50)
    set identity_insert hbin off
    set identity_insert fbin on
    set textsize 2147483647
    WHILE @cnt < -1922969932
    BEGIN
      insert into fbin (Id, Bin) select top 100000 * from eOVSA06.dbo.fbin where id between @cnt and @cnt + 100000
      set @cnt = @cnt + 100000
      select @msg = 'CURRENT RECORD NUMBER' + STR(@CNT,15)
      RAISERROR(@msg, 0, 1) WITH NOWAIT
    END
    
This script starts with the first record in the fbin table (record ID -2147483646) and transfers 100000 records at a time, looping until the last record ID (-1922969932). The statements regarding @msg are just to print out the current record number after each 100000 were transferred, in case of an error. This transfer required about 90 h to complete. In practice, the transfer would die at some point due to the above-mentioned dik error, in which case I would reduce the 100000 to a smaller number, e.g. 1000, and change the @cnt declaration to the last ID printed out, and thus pin-point the failing record number (within 1000 records or so) and then set @cnt just beyond the failure point and go back to 100000 records at a time. 

Anyway, now that it is done we can use a version of the above to keep the "test" database up to date by running a similar transfer once per week or so. Annoyingly, it seems that the SQLserver SSMS forgets its connection to the \\\NAS4\nas4 share. To reestablish it: 
    
    EXEC sp_configure 'show advanced options', 1;
    GO
    RECONFIGURE;
    GO
    
    EXEC sp_configure 'xp_cmdshell',1
    GO
    RECONFIGURE
    GO
    
    EXEC XP_CMDSHELL 'net use N: \\nas4\nas4 /user:whatever\<username> <password>'
    
where the username and password are the credentials for connecting to the share. At this moment, there is an issue connecting to the "test" database from SMSS on the SQLserver. It is complaining that the database is at a higher version level, which is nonsense. What seems to have happened is that I connected a later version of SMSS to the database from another computer, and although I did not write to it I suppose something was noted in the log. I'll have to look for a way around this before we can add more records. Ah, Microsoft... 

## Updating SQL with Saved Records

If/when the SQL server is not available for any reason, observations are still possible by writing the "raw" stateframe and scanheader records to the disk for later restoration to the main SQL database. Such records are currently written to /nas4/Tables/scanheader/ and /nas4/Tables/stateframe folders. When the SQL server is again available, these raw records can be written to the SQL database. The following commands would restore a list of scanheader logs contained in the files variable: 
    
    from stateframedef import scanheader_log2sql
    from time import time
    for file in files:
        t = time(); scanheader_log2sql('/nas4/Tables/scanheader/'+file); print 'Took',time()-t,'seconds'
    
Each day takes only 1-2 s to restore. 

Similar commands are used to restore stateframe records: 
    
    from stateframedef import badlog2sql
    from time import time
    for file in files:
        t = time(); scanheader_log2sql('/nas4/Tables/stateframe/'+file); print 'Took',time()-t,'seconds'
    
But note in the case of stateframes that it takes about 40 min to restore a single day. 

# MySQL

It has become desirable to be able to calibrate EOVSA data from any machine, but that requires access to the calibration data, which has only been available on the Microsoft SQLserver at OVRO. That MS SQL database has two purposes, for calibration and for recording the 1-s stateframe consisting of monitor points for the entire array. The latter has developed into a multi-TB volume of data by now, which is prohibitive for copying elsewhere, but most of those data are not relevant to remote calibration anyway. 

For that reason, I have developed a truly calibration-only database consisting of those parts of the stateframe needed for calibration (basically the 1-s cadence gain state in the fV* tables), some parts of the scanheader data (hV* tables), and all the calibration records (abin table). This is a much more manageable volume of about 120 GB so far, after 7 years of operation, so we can expect that it will grow modestly in the future as well. 

For ease of portability, this new database is in MySQL format, which is accessed via Python using the mysql.connector routines. And to make it truly usable from anywhere, we have created an instance in the AWS RDB cloud service. 

## Creating the Database

### MySQL Tables

The MySQL database name is eOVSA, and contains tables that are created with the following SQL statements (part of the mysql_tables.txt file in the SourceCat folder of the eovsapy software): 
    
    CREATE TABLE `abin` (
      `Id` int(11) NOT NULL AUTO_INCREMENT,
      `Timestamp` double NOT NULL,
      `Version` float NOT NULL,
      `Description` varchar(8000) DEFAULT NULL,
      `Bin` blob NOT NULL,
      PRIMARY KEY (`Id`)
    );
    
    CREATE TABLE `fV66_vD15` (
      `Timestamp` double NOT NULL,
      `I15` TINYINT NOT NULL,
      `Ante_Fron_Wind_State` TINYINT NOT NULL,
      `Ante_Fron_FEM_HPol_Atte_First` TINYINT NOT NULL,
      `Ante_Fron_FEM_HPol_Atte_Second` TINYINT NOT NULL,
      `Ante_Fron_FEM_Clockms` INT NOT NULL,
      `Ante_Cont_SystemClockMJDay` INT NOT NULL,
      `Ante_Cont_Azimuth1` INT NOT NULL,
      `Ante_Cont_AzimuthPositionCorre` INT NOT NULL,
      `Ante_Cont_Elevation1` INT NOT NULL,
      `Ante_Cont_ElevationPositionCor` INT NOT NULL,
      `Ante_Cont_AzimuthPosition` INT NOT NULL,
      `Ante_Cont_ElevationPosition` INT NOT NULL,
      `Ante_Cont_RunMode` TINYINT NOT NULL,
      `Ante_Cont_AzimuthVirtualAxis` INT NOT NULL,
      `Ante_Cont_ElevationVirtualAxis` INT NOT NULL,
      `Ante_Cont_RAVirtualAxis` INT NOT NULL,
      `Ante_Cont_DecVirtualAxis` INT NOT NULL,
      `Ante_Cont_RAOffset` INT NOT NULL,
      `Ante_Cont_DecOffset` INT NOT NULL,
      `Ante_Cont_AzOffset` INT NOT NULL,
      `Ante_Cont_ElOffset` INT NOT NULL,
      `Ante_Fron_FEM_HPol_Regi_Level` TINYINT NOT NULL,
      `Ante_Fron_FEM_VPol_Regi_Level` TINYINT NOT NULL,
      PRIMARY KEY (`Timestamp`,`I15`)
    );
    
    CREATE TABLE `fV66_vD1` (
      `Timestamp` double NOT NULL,
      `FEMA_Powe_RFSwitchStatus` TINYINT NOT NULL,
      `FEMA_Rece_LoFreqEnabled` TINYINT NOT NULL,
      `LODM_LO1A_FSeqFile` VARCHAR(32) NOT NULL,
      `DPPoffsetattn_on` TINYINT NOT NULL,
      `Sche_Data_Weat_AvgWind` float NOT NULL,
      PRIMARY KEY (`Timestamp`)
    );
    
    CREATE TABLE `hV37_vD1` (
      `Timestamp` double NOT NULL,
      `TimeAtAcc0` double NOT NULL,
      `Project` varchar(32) NOT NULL,
      `SourceID` varchar(32) NOT NULL,
      PRIMARY KEY (`Timestamp`)
    );
    
    CREATE TABLE `hV37_vD50` (
      `Timestamp` double NOT NULL,
      `I50` TINYINT NOT NULL,
      `FSeqList` float NOT NULL,
      PRIMARY KEY (`Timestamp`, `I50`)
    );
    
### Backup and Restore

The primary MySQL database is on the Pipeline machine at OVRO. Records are periodically (daily) transferred to that database from MS SQL and the AWS Cloud database must then be updated to correspond. To create the initial Cloud databse, I used the command on Pipeline: 
    
    mysqldump -u root -p eOVSA > /data1/dgary/eOVSA_20220517.sql
    
which took about two hours to create the full backup (on 2022 May 17, when the database was about 130 GB). 

## Keeping the MySQL database up to date

Once these tables are created, they can be filled by querying the MS SQL database. The routines for doing this are in the Python3 eovsactl package, in the module sql2mysql. A single routine can handle the transfer to each table, one at a time. For example, the following lines will transfer all records from table fV66_vD1 taken during May 2022. 
    
    import eovsactl.sql2mysql as s2m
    s2m.sqltable2mysql('fV66_vD1',Time(['2022-05-01','2022-05-31']))
    
Note that when specifying a stateframe table (those starting with 'f', e.g. 'fV66_vD1'), only the columns noted above are transferred, and only those during times when EOVSA actually has data. This is accomplished by getting the scan times from FDB files, which must be on the system. For most tables, transferring a month of data from MS SQL to MySQL takes only a short time (minutes), but for the fV66_D15 table it can take several hours, so running that command using **screen** is recommended. 

The abin table is handled differently since the records are not in time order. To transfer all records later than the most recent record in MySQL 
    
    import eovsactl.sql2mysql as s2m
    s2m.sqltable2mysql('abin')
    
with no time specified. The latest Id from MySQL is read and all newer records are transferred from MS SQL up to the latest one. 

I have written a 1-liner that will send all fV* and hV* new records in the MS SQL database to the MySQL databases on both localhost and the amazonaws cloud: 
    
    import eovsactl.sql2mysql as s2m
    s2m.sync2mysql()
    
This is the command that will be run daily to keep the MS SQL and local MySQL databases in sync. It should take only a few minutes to run if done daily. It also dumps the updated data to a file /data1/YYYY-MM-DD.sql, which can be transferred to the cloud MySQL using the command: 
    
    mysql -h eovsa-db0.cgb0fabhwkos.us-west-2.rds.amazonaws.com -u admin -p eOVSA < /data1/YYYY-MM-DD.sql
    
## Maintaining the abin table

Note that among the above tables the abin table is unique in that new records can be written at any time with a timestamp that refers to the past, and in fact new ones have to be written well after the date of the data as new calibrations are done. Sometimes existing abin entries have to be overwritten with new ones using the same timestamp. Thus, it is not enough to update the abin table simply by updating a date range based on timestamp. However, the abin table Id column auto-increments so it should be enough to take the last abin record in MySQL and find it in the MS SQL, then update MySQL with all Ids larger than that. In fact this MySQL query: 
    
    select Id,Timestamp from abin order by Id desc limit 1
    
returns the laset MySQL record, which I find has the same Id as the corresponding record in MS SQL so if we always transfer from MS SQL to MySQL the record numbers should remain in sync and we can just find newer (greater) Id numbers. This is what the above 
    
    sqltable2mysql('abin')

call does. 

A further complication is that the MS SQL is not the only source of new abin records. By having a copy of the MySQL database in the cloud, abin records can be written by other users based on their new analysis of calibration data. For security reasons these records will be written to a "staging" table and at some regular cadence (e.g. 30 minutes) those records will be vetted (by some as-yet undefined means) and then transferred to the actual abin table. Those vetted records could first be written to the MS SQL abin table to keep it up to date, but then latency is a worry. Probably they can be written simultaneously to MS SQL and MySQL. 

I have adapted the code in the eovsapy.cal_header module to automatically update all three databases if an abin record is written at OVRO. The routine that allows that to happen is eovsactl.sql2mysql.abin2all3(). 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Database_Maintenance&oldid=6589](http://ovsa.njit.edu//wiki/index.php?title=Database_Maintenance&oldid=6589)"
