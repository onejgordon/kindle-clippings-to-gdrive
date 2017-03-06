# Kindle Notes to GDrive

A Python script to load clippings/notes/highlights from a Kindle (connected via USB)
and save to a Google Sheet.

While https://kindle.amazon.com/your_highlights works well for purchased books, it doesn't include highlights/notes from PDFs and articles loaded onto the Kindle. Notes are saved as a .txt file on the device, but it's much more useful to collect them in a spreadsheet. This script makes it easy to automate this process.

## Requirements

Python 2.7

## Setup

### Install requirements

```
pip install -r requirements.txt
```

### Create a Google API project

You'll need Google API project to authenticate the calls to Google Sheets.

Go to https://console.developers.google.com to create your project.

Create an oauth2 credential, and download the client_secret.json file to the main directory.

### Create your Spreadsheet

Create a Google Sheet.
If you don't update the config, the sheet expects headers:

`Id`, `Type`, `Quote`, `Source`, `Location`, `Date`

### Update configuration

Copy config.template.py to config.py and update constants:

* GOOGLE_SHEET_KEY - Key of the Google Sheet you created

## Usage

Each time you want to save notes from your kindle, plug it in and run:

```
python push_clippings.py
```