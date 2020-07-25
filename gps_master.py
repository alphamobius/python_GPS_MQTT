import psutil
import json
import gpsd
import subprocess
import time
import logging


#configure logging
error_log = "/home/pi/GPS.log"
logging.basicConfig(filename=error_log, level=logging.DEBUG)

#see if I'm already running
#print('checking if Im alive')
count=0
for name in (p.name() for p in psutil.process_iter()):
    if name == "python3":
        count += 1
if count > 1:
    logging.debug("i'm already running")
    print('Bye!')
    exit()
#print('Im alive!')

#default 5 minutes
delay = 300
#connect to gpsd socket, provided by gpsd linux service
try:
    gpsd.connect()
    logging.debug("gpsd connected successfully")
except:
    logging.exception("gpsd failed to connect")
    print("gpsd failed to connect")
#    #exit()

while 1:
    #update timer for log
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    #get json
    packet = gpsd.get_current()
    
    #if good fix, make a more portable json of the data I want
    if packet.mode >= 2:
        location = {
            "lat" : str(packet.lat),
            "long" : str(packet.lon),
            "alt" : str(packet.alt), 
            "time" : str(packet.time),
            #"speed" : str(packet.speed),
        }
    else:
    #no good satellite fix :( 
        logging.debug('no 2d fix')
        logging.debug(current_time)
        location = {
            "Satellites" : str(packet.sats),
            "Mode" : str(packet.mode),
        }
    
    #convert to string for easy printing
    location = json.dumps(location)
    
    #print to a file
    logging.info(location)
    with open('/home/pi/location','w') as f:
        f.write(location)
    
    #attempt wifi host, then attempt 4g connection to home
    try:
        #publish over wifi
        subprocess.check_output(['mosquitto_pub', '-h', 'x.x.x.x', '-p', '1883', '-u', 'user', '-P', 'pass', '--capath', '/home/pi', '--cafile', 'ca.crt', '-t', '/car/location', '-m', location])
    except:
        #publish over 4g
        logging.debug("Not on WIFI")
        try:
            subprocess.check_output(['mosquitto_pub', '-h', 'www.website.com', '-p', '1883', '-u', 'user', '-P', 'pass', '--capath', '/home/pi', '--cafile', 'ca.crt', '-t', '/car/location', '-m', location])
        except:
            logging.debug('no route home')

    #future expansion for subscribe and two way C2
    #make functions that are called here with try/catches based upon what the input was. 

    #adjust timing interval

    #start car

    #turn off car

    #roll down windows

    #roll up windows

    #lock doors

    #unlock doors

    #error: invalid command
    #security lockout of 3 bad commands?

    time.sleep(delay)
