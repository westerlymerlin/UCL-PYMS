import json
import base64
import requests
from pathlib import Path
from msal import ConfidentialClientApplication
import threading


def msgraph_auth(tenantid, appid, thumbprint, scope, cert_file_name):
    authority = 'https://login.microsoftonline.com/' + tenantid
    scope = [scope + '/.default']
    clientSecret = {"thumbprint": thumbprint, "private_key": open(cert_file_name).read()}
    app = ConfidentialClientApplication(appid, authority=authority, client_credential = clientSecret)
    try:
        accessToken = app.acquire_token_silent(scope, account=None)
        if not accessToken:
            try:
                accessToken = app.acquire_token_for_client(scopes=scope)
                if accessToken['access_token']:
                    print('backup.py: New access token retreived')
                else:
                    print('backup:py Error aquiring authorization token. Check your tenantID, clientID and clientSecret.')
            except:
                pass
        else:
            print('backup.py Token retreived from MSAL Cache')
        return accessToken
    except Exception as err:
        print('Backup.py: %s' % err)


def delayedbackupfile(file_name):
    p = Path(file_name)
    filedec = p.parts[len(p.parts) - 1]
    nested_folder = p.parts[len(p.parts) - 2]

    certfile = 'backup.pem'
    with open('backup.json') as json_file:
        backupsettings = json.load(json_file)
    json_file.close()
    o365_key = str(base64.b64decode(backupsettings['O365Key']), 'UTF-8').split(' ')
    accessToken = msgraph_auth(o365_key[0], o365_key[1], o365_key[2], o365_key[3], certfile)
    headers = {
        'Authorization': 'Bearer ' + accessToken['access_token'],
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json;odata=verbose',
        'user-agent': 'python_agent/backup'
    }

    session = requests.session()
    session.headers.update(headers)

    base_url = o365_key[4]
    sys_folder = backupsettings['Identifier']
    fileurl=base_url + "web/GetFolderByServerRelativeUrl('Documents/" + sys_folder + '/' + nested_folder + "')/Files/add(url='" + filedec + "',overwrite=true)"
    folderurl = base_url + "web/GetFolderByServerRelativeUrl('Documents/" + sys_folder + "')/folders/add(url='" + nested_folder + "')"
    response1 = session.post(url=folderurl)
    # print("%i: %s" % (response1.status_code, response1.text))
    # Upload file
    with open(file_name, 'rb') as file_input:
        try:
            response = session.post(url=fileurl, data=file_input)
            if response.status_code == 200:
                print("backup.py: %i: %s uploaded" % (response.status_code, file_name))
            else:
                print("backup.py: %i: %s" % (response.status_code, response.text))
        except Exception as err:
            print("backup.py: Something went wrong uploading to sharepoint: " + str(err))
    file_input.close()


def backupfile(file_name):
    threading.Timer(1, lambda: delayedbackupfile(file_name)).start()
