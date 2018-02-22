import ConfigParser, json

tempIni = "/home/pi/TemperatureSensor/temperaturelogger.ini"
smsStatus = 0
Config = ConfigParser.ConfigParser()
Config.read(tempIni)
smsStatus = Config.get('SMSSettings','SMSEnabled')

if smsStatus == '1':
    Config.set('SMSSettings','SMSEnabled', '0')
    #print "Disabling SMS"
    with open(tempIni, 'wb') as configfile:
        Config.write(configfile)
    print "Pyhton Disabled the SMS Service"
    
else:
    Config.set('SMSSettings','SMSEnabled', '1')
    #print "Enabling SMS"
    with open(tempIni, 'wb') as configfile:
        Config.write(configfile)
    print "Pyhton Enabled the SMS Service"
