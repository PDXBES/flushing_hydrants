import utility
import os
import arcpy

utility.datetime_print("Running Config")

log_file = r"\\besfile1\ISM_PROJECTS\Work_Orders\WO_10233_M_Wood\hydrant_flushing_log"

# this is the survey123 media folder: beware - will vary depending on WS/user
# output_dir = r"C:\Users\DASHNEY\ArcGIS\My Survey Designs\Hydrant Request Form - Pilot3\media" #OLD
output_dir = r"C:\Users\DASHNEY\ArcGIS\My Survey Designs\Hydrant Flushing Request Form\media"

# question - use this instead of EGH_PUBLIC connection for consistency with assets in web map?
ref_collection_nodes_fs = "https://www.portlandmaps.com/private/rest/services/BES_REFERENCE/FeatureServer/0"
# flushing_areas_fs = "https://www.portlandmaps.com/ags/rest/services/Hosted/Flush_Areas_Pilot/FeatureServer/11" # test version
flushing_areas_fs = "https://www.portlandmaps.com/private/rest/services/PWB_FlushingAreas/FeatureServer/0"

# create separate connections folder for this job?
sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"

PWBWATER_sde = os.path.join(sde_connections, "GISDB1.PWBWATER.sde")
EGH_PUBLIC_sde = os.path.join(sde_connections, "GISDB1.EGH_PUBLIC.sde")

WB_hydrants_raw = PWBWATER_sde + r"\PWBWATER.ARCMAP_ADMIN.Hydrant"
BES_nodes_raw = EGH_PUBLIC_sde + r"\EGH_PUBLIC.ARCMAP_ADMIN.collection_points_bes_pdx"
BES_alt_nodes_raw = EGH_PUBLIC_sde + r"\EGH_PUBLIC.ARCMAP_ADMIN.collection_points_alt_bes_pdx"

BES_nodes_fl = arcpy.MakeFeatureLayer_management(BES_nodes_raw,
                                                 r"in_memory\BES_nodes_fl",
                                                 "LAYER_GROUP = 'SEWER NODES' AND SYMBOL_GROUP = 'MANHOLES'")
BES_alt_nodes_fl = arcpy.MakeFeatureLayer_management(BES_alt_nodes_raw,
                                                     r"in_memory\BES_alt_nodes_fl",
                                                     "ALTIDTYP = 'UICDEQID'") # ie sumps

WB_hydrants_copy = arcpy.CopyFeatures_management(WB_hydrants_raw, r"in_memory\WB_hydrants_copy")
BES_nodes_copy = arcpy.CopyFeatures_management(BES_nodes_fl, r"in_memory\BES_nodes_copy")
BES_alt_nodes_copy = arcpy.CopyFeatures_management(BES_alt_nodes_fl, r"in_memory\BES_alt_nodes_copy")

BES_assets_combined = arcpy.Merge_management([BES_nodes_copy, BES_alt_nodes_copy], r"in_memory\assets_combined")