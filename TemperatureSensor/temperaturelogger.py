#!/usr/bin/python
import time, ConfigParser, os, pycurl, json, MySQLdb, sys, requests
from StringIO import StringIO
#from twilio.rest import TwilioRestClient

print "Initiating the Temperature Logger"

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

text_delay = 300
#text_delay = 60

global_counter = text_delay	
looptimeSeconds = 30
#looptimeSeconds = 10
sampleCount = 10
#sampleCount = 2
highTempAlert = 26
lowTempAlert = 23

def SendInstaPush(message):
    data_send = {"type": "note", "title": "Temperature Alert", "body": message}
    ACCESS_TOKEN = ""
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send), headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    
def sendAlert(message):
	global global_counter

	if global_counter >= text_delay:
		global_counter = 0

	print "Counter at: " + str(global_counter)

	if (global_counter == 0):
		Config = ConfigParser.ConfigParser()
		Config.read("/home/pi/TemperatureSensor/temperaturelogger.ini")
		smsStatus = Config.get('SMSSettings','SMSEnabled')
		if (smsStatus == "1"):
			print " Sending Notification"
			SendInstaPush(message)
	global_counter = global_counter + looptimeSeconds
	return

def LogTemp ( tankTemp, roomTemp, bedTankTemp, tableName ):
    database = OpenDatabase("temperature_readings")
    
    #print "Logging Temperature: ",str(tank)
    cursor = database.cursor()
    cursor.execute("INSERT INTO " + tableName + " VALUES (NULL, NULL, " + str(tankTemp) + ", " + str(roomTemp) + ", " + str(bedTankTemp) + ")")
    ##cursor.execute("SELECT * FROM " + tableName)
    database.commit()
    database.close()
    return

def OpenDatabase(databaseName):
    print "Opening the database"
    db = MySQLdb.connect(host="localhost", user='mysql-all', passwd='password', db=databaseName )
    return db

def ReadRawTemp(sensorName):
    temperatureFile = open("/sys/bus/w1/devices/" + sensorName + "/w1_slave")
    #temperatureFile = open("/home/pi/" + sensorName + "/w1_slave")
    sensorList = temperatureFile.readlines()
    temperatureFile.close()
    return sensorList

def GetTemp(sensorName):
    temp_float = float(0)
    sensorList = ReadRawTemp(sensorName)
    while sensorList[0].strip()[-3:] !='YES':
        print "Waiting for a good result"
        time.sleep(0.5)
        sensorList= ReadRawTemp(sensorName)
    equalsPos = sensorList[1].find('t=')
    if equalsPos != -1:
        temperatureData = sensorList[1][equalsPos+2:]
        temp_float = float(temperatureData) / 1000.0
    else:
		# Not got a good temp so try again!
        GetTemp(sensorName)
    ###############  print " Current Temperature " + str(temp_float)
    return temp_float

def RunTempLog(sensorNames, totalSensors):
    #get 10 temps, average them and send them to the database
    count = 0
    sensorCount = 0
    totalTemp = [float(0)] * totalSensors
    averageTemp = [float(0)] * totalSensors
    averageTemp_str = [""] * totalSensors
    
    while count < sampleCount:
        sensorCount = 0
        while sensorCount < totalSensors:
            totalTemp[sensorCount] = totalTemp[sensorCount] + GetTemp(sensorNames[sensorCount])
            sensorCount += 1
        time.sleep(2)
        count = count + 1

    sensorCount = 0
    while sensorCount < totalSensors:
        averageTemp[sensorCount] = totalTemp[sensorCount] / sampleCount
        averageTemp_str[sensorCount] = '%.1f' % averageTemp[sensorCount]
        sensorCount += 1
        
    ##Get the Bedroom Tank Temperature
	bedroomTankTemp = "0"
	file = None
    
    while (bedroomTankTemp == "0") or (not bedroomTankTemp):
        try:
            file = open('/home/pi/TemperatureSensor/bedroomTank.txt', 'r')
            bedroomTankTemp = file.readline()
                # do stuff with f

        finally:
            if file is not None:
                file.close()
        time.sleep(1)
    
    print "Logging Average Tank Temperature as  " + averageTemp_str[0]
    print "Logging Average Bedroom Tank Temp as " + bedroomTankTemp
    print "Logging Average Room Temperature as  " + averageTemp_str[1]
    
    LogTemp(averageTemp_str[0], averageTemp_str[1], bedroomTankTemp, "temps")
    #LogTemp(averageTemp_str[0], averageTemp_str[1], "25", "temps")

    if averageTemp[0] > highTempAlert:
        sendAlert("Tank Temperature at " + averageTemp_str[0])
    if averageTemp[0] < lowTempAlert:
        sendAlert("Tank Temperature at " + averageTemp_str[0] + " have you unplugged the heater?")
    if float(bedroomTankTemp) > highTempAlert:
        sendAlert("Bedroom Tank Temperature at " + bedroomTankTemp)
    if float(bedroomTankTemp) < lowTempAlert:
        sendAlert("Bedroom Tank Temperature at " + bedroomTankTemp + " have you unplugged the heater?")
        
    
while 1:
    startTime = time.time()
    #RunTempLog("sensorName", "tank")

    sensorNames = ["28-041621ea78ff", "28-0116005dd6ff"]
    dbTableNames = ["tank", "room"]
    
    RunTempLog(sensorNames, 2)
    endTime = time.time()
    if (looptimeSeconds - (endTime - startTime)) > 0:
        print "Sleep Required pausing for " + str(looptimeSeconds - (endTime - startTime))
        time.sleep(looptimeSeconds - (endTime - startTime))
    
    
#tableName = "tank"
#LogTemp( 25.2, tableName )
