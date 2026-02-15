"""
Provides functionality to send emails using the Microsoft Graph API.

This module defines a function that sends an email through the Microsoft Graph API by authenticating
via Microsoft Authentication Library (MSAL). It uses OAuth2-based client authentication and constructs
an email payload dynamically based on input data. The email can include sender, recipient, subject, and
message body details. Logs and errors are appropriately recorded.

"""

import msal
import requests
from logmanager import logger
from app_control import settings, SECRETS


def alert(body):
    """
    Sends an email using Microsoft Graph API based on the provided email payload.

    This function utilises the MSAL library to authenticate using client credentials
    and obtain an OAuth2 token, which is used to send the email through the API.
    Email details such as the subject, body, sender, and recipient are customised
    based on the input data.
    """
    if len(settings['email_recipients']) == 0:
        return

    client_id = SECRETS['email_client_id']
    tenant_id = SECRETS['email_tenant_id']
    client_secret = SECRETS['email_client_secret']
    message_body ='PyMS - Alert has activated\n\n%s ' % body
    subject = 'PyMS Alert'

    recipients = []
    for recipient in settings['email_recipients'].split(';'):
        recipients.append({'emailAddress': {'address': recipient.strip()}})

    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": message_body
            },
            "toRecipients": recipients
        },
        "saveToSentItems": "false"
    }

    # Initialize MSAL Confidential Client
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret
    )

    # Acquire token for the Service Principal
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        logger.error("Error acquiring token: %s", result.get('error_description'))
        return False
    access_token = result['access_token']

    # Send the Request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f"https://graph.microsoft.com/v1.0/users/{SECRETS['email_account']}/sendMail",
                             headers=headers, json=email_data, timeout=10)

    if response.status_code == 202:
        logger.info("Alert email sent successfully!")
        return True

    logger.error("Failed to send alert email: %s", response.status_code)
    print(response.json())
    return False
