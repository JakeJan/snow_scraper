# snow_scraper
Gather year over year snowfall info from the internet for Epic pass resorts

## How to run
Run the script snow_scraper.py to produce the reports into your export path configured in the script.

## Add new resorts
New resorts can be added by adding entries into the region_resort_dict. The key is the region and the value is an array of resort names. The exact region and resort name should be found on onthesnow.com.

## Results
The data is produced into a comma delimited file where snowfall is reported in inches. Example:
keystone,Jan 01,Jan 02,Jan 03,Jan 04
2009,0,1,0,4
2010,1,1,5,1
2011,1,1,3,1
2012,1,0,0,0
2013,2,1,1,0
2014,4,1,0,1
2015,0,1,2,4
2016,0,0,0,0
2017,0,0,1,3
