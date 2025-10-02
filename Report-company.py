#Import the JSON file
import json

# Read json from products.json to the variable data
data = json.load(open("network_devices.json","r",encoding = "utf-8"))

# Create a variable that holds our whole text report
report = ""

#1 Last updated report & company name
report += "\n" + "Company Name: "  + data["company"] + "\n"
report += "\n" + "LAST UPDATED:" "\n" + data["last_updated"] + "\n"

#2 List all devices with warning
report += "\n" "ATTENTION! Devices with warnings" "\n"
report += "--------------------------------------------------------------------------------------------" "\n"
for location in data["locations"]:
   for device in location["devices"]:
      if device["status"] != "online" and device["status"] != "offline":
         report += device["hostname"].ljust (12) + " | " + device["status"] + " | " + device["ip_address"].ljust (14) + " | " + device["type"].ljust (12) + " | " + location["site"] + "\n"
# List all devices with Offline
report += "\n" "ATTENTION! Devices with status offline!" "\n"
report += "--------------------------------------------------------------------------------------------" "\n"
for location in data["locations"]:
   for device in location ["devices"]:
      if device["status"] != "online" and device["status"] != "warning":
        report += device["hostname"].ljust (12) + " | " + device["status"] + " | " + device["ip_address"].ljust (15) + " | " + device ["type"].ljust (12) + " | " + location["site"] + "\n"
        

# loop through the location list 
for location in data["locations"]:
    # add the site/'name' of the location to the report
    report += "\n" + location["site"] + "\n"
    # add a list of the host names of the devices 
    # on the location to the report
    for device in location["devices"]:
      report += "  " + device["hostname"] + "\n"

# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)