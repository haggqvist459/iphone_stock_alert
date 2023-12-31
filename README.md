
# Stock level monitor for Apple devices 

## [Updated version of a masterpiece by Insanoid](https://github.com/insanoid/Apple-Store-Reserve-Monitor#apple-store-reserve-monitor)

**Updated the script for the iPhone 15 lineup** 

**Works for any Apple device, as long as you have the model number**

**Turn up the volume on your computer and it wakes you up in the morning when your favourite phone becomes available!**

### Basic info:
 - Used Python 3.12.0 while updating the script
 - run pip3 install -r requirements.txt
 - If you run into issues with requests, reinstall requests, urllib3 & six. 
 - iphone_checker.py runs the script once while stock_monitor.py runs every 10 seconds. 
 - Change MONITOR_INTERVAL in stock_monitor.py to change the checking interval

### Setup - variables.json
 1. "device_family" - the entire line up of a certain year (e.g. "iphone15" or "iphone15pro")
 2. "model_list" - find your model, (e.g. "MU793ZP/A" for the global version of iPhone 15 Pro Max, 256GB, Natural Titanium)
 3. "store_list" - Find the store(s) closest to you (e.g. "R238")
 4. "country" - ISO code required for all countries except US (e.g. "au")
 5. "post_code" - search for devices in stores near your post code (e.g. "2000")
 6. "carriers" - For US users only, see example in test_variables.md 

 **variables.json needs a value in either device family or model list**


_[Link to all the apple stores with IDs](https://gist.github.com/iF2007/ff127f7722af91c47c0cb44d6c1e961d)_

_[Find the specific model numbers based on country on TechWalls](https://www.techwalls.com/?s=iPhone+15+pro+max)_

__Todo:__
 * Add names to the presented list instead of just model numbers
 * ???