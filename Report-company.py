#Import the JSON file
import json

# Read json from products.json to the variable data
data = json.load(open("network_devices.json","r",encoding = "utf-8"))

# Create a variable that holds our whole text report
report = ""
intro_report = ""
#1 Last updated report & company name
intro_report += "\n" + "Company Name: "  + data["company"] + "\n"
intro_report += "\n" + "LAST UPDATED:" "\n" + data["last_updated"].replace("T"," ")  + "\n"

#2 List all devices with warning
report += "\n############################################################################################"
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
report += "\n" "-Switch port usage-\n"
report += "   Site ".ljust(12) + "Switches " + " Used/total " + " Percent " + "\n"
total_ports = 0
used_ports = 0
total_used = 0
# Total port usage
for location in data["locations"]:
    port_count = 0
    used_count = 0
    switch_count = 0
    for device in location["devices"]:
        if device.get("type") == "Switch":
            switch_count += 1
            ports = device.get("ports")
            if ports:
                used_count += ports["used"]
                port_count += ports["total"]
    total_used += used_count
    total_ports += port_count
    percent_site = round(used_count / port_count * 100, 1)
    report += location["site"].ljust(15) + " " + str(switch_count).ljust(5) + " " + str(used_count).ljust(3) + "/" + str(port_count).ljust(8) + str(percent_site) + "%"
    if percent_site > 80:
        report += " ⚠"
        if percent_site > 90:
           report += " CRITICAL!"
    report += "\n"
percent = round(total_used / total_ports * 100, 1)
report += ("\n Total switch port usage: "
           + str(total_used) + "/"
           + str(total_ports) + " ("
           + str(percent) + "%)\n")
# Per location
report += "\n" "-Switch ports usage per location with over 80%-" "\n"
for location in data["locations"]:
   loc_ports = 0
   loc_used = 0
   for device in location["devices"]:
      if device.get("type") == "Switch":
         ports = device.get("ports")
         if ports:
            used = ports["used"]
            total = ports["total"]
            percent = round(used / total * 100, 1)
            if percent >= 80:
                warning = "CAUTION!"

                report += (device["hostname"].ljust(14) + "|" + location["site"].ljust(12) + "|" + ": "
                + str(used) + "/"
                + str(total) + " ("
                + str(percent).ljust(5) + "%)".ljust(3) + " | "
                + warning + "\n")

#6. List of all unique VLANs in use
report += "------------------------------------------------------------------------------------------" 
report += "\n" "-Unique VLANs in network-""\n"

vlans_set = set() #Dodge doublets
for location in data ["locations"]:
    for device in location["devices"]:
      if "vlans" in device:
         for vlan_id in device["vlans"]:
            vlans_set.add(vlan_id)
vlan_count = len(vlans_set)
report += "Total amount of VLANs: " + str(vlan_count) + "\n"
#for vlan in sorted(vlans_set):
    #report += str(vlan) + ", "
for i, vlan in enumerate(sorted(vlans_set)): # i = index, row 106 - 109 is all about removing the last ","
    report += str(vlan)
    if i < (vlan_count) -1:
       report += ","

#7. Overview of every location with devices and online/offline devices
report += "\n" "------------------------------------------------------------------------------------------" 
report += "\n\n" + "-Overview-" + "\n"
report += "Site:".ljust(15) + " Devices  " + "Online  " + "Offline  " + "\n"
total_offline_count = 0
for location in data["locations"]:
    num_devices = 0
    offline_count = 0
    online_count = 0
    for device in location["devices"]:
        num_devices += 1
        if device["status"] == "offline":
            offline_count += 1
        elif device["status"] == "online":
           online_count += 1    
    total_offline_count += offline_count
    report += location["site"].ljust(14) + " | " + str(num_devices).rjust(3) + " " + str(offline_count).rjust(7) + " " + str(online_count).rjust(8) + "\n"
      
      
#Summary
exec_report = ""
exec_report += "############################################################################################"
exec_report += "\n                            -----EXECUTIVE SUMMARY-----\n"
warning_count = 0
low_uptime_count = 0
high_port_count = 0
for location in data ["locations"]:
    for device in location["devices"]:
        if device["status"] == "warning":
            warning_count += 1
        if device.get("uptime_days", 9999) < 30:
            low_uptime_count += 1    
        if device.get("type") == "Switch":
            ports = device.get("ports")
            if ports:
                used = ports["used"]
                total = ports["total"]
                percent = round(used / total * 100, 1)
                if percent > 80:
                    high_port_count += 1

exec_report += "⚠ CRITICAL! " + str(total_offline_count) + " devices offline" + "\n"
exec_report += "⚠ WARNINGS! " + str(warning_count) + " devices with warning status" + "\n"
exec_report += "⚠ " + str(low_uptime_count) + " devices with low uptime < 30 days, could indicate instability!" + "\n" 
exec_report += "⚠ " + str(high_port_count) + " switches with high port usage > 80%! " + "\n"
# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(intro_report)
    f.write(exec_report)
    f.write(report)