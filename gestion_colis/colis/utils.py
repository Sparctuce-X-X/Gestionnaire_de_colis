from decouple import config
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_sms(to, body):
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    from_number = config('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to
        )
        return message.sid
    except TwilioRestException as e:
        print(f"Erreur lors de l'envoi du SMS: {e}")
        return None
