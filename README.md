# Data 512 - Project - Final Report
## Project Goal
The goal of this project is to investigate forest fires within 1250 miles of Kingman, Arizona from 1963-2020 by developing a smoke impact metric, predicting this metric through 2049, and creating informative visualizations.
## Licenses and Links
USGS Wildfire Data -  
https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81  
EPA AQI Information -  
https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf  
Pyproj Documentation -  
https://pyproj4.github.io/pyproj/stable/index.html  
Geojson Documentation -  
https://pypi.org/project/geojson/  
Code License -  
https://creativecommons.org/licenses/by/4.0/  
EPSG:4326 Information -  
https://epsg.io/4326  
US EPA AQI Documentation -  
https://aqs.epa.gov/aqsweb/documents/data_api.html  
US EPA FAQ -  
https://www.epa.gov/outdoor-air-quality-data/frequent-questions-about-airdata  
FIPS Information -  
https://www.census.gov/library/reference/code-lists/ansi.html
## Data Files
### USGS_Wildland_Fire_Combined_Dataset.json
Note: Only a sample of this data, called Wildfire_short_sample.json, is in this repository due to the 25MB upload limit. The entire file is provided in the first link above.  
This data file includes information for all forest fires in the United States from the 1800s to present day. It has many fields, but we will only discuss the fields that are relevant to this project. It includes a Fire_Year field with the year of the fire, a USGS_Assigned_ID field with the USGS assigned ID for that fire, a Listed_Fire_Names field with the names used for that fire, a GIS_Acres field with the acres burned by that fire, an Assigned_Fire_Type field with the assigned fire type for that fire, and a rings field with the coordinates representing the perimeter of that fire.
### wf_data.csv
This data file includes information for every forest fire in the United States from the 1800s to present day. It is a converted form of the USGS_Wildland_Fire_Combined_Dataset.json file. It includes a year field with the year of the fire, an id field with the id number of the fire, a name field with the name of the fire, a size field with the number of acres burned by the fire, a type field with the type of the fire, a close_lat field with the closest point's latitude to Kingman, Arizona for the fire, a close_lon field with the closest point's longitude to Kingman, Arizona for the fire, and a distance field with the distance in miles of the closest perimeter point of the fire to Kingman, Arizona.
### aqi_data.csv
This data file includes information for estimates of the US EPA AQI across the sensors within Mohave County from 1996 through October 2023. It includes a year field with the year of the AQI measurements and an aqi field with the average AQI across the sensors for that year.
## Special Considerations
Processing the USGS_Wildland_Fire_Combined_Dataset.json from JSON to CSV takes a few hours, so budget time accordingly. Also, consider using bounding boxes if not enough data is given from the county method for requesting sensor data on AQI measurements.
