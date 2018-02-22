#!/usr/bin/env python  
import pigpio   
import sys
import time
import random
from time import sleep

colour = sys.argv[1] 
pi = pigpio.pi() 

Red = 16
Green = 20  
Blue = 21
White = 19  

if colour == "red":
	pi.set_PWM_dutycycle(Red, 255)
	pi.set_PWM_dutycycle(Green, 0)
	pi.set_PWM_dutycycle(Blue, 0)
	pi.set_PWM_dutycycle(White, 0)
if colour == "green":
	pi.set_PWM_dutycycle(Red, 0)	
	pi.set_PWM_dutycycle(Green, 255)
	pi.set_PWM_dutycycle(Blue, 0)
	pi.set_PWM_dutycycle(White, 0)

if colour == "blue":
	pi.set_PWM_dutycycle(Red, 0)
	pi.set_PWM_dutycycle(Green, 0)
	pi.set_PWM_dutycycle(Blue, 255)
	pi.set_PWM_dutycycle(White, 0)
	
if colour == "white":
	pi.set_PWM_dutycycle(Red, 0)
	pi.set_PWM_dutycycle(Green, 0)
	pi.set_PWM_dutycycle(Blue, 0)
	pi.set_PWM_dutycycle(White, 255)
