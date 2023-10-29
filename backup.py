"""
Backup files to sharepoint
Author: Gary Twinn
"""

import json
import base64
import threading
import sys
from pathlib import Path
import requests
from msal import ConfidentialClientApplication
from logmanager import logger


def msgraph_auth(tenantid, appid, thumbprint, scope, cert_file_name):
    """Get an azure token from MSGraph"""
    authority = 'https://login.microsoftonline.com/' + tenantid
    scope = [scope + '/.default']
    thumbprint_and_cert = {"thumbprint": thumbprint, "private_key": open(cert_file_name, encoding='utf-8').read()}
    app = ConfidentialClientApplication(appid, authority=authority, client_credential = thumbprint_and_cert)
    try:
        access_token = app.acquire_token_silent(scope, account=None)
        if not access_token:
            try:
                access_token = app.acquire_token_for_client(scopes=scope)
                if access_token['access_token']:
                    logger.debug('backup.py: New access token retreived')
                else:
                    logger.error('backup:py Error aquiring authorization token. Check your tenantID, clientID and clientSecret.')
            except:
                pass
        else:
            logger.debug('backup.py Token retreived from MSAL Cache')
        return access_token
    except Exception as err:
        logger.error('Backup.py: %s', err)


def delayedbackupfile(file_name):
    """Backup a file to sharepoint (runs in ints own thread)"""
    p = Path(file_name)
    filedec = p.parts[len(p.parts) - 1]
    nested_folder = p.parts[len(p.parts) - 2]

    certfile = 'backup.pem'
    with open('backup.json', 'r', encoding='utf-8') as json_file:
        backupsettings = json.load(json_file)
    json_file.close()
    o365_key = str(base64.b64decode(backupsettings['O365Key']), 'UTF-8').split(' ')
    access_token = msgraph_auth(o365_key[0], o365_key[1], o365_key[2], o365_key[3], certfile)
    headers = {
        'Authorization': 'Bearer ' + access_token['access_token'],
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json;odata=verbose',
        'user-agent': 'python_agent/backup'
    }
    session = requests.session()
    session.headers.update(headers)
    base_url = o365_key[4]
    sys_folder = backupsettings['Identifier']
    fileurl=(base_url + "web/GetFolderByServerRelativeUrl('Documents/" + sys_folder + '/' + nested_folder
             + "')/Files/add(url='" + filedec + "',overwrite=true)")
    folderurl = (base_url + "web/GetFolderByServerRelativeUrl('Documents/" + sys_folder + "')/folders/add(url='"
                 + nested_folder + "')")
    response1 = session.post(url=folderurl)
    logger.debug("backup: %i: %s", response1.status_code, response1.text)
    # Upload file
    with open(file_name, 'rb') as file_input:
        try:
            response = session.post(url=fileurl, data=file_input)
            if response.status_code == 200:
                logger.debug("backup.py: %i: %s uploaded", response.status_code, file_name)
            else:
                logger.warning("backup.py: %i: %s", response.status_code, response.text)
        except Exception as err:
            logger.error("backup.py: Something went wrong uploading to sharepoint: %s", str(err))
    file_input.close()


def backupfile(file_name):
    """run backup in its own thread"""
    threading.Timer(1, lambda: delayedbackupfile(file_name)).start()

if __name__ == '__main__':
    print('Starting backup')
    backupfile(sys.argv[1])
