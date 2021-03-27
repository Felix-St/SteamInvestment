# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 11:59:36 2021

@author: Felix
"""

from flask import Flask, render_template, g, request, session,Markup
import urllib.request
import time
import json
import copy
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import csv

app = Flask(__name__)


#############################################################################
# Global Variables
#############################################################################
# Cost for the investment (has obviously to be manually set)

# Automatically fetched value with respective date
dateAll = []
valueInvestments = []

dataInvestments = []



###############################################################################
# The only things that needs manually changing is the bit below, because obv 
# it is not possible to grab your investments automatically. For each 
# Investment (that is for each distinct chart/graph) you need to declare
# a dictionary holding the items you have invested in. The dictionaries have
# the structure name:amount, the example below should make that quite clear.
# Also if you want to calculate your profit you need to enter the amount you
# have spent on the respective investment (dictionary) in the 'costInvestments' list.
# Moreover you have to add the additional dictonaries you create to the investmentList
# which is initialized below the dictionaries.
    
    

    
itemsInvestment1 ={'Sticker | Stone Scales (Foil)':1,
'Sticker | Ancient Beast (Foil)':1,
'Sticker | Battle Scarred (Holo)':1,
'Sticker | Coiled Strike (Holo)':1,
'Sticker | Broken Fang (Holo)':1,
'Sticker | Enemy Spotted (Holo)':1,
'Sticker | Battle Scarred':1,
'Sticker | Stalking Prey':1,
'Sticker | Enemy Spotted':1,
'Sticker | Broken Fang':1,
'Sticker | Coiled Strike':1,
'Sticker | Stone Scales':1,
'Sticker | Ancient Marauder':1,
'Sticker | Ancient Protector':1,
'Sticker | Ancient Beast':1,
'Sticker | Badge of Service':1
}

itemsInvestment2 ={'Sticker | Mastermind':1,
'Sticker | Web Stuck':1,
'Sticker | Terrorist-Tech':1,
'Sticker | Shattered Web':1,
'Sticker | Counter-Tech':1,
'Sticker | Gold Web':1,
'Sticker | Mastermind (Holo)':1,
'Sticker | Web Stuck (Holo)':1,
'Sticker | Gold Web (Foil)':1,
}

investmentList = [itemsInvestment1,itemsInvestment2]

# Resize list of lists which hold all the scraped values
for item in investmentList:
    dataInvestments.append([])
    
# If no costs are specified the default value is set to zero. It is recommended
# to the set the costs manually as shown below the default initialization.
costInvestments = [0] * len(dataInvestments)

#costInvestments = [38.50,38.50]

##############################################################################

def calculateValue(items_dict):
    # Generic function to calculate the total value of an investment structured
    # like the dictionaries above. This functin is called in the background task
    # (executing every hour) to update the prices. Hence this function can be easily
    # 'copy/pasted' and it retains full functionality so feel free to use it in you
    # own project.
    
    itemsInvestment = {}
    itemsInvestment.clear()
    valueInvestment = 0
    for i,item in enumerate(items_dict):
        # Scrape the needed information from the json object that is returned by
        # the request made by the url below (you can test it manually in your browser
        # to see what is actually returned)
        key = copy.deepcopy(item)
        item = item.replace(" ","%20")
        url ='https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name=' + item
        contents = urllib.request.urlopen(str(url))
        contentsJson = json.load(contents)
        
        # Suboptimal but having a 3.5 seconds timeout ensures that steam doesn't 
        # this server for requesting too often (20 requests per minute are allowed AFAIK)
        time.sleep(3.5)
        
        # You can choose between 'lowest_price' or 'median_price' (using 'volume' you can also
        # get the volume of the respective item on the steam market)
        itemsInvestment[key] = contentsJson['lowest_price']
        
    # This loop converts the scraped values to a different decimal representation
    # and multiplies it by the amount
    for i,item in enumerate(items_dict):
        temp = itemsInvestment.get(item)
        if temp == 0:
            continue
        temp = temp.replace(',','.')
        
        euro_dec = float(temp[:-1])
        valueInvestment += float(euro_dec*items_dict.get(item))
    return valueInvestment 
        

def helper():
    # This helper funtion calls the 'calculateValue' function for every
    # investment (dictionary) that was specified and added to the 'investmentList'
    print('Background Task called')
    global investmentList,dataInvestments,dateAll
    
    for i,investment in enumerate(investmentList):
        tempValueInvestment = 0
        tempValueInvestment = calculateValue(investment) 
        dataInvestments[i].append(tempValueInvestment)

    # Get the current time as x values. (Your timezone may differ)
    temp = datetime.now()
    temp = temp.strftime("%d/%m/%Y %H:%M:%S")
    dateAll.append(temp)

def save():
    # Once a day the values are saved to an csv File. When this server is restarted
    # it automatically searches for an csv file to load. 
    raise NotImplementedError('This function is not yet implemented')
    
def load_data():
    raise NotImplementedError('This function is not yet implemented')
    
# Call Backgroundtask at the start
helper()
#load_data()
  
##############################################################################
scheduler = BackgroundScheduler()
# Once an hour
scheduler.add_job(func=helper, trigger="interval", seconds=3600)#3600)
# Once a day
scheduler.add_job(func=save, trigger="interval", seconds=86400)
scheduler.start()    
##############################################################################

@app.route("/")
def main():
    # Main Method to return the Home Page
    global valueInvestments,dateAll,dataInvestments
    global costInvestment1
    return render_template("SteamMain.html",values = valueInvestments,dataInvestments=dataInvestments,dateVal=dateAll,costInvestments=costInvestments)   


if __name__ == "__main__":
    app.run(debug = True, host= '127.0.0.1', port = 80, use_reloader=False)


# Shutdown scheduler which calls the periodic update
atexit.register(lambda: scheduler.shutdown())
