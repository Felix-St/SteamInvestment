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




dateAll = []

valueInvestments = []

#############################################################################
# Global Variables
#############################################################################

# Cost for the investment (has obviously to be manually set)
costInvestment1 = 38.50
costInvestment2 = 38.50


# Current value of the investment (automatically fetched)
# Create one dictionary with the item name as key and the amount as value, also
# create one variable to hold its total value (valueInvestment3,valueInvestment4,...)
valueInvestment1 = 0
valueInvestment2 = 0

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
dataInvestments = []

for item in investmentList:
    dataInvestments.append([])

def calculateValue(items_dict):
    itemsInvestment = {}
    itemsInvestment.clear()
    valueInvestment = 0
    for i,item in enumerate(items_dict):
        key = copy.deepcopy(item)
        item = item.replace(" ","%20")
        url ='https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name=' + item
        contents = urllib.request.urlopen(str(url))
        contentsJson = json.load(contents)
        
        time.sleep(3.5)
        # You can choose between 'lowest_price' or 'median_price' (using 'volume' you can also
        # get the volume of the respective item on the steam market)
        itemsInvestment[key] = contentsJson['lowest_price']
        
        
    for i,item in enumerate(items_dict):
        temp = itemsInvestment.get(item)
        if temp == 0:
            continue
        temp = temp.replace(',','.')
        
        euro_dec = float(temp[:-1])
        valueInvestment += float(euro_dec*items_dict.get(item))
    return valueInvestment 
        

def helper():
    print('Background Task called')
    global investmentList,dataInvestments,dateAll
    
    for i,investment in enumerate(investmentList):
        tempValueInvestment = 0
        tempValueInvestment = calculateValue(investment) 
        print('Calculated Value',tempValueInvestment)
        dataInvestments[i].append(tempValueInvestment)
        print(dataInvestments)
  
    temp = datetime.now()
    temp = temp.strftime("%d/%m/%Y %H:%M:%S")
    dateAll.append(temp)

def save():
    # Once a day the values are saved to an csv File. When this server is restarted
    # it automatically searches for an csv file to load.
    print('test')
    
def load_data():
    pass
    
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
    return render_template("SteamMain.html",values = valueInvestments,dataInvestments=dataInvestments,dateVal=dateAll)   


if __name__ == "__main__":
    app.run(debug = True, host= '127.0.0.1', port = 80, use_reloader=False)


# Shutdown scheduler which calls the periodic update
atexit.register(lambda: scheduler.shutdown())
