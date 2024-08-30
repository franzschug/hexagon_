#!/usr/bin/env python3


#+
# :AUTHOR: Franz Schug [fschug@wisc.edu]
# :DATE: 09 Jun. 2024
#
# :Description: CNN training using ArcGIS deep learning model implementation.

# :Parameters:  in_folder - path to training_chips
#               out_folder - directory to save model
#
## Further parameters: Check documentation (1) and manuscript.
# (1) https://pro.arcgis.com/en/pro-app/latest/tool-reference/image-analyst/train-deep-learning-model.htm
#
# Use at own risk.

# Import system modules  
import os
import arcpy  
from arcpy.ia import *  
import tensorflow as tf

os.environ["CUDA_VISIBLE_DEVICES"]="0"

# Check out the ArcGIS Image Analyst extension license 
arcpy.CheckOutExtension("ImageAnalyst") 

in_folder = "Z:/data/training_chips/region/tr_32_256_11"
out_folder = "Z:/data/model/region/model"
max_epochs = 100 #100
model_type = "MASKRCNN"
batch_size = 16
arg = "chip_size 256;monitor valid_loss"
augmentation = "DEFAULT"
#augmentation_parameters = "rotate (30.0,);0.8;brightness;contrast;zoom;crop"
learning_rate = None
backbone_model = "RESNET50" 
pretrained_model = None
validation_percentage = 15

stop_training = "CONTINUE_TRAINING"
freeze = "UNFREEZE_MODEL"

TrainDeepLearningModel(in_folder, out_folder, max_epochs, model_type, batch_size, arg, learning_rate, backbone_model, pretrained_model, validation_percentage, stop_training, freeze, augmentation)