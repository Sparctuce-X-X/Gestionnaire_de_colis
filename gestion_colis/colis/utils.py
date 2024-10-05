from twilio.rest import Client

# Remplacez les valeurs par vos identifiants Twilio
TWILIO_ACCOUNT_SID = 'ACdf1b4f6b29c3c60a91707243eba75ea9'  # Votre SID
TWILIO_AUTH_TOKEN = '1cbf420c864513c1afab84303f025095'  # Votre token
TWILIO_PHONE_NUMBER = '+15402742024'  # Votre numéro Twilio

def send_sms(to, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,  # Utiliser la variable ici
        to=to
    )
    return message.sid
