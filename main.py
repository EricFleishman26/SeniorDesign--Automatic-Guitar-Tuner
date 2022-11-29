from machine import Pin, I2C
import ssd1306
import framebuf
import time
from rotary_irq_esp import RotaryIRQ
import MotorControl

###CLASS DEFINITIONS

class Tuning: #Tuning class definition
  def __init__(self, name, string1, string2, string3, string4, string5, string6):
    self.name = name
    self.string = [string1, string2, string3, string4, string5, string6]


###FUNCTION DEFINITIONS

def Bound(low, high, value):
    return max(low, min(high, value))

def SetWindow(goToWindow):
    global selMin
    global selMax
    global windowState
    
    if goToWindow == 0:
        selMin = -350
        selMax = 350
        r.set(value=0, min_val=selMin, max_val=selMax, range_mode=RotaryIRQ.RANGE_BOUNDED)
        windowState = 0
    elif goToWindow == 1:
        selMin = 0
        selMax = len(tuningList) + 1
        r.set(value=0, min_val=selMin, max_val=selMax, range_mode=RotaryIRQ.RANGE_WRAP)
        windowState = 1
    elif goToWindow == 2:
        selMin = 0
        selMax = 7
        r.set(value=0, min_val=selMin, max_val=selMax, range_mode=RotaryIRQ.RANGE_WRAP)
        windowState = 2        
    elif goToWindow == 3:
        selMin = -350
        selMax = 350
        r.set(value=0, min_val=selMin, max_val=selMax, range_mode=RotaryIRQ.RANGE_BOUNDED)
        windowState = 3
    elif goToWindow == 4:
        selMin = 0
        selMax = 27
        r.set(value=0, min_val=selMin, max_val=selMax, range_mode=RotaryIRQ.RANGE_WRAP)
        windowState = 4
        
    print("selMin " + str(selMin))
    print("selMax " + str(selMax))
    print("ws " + str(windowState))
    print(" ")

def DisplayMain(tuningSelected, freq, bat_level):
    oled.fill(0)
    oled.text(str(bat_level) + "%", 95, 2)   

    oled.text('Tuning Selected:', 3, 15)
    oled.text(tuningSelected, 10, 25)

    freq_str = "Freq: " + str(freq) + " Hz"
    oled.text(freq_str, 5, 40)
    oled.text("String:x", 5, 50)
    oled.text("x Hz", 95, 50)

    oled.show()
  
def DisplayListOfTunings(tuningList, tuningSelected, select, bat_level):    
    oled.fill(0)
    oled.text(str(bat_level) + "%", 95, 2)
    
    oled.text('Tuning Selected:', 3, 15)
    oled.text(tuningSelected, 10, 25)

  
    oled.text('Select', 3, 35)
    if select == 0:
        oled.text('Exit', 10, 45)
    elif select == 1:
        oled.text('Add new Tuning', 10, 45)
    else:
        #oled.text(str(select), 10, 25)
        oled.text(tuningList[select - 2].name, 10, 45) #SELECT - 2 TO ACCOUNT FOR EXIT and add new

    oled.show()
    
def DisplayIndividual(curFreq, stringSelected, bat_level):
    oled.fill(0)
    oled.text(str(bat_level) + "%", 95, 2)   

    oled.text('String ' + str(stringSelected + 1) + ' Freq', 5, 12)
    oled.text(str(curFreq) + " Hz", 10, 25) 
    oled.show()


def DisplayTuning(tuning, select, bat_level):
    oled.fill(0)

    oled.text(tuning.name, 55, 0)
    oled.text('Exit', 7, 0)
    oled.text('str 1: ' + str(tuning.string[0]) + " Hz", 7, 8)      
    oled.text('str 2: ' + str(tuning.string[1]) + " Hz", 7, 16)      
    oled.text('str 3: ' + str(tuning.string[2]) + " Hz", 7, 24)      
    oled.text('str 4: ' + str(tuning.string[3]) + " Hz", 7, 32)      
    oled.text('str 5: ' + str(tuning.string[4]) + " Hz", 7, 40)
    oled.text('str 6: ' + str(tuning.string[5]) + " Hz", 7, 48)      

    
    if select == 0:
        oled.text('>',0, 0)
    elif select == 1:
        oled.text('>', 47, 0)
    else:
        oled.text('>',0, select*8 - 8)

    oled.show()
    
