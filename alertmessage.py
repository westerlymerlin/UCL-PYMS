"""
Alert Message Module
Author: Gary Twinn
"""
import smtplib
import json
import base64
from logmanager import logger


def alert(body):
    """
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
    """
    with open('alerts.json', 'r', encoding='utf-8') as json_file:
        alertsettings = json.load(json_file)
    for recipient in alertsettings['Recipients']:
        message = 'From: ' + alertsettings['O365Sender'] + '\nTo:%s\nSubject: PyMS Alert : %s\n\n%s\n%s\n' \
                  % (recipient, alertsettings['Subject'], alertsettings['Message'], body)
        mailserver = smtplib.SMTP(alertsettings['SMTPServer'], alertsettings['SMTPPort'])
        mailserver.ehlo()
        mailserver.starttls()
        o365_key = str(base64.b64decode(alertsettings['O365Key']), 'UTF-8').split(' ')
        mailserver.login(o365_key[0], o365_key[1])
        mailserver.sendmail(alertsettings['O365From'], recipient, message)
        mailserver.quit()
        logger.info('Alert sent to %s', recipient)
