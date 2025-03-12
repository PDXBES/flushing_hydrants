import arcpy
import os
import csv
import sys
import config
import utility

log_obj = utility.Logger(config.log_file)


def create_areaid_csv():

    # get ids from feature service
    print("get ids from feature service")
    area_ids_list = []
    with arcpy.da.SearchCursor(config.flushing_areas_fs, ['areaid']) as cursor:
        for row in cursor:
            if row[0] is not None and row[0] != '' and row[0] != ' ':
                area_ids_list.append(row[0])

    # write ids to csv
    header = ['list_name', 'name', 'label']
    output_file_name = r"areaid_list.csv"
    full_output = os.path.join(config.output_dir, output_file_name)

    if os.path.exists(full_output):
        print("remove existing file")
        os.remove(full_output)

    with open(full_output, 'w', newline='') as output:
        print("write file")
        writer = csv.writer(output)
        writer.writerow(header)
        for id in area_ids_list:
            writer.writerow(["area_id", id, id])

# could get the area_id.csv set up as a web service but is that any more useful?



create_areaid_csv()