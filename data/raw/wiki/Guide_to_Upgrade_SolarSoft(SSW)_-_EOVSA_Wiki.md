# Guide to Upgrade SolarSoft(SSW) - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Guide_to_Upgrade_SolarSoft(SSW)
**Scraped:** 2025-08-05 09:13:41

# Guide to Upgrade SolarSoft(SSW)

From EOVSA Wiki

Jump to navigation Jump to search

This guide compiles all the (scattered) steps to upgrade SSW taken from different sources. SSW upgrade using passive_ftp was stopped in August 2019. The current way to upgrade SSW is to use the WGET executable. If you have done an update on SSW since August 2019 and your system already has WGET, any further upgrade can be made by directly following the steps underlined [here](https://hesperia.gsfc.nasa.gov/rhessi3/docs/ssw_update_help.html). For Linux and MacOS you can check if you already have WGET by typing the command "which wget" in the bash shell. 

If your system was not updated since August 2019, follow the steps below: 

### MacOS

In order to perform the upgrade, you must be the owner of the SSW tree. If you do not have admin privileges, consider installing ssw in $HOME directory. If you already have wget installed in your system, then **skip to point 3**. **Using homebrew**

To install homebrew, type the following command in the terminal: 
    
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    
Once homebrew is installed, you can simply install wget by using the following command: 
    
    brew install wget
    
**Using MacPorts**

Alternatively, wget can also be installed using MacPorts. Directions to install MacPorts for specific OS versions are given [here](https://www.macports.org/install.php) After installation, the following command will install wget: 
    
    sudo port install wget
    
#### 2\. Prepare SSW to use wget for the first time

  * Go to [[1]](http://www.lmsal.com/solarsoft/) and scroll all the way down to the SSW installation form.
  * For "Installation Type", select "Upgrade Existing".
  * For "Transfer Protocol", select "curl".
  * Specify the existing path to SSW on your computer. (You can find it in your ~/.bashrc or ~/.cshrc)
  * Click on "Generate Installation Script" and download it.
  * If you are in the bash shell, please change to csh or tcsh, open the directory where the installation script was downloaded and run it

    % tcsh
    Execute the script using the C-Shell 
    % csh -f scriptname
    
#### 3\. Upgrade SSW

  * While in SSWIDL type:

    ssw_upgrade, /loud , /spawn
    
This will update all the SSW branches listed in the SSW_INSTR environment variable (as well as their dependencies, and always includes gen and packages/binaries). This most likely will not update every branch in your SSW tree since you probably run SSW with a subset of branches activated. 

  * To upgrade specific branches, type for example

    ssw_upgrade, /lasco, /spawn
    
##### Possible Errors

  * **Error: bash:wget command not found** : Indicates that wget was installed using bash and csh/tcsh is not able to locate it. To resolve, simply give the path to wget in the upgrade command

    ssw_upgrade, /loud, /spawn, wget = 'path/to/wget'                          
    
  * **RD_TFILE: No file: /usr/local/ssw/site/mirror/ssw_upgrade.mirror** : check if the "**/spawn** " keyword has been missed

  * **Other errors with WGET** : Sometimes using an older version of wget gives errors during SSW_upgrade, in this case add the keyword "**/lmsal** " to the upgrade command. This allows use of older wget versions.

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Guide_to_Upgrade_SolarSoft(SSW)&oldid=6192](http://ovsa.njit.edu//wiki/index.php?title=Guide_to_Upgrade_SolarSoft\(SSW\)&oldid=6192)"
