#!/usr/bin/python


#+
# :AUTHOR: Franz Schug [fschug@wisc.edu]
# :DATE: 17 Nov. 2023
#
# :Description: This script downloads thumbnails of Hexagon satellite data (KH-9) based on an earthexplorer metadata search and export. Use as follows:
# 1. Conduct earthexplorer metadata search of  Hexagon (KH-9, data: 'Declassified 3'), https://earthexplorer.usgs.gov/, for your area of interest.
# 2. Using your USGS account credentials, export the metadata search as csv.
# 3. Rename csv file as desired, use names as region names below.
# 4. Run
#
# :Input:       inP - path to directory where metadata files are located
#               outD - path to directory where image previws will be saved
#               regions - array of names that correspond to the names of the metadata files
#
# :Output:      Folder that contains all Hexagon image thumbnails as .jpg files for easier data availability assessment
#
# Use at own risk.


import pandas as pd
import requests
import shutil 

inP = '/data/inP/'
outD = '/data/outD/'
regions = ['r6','r7','r12','r13','r15','r16','r17'] # subfolder names
regions = ['sydney'] # subfolder names

for r in regions:
    outDir = outD + str(r) + '/'
    inPath = inP + str(r) + '.csv'
    df = pd.read_csv(inPath, sep=",", index_col=False)
    for index, row in df.iterrows():    
        # build image_url
        image_url = 'https://ims.cr.usgs.gov//browse//declass3//'
        image_url += row['Mission'] + '//'
        operations = str(row['Operations Number']).zfill(5) + '//'
        image_url += operations + '//'
        image_url += row['Camera'] + '//'
        image_url += row['Entity ID']
        image_url += '.jpg'
        img_name = row['Entity ID'] + '.jpg'
        
        res = requests.get(image_url, stream = True)
        print(res.status_code)
        if res.status_code == 200:
            with open(outDir + '/' + img_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ',img_name)
        else:
            print('Image Couldn\'t be retrieved')