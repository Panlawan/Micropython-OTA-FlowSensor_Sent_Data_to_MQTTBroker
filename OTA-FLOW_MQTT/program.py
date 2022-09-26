import urequests
from utime import sleep
from machine import Pin, Timer
import utime
import ubinascii
import machine
from umqttsimple import MQTTClient
import ujson
sf = Pin(23, Pin.IN)

np = 0 # Numero de pulsos

calibrationFactor = 4.52
total = 0
last_time = utime.ticks_ms()
last_time1 = utime.ticks_ms()
c = 0
def pulseCounter(pin):
    global np
    np += 1

def freq():
    global np, Q, total
    frec = np * calibrationFactor     
    Q = (frec / 60) * 1000
    total += Q
    total_volume = total / 1000
    
    #print (f"flow= {frec} L/s, Q= {total_volume} L")
    np = 0
    return frec, total_volume


sf.irq(trigger = Pin.IRQ_RISING, handler = pulseCounter)

client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b'data/flow/1'

last_message = 0

mqtt_server = 'lalidts.com'

upd_url="https://www.download.lalidts.com/upload/firmware-flow_v0.0.1.py"

def restart_and_reconnect():
  #print('Failed to connect to MQTT broker. Reconnecting...')
  utime.sleep(10)
  #machine.reset()
  connect_and_subscribe()
  
def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.connect()
  #print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def check_for_updates(OTA):
    try:
        #print ('Checking for updates')
        response = urequests.get(upd_url)
        x = response.text.find("FAIL")
        if x > 15:
            OTA = 1
            #print('There is an update available')
            return(OTA)
        else:
            #print('There are no updates available.')
            return(OTA)
    except:
        #print('unable to reach internet')
        return(OTA)


def mainprog(OTA):
    #print('Mainprog - OTA is' + str(OTA))
    #This is the entry point for your program code
    #print('Program start')
    while OTA == 0:
        global now1, last_time1
        program_tasks()
        
        now1 = utime.ticks_ms()
        if utime.ticks_diff(now1, last_time1) > 5000:
            
            OTA = check_for_updates(OTA)
            last_time1 = now
        if OTA == 1:
           return(OTA)
        #print('OTA = ' + str(OTA))

def program_tasks():
    #do program tasks. If continuous loop, use counter or sleep to pass some time between
    #update checks. At your designated point, check for updates
    #try:
    
    #except OSError as e:
        #restart_and_reconnect()
        
    global frec, Q, now, last_time, client, now2, last_message, c

    now = utime.ticks_ms()
    now2 = utime.ticks_ms()
    if utime.ticks_diff(now, last_time) > 1000:
        frec, Q = freq()
        #print (f"flow= {frec} L/s, Q= {Q} L")
        last_time = now
        
    #try:
    if c == 0:
        try:
          client = connect_and_subscribe()
        except OSError as e:
          restart_and_reconnect()
        c = 1
    client.check_msg()
        
    if utime.ticks_diff(now2, last_message) > 7000:
        #msg = b'{"flow" = %f, "Q": %f}' % frec, %Q
            #json = '{"flow": {}, "Q": {} }'.format(frec, Q)
        msg = ujson.dumps(make_config(frec, Q))
        utime.sleep(1)
        client.publish(topic_pub, msg)
        last_message = now2
    #except OSError as e:
        #restart_and_reconnect()
        #print(e)
        
def make_config(a, b):
    return {'data': {'flow': a, "Q": b}}
