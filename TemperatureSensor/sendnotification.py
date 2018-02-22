import pycurl, json
from StringIO import StringIO


appID = ""
appSecret = ""
pushEvent = "TemperatureAlert"
pushMessage = "Hello!"

# use StringIO to capture the response from our push API call
buffer = StringIO()

# use Curl to post to the Instapush API
c = pycurl.Curl()

# set Instapush API URL
c.setopt(c.URL, 'https://api.instapush.im/v1/post')

# setup custom headers for authentication variables and content type
c.setopt(c.HTTPHEADER, ['x-instapush-appid: ' + appID,
'x-instapush-appsecret: ' + appSecret,
'Content-Type: application/json'])

# create a dictionary structure for the JSON data to post to Instapush
json_fields = {}

# setup JSON values
json_fields['event']=pushEvent
json_fields['trackers'] = {}
json_fields['trackers']['message']=pushMessage

postfields = json.dumps(json_fields)

# make sure to send the JSON with post
c.setopt(c.POSTFIELDS, postfields)

# set this so we can capture the resposne in our buffer
c.setopt(c.WRITEFUNCTION, buffer.write)

# uncomment to see the post that is sent
c.setopt(c.VERBOSE, True)
c.perform()
