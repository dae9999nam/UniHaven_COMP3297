'''    import requests

   params = {
        "datasetId": "dpo_rcd_1629267205232_33603",
        "lang": "en",
        "q": "KING'S COLLEGE OLD BOYS' ASSOCIATION PRIMARY SCHOOL", # input address element information (mandatory; URL-encoded(percent-encoded)); 
        "n": 1, #range in 1-200, default=200
        "t": 35, # tolerance on returned record scores (optional; range: 0-80; default: 35);
        "b": 0,# enable/disable basic searching mode, default disabled (optional; range: 0 or 1; default: 0). 
        "3d": 0
    }
    #Address Lookup Service
    base_url = "https://www.als.gov.hk/lookup?"
    #GeoAddress Lookup Service
    ga = "https://www.als.gov.hk/galookup?ga=<input GeoAddress>"

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            print("GET Response JSON:", data)
        except Exception as e:
            print("JSON parse error:", e)
            print("Raw response:", response.text)
    else:
        print("Request failed with status code:", response.status_code)
'''
import requests
import xml.etree.ElementTree as ET

# Define the API endpoint and parameters
url = "https://www.als.gov.hk/lookup"
params = {"q": "KING'S COLLEGE OLD BOYS' ASSOCIATION PRIMARY SCHOOL"}
#url params
''' "q": "KING'S COLLEGE OLD BOYS' ASSOCIATION PRIMARY SCHOOL", # input address element information (mandatory; URL-encoded(percent-encoded)); 
        "n": 1, #range in 1-200, default=200
        "t": 35, # tolerance on returned record scores (optional; range: 0-80; default: 35);
        "b": 0,# enable/disable basic searching mode, default disabled (optional; range: 0 or 1; default: 0). '''

#GeoAddress Lookup Service
ga_url = "https://www.als.gov.hk/galookup?"
params_for_ga = {"ga":""}

# Make the GET request
response = requests.get(url, params=params)

if response.status_code == 200:
    # Print out the raw response text for debugging
    print("Raw response:", response.text)
    try:
        # Parse the XML response
        root = ET.fromstring(response.content)
        
        # For example, extract the building name in English.
        # According to your XML, it's inside SuggestedAddress > Address > PremisesAddress > EngPremisesAddress > BuildingName
        eng_building = root.find(".//EngPremisesAddress/BuildingName")
        if eng_building is not None:
            print("English Building Name:", eng_building.text)
        # If you also want to extract latitude and longitude from GeospatialInformation:
        latitude_el = root.find(".//GeospatialInformation/Latitude")
        longitude_el = root.find(".//GeospatialInformation/Longitude")
        GeoAddress_el = root.find(".//GeoAddress")
        if latitude_el is not None and longitude_el is not None and GeoAddress_el is not None:
            print("Latitude:", latitude_el.text)
            print("Longitude:", longitude_el.text)
            print("GeoAddress:", GeoAddress_el.text)
            
    except ET.ParseError as e:
        print("XML parse error:", e)
else:
    print("Request failed with status code:", response.status_code)
