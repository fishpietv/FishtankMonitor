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

intensity = random.randrange(40, 255, 1)

while 1:
	direction = random.uniform(0, 1)
	gain =  random.randrange(0, 4, 1)
	msleepduration = random.randrange(5, 50, 1)/1000.0
	
	if gain != 0:
		if direction < 0.5:
			new_intensity = intensity + gain
			if new_intensity > 255:
				new_intensity = 255
		else:
			new_intensity = intensity - gain
			if new_intensity < 0:
				new_intensity = 0
		printProgress(new_intensity, 255, prefix = '', suffix = '', barLength = 50, fill="-")
		pi.set_PWM_dutycycle(Red, new_intensity) # PWM 3/4 on 
		pi.set_PWM_dutycycle(Green, new_intensity) # PWM 3/4 on 
		pi.set_PWM_dutycycle(Blue, new_intensity) # PWM 3/4 on 
		pi.set_PWM_dutycycle(White, new_intensity) # PWM 3/4 on 
		intensity = new_intensity

	sleep(msleepduration)
	