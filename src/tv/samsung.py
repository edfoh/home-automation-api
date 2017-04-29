import sys
sys.path.insert(0, './lib')

import os
import socket
import base64
import time, datetime
from uuid import getnode as get_mac

def get_mac_address():
    mac_address = get_mac()
    h = hex(mac_address)[2:].zfill(12)
    return ":".join(i + j for i, j in zip(h[::2], h[1::2]))

#IP Address of TV
tvip = os.environ.get("TV_IP_ADDRESS")
#IP Address of TV
myip = socket.gethostbyname(socket.gethostname())
#Used for the access control/validation, but not after that AFAIK
mymac = get_mac_address()
#What the iPhone app reports
appstring = "iphone..iapp.samsung"
#Might need changing to match your TV type
tvappstring = "iphone.UE55C8000.iapp.samsung"
#What gets reported when it asks for permission
remotename = "Python Samsung Remote"

# Key Reference
# Normal remote keys
 #KEY_0
 #KEY_1
 #KEY_2
 #KEY_3
 #KEY_4
 #KEY_5
 #KEY_6
 #KEY_7
 #KEY_8
 #KEY_9
 #KEY_UP
 #KEY_DOWN
 #KEY_LEFT
 #KEY_RIGHT
 #KEY_MENU
 #KEY_PRECH
 #KEY_GUIDE
 #KEY_INFO
 #KEY_RETURN
 #KEY_CH_LIST
 #KEY_EXIT
 #KEY_ENTER
 #KEY_SOURCE
 #KEY_AD #KEY_PLAY
 #KEY_PAUSE
 #KEY_MUTE
 #KEY_PICTURE_SIZE
 #KEY_VOLUP
 #KEY_VOLDOWN
 #KEY_TOOLS
 #KEY_POWEROFF
 #KEY_CHUP
 #KEY_CHDOWN
 #KEY_CONTENTS
 #KEY_W_LINK #Media P
 #KEY_RSS #Internet
 #KEY_MTS #Dual
 #KEY_CAPTION #Subt
 #KEY_REWIND
 #KEY_FF
 #KEY_REC
 #KEY_STOP
# Bonus buttons not on the normal remote:
 #KEY_TV
#Don't work/wrong codes:
 #KEY_CONTENT
 #KEY_INTERNET
 #KEY_PC
 #KEY_HDMI1
 #KEY_OFF
 #KEY_POWER
 #KEY_STANDBY
 #KEY_DUAL
 #KEY_SUBT
 #KEY_CHANUP
 #KEY_CHAN_UP
 #KEY_PROGUP
 #KEY_PROG_UP

class SamsungTv(object):
    def __init__(self):
        # Open Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((tvip, 55000))

        # First configure the connection
        ipencoded = base64.b64encode(myip)
        macencoded = base64.b64encode(get_mac_address())
        messagepart1 = chr(0x64) + chr(0x00) + chr(len(ipencoded)) \
        + chr(0x00) + ipencoded + chr(len(macencoded)) + chr(0x00) \
        + macencoded + chr(len(base64.b64encode(remotename))) + chr(0x00) \
        + base64.b64encode(remotename)

        part1 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring \
        + chr(len(messagepart1)) + chr(0x00) + messagepart1
        self.sock.send(part1)

        messagepart2 = chr(0xc8) + chr(0x00)
        part2 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring \
        + chr(len(messagepart2)) + chr(0x00) + messagepart2
        self.sock.send(part2)

    def __enter__(self):
        return self

    # Function to send keys
    def sendKey(self, skey):
        messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(base64.b64encode(skey))) + chr(0x00) + base64.b64encode(skey)
        part3 = chr(0x00) + chr(len(tvappstring)) + chr(0x00) \
        + tvappstring + chr(len(messagepart3)) + chr(0x00) + messagepart3
        self.sock.send(part3)

    def powerOn(self):
        self.sendKey("KEY_POWERON")

    def powerOff(self):
        self.sendKey("KEY_POWEROFF")

    def sendHdmi(self):
        self.sendKey("KEY_HDMI")

    def sendTv(self):
        self.sendKey("KEY_DTV")

    def sendComponent1(self):
        self.sendKey("KEY_COMPONENT1")

    def volup(self):
        self.sendKey("KEY_VOLUP")

    def voldown(self):
        self.sendKey("KEY_VOLDOWN")

    def mute(self):
        self.sendKey("KEY_MUTE")

    def volupTimes(self, times):
        for i in range(times):
            self.volup()
            time.sleep(0.25)

    def voldownTimes(self, times):
        for i in range(times):
            self.voldown()
            time.sleep(0.25)

    def changeChannel(self, channelNumber):
        for digit in str(channelNumber):
            self.sendKey("KEY_{}".format(digit))
            time.sleep(0.25)
        self.sendKey("KEY_ENTER")

    def sendSource(self):
        self.sendKey("KEY_SOURCE")

    def sendExit(self):
        self.sendKey("KEY_EXIT")

    def keyUpTimes(self, times):
        for i in range(times):
            self.sendKey("KEY_UP")
            time.sleep(0.25)
        self.sendKey("KEY_ENTER")

    def keyDownTimes(self, times):
        for i in range(times):
            self.sendKey("KEY_DOWN")
            time.sleep(0.25)
        self.sendKey("KEY_ENTER")

    def sendAbcKids(self):
        self.sendKey("KEY_2")
        time.sleep(0.25)
        self.sendKey("KEY_2")
        time.sleep(0.25)
        self.sendKey("KEY_ENTER")

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()

# Now send the keys as you like, e.g.,
#sendKey("KEY_VOLUP",sock,tvappstring)
#time.sleep(1)
#sendKey("KEY_TOOLS",sock,tvappstring)
#time.sleep(1)
#sendKey("KEY_RIGHT",sock,tvappstring)
#time.sleep(1)
#sendKey("KEY_DOWN",sock,tvappstring)
#time.sleep(1)
#sendKey("KEY_RIGHT",sock,tvappstring)

# Close the socket when done
#sock.close()
