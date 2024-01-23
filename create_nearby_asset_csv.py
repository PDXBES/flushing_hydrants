
# per Chris - drains to assets (inlets, sed MHs, etc) can cross boundaries so can't exclude (create domains) strictly based on boundaries
# may be able to exclude based on distance - says 200 - 250' should do it - therefore need to modify original pseudo
# buffer hydrant, intersect buffer with "drains to" assets to create asset_dict

import arcpy
import os
import csv
import sys
import config
import utility

log_obj = utility.Logger(config.log_file)

try:

    log_obj.info("Create Nearby Asset CSV - Starting".format())

    log_obj.info("Create Nearby Asset CSV - Buffering targets".format())
    buff = arcpy.Buffer_analysis(config.WB_hydrants_copy, r"in_memory/buff250", "250 Feet")
    log_obj.info("Create Nearby Asset CSV - Intersecting assets with buffer".format())
    sect = arcpy.Intersect_analysis([buff, config.BES_assets_combined], r'in_memory/sect', "ALL", '', "POINT")

    # header (and data) must be in the format of ['name', 'label', group_name] eg group_name = FACILITYID (the hydrant_ID) if drains to assets are grouped by hydrant
    header = ['name', 'label', 'hydrant_id']
    output_file_name = r"group_names.csv"
    full_output = os.path.join(config.output_dir, output_file_name)

    log_obj.info("Create Nearby Asset CSV - Writing assets to csv at {}".format(full_output))
    with open(full_output, 'wb') as output:
        writer = csv.writer(output)
        writer.writerow(header)
        with arcpy.da.SearchCursor(sect, ['UNITID', 'FACILITYID']) as cursor:
            for row in cursor:
                if row[1] is not None and row[1] != '' and row[1] != ' ':
                    writer.writerow([row[0], row[0], row[1]])

    log_obj.info("Create Nearby Asset CSV - Complete".format())

except Exception as e:
    arcpy.ExecuteError()
    log_obj.exception(str(sys.exc_info()[0]))
    log_obj.info("Hazard Area Creation Failed".format())
    pass