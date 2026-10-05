import os

from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


# LOAD ENVIRONMENT VARIABLES
load_dotenv()


def send_alert_sms(alert_message=None):
    """
    Send an industrial alert SMS.

    Current Twilio trial accounts only allow Twilio predefined SMS
    templates. After upgrading the account, set:

        TWILIO_CUSTOM_SMS=true

    in .env to send the detailed machine-specific message created
    by the dashboard.

    Returns:
        (True, message_sid) on success
        (False, error_message) on failure
    """

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
    alert_phone = os.getenv("ALERT_PHONE_NUMBER")
    custom_sms = (
        os.getenv("TWILIO_CUSTOM_SMS", "false").strip().lower()
        == "true"
    )

    if not account_sid:
        return False, "TWILIO_ACCOUNT_SID is missing."

    if not auth_token:
        return False, "TWILIO_AUTH_TOKEN is missing."

    if not twilio_phone:
        return False, "TWILIO_PHONE_NUMBER is missing."

    if not alert_phone:
        return False, "ALERT_PHONE_NUMBER is missing."

    try:
        client = Client(
            account_sid,
            auth_token
        )

        if custom_sms and alert_message:
            message = client.messages.create(
                body=alert_message,
                from_=twilio_phone,
                to=alert_phone
            )
        else:
            # Twilio trial predefined template.
            message = client.messages.create(
                body="sms_internal_alerts",
                from_=twilio_phone,
                to=alert_phone
            )

        return True, message.sid

    except TwilioRestException as error:
        return False, f"Twilio Error {error.code}: {error.msg}"

    except Exception as error:
        return False, f"Unexpected Error: {error}"
