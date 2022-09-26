from machine import Pin, Timer
import utime

sf = Pin(23, Pin.IN)

np = 0 # Numero de pulsos

calibrationFactor = 4.52

looptime = Timer(0)
total = 0
def pulseCounter(pin):
    global np
    np += 1

def freq():
    global np, Q, total
    frec = np * calibrationFactor     
    Q = (frec / 60) * 1000
    total += Q
    total_volume = total / 1000
    
    print (f"flow= {frec} L/s, Q= {total_volume} L")
    np = 0
    return frec, Q


sf.irq(trigger = Pin.IRQ_RISING, handler = pulseCounter)

#last_time = utime.ticks_ms()
"""
while True:
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_time) > 1000:
        frec, Q = freq()
        last_time = now
"""
#looptime.init(mode= Timer.PERIODIC, period= 1000, callback= freq)