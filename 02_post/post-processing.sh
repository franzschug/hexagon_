#!/bin/bash


#+
# :AUTHOR: Franz Schug [fschug@wisc.edu]
# :DATE: 12 Jun. 2024
#
# :Description: Merges building footprint predictions as resulting from ArcPy CNN models. For workflow description, please see manuscript.
#
# :Input:       inModel1 - building footprints as extracted with a model using chip size 256x256
#               inModel2 - building footprints as extracted with a model using chip size 256x256

# :Output:      out - Path to merged building footprint vector file.
#
# Use at own risk.

inModel1='tr_32_256_defaultaug_noft_on_e100_nostop_nms'
inModel2='tr_32_512_defaultaug_noft_on_e100_nostop_nms'
out='tr_32_256512_defaultaug_noft_on_e100_nostop_post'

crs=32644 #UTM EPSG, Values: 32611 San Diego County, 32616 Madison, 32736 Harare, 32644 Hyderabad
region='hyderabad' # Values: sandiego, madison, harare, hyderabad

python3 post_processing.py $inModel1 $inModel2 $crs $region

path1='/data/FS_hexagon/012_cnn/objects/'$region'/final/'$inModel1'.shp_temp.shp'
path2='/data/FS_hexagon/012_cnn/objects/'$region'/final/'$inModel2'.shp_temp.shp'
out='/data/FS_hexagon/012_cnn/objects/'$region'/final/'$out'.shp'

ogrmerge.py -single -f 'ESRI Shapefile' -o $out $path1 $path2