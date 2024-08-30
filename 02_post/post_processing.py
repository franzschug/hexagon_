#!/usr/bin/python


#+
# :AUTHOR: Franz Schug [fschug@wisc.edu]
# :DATE: 12 Jun. 2024
#
# :Description: Cleans extracted building footprint polygons with extraction conficdence < 60%, DEM > 400 m, area < 20 m2 and > 3000 m2 for 256x256 input model as well as extraction confidence < 60%, area < 1000m2 for 512x512 input morel. For workflow description, please see manuscript.

# Use at own risk.
            
import os
import sys
from osgeo import ogr, osr
import fiona
from shapely.geometry import mapping, shape

model1 = str(sys.argv[1]).split(" ")[0]
model2 = str(sys.argv[2]).split(" ")[0]
crs = str(sys.argv[3]).split(" ")[0]
region = str(sys.argv[4]).split(" ")[0]
    
path1 = '/data/objects/' + region + '/final/' + model1 + '.shp'
path2 = '/data/objects/' + region + '/final/' + model2 + '.shp'

driverName = "ESRI Shapefile"
driver = ogr.GetDriverByName(driverName)

if not (os.path.exists(path1 + '_temp.shp')):
    # Read the original Shapefile
    with fiona.collection(path1, 'r') as input:
        # The output has the same schema
        schema = input.schema.copy()
        # write a new shapefile
        with fiona.collection(path1 + '_temp.shp', 'w', 'ESRI Shapefile', schema,crs='epsg:' + str(crs)) as output:
            for elem in input:
                 try:
                    output.write({'properties': elem['properties'],'geometry': mapping(shape(elem['geometry']))})
                 except:
                    print('invalid geometry')

if not (os.path.exists(path2 + '_temp.shp')):
    # Read the original Shapefile
    with fiona.collection(path2, 'r') as input:
        # The output has the same schema
        schema = input.schema.copy()
        # write a new shapefile
        with fiona.collection(path2 + '_temp.shp', 'w', 'ESRI Shapefile', schema,crs='epsg:' + str(crs)) as output:
            for elem in input:
                try:
                    output.write({'properties': elem['properties'],'geometry': mapping(shape(elem['geometry']))})
                except:
                    print('invalid geometry')
                    
           
inShp = '/data/objects/' + region + '/final/' + model1 + '.shp_temp.shp'
data256 = driver.Open(inShp, 1) # 0 means read-only. 1 means writeable.

inShp = '/data/objects/' + region + '/final/' + model2 + '.shp_temp.shp'
data512 = driver.Open(inShp, 1) # 0 means read-only. 1 means writeable.

layer256 = data256.GetLayer()
layer512 = data512.GetLayer()

for feature in layer256:        
        geom = feature.GetGeometryRef()
        area = geom.GetArea() 
            
        if(feature.GetField('Confidence') < 60):
            layer256.DeleteFeature(feature.GetFID())
                    
        try:
            if(feature.GetField('DEM') > 400):
                layer256.DeleteFeature(feature.GetFID())
        except:
            print('field DEM does not exist')
              
        if(area < 20):
            layer256.DeleteFeature(feature.GetFID())
            
        if(area > 3000):
            if(feature.GetField('Confidence') < 90):
                layer256.DeleteFeature(feature.GetFID())

for feature in layer512:        
        geom = feature.GetGeometryRef()
        area = geom.GetArea() 
        
        if(feature.GetField('Confidence') < 60):
            layer512.DeleteFeature(feature.GetFID())
            
        if(area <= 1000):
            layer512.DeleteFeature(feature.GetFID())

