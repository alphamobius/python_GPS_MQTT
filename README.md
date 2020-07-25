# python_GPS_MQTT
Python script for GPSD enabled devices to call home over MQTT(S)

#install
place in /home/pi
crontab -e #not as root...
* * * * * python3 /home/pi/gps_master.py &
It'll run every minute, for debugging, otherwise slow this down.
Will kill itself if another process is already successfully running, with psutil loop

#attach GPS
Install GPSD, pointed at /dev/ttyACM0, or whatever the device is

#attach 4g dongle
Install your favorite 4g dongle
  PIs should use the sixfab 4g with base hat
  https://docs.sixfab.com/docs/raspberry-pi-3g-4g-lte-base-hat-introduction

#provide constant power with whatever it is attached to, like your car. 

#setup mosquitto server to catch the callouts. Enable TLS/SSL...

#???

#profit









#background

Version 1: Tested in 2018, but In 2020, the rest of the 2g networks in the U.S. will come down, requiring updates from previous hardware. Ran off of a pi - zero as a test of concept, to learn about AT commands, and SSL+MQTT compatibility. Disassembled immediately.

Version 2 ran compiled c code on a Teensy w/ ARM cortex m-0, (yay real-time operating systems) but using the WOLFPACK SSL library was not worth the hassle for a single project. 
I reluctantly went back to using a pi and python libraries as it's easier to make edits and experimental changes when you don't have to pull device out from the dash and recompile the entire thing for a small change. Excellent engineering practice, but frankly I'm tired of overly complicated updates to a simple problem, for the few trackers I'll be using personally.  If producing large scale, I'd continue the efforts here to keep hardware and platform small, on an RTOS, minimizing additional non-necessary services. 
Example: Ran into BIRD scooters at defcon 2019, who are doing the RTOS concept well; anyone solving the GPS asset tracking problem at scale should use that kind of a model

Version 3 of this effort, running on a pi. Python for the win. Commercial GPS trackers exist, but this allows the reporting server to be self-hosted. 
