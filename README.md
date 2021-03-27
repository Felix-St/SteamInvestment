# SteamInvestment
Python project used for hosting a Webserver in your local network displaying Market Values using Chart.js

## Prerequisites
This programm needs only a handful of smaller libraries that can be easily installed with pip. Some of them are installed by default so I will update the requirements soon but mainly just install all libraries that are listet at the top of 'Steam_Webpage.py' (most importantly flask, apscheduler and the urllib).

## Use
This application shouldn't be used as an full fledged web server but rather an application that might run on an raspberry pi in your local network so that you can check your investments from any device in your local network. The only change you need to do after manually inserting your investments (read the comments in Steam_Webpage.py) is to change the IP in 'app.run(debug = True, host= '127.0.0.1', port = 80, use_reloader=False)' to '0.0.0.0' so that the webpage can be contacted by simply calling the IP of the device (so dont try to open 0.0.0.0 but the IP of the device which executes this apllication, e.g. 192.168.178.64).

## Functionality


## External libraries
Next to the python libraries I also used Chart.js (https://github.com/chartjs) for the graphical representation of the price development.
