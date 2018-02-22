import json, ConfigParser

smsStatus = 0
Config = ConfigParser.ConfigParser()
Config.read("/home/pi/TemperatureSensor/temperaturelogger.ini")
smsStatus = Config.get('SMSSettings','SMSEnabled')

print json.dumps(smsStatus)