def DisplayNameChange(currName, newName, currLetter, bat_level):
    oled.fill(0)
    oled.text(str(bat_level) + "%", 95, 2)   
    
    oled.text("Curr Name: ", 2, 10)
    oled.text(currName, 10, 20)
    oled.text("New Name: ", 2, 30)    
    oled.text(newName, 10, 40)
    oled.text(currLetter, 59, 50)      
    
    oled.show()

def buttonInterrupt(pin):
    global button_pressed
    button_pressed = 1

      
#alphabet for keyboard
      
###VALUE INITIALIZATION
      
# ESP32 Pin assignment 
i2c = I2C(0, scl=Pin(22), sda=Pin(23))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Button setup
button = Pin(14, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=buttonInterrupt)

# Rotary Encoder Setup
r = RotaryIRQ(pin_num_clk=13, pin_num_dt=12, min_val=-350, max_val=350, reverse=True, range_mode=RotaryIRQ.RANGE_BOUNDED)
r.set(value=0)

# Window States
button_pressed = 0
windowState = 0
selMin = 0
selMax = 0

curFreq = 0
bat_level = 100 # range determined by linear interpolation from 4.2 - 2.8 V 0-100, 

#init values
tuning1 = Tuning("Preset1", 10,20,30,40,50,60)
tuning2 = Tuning("Preset2", 50,100,150,200,250,300)

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '<-', 'exit']
currLetter = alphabet[0]
newName = ' '

tuningList = [tuning1, tuning2]
tuningSelected = 0 #which configuration is selected
stringSelected = 0 #which str  is selected
newStringFreq = 0 #new string frequency being written

#set first window values
SetWindow(0)

while True:
    #time.sleep(0.1) #sleep a tenth a second #messes with button logic
    
    select = r.value()

    #button pressed code
    if button_pressed:
        time.sleep(0.1)
        
        #print("windowState: " + str(windowState))
        #print('Button pressed!')        
        if windowState is 0: #main
            SetWindow(1)
        
        elif windowState is 1:#list of tunings
            if select is 0:
                SetWindow(0)
            elif select is 1:
                emptyTuning = Tuning('blank', 0,0,0,0,0,0)
                tuningList.append(emptyTuning)
                SetWindow(1) #MUST SET WINDOW TO UPDATE BOUNDS
            else:

                SetWindow(2)
                tuningSelected = Bound(selMin, selMax, select) - 2 # MINUS 2 TO ACCOUNT FOR EXIT
                print("tuningSelected: " + str(tuningSelected))

        elif windowState is 2: #string or name select
            if select is 0: #exit
                SetWindow(0)
            elif select is 1:
                #stuff with the name change
                #print("add name changing!!")
                SetWindow(4)
                newName = ''
            else:
                stringSelected = Bound(selMin, selMax, select) - 2
                print("string selected: " + str(stringSelected))
                SetWindow(3)
        
        elif windowState is 3: #individual string frequency change
            newStringFreq = Bound(selMin, selMax, select)
            print("new tuning value: " + str(newStringFreq))
            tuningList[tuningSelected].string[stringSelected] = newStringFreq

            SetWindow(2)                    
        elif windowState is 4: #name change
            if select is 27:
                #set name
                tuningList[tuningSelected].name = newName
                SetWindow(2)
            elif select is 26:
                print('backspace')
                newName = newName[:-1]
            else:
                print('add letter')
                newName = newName + alphabet[select]
        
        else: #ELSE FOR IF ITS BROKEN
            SetWindow(0)
            
        button_pressed = 0 #return value to 1
        select = Bound(selMin, selMax, select) #bound before (JUST IN CASE? not sure if needed) 

    select = Bound(selMin, selMax, select)

    #individual display and encoder control logic
    if windowState is 0:
        curFreq = MotorControl.getFrequency()
        targetFreq = tuningList[tuningSelected].string[0]
        MotorControl.setDesired(targetFreq)
        DisplayMain(tuningList[tuningSelected].name, curFreq, bat_level)
    elif windowState is 1:
        DisplayListOfTunings(tuningList, tuningList[tuningSelected].name, select, bat_level)
    elif windowState is 2:    
        DisplayTuning(tuningList[tuningSelected], select, bat_level)
    elif windowState is 3:
        DisplayIndividual(select, stringSelected, bat_level)
    elif windowState is 4:
        DisplayNameChange(tuningList[tuningSelected].name, newName, alphabet[select], bat_level)
  
        
    time.sleep_ms(50)



