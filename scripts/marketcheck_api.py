# -*- coding: utf-8 -*-
"""
@author: Daniel Navarrete

This script allows for the MarketCheck Inventory Search API to be queried.
Slight wrangling allows for data contained in nested lists to be retrieved,
data to be arrayed in dataframes, merged, and ultimately exported as CSV(s).
"""

import requests
import json
import pandas as pd

#####################
#  Build API Query  #
#####################

url = "http://api.marketcheck.com/v1/search?"

headers = {'Content-Type': 'application/json',
           'host': 'marketcheck-prod.apigee.net'}

payload = {'api_key':'YOUR_KEY_HERE',
           'radius':'100',
           'car_type':'used',
           'year':'2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005',
           'make':'toyota',
           'model':'prius',
           'start': '0',
           'rows': '50'
           }

api_response = requests.get(url = url, headers = headers, params = payload)

##############
#  Call API  #
##############

def get_request_info():
    if api_response.status_code == 200:
        return json.loads(api_response.content.decode('utf-8'))
    else:
        return "API did not connect."

get_request_info()

json_response = json.loads(api_response.content.decode('utf-8'))

# See the JSON response in 'prettified' context:
print(json.dumps(json_response, indent = 4, sort_keys = True))

#################################
#  Navigating the API Response  #
#################################

# View the dictionary key (or 'folder') structure:
for item in json_response:
    print('Key/Folder is: ' + item)

# Drill down into the 'listings' key/folder:
for item in json_response['listings']:
    print(item)

# See the 'listings' folder content in 'prettified' context:
print(json.dumps(json_response['listings'], indent = 4, sort_keys = True))

###########################
#  Data Injestion Set-Up  #
###########################

#### VIN Numbers
# Create a dictionary with all of the VIN numbers in our response.
# As VINs are unique identifiers, we will use this variable to merge
# different dataframes we create from nested structures.

vins = []
for item in json_response['listings']:
    print(item['vin']) # This isn't necessary but it's visual confirmation.
    vins.append({'vin':item['vin']})


#### "Build" Features
# The car's build features are nested within our query response.
# We create a dictionary to store this feature list.

build = []
for item in json_response['listings']:
    print(item['build']) # This isn't necessary but it's visual confirmation.
    build.append(item['build'])

#### "Dealer" Features
# The car's dealer information is nested within our query response.
# We create a dictionary to store this feature list.
    
dealer = []
for item in json_response['listings']:
    print(item['dealer']) # This isn't necessary but it's visual confirmation.
    dealer.append(item['dealer'])

#### "Financing Options"
# This is also nested within our results.  NOTE:  Could not flatten this nested data...

#financing = []
#for item in json_response['listings']:
#    print(item['financing_options']) # This isn't necessary but it's visual confirmation.
#    financing.append(item['financing_options'])
    
##################
#  Data Outputs  #
##################

# Create our dataframes using the different dictionaries / lists we created:

# Listings
df_listings = pd.DataFrame(json_response['listings'])
df_listings = df_listings.drop(['build', 'dealer', 'media', 'financing_options'], axis = 1)

# Build
df_build = pd.DataFrame(build)
df_build['vin'] = ''

# Dealer
df_dealer = pd.DataFrame(dealer)
df_dealer['vin'] = ''

# VIN
df_vin = pd.DataFrame(vins)

# Append VIN to the "build" and "dealer" lists.
df_build.loc[df_build['vin'] == '', 'vin'] = df_vin['vin']
df_dealer.loc[df_dealer['vin'] == '', 'vin'] = df_vin['vin']

# Merge the different dataframes:
MarketCheck = pd.merge(df_listings, df_build, on='vin', how='outer')
MarketCheck = pd.merge(MarketCheck, df_dealer, on='vin', how='outer')

# As there are two columns labeled "id", we will rename the 'id' variable in
# the 'Dealer' dataframe to "dealer_id".
MarketCheck = MarketCheck.rename(columns = {'id_y':'dealer_id'})

# Export dataframe to CSV:
#df_listings.to_csv('Listings.csv', index = False)
#df_build.to_csv('Build.csv', index = False)
#df_dealer.to_csv('Dealer.csv', index = False)
MarketCheck.to_csv('MarketCheck_API.csv', index = False)