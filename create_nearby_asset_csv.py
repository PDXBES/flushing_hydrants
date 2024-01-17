
# per Chris Kochiss - drains to assets (inlets, sed MHs, etc) can cross boundaries so can't exclude (create domains) strictly based on boundaries
# may be able to exclude based on distance - says 200 - 250' should do it - therefore need to modify original pseudo
# buffer hydrant, intersect buffer with "drains to" assets to create asset_dict

import arcpy, os, csv
import config


# interset with flushing areas doesn't work - see above
#sect = arcpy.Intersect_analysis(["Flush_Areas", 'Hansen Assets - Inlets'], r'in_memory/sect', "ALL", '', "POINT")

buff = arcpy.Buffer_analysis("PWB Hydrants", r"in_memory/buff250", "250 Feet")
sect = arcpy.Intersect_analysis([buff, 'Hansen Assets - Inlets'], r'in_memory/sect', "ALL", '', "POINT")

flushing_asset_dict = {}
# b/c this is a dict any duplicate UNITIDs (eg XXXX) will only show up once and the others dropped
with arcpy.da.SearchCursor(sect, ['UNITID', 'FACILITYID']) as cursor:
    for row in cursor:
		if row[1] is not None and row[1] <> '' and row[1] <> ' ':
			flushing_asset_dict[row[0]] = row[1]

# header (and data) must be in the format of ['name', 'label', group_name] eg group_name = FACILITYID (the hydrant_ID) if drains to assets are grouped by hydrant
header = ['name', 'label', 'group_name']
output_dir = r"C:\Users\DASHNEY\ArcGIS\My Survey Designs\3095ba6b96484c45b226e5a0ea11b88e" # this is the survey123 media folder: beware - will vary depending on WS/user
output_file_name = r"group_names.csv"
full_output = os.path.join(output_dir, output_file_name)

with open(full_output, 'wb') as output:
    writer = csv.writer(output)
    writer.writerow(header)
    for key, value in flushing_asset_dict.items():
        writer.writerow([key, key, value])