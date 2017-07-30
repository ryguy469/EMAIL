import os
import sendgrid
from sendgrid.helpers.mail import * # source of Email, Content, Mail, etc.

# AUTHENTICATE

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
MY_EMAIL_ADDRESS = os.environ.get('MY_EMAIL_ADDRESS')
my_email = Email(MY_EMAIL_ADDRESS)


sg = sendgrid.SendGridAPIClient(apikey = SENDGRID_API_KEY)

# COMPILE REQUEST PARAMETERS

subject = "Hello World from the SendGrid Python Library!"

from_email = my_email
to_email = my_email
content = Content("text/plain", "Hello, Email!")
mail = Mail(from_email, subject, to_email, content)

# ISSUE REQUEST

response = sg.client.mail.send.post(request_body=mail.get())

# PARSE RESPONSE

print(response.status_code)
print(response.body)
print(response.headers)
