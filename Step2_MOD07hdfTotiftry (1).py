# -*- coding: utf-8 -*-
"""
Created on Sat May 11 09:32:27 2024

@author: lü'lü'lü
"""

import glob,sys,os
import gdal

#MOD07Path_Tif=r'F:\BIGDATA\ScienceOfTheTotalEnvironment_RevisedandOrganized\Data\MOD07\MOD07_L2\2017\'
MOD07Path_HDF=r'D:\A-Projects\UrbanHeatIsland\Day_Hdf'

writepath=r'D:\A-Projects\UrbanHeatIsland\Daytime_Tif'
for root, dirs, files in os.walk(MOD07Path_HDF):
    for name in files:
        try:
            fullfilepath=os.path.join(root,name)
            print(fullfilepath)
            hdf = gdal.Open(fullfilepath,gdal.GA_ReadOnly)
            hdf_metadata=hdf.GetMetadata()
            hdf_Sub=hdf.GetSubDatasets()
#            inputname_sf=hdf_Sub[14][0]
#            outputname_sf=os.path.join(r'G:\E\python\MOD07/RTP/' +name+'_RTP.tif')
#            os.system("gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326"+' -tr 0.05 0.05'+' -r near'+' ' + inputname_sf + ' ' +  outputname_sf)
##            
#            inputname_sf=hdf_Sub[8][0]
#            outputname_sf=os.path.join(r'G:\E\python\MOD07/SP/' +name+'_surfacepressure.tif')
#            os.system("gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326"+' -tr 0.05 0.05'+' -r near'+' ' + inputname_sf + ' ' +  outputname_sf)
            inputname_sf=hdf_Sub[14][0]
            outputname_sf=os.path.join(r'D:\A-Projects\UrbanHeatIsland\Daytime_Tif/' +name+'_RTP.tif')
            os.system("gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326"+' -tr 0.05 0.05'+' -r near'+' ' + inputname_sf + ' ' +  outputname_sf)
        except:
            pass
            continue