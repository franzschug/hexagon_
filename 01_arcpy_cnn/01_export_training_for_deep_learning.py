#!/usr/bin/env python3


#+
# :AUTHOR: Franz Schug [fschug@wisc.edu]
# :DATE: 23 May 2024
#
# :Description: Extracts training data from imagery for deep learning.

# :Parameters:  inRaster - path to image. here: Hexagaon-derived orthophoto
#               out_folder - directory to save image chips as training data
#               in_training - reference building footprints for training in polygon form
#               in_mask_polygons - study area to spatially restrict training data collection
#
## Further parameters: Check documentation (1) and manuscript.
# (1) https://pro.arcgis.com/en/pro-app/latest/tool-reference/image-analyst/export-training-data-for-deep-learning.htm
#
# Use at own risk.

# Import system modules and check out ArcGIS Image Analyst extension license
import os
import arcpy
from arcpy.ia import *

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("ImageAnalyst")

inRaster = "Z:/data/region/orthophoto.tif"
out_folder = "Z:/data/training_chips/region/tr_32_256_11"
in_training = "Z:/data/training/region/building_reference_vectors.shp"
in_mask_polygons = "Z:/data/training_areas/region/mask.shp"

image_chip_format = "TIFF"
tile_size_x = "256"
tile_size_y = "256"
stride_x= "64"
stride_y= "64"
output_nofeature_tiles= "ALL_TILES" #"ONLY_TILES_WITH_FEATURES"
metadata_format= "RCNN_Masks"
start_index = 0
classvalue_field = "id"
buffer_radius = 0
rotation_angle = 0
reference_system = "MAP_SPACE"
processing_mode = "PROCESS_AS_MOSAICKED_IMAGE"
blacken_around_feature = "NO_BLACKEN"
crop_mode = "FIXED_SIZE"

# Execute 
ExportTrainingDataForDeepLearning(inRaster, out_folder, in_training, 
    image_chip_format,tile_size_x, tile_size_y, stride_x, 
    stride_y,output_nofeature_tiles, metadata_format, start_index, 
    classvalue_field, buffer_radius, in_mask_polygons, rotation_angle, 
    reference_system, processing_mode, blacken_around_feature, crop_mode)