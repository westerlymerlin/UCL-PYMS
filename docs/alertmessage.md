# None

<a id="alertmessage"></a>

# alertmessage

Alert Message Module
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

