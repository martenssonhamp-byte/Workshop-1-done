#Import the JSON file
import json

# Read json from products.json to the variable data
data = json.load(open("network_devices.json","r",encoding = "utf-8"))

# Create a variable that holds our whole text report
report = ""

#1 Last updated report & company name
report += "\n" + "Company Name: "  + data["company"] + "\n"
report += "\n" + "LAST UPDATED:" "\n" + data["last_updated"].replace("T"," ")  + "\n"

#2 List all devices with warning
report += "############################################################################################"
report += "\n" "ATTENTION! Devices with status: Warning!" "\n\n"
for location in data["locations"]:
   for device in location["devices"]:
      if device["status"] != "online" and device["status"] != "offline":
         report += device["hostname"].ljust (12) + " | " + device["status"] + " | " + device["ip_address"].ljust (14) + " | " + device["type"].ljust (12) + " | " + location["site"] + "\n"

# List all devices with Offline
report += "--------------------------------------------------------------------------------------------"
report += "\n" "ATTENTION! Devices with status: Offline!" "\n\n"
for location in data["locations"]:
   for device in location ["devices"]:
      if device["status"] != "online" and device["status"] != "warning":
        report += device["hostname"].ljust (12) + " | " + device["status"] + " | " + device["ip_address"].ljust (15) + " | " + device ["type"].ljust (12) + " | " + location["site"] + "\n"

#3. Total devices per type
device_count = {}
report +="------------------------------------------------------------------------------------------"
report += "\n" "-Number of devices-" "\n\n"
for location in data["locations"]:
   for device in location["devices"]:
        t = device["type"]
        if t not in device_count:
           device_count[t] = 0
        device_count[t] += 1
for t in device_count:
   report += t.ljust(13) + ": " + str(device_count[t]) + "\n"

#4. Devices with less than 30 days uptime
report +="------------------------------------------------------------------------------------------"
report += "\n" "-Devices with < 30 days uptime-" "\n\n"
for location in data["locations"]:
   for device in location["devices"]:
      if device.get("uptime_days", 9999) < 30:
         report += device["hostname"].ljust(13) + "|" + " " + str(device["uptime_days"]).ljust(3) + "|" + " " + "days" + "\n"

#5. Calculate total port usage
report += "------------------------------------------------------------------------------------------" 
report += "\n" "-Switch port usage-"

total_ports = 0
used_ports = 0
total_used = 0
# Total port usage
for location in data["locations"]:
   for device in location["devices"]:
      if device.get("type") == "Switch":
         ports = device.get("ports")
         if ports:
            total_used += ports["used"]
            total_ports += ports["total"]
percent = round(total_used / total_ports * 100, 1)
report += ("\n Total switch port usage: "
           + str(total_used) + "/"
           + str(total_ports) + " ("
           + str(percent) + "%)\n" + "\n")
# Per location
report += "\n" "-Switch ports usage per location-" "\n"
for location in data["locations"]:
   loc_ports = 0
   loc_used = 0
   for device in location["devices"]:
      if device.get("type") == "Switch":
         ports = device.get("ports")
         if ports:
            used = ports["used"]
            total = ports["total"]
            percent = round(used / total * 100, 1) if total > 0 else 0
            
            warning = "CAUTION!" if percent >= 85 else ""

            report += (device["hostname"].ljust(14) + ": "
                + str(used) + "/"
                + str(total) + " ("
                + str(percent) + "%)".ljust(4) + warning + "\n")

#6. List of all unique VLANs in use
report += "------------------------------------------------------------------------------------------" 
report += "\n" "-Unique VLANs in network:-"
vlans = set()
vlans = {10, 20, 30}
for location in data["locations"]:
   for device in location["devices"]:
      if 20 in vlans:
         report += "VLAN 20 finns!" "\n"


# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)