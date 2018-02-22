#!/usr/bin/env python  
import pigpio   
import datetime 
import time
import sys 

Mode = sys.argv[1] 
pi = pigpio.pi()  

Red = 16
Green = 20  
Blue = 21
White = 19  

delay = 0.009

def time_in_range(start, end, x): 
 if start <= end: 
  return start <= x <= end 
 else: 
  return start <= x or x <= end 
 
def slow_change(red_target, green_target, blue_target, white_target):
 try:
  current_red = pi.get_PWM_dutycycle(Red)
  current_green = pi.get_PWM_dutycycle(Green)
  current_blue = pi.get_PWM_dutycycle(Blue)
 except:
  current_red = 0
  current_green = 0
  current_blue = 0
 try:
  current_white = pi.get_PWM_dutycycle(White)
 except:
  if(pi.read(White) == 1):
   current_white = 255
  else:
   current_white = 0 
        
 while current_red != red_target or current_green != green_target or current_blue != blue_target or current_white != white_target:
  if current_red < red_target:
    current_red += 1
    pi.set_PWM_dutycycle(Red, current_red)
    time.sleep(delay);
  if current_red > red_target:
    current_red -= 1
    pi.set_PWM_dutycycle(Red, current_red)
    time.sleep(delay);
  if current_green < green_target:
    current_green += 1
    pi.set_PWM_dutycycle(Green, current_green)
    time.sleep(delay);
  if current_green > green_target:
    current_green -= 1
    pi.set_PWM_dutycycle(Green, current_green)
    time.sleep(delay);
  if current_blue < blue_target:
    current_blue += 1
    pi.set_PWM_dutycycle(Blue, current_blue)
    time.sleep(delay);
  if current_blue > blue_target:
    current_blue -= 1
    pi.set_PWM_dutycycle(Blue, current_blue)
    time.sleep(delay);
  if current_white < white_target:
    current_white += 1
    pi.set_PWM_dutycycle(White, current_white)
    time.sleep(delay);
  if current_white > white_target:
    current_white -= 1
    pi.set_PWM_dutycycle(White, current_white)
    time.sleep(delay);
  
def update_status(redintensity, greenintentity, blueintensity, whiteintensity):
 
 try:
  whitefile = open('/home/pi/Lights/currentWhite.txt', 'w')
  whitefile.write('#{0:02x}'.format(whiteintensity))     
  whitefile.close()
 except IOError:
  print "Error - Unable to write white light intensity"
  
 try:
  file = open('/home/pi/Lights/currentColour.txt', 'w')
  file.write('#{0:02x}'.format(redintensity) + '{0:02x}'.format(greenintentity) + '{0:02x}'.format(blueintensity))
  file.close()
 except IOError:
  print "Error - Unable to write RGB intensity"

  
###### Main ###### 
 
if Mode == "reboot":
 if datetime.datetime.now().weekday() < 5:
  # Check Dawn
  if time_in_range(datetime.time(7,0,0), datetime.time(12,00,0), datetime.datetime.now().time()):
   Mode = "dawn"
  # Check Day
  if time_in_range(datetime.time(12,0,0), datetime.time(18,55,0), datetime.datetime.now().time()):
   Mode = "off"
  # Check Dusk
 else:
  # Weekend!
  if time_in_range(datetime.time(7,0,0), datetime.time(9,5,0), datetime.datetime.now().time()):
   Mode = "dawn"
  if time_in_range(datetime.time(9,05,0), datetime.time(18,55,0), datetime.datetime.now().time()):
   Mode = "off"
  
 if time_in_range(datetime.time(18,55,0), datetime.time(0,0,0), datetime.datetime.now().time()):
  Mode = "dusk"
 if time_in_range(datetime.time(21,00,0), datetime.time(0,0,0), datetime.datetime.now().time()):
  Mode = "dusklow"
 # Check Night
 if time_in_range(datetime.time(0,0,0), datetime.time(7,0,0), datetime.datetime.now().time()):
  Mode = "night"  
  
if Mode == "dawn":
 slow_change(255, 255, 255, 255)
 update_status(255, 255, 255, 255)
if Mode == "clean":
 slow_change(255, 255, 255, 255)
 update_status(255, 255, 255, 255)
if Mode == "dusklow":
 slow_change(100, 100, 100, 50)
 update_status(100, 100, 100, 50)
if Mode  == "day":
 slow_change(255, 255, 255, 255) 
 update_status(255, 255, 255, 255)
if Mode == "dusk":
 slow_change(255, 255, 255, 255)
 update_status(255, 255, 255, 255)
if Mode  == "night":
 slow_change(0, 0, 200, 0) 
 update_status(0, 0, 200, 0)
if Mode  == "off":
 slow_change(0, 0, 0, 0) 
 update_status(0, 0, 0, 0)
