#!/usr/bin/env python3


#+
# :AUTHOR: Franz Schug [fschug@wisc.edu]
# :DATE: 10 Jun. 2024
#
# :Description: Extract building footprints from Hexagon-derived othophotosArcGIS deep learning model implementation.

# :Parameters:  in_raster - path to orthophoto
#               in_model_definition - path to model
#               out_detected_objects - path to save objects
#
## Further parameters: Check documentation (1) and manuscript.
# (1) https://pro.arcgis.com/en/pro-app/latest/tool-reference/image-analyst/detect-objects-using-deep-learning.htm
#
# Use at own risk.


# Import system modules  
import os
import arcpy  
from arcpy.ia import *  
import tensorflow as tf

arcpy.env.processorType = "GPU"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

# Check out the ArcGIS Image Analyst extension license 
arcpy.CheckOutExtension("ImageAnalyst") 
 
in_raster = "Z:/data/region/orthophoto.tif"
in_model_definition = "Z:/data/model/region/model/model.emd"
out_detected_objects = "Z:/data/objects/region/objects.shp"

model_arguments = "padding 64; threshold 0.4; batch_size 16; tile_size 256"
run_nms = "NO_NMS" #NO_NMS
confidence_score_field = "Confidence"
class_value_field = "Id"
max_overlap_ratio = 0
processing_mode = "PROCESS_AS_MOSAICKED_IMAGE"

DetectObjectsUsingDeepLearning(in_raster, out_detected_objects, in_model_definition, model_arguments, run_nms, confidence_score_field, class_value_field, max_overlap_ratio, processing_mode)