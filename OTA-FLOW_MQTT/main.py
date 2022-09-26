#When prog.py finishes, if OTA = True, main downloads it and overwrites program.py, then effectively reboots.
#If OTA is false main just exits.

#this is the program to be executed. Note we do not use the '.py' extension.
import program
import time
import machine #needed for the deep sleep function

upd_url = program.upd_url

#change your wifi credentials here.
ssid = '4G UFI-8975'
password = '1234567890'


OTA = 0
#print('OTA is ' + str(OTA))#debug

#here we set up the network connection
station = network.WLAN(network.STA_IF)
station.active(False)
station.active(True)
#station.config(reconnects = 5)

station.connect(ssid,password)

while station.isconnected() == False:
  #print('wait for connecting to WiFi')
  time.sleep(0.5)
  pass

#print board local IP address
print(station.ifconfig())
if OTA == 0:
    #print('starting program')
    OTA = program.mainprog(OTA)

#mainprog() is the starting function for my program. OTA is set to 0 on boot so the first time this code
#is run, it sets up the network connecton and then runs the program.
#The following code only runs when program.py exits with OTA = 1

if OTA == 1:
    #print('Downloading update')
    #download the update and overwrite program.py
    response = requests.get(upd_url)
    x = response.text.find("FAIL")
    if x > 15:
        #download twice and compare for security
        x = response.text
        response = requests.get(upd_url)
        if response.text == x:
            f = open("program.py","w")
            f.write(response.text)
            f.flush()
            f.close

            #soft reboot
            print('reboot now')
            machine.deepsleep(5000)