## Synopsis

At the top of the file there should be a short introduction and/ or overview that explains **what** the project is. This description should match descriptions added for package managers (Gemspec, package.json, etc.)

## Code Example

Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## Motivation

Exercise:  Create a Web App that will display sensor data for the previous 30 minutes.  The sensor data includes data for 5 different sensors.Included is the message spec of the payloads returned from the Rest API so you can parse the message properly.  We are looking for Uplink Message 2, Sensor data.  

Data is available via REST GET.  The api to fetch data

https://clientedge-conductor.link-labs.com/clientEdge/data/uplinkPayload/applicationToken/b2f41103d2ba369afb75/events/<beforeTime>/<afterTime>?maxResults=<maxResultCount>

example api calls:
https://clientedge-conductor.link-labs.com/clientEdge/data/uplinkPayload/applicationToken/b2f41103d2ba369afb75/events/2016-10-20T15:51:26.213/2016-10-15T15:50:26.213?maxResults=500


## Installation

Prerequisites: 
Python must be installed 2.7 or greater. 

Step 1) Navigate to the directory you wish to clone this app and run:
	git init
	git clone https://github.com/aberkowgg/sensor_data.git

Step 2) Install pythons virtual env. Cd to fsensor_data/myproject and run:
	sudo pip install virtualenv

Step 3) Init pythons virtual env by running:
	virtualenv venv

Step 4) Active virtual env:
	Mac OSX/ Linux:
		. venv/bin/activate
	Windows:
		venv\scripts\activate

Step 5) Install python requirements. Make sure you are in myproject/myproject and run: 
	pip install -r requirements.txt

step 6) Run application: 
	python myproject.py

step 7: Go to http://0.0.0.0:5000/ on your browser and enjoy!


## Contributors

Andrew Berkow

