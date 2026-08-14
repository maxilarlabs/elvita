
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID=os.environ.get("TWILIO_SID")
TWILIO_AUTH=os.environ.get("TWILIO_AUTH")

client = Client(TWILIO_SID, TWILIO_AUTH)

abuela="+51988482104"

call = client.calls.create(
    #from_="+18168282132",
    from_="+17402763528",
    to="+51960400734",
    #to="+51927144823",
    #to = "+51992020414",
    url="https://29a1-2800-200-ea80-1b2-49bc-e6c0-1809-8403.ngrok-free.app/incoming-call",
)

print(call.sid)