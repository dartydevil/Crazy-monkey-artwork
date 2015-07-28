import csv
import base64
import json
import glob

import place

street_id_to_street = {}
crime_data = []

def convert_csv_file(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        
        rows = [row for row in reader][1:]
        
        for row in rows:
            if "violence" in row[9].lower():
                longitude = row[4]
                latitude = row[5]
                
                if longitude == "" or latitude == "":
                    continue
                
                street = row[6][len("On or near "):]
                street_id = place.format_uk(base64.urlsafe_b64encode(street))
                
                if street_id in street_id_to_street:
                    street_id_to_street[street_id]["num_crimes"] += 1
                else:
                    street_id_to_street[street_id] = {"label": street,
                                                      "longitude": float(longitude),
                                                      "latitude": float(latitude),
                                                      "num_crimes": 1}
                
                crime_data.append({"longitude": float(longitude),
                                   "latitude": float(latitude),
                                   "street_id": street_id})

files = glob.glob("data/*.csv")

for filename in files:
    convert_csv_file(filename)

with open("crime_data.json", "w") as f:
    json.dump({"crimes": crime_data}, f)

with open("streets.json", "w") as f:
    json.dump(street_id_to_street, f)
