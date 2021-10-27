# ArcGIS_Traffic-Accident-Analysis
An Arcpy script used to determine traffic accidents involving pedestrians and its location and time in the City of Toronto. 
The geodatabse contained Pedestrian Injuries.zip is the data used for this task. Python IDE must be linked to ArcGIS Pro for proper function.
This script allows the user to analyze when and where traffic accidents occur most frequently, in respect to the population and income of an area. 

This tool involves setting the appropriate cordinate system to a Canada census tract feature class before adding and calculating necessary fields. 
Censs tracts from the City of Toronto are selected from the census tracts dataset and prepared for geoprocessing.
During the processing, data such as census tract population and mean household income are calculated and added to Toronto census tracts. 

Additionally, a table consisting of accidents involving pedestrians in Toronto must be processed to include time of day accident occurs. 

Once the groprocessing scripting for the Toronto census tract feature class and accidents table complete, the two are spatially joined.  

The end result exports to an Excel table featuring information to faciliate the pedestrian accident analysis. 
