#this code is used for the integration between GG Sheet and Lu.ma 

#for a list of all participants of a particular event on GG sheet, this code 
#will find new/unrecorded registration on lu.ma and update it on GG Sheet

#first, find all records in the google sheet


#connect to the google drive sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
#download credentials from google console, put it in the same folder as the python file
credentials = ServiceAccountCredentials.from_json_keyfile_name('FILE_NAME.json', scope)
client = gspread.authorize(credentials)

spreadsheet_list = client.openall()

#Open the google sheet by its name
sheet_name = 'THE_GOOGLE_SHEET_NAME'
sheet = client.open(sheet_name).worksheet('THE_WORKSHEET_NAME')

# Get all the data from the sheet as a list of lists
all_data = sheet.get_all_values()[2:] #rows that have data

data = list(zip(*all_data))

# data[1] contain all the emails of participants


#second: connect to the particular luma event 
import requests
import pandas as pd

# Define the endpoint URL for the lu.ma API
event_api_key = 'EVENT_API_KEY' #from manage event on lu.ma
url = f'https://api.lu.ma/public/v1/event/get-guests?event_api_id={event_api_key}'

# Set up headers and parameters for the API request
headers = {
    "x-luma-api-key": "LUMA_API_KEY", #from personal/settings
    "accept": "application/json"
}

# Send the API request and retrieve the response as a JSON object
response = requests.get(url, headers=headers)
entries = response.json()['entries']

#third: search for unrecorded entry
for entry in entries: #retrieve important information
    guest = entry['guest']
    user_name = guest['user_name']
    user_email = guest['user_email']
    #discount code is the ninth question asked, from question number 1
    code = guest['registration_answers'][8]['answer']
    if user_email not in data[1]:
        new_row = [user_name,user_email,'',code,'']
        sheet.append_row(new_row)
