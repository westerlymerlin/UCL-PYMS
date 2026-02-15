# None

<a id="alertmessage"></a>

# alertmessage

Provides functionality to send emails using the Microsoft Graph API.

This module defines a function that sends an email through the Microsoft Graph API by authenticating
via Microsoft Authentication Library (MSAL). It uses OAuth2-based client authentication and constructs
an email payload dynamically based on input data. The email can include sender, recipient, subject, and
message body details. Logs and errors are appropriately recorded.

<a id="alertmessage.msal"></a>

## msal

<a id="alertmessage.requests"></a>

## requests

<a id="alertmessage.logger"></a>

## logger

<a id="alertmessage.settings"></a>

## settings

<a id="alertmessage.SECRETS"></a>

## SECRETS

<a id="alertmessage.alert"></a>

#### alert

```python
def alert(body)
```

Sends an email using Microsoft Graph API based on the provided email payload.

This function utilises the MSAL library to authenticate using client credentials
and obtain an OAuth2 token, which is used to send the email through the API.
Email details such as the subject, body, sender, and recipient are customised
based on the input data.

