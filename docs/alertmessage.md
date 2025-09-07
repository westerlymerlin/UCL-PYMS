# None

<a id="alertmessage"></a>

# alertmessage

Alert Message Module

This module provides functionality to send alert notifications via email using
SMTP and Office 365 authentication. It reads configuration from 'alerts.json'
and supports sending customized alert messages to multiple recipients.

Features:
- Secure authentication using base64 encoded Office 365 credentials
- Configurable SMTP settings, subjects, and message templates
- Logging of alert delivery status
- Support for multiple recipients

Usage:
    from alertmessage import alert

    # Send a custom alert message
    alert("Critical error in data processing module")

Configuration:
    Requires 'alerts.json' file with the following structure:
    {
        "SMTPServer": "smtp.office365.com",
        "SMTPPort": 587,
        "O365Sender": "alerts@example.com",
        "O365From": "alerts@example.com",
        "O365Key": "<base64-encoded-username-and-password>",
        "Subject": "System Alert",
        "Message": "The following alert was triggered:",
        "Recipients": ["admin@example.com", "manager@example.com"]
    }

Author: Gary Twinn

<a id="alertmessage.smtplib"></a>

## smtplib

<a id="alertmessage.json"></a>

## json

<a id="alertmessage.base64"></a>

## base64

<a id="alertmessage.logger"></a>

## logger

<a id="alertmessage.alert"></a>

#### alert

```python
def alert(body)
```

Sends an alert through email by loading configuration information from a JSON file,
formatting the message content, and sending the email to specified recipients.

Parameters
----------
body : str
    The custom message content to be included in the body of the alert email.

Raises
------
FileNotFoundError
    If the 'alerts.json' configuration file does not exist.
JSONDecodeError
    If there is an error parsing the 'alerts.json' file.
SMTPException
    If an error occurs while connecting to or interacting with the SMTP server.

