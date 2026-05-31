# 27-m Antenna Commands - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/27-m_Antenna_Commands
**Scraped:** 2025-08-05 09:12:48

# 27-m Antenna Commands

From EOVSA Wiki

Jump to navigation Jump to search

JWL 2015-10-14 

27-M ANTENNA COMMAND LIST   
---  
**Command** | **Syntax** | **Arguments Value(s) Units** | **Description** | **Hardware  
** controlled****  
FRM-HOME  | frm-home <ant> | <ant> antenna ant14|ant15  | Homes the x-axis (receiver select),  
and Position angle axis.  | Geo Brick LV (PMAC)   
FRM-RX-SEL  | frm-rx-sel <rx> <ant> | <rx> receiver no. Lo|Hi   
<ant> antenna ant14|ant15  | Move x- and z-axes to select receiver.   
1: low-frequency receiver,   
2 : high-frequency receiver.  | Geo Brick LV (PMAC)   
FRM-SET-PA  | frm-set-pa <pa> <ant> | <pa> position angle -90 to 90 degrees   
<ant> antenna ant14|ant15  | Set the position angle for polarization.   
Pointing to the south, the angle is 0˚  | Geo Brick LV (PMAC)   
FRM-X-OFFSET  | frm-x-offset <xoff> <ant> | <xoff> x-axis offset mm   
<ant> antenna ant14|ant15  | Offset in x relative to the selected receiver.   
In effect until a new value is set,   
or the Geo Brick is reset.  | Geo Brick LV (PMAC)   
FRM-Z-OFFSET  | frm-z-offset <zoff> <ant> | <zoff> z-axis offset mm   
<ant> antenna ant14|ant15  | Offset in z relative to the selected receiver.   
In effect until a new value is set,   
or the Geo Brick is reset.  | Geo Brick LV (PMAC)   
FRM-ABS-X  | frm-abs-x <xpos> <ant> | <xpos> x-axis position mm   
<ant> antenna ant14|ant15  | Set to an absolute x position. Not use  | Geo Brick LV (PMAC)   
FRM-ABS-Z  | frm-abs-z <zpos> <ant> | <zpos> z-axis position mm   
<ant> antenna ant14|ant15  | Set to an absolute z position. Not use  | Geo Brick LV (PMAC)   
FRM-KILL  | frm-kill <ant> | <ant> antenna ant14|ant15  | Kill all motors. They will be unpowered  | Geo Brick LV (PMAC)   
FRM-ENABLE  | frm-enable <ant> | <ant> antenna ant14|ant15  | Enable all motors after a kill  | Geo Brick LV (PMAC)   
OUTLET  | outlet <out> <state> | <outlet> outlet no. 1 to 8   
<state> new state on|off  
<ant> antenna ant14|ant15  | Turns the selected outlet on or off  | Ethernet power strip   
ND-ON  | nd-on <ant> | <ant> antenna ant14|ant15  | Turns noise diode on via power strip  | Ethernet power strip   
ND-OFF  | nd-off <ant> | <ant> antenna ant14|ant15  | Turns noise diode off via power strip  | Ethernet power strip   
RX-SELECT  | rx-select <rx> <ant> | <rx> receiver no. Lo|Hi   
<ant> antenna ant14|ant15  | Moves the requested receiver to focus   
and sets RF switch appropriately  | Geo Brick LV,  
Ethernet power strip   
LNA-GATE1  | lna-gate1 <Ina> <vg1> | <lna> amplifier LV|LH|HV|HH   
<vg1> first gate voltage -2.0 to 2.0 V   
<ant> antenna ant14|ant15  | Sets the first gate bias on the selected   
amplifier to the requested voltage.  
Will only operate if that amplifier is enabled  | Beaglebone   
LNA-GATE2  | lna-gate2 <Ina> <vg1> | <lna> amplifier LV|LH|HV|HH   
<vg1> first gate voltage -2.0 to 2.0 V   
<ant> antenna ant14|ant15  | Sets the second gate bias on the selected   
amplifier to the requested voltage.  
Will only operate if that amplifier is enabled  | Beaglebone   
LNA-DRAIN  | lna-drain <lna> <vd> | <lna> amplifier LV|LH|HV|HH   
<vd> drain voltage 0 to 2.0 V  
<ant> antenna ant14|ant15  | Sets the drain bias on the selected   
amplifier to the requested voltage.  
Will only operate if that amplifier is enabled  | Beaglebone   
LNA-ENABLE  | lna-bias <lna> <state> | <lna> amplifier LV|LH|HV|HH  
<state> amplifier enabled state on|off  
<ant> antenna ant14|ant15  | Turn the requested amplifier on or off  | Beaglebone   
  
**Notes:**

  1. The antenna number, <ant>, is required only for the ACC command. The front-end computer should ignore it.
  2. All numbers are floats
  3. The frontend will echo the command (but not the arguments)
  4. Everything is case-insensitive

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=27-m_Antenna_Commands&oldid=375](http://ovsa.njit.edu//wiki/index.php?title=27-m_Antenna_Commands&oldid=375)"
