import pandas as pd
import requests
import json
import csv
from datetime import date
# from requests.api import head
from dash import Dash


#%% Data Retrieval from API -----------------------------------------------------------------------
# API request to retrieve data
response = requests.get("https://www.bankofcanada.ca/valet")    # returns a response object (i.e., base URL)
print(response.status_code)

today = str(date.today())

url = "https://www.bankofcanada.ca/valet/observations/"
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
pars = {"start_date": '2000-01-01', "end_date": today,}    # dates formatted as YYYY-MM-DD (inclusive)


series_list = [
    'V39079' # Target for the overnight rate
]

full_url = url + series_list[0]

response = requests.request("GET", full_url, headers=headers, data={}, params = pars); response.status_code
myjson = response.json(); print(myjson)


df = []
for x in myjson['observations']:
    listing = [x['d'], x[series_list[0]]['v']]
    df.append(listing)

print(df)

df_tbills = pd.DataFrame(data=df, columns=['Date', 'T_BILLS'])



#%% API Retrieval ---------------------------------------------------------------------------------
# API request to retrieve data
response = requests.get("https://www.bankofcanada.ca/valet")    # returns a response object (i.e., base URL)
print(response.status_code)

today = str(date.today())

#>> API DATA RETRIEVAL
url = "https://www.bankofcanada.ca/valet/observations/V36653"
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
pars = {"start_date": '2000-01-01', "end_date": today,}    # dates formatted as YYYY-MM-DD (inclusive)


url = "https://www.bankofcanada.ca/valet/observations/"

series_list = [
    'V39079'
]
full_string = ""
for item in series_list:
   full_string += item + "%2C"

full_url = url + full_string[:-3]

response = requests.request("GET", full_url, headers=headers, data={}, params = pars); response.status_code
# response = requests.request("GET", url, headers=headers, data={}, params = pars); response.status_code
myjson = response.json(); print(myjson)


df = []
for x in myjson['observations']:
    listing = [x['d'], x['V36653']['v']]
    df.append(listing)

print(df)

df_tbills = pd.DataFrame(data=df, columns=['Date', 'T_BILLS'])








# #>> Write 'df' to a .csv file
# csvheader = ['Date', 'T_BILLS']

# with open('tbills.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(csvheader)
#     writer.writerows(df)

# #>> API Group Data
# group_link = "groups/B1_MONTHLY/csv"      # enter group name here "/groups/groupName/csv"

# response = requests.get("https://www.bankofcanada.ca/valet/" + group_link); response.status_code
# print(response.json())

# # response.content

# # https://www.bankofcanada.ca/valet/groups/B1_MONTHLY/csv




#%% Dashboard creation ----------------------------------------------------------------------------

def load_transaction_data(path: str) -> pd.DataFrame:
    # Load the data from CSV file
    data = pd.read_csv(
        path, 
        dtype={"amount":float, "category":str}, 
        parse_dates=["date"]
    )
    return data

# len(df)


#* Notes ------------------------------------------------------------------------------------------
# len() of dataframe is also the num. of rows
# if not len(df):
# Is the same as
# if df.shape[0] == 0:

