#!/usr/bin/python


#+
# :AUTHOR: Franz Schug [fschug@wisc.edu]
# :DATE: 28 Nov. 2023
# !!!!!!Adapted code from: https://github.com/microsoft/GlobalMLBuildingFootprints/blob/main/examples/example_building_footprints.ipynb !

# :Description: Downloads Microsoft building footprint data based on a given area of interest
#


import pandas as pd
import geopandas as gpd
import shapely.geometry
import mercantile
from tqdm import tqdm
import os
import tempfile
import fiona


output_fn = "/data/ms_building_footprints_site.geojson"

# Site: San Diego County
#[-118, 34],
#[-118, 32],
#[-116, 32],
#[-116, 34],
#[-118, 34]

# Site: Madison
#[-90, 44],
#[-89, 44],
#[-89, 42],
#[-90, 42],
#[-90, 44] 

# Site: Harare
#[30, -18],
#[30, -17],
#[32, -17],
#[32, -18],
#[30, -18]

# Site: Hyderabad
#[78, 18],
#[79, 18],
#[79, 17],
#[78, 17],
#[78, 18]   


# Geometry copied from https://geojson.io
aoi_geom = {
        "coordinates": [
          [
            [-118, 34],
            [-118, 32],
            [-116, 32],
            [-116, 34],
            [-118, 34]
          ]
        ],
    "type": "Polygon",
}
aoi_shape = shapely.geometry.shape(aoi_geom)
minx, miny, maxx, maxy = aoi_shape.bounds


quad_keys = set()
for tile in list(mercantile.tiles(minx, miny, maxx, maxy, zooms=9)):
    quad_keys.add(int(mercantile.quadkey(tile)))
quad_keys = list(quad_keys)

print(f"The input area spans {len(quad_keys)} tiles: {quad_keys}")
     
df = pd.read_csv("https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv")

idx = 0
combined_rows = []

with tempfile.TemporaryDirectory() as tmpdir:
    # Download the GeoJSON files for each tile that intersects the input geometry
    tmp_fns = []
    for quad_key in tqdm(quad_keys):
        rows = df[df["QuadKey"] == quad_key]
        print('rows.shape[0]')                   
        print(rows.shape[0])                   
        if rows.shape[0] == 1:
            url = rows.iloc[0]["Url"]
        
            df2 = pd.read_json(url, lines=True)
            df2["geometry"] = df2["geometry"].apply(shapely.geometry.shape)
        
            gdf = gpd.GeoDataFrame(df2, crs=4326)
            fn = os.path.join(tmpdir, f"{quad_key}.geojson")
            tmp_fns.append(fn)
            if not os.path.exists(fn):
                gdf.to_file(fn, driver="GeoJSON")
        elif rows.shape[0] > 1:
            raise ValueError(f"Multiple rows found for QuadKey: {quad_key}")
        else:
            raise ValueError(f"QuadKey not found in dataset: {quad_key}")
    
    # Merge the GeoJSON files into a single file
    for fn in tmp_fns:
        with fiona.open(fn, "r") as f:
            for row in tqdm(f):
                row = dict(row)
                shape = shapely.geometry.shape(row["geometry"])

                if aoi_shape.contains(shape):
                    if "id" in row:
                        del row["id"]
                    row["properties"] = {"id": idx}
                    idx += 1
                    combined_rows.append(row)           
          
schema = {"geometry": "Polygon", "properties": {"id": "int"}}
print("dll")
with fiona.open(output_fn, "w", driver="GeoJSON", crs="EPSG:4326", schema=schema) as f:
    f.writerecords(combined_rows)
print("out")
print(output_fn)