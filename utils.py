from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, tools, client


SCOPES = 'https://www.googleapis.com/auth/drive.file'


def authorize_google_drive():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service
