import os
import sendgrid
from sendgrid.helpers.mail import * # source of Email, Content, Mail, etc.
import urllib.parse
import urllib.request
import json #source weather api client



# AUTHENTICATE

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
MY_EMAIL_ADDRESS = os.environ.get('MY_EMAIL_ADDRESS')
my_email = Email(MY_EMAIL_ADDRESS)


sg = sendgrid.SendGridAPIClient(apikey = SENDGRID_API_KEY)


# COMPILE QUERY
# ... See Yahoo Weather API Docs!

baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='new york, ny')"
yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query_nj = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='beach haven, nj')"
yql_url_nj = baseurl + urllib.parse.urlencode({'q':yql_query_nj}) + "&format=json"

# ISSUE REQUEST

response = urllib.request.urlopen(yql_url).read()
response_nj = urllib.request.urlopen(yql_url_nj).read()

# PARSE RESPONSE

raw_response = json.loads(response)
results = raw_response["query"]["results"]["channel"]
weather = results["item"]

raw_response_nj = json.loads(response_nj)
results_nj = raw_response_nj["query"]["results"]["channel"]
weather_nj = results_nj["item"]

#print(weather["title"])
#print(weather["condition"]["temp"])
#print(weather["condition"]["text"])
#print(weather_nj["title"])
#print(weather_nj["condition"]["temp"])
#print(weather_nj["condition"]["text"])

#COMPILE REQUEST PARAMETERS

email_message = weather["title"] + "\n" + weather["condition"]["temp"] + "\n" + weather["condition"]["text"] + "\n" + weather_nj["title"] + "\n" + weather_nj["condition"]["temp"] + "\n" + weather_nj["condition"]["text"]

subject = "Here's today's weather forecast"

from_email = my_email
to_email = my_email
content = Content("text/plain", email_message)
mail = Mail(from_email, subject, to_email, content)

# ISSUE REQUEST

response = sg.client.mail.send.post(request_body=mail.get())

# PARSE RESPONSE

print(response.status_code)
print(response.body)
print(response.headers)
