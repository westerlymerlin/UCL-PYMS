import smtplib
import json
import base64


def alert(body):
    with open('alerts.json') as json_file:
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
        print('Alert sent to %s' % recipient)



