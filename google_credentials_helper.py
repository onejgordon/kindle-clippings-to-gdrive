# -*- coding: utf-8 -*-

import oauth2client
import webbrowser
import httplib2
import apiclient


class GoogleCredentialHelper():

    def __init__(self, service_name='sheets', version='v4'):
        self.service_name = service_name
        self.version = version

    def get_credentials(self):
        """Gets google api credentials, or generates new credentials
        if they don't exist or are invalid."""
        scope = 'https://www.googleapis.com/auth/spreadsheets'

        flow = oauth2client.client.flow_from_clientsecrets(
                'client_secret.json', scope,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob')

        storage = oauth2client.file.Storage('credentials.dat')
        credentials = storage.get()

        if not credentials or credentials.invalid:
            auth_uri = flow.step1_get_authorize_url()
            webbrowser.open(auth_uri)

            auth_code = raw_input('Enter the auth code: ')
            credentials = flow.step2_exchange(auth_code)

            storage.put(credentials)

        return credentials

    def get_service(self):
        credentials = self.get_credentials()
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = apiclient.discovery.build(self.service_name, self.version, http=http)
        return service
