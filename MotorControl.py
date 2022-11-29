import time
from machine import Pin
from machine import Timer

#Implement the frequency detection function
def detectFrequency(p):
    global start_time
    global frequency
    
    if start_time == 0:
        start_time = time.ticks_us()
    else:
        time_diff = time.ticks_diff(time.ticks_us(), start_time)
        try:
            listened_frequency = 1 / (time_diff / 1000000)
            if abs(listened_frequency - desired) >= 20:
                pass
            else:
              frequency = listened_frequency  
        except:
            pass
        start_time = 0


#Implement the handler for Timer 1
def tim1Callback(t):
    global frequency
    
    lower_thresh = desired - 1
    upper_thresh = desired + 1
    
    if frequency >= lower_thresh and frequency <= upper_thresh:
        print("Tuned to {} Hz".format(frequency))
        t.deinit()
    else:
        tuneToFrequency(frequency, desired)

#Implement the function to determine clockwise or counter clockwise rotation
def tuneToFrequency(frequency, desired):
    if 0 <= frequency and frequency < 5:
        print("Current Note: E (low)")
    elif 5 <= frequency and frequency < 10:
        print("Current Note: A")
    elif 10 <= frequency and frequency < 15:
        print("Current Note: D")
    elif 15 <= frequency and frequency < 20:
        print("Current Note: G")
    elif 20 <= frequency and frequency < 25:
        print("Current Note: B")
    else:
        print("Current Note: E (high)")
    
    
    if frequency < desired:
        print("Current Frequency: {}".format(frequency))
        turnClockwise(frequency, desired)
    else:
        print("Current Frequency: {}".format(frequency))
        turnCounterClockwise(frequency, desired)

#Implement the function to rotate the motor clockwise
def turnClockwise(frequency, desired):
    #0 for higher
    dir_pin.value(0)
    steps = (round(abs(desired - frequency)))
    
    if steps == 0:
        steps = 1
        
    print("Steps: {}".format(steps))
    
    for i in range(steps):
        step_pin.value(1)
        time.sleep(0.001)
        step_pin.value(0)
        time.sleep(0.001)
        
        
#Implement the function to rotate the motor counter clockwise
def turnCounterClockwise(frequency, desired):
    #1 for higher
    dir_pin.value(1)
    steps = (round(abs(desired - frequency)))
    
    if steps == 0:
        steps = 1
    
    print("Steps: {}".format(steps))
    
    for i in range(steps):
        step_pin.value(1)
        time.sleep(0.001)
        step_pin.value(0)
        time.sleep(0.001)

#Set desired frequency
desired = 330

#Initialize the start time and detected frequency
start_time = 0
frequency = 0

#Initialize the interrupt on the rising edge of the incoming signal
frequency_pin = Pin(4, Pin.IN)
frequency_pin.irq(trigger=Pin.IRQ_RISING, handler=detectFrequency)

#Initialize pins for the motor
dir_pin = Pin(25, Pin.OUT)
step_pin = Pin(26, Pin.OUT)

#Initialize timer to check if the current input frequency needs to be tuned
tim1 = Timer(1)
tim1.init(period=1000, callback=tim1Callback)


