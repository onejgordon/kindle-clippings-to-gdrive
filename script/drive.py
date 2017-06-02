# noinspection PyPackageRequirements
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def init():
    # use creds to create a client to interact with the Google Drive API
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    try:
        sheet = client.open('A New Spreadsheet2')
        print "Found sheet opening, ID= " + sheet.id
    except:
        sheet = client.create("A New Spreadsheet2")
        sheet.share('Calebrud1@gmail.com', perm_type='user', role='writer')
        print "Exception, creating, ID= " + sheet.id

    worksheet = sheet.sheet1
    return worksheet

if __name__ == '__main__':
    worksheet = init()
