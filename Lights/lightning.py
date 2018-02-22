#!/usr/bin/env python  
import pigpio   
import sys
import time
import random
from time import sleep
pi = pigpio.pi() 

Red = 16
Green = 20  
Blue = 21
White = 19  

MaxIntensity = 255
MinIntensity = 25

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100, fill = ' '):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(barLength * iteration // total)
    bar = fill * filledLength + ' ' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    sys.stdout.flush()

#### Main ####
pi.set_PWM_dutycycle(Red, 255) 
pi.set_PWM_dutycycle(Green, 255) 
pi.set_PWM_dutycycle(Blue, 255) 
pi.set_PWM_dutycycle(White, 10) 

intensity = random.randrange(MinIntensity, MaxIntensity, 1)
#pi.set_PWM_dutycycle(Blue, 100) 

def lightning_strike():
	flash_count = random.randrange(0, 5, 1)
	
	msleepduration = random.randrange(40, 120, 1)/1000.0
	
	while flash_count > 0:
		flash_intensity = random.randrange(MinIntensity,MaxIntensity,1)
		mflash_length = random.randrange(40,100,1)/1000.0
		mdarkness_length = random.randrange(40,200,1)/1000.0
		#printProgress(flash_intensity, 255, prefix = '', suffix = '', barLength = 50, fill="-")
		
		pi.set_PWM_dutycycle(Red, flash_intensity) 
		pi.set_PWM_dutycycle(Green, flash_intensity) 
		pi.set_PWM_dutycycle(Blue, flash_intensity)
		pi.set_PWM_dutycycle(White, flash_intensity) 
		
		sleep(mflash_length)
		#printProgress(0, 255, prefix = '', suffix = '', barLength = 50, fill="-")
		pi.set_PWM_dutycycle(Red, 255) 
		pi.set_PWM_dutycycle(Green, 255) 
		pi.set_PWM_dutycycle(Blue, 255)
		pi.set_PWM_dutycycle(White, 10) 
		
		sleep(mdarkness_length)
		flash_count = flash_count - 1
		

while 1:
	lightning_strike()
	sleep(random.randrange(1, 7, 1))
