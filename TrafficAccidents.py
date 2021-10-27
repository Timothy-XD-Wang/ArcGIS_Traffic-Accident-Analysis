import arcpy as ap

ws = ap.env.workspace = "C:/Student/Pedestrian Injuries.gdb"
ap.env.overwriteOutput = True

CensusTracts = "C:/Pedestrian Injuries.gdb/Census/CensusTracts"
# Creating new feature class with only census tracts from Toronto
censusTractsToronto = ap.CreateFeatureclass_management(ws, "Toronto_CT")
ap.Select_analysis(CensusTracts, censusTractsToronto, "CMANAME = 'Toronto'")

# Creating new feature class to store the projected version of CensusTracts_Toronto
proj_censusTractsToronto = ap.CreateFeatureclass_management(ws, "Toronto_CT_NAD1983")
# Inputting spatial reference
SR = ap.SpatialReference("NAD 1983 UTM Zone 17N")
# Projecting CT_Toronto with SpatialRef and storing output in CT_TorontoP
ap.Project_management(censusTractsToronto, proj_censusTractsToronto, SR)

# Adding "Area" field
ap.AddField_management(proj_censusTractsToronto, "Area", "Double")
# Populating "Area" field with values from "Shape_Area"
ap.CalculateField_management(proj_censusTractsToronto, "Area", "!Shape_Area!")

CensusData = "C:/Student/Pedestrian Injuries.gdb/CensusData"
# The fields "CTUID" from the projected feature class and "CT_ID" from CensusData are to be be joined.
# CTUID and CT_ID have different data types so they cannot be joined directly, so a new interim field is created
# The new "CTUID" text field in CensusData takes values from "CT_ID" field to allow joining with projected feature class
ap.AddField_management(CensusData, "CTUID", "Text")
ap.CalculateField_management(CensusData, "CTUID", "!CT_ID!")
ap.JoinField_management(proj_censusTractsToronto, "CTUID", CensusData, "CTUID", ["POP", "HHINC_MED"])

PD = "C:/Student/Pedestrian Injuries.gdb/Injuries/Pedestrians"
# Creating new Period field to be populated by time in the day
ap.AddField_management(PD, "Period", "Text")
# Populating Period field by adding time descriptions based on Hour field
with ap.da.UpdateCursor(PD, ["Hour", "Period"]) as cursor:
    for row in cursor:
        if 6 <= row[0] <= 8:
            row[1] = "Morning_Peak"
        elif 9 <= row[0] <= 15:
            row[1] = "Day"
        elif 16 <= row[0] <= 18:
            row[1] = "Evening_Peak"
        elif row[0] >= 19 or row[0] <= 5:
            row[1] = "Night"
        cursor.updateRow(row)

# Adding new fields from Period variables
ap.AddField_management(PD, "Morning_Peak", "Short")
ap.AddField_management(PD, "Day", "Short")
ap.AddField_management(PD, "Evening_Peak", "Short")
ap.AddField_management(PD, "Night", "Short")
# Assigning default values of 0 for these new fields
ap.AssignDefaultToField_management(PD, "Morning_Peak", 0)
ap.AssignDefaultToField_management(PD, "Day", 0)
ap.AssignDefaultToField_management(PD, "Evening_Peak", 0)
ap.AssignDefaultToField_management(PD, "Night", 0)

binaryFields = ["Period", "Morning_Peak", "Day", "Evening_Peak", "Night"]
with ap.da.UpdateCursor(PD, binaryFields) as cursor:
    for row in cursor:
        if row[0] == "Morning_Peak":
            row[1] = 1
        elif row[0] == "Day":
            row[2] = 1
        elif row[0] == "Evening_Peak":
            row[3] = 1
        elif row[0] == "Night":
            row[4] = 1
        cursor.updateRow(row)

# Spatially joining Pedestrian and Toronto census tracts into one feature class
outFC = "C:/Student/Pedestrian Injuries.gdb/CT_Pedestrian_joined"
ap.SpatialJoin_analysis(PD, proj_censusTractsToronto, outFC)

# Deleting fields from outFC that are unnecessary
ap.DeleteField_management(outFC, ["Join_Count", "Target_FID", "Index_", "CMATYPE"])

# Deleting intermediate feature classes
ap.Delete_management("C:/Student/Pedestrian Injuries.gdb/Toronto_CT")
ap.Delete_management("C:/Student/Pedestrian Injuries.gdb/Toronto_CT_NAD1983")

# Converting joined CT & Pedestrian featureclass attribute table to Excel file
ap.TableToExcel_conversion(outFC, "CT_Pedestrian_joined.xls")


