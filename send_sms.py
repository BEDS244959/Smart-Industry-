import os

from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# GET CREDENTIALS
# ==================================================

account_sid = os.getenv(
    "TWILIO_ACCOUNT_SID"
)

auth_token = os.getenv(
    "TWILIO_AUTH_TOKEN"
)

twilio_phone = os.getenv(
    "TWILIO_PHONE_NUMBER"
)

alert_phone = os.getenv(
    "ALERT_PHONE_NUMBER"
)


# ==================================================
# CHECK CREDENTIALS
# ==================================================

if not account_sid:

    print(
        "ERROR: TWILIO_ACCOUNT_SID is missing."
    )

    exit()


if not auth_token:

    print(
        "ERROR: TWILIO_AUTH_TOKEN is missing."
    )

    exit()


if not twilio_phone:

    print(
        "ERROR: TWILIO_PHONE_NUMBER is missing."
    )

    exit()


if not alert_phone:

    print(
        "ERROR: ALERT_PHONE_NUMBER is missing."
    )

    exit()


# ==================================================
# CREATE TWILIO CLIENT
# ==================================================

client = Client(
    account_sid,
    auth_token
)


# ==================================================
# SEND TRIAL SMS
# ==================================================

try:

    message = client.messages.create(

        body="sms_internal_alerts",

        from_=twilio_phone,

        to=alert_phone
    )


    print()
    print(
        "=============================================="
    )

    print(
        "SMART INDUSTRY AI - SMS TEST"
    )

    print(
        "=============================================="
    )

    print()

    print(
        "SMS request accepted by Twilio!"
    )

    print()

    print(
        "Message SID:"
    )

    print(
        message.sid
    )

    print()

    print(
        "Message status:"
    )

    print(
        message.status
    )

    print()

    print(
        "From:",
        message.from_
    )

    print(
        "To:",
        message.to
    )

    print()

    print(
        "=============================================="
    )


except TwilioRestException as error:

    print()
    print(
        "=============================================="
    )

    print(
        "TWILIO SMS ERROR"
    )

    print(
        "=============================================="
    )

    print()

    print(
        "Error code:",
        error.code
    )

    print()

    print(
        "Error message:",
        error.msg
    )

    print()

    print(
        "Please check your Twilio trial restrictions, "
        "verified recipient and SMS configuration."
    )