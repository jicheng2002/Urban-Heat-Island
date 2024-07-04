#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 20:32:45 2021

@author: wenjiezhang
"""


###extract the mod07 v6 and then match with the site data
#-*-coding: utf-8-*-
###extract the mod07 v6 and then match with the site data
#-*-coding: utf-8-*-
import glob,sys,os
import pandas as pd
import gdal
import numpy as np
import datetime
#from pytz import timezone
from datetime import datetime, timedelta
from openpyxl import Workbook
import subprocess
import gc
import ephem
from datetime import datetime

# #读取站点信息，全国一共两千个站点！
SiteInfo_path = r'G:\E\python\point1.csv'

SiteInfoDf = pd.read_csv(SiteInfo_path,header=0) #如果读取的是全国的文件，改成'Sheet1'

Pressure_Levels = [5,10,20,30,50,70,100,150,200,250,300,400,500,620,700,780,850,920,950,1000]
MOD07RootPath = r'G:\E\python\MOD07\ST/'
#MOD07RootPath = 'F:\BIGDATA\ScienceOfTheTotalEnvironment_RevisedandOrganized\Data\MOD07\MOD07daqikuoxian/'

Parameters = ['Skin_Temperature']
Years = ['A2017']
#Overpasses = ['Day','Night']

#for Year in Years:
for root, dirs, files in os.walk(MOD07RootPath):
    #for name in files:  
    #for Overpass in Overpasses:
       # print(name)
    MOD07FilePath = MOD07RootPath #+ Year + '/' + Overpass + '/'
    
    for Parameter in Parameters:
        print(Parameter)
#MOD07Files = glob.glob(MOD07FilePath+'*'+Parameter+'.tif')
        MOD07Files = glob.glob(MOD07FilePath+'*'+'.tif')
        excelpath = r"G:\E\python\csv2/"
        excelname = "results-3-MOD07_"+Parameter+".csv"
        Sites = pd.DataFrame([])
        
        csv_size = 0
        for MOD07_HDF in MOD07Files:
            print(MOD07_HDF)
            MOD07_RealTime = MOD07_HDF
            yearjulian = MOD07_RealTime.split('.')[1][1:8]
          
            YearMonth = datetime.strptime(yearjulian,'%Y%j')
            hour = MOD07_RealTime.split('.')[2][0:2]
            minutes= MOD07_RealTime.split('.')[2][2:4]
           
            DateHdf = datetime(year = YearMonth.year,month = YearMonth.month,day=YearMonth.day)### for computing the sunrise and sunset
            DateHdf2 = datetime(year = YearMonth.year,month = YearMonth.month,day=YearMonth.day,hour=int(hour),minute=int(minutes))###record the real utc time of satelite
         
            RTP = gdal.Open(MOD07_HDF) #Retrieved_Temperature_Profile
            #SP = gdal.Open(outputname_SP)
            RTP_cols = RTP.RasterXSize
            RTP_rows = RTP.RasterYSize
            a=RTP.GetMetadata()
            RTP_GeoTransform = RTP.GetGeoTransform()
            #print RTP_GeoTransform
            Site_Tile = SiteInfoDf[(SiteInfoDf['Lat_New']>(RTP_GeoTransform[3]-RTP_rows*RTP_GeoTransform[1]))&(SiteInfoDf['Lat_New']<RTP_GeoTransform[3])&(SiteInfoDf['Lon_New']>RTP_GeoTransform[0])&(SiteInfoDf['Lon_New']<(RTP_GeoTransform[0]+RTP_cols*RTP_GeoTransform[1]))]
        
            RTP_data = RTP.ReadAsArray()
            csv_size = csv_size + Site_Tile.shape[0]
            
            #SP_data = SP.ReadAsArray()
            if np.size(Site_Tile)>0:
                #print MOD07_HDF
                yOffset_site = [abs(int((Site_Tile['Lat_New'].iloc[i]-RTP_GeoTransform[3]) / RTP_GeoTransform[1])) for i in range(np.size(Site_Tile['Lon_New']))]
                xOffset_site = [abs(int((Site_Tile['Lon_New'].iloc[i]-RTP_GeoTransform[0]) / RTP_GeoTransform[1])) for i in range(np.size(Site_Tile['Lon_New']))]
        
                for site in range(np.size(xOffset_site)):
                    #print(site)
                    if np.size(RTP_data.shape)>2:
                        RTP_data_Site = RTP_data[:,yOffset_site[site],xOffset_site[site]]
                    else:
                        RTP_data_Site = RTP_data[yOffset_site[site],xOffset_site[site]]
                   
                    ###calculate the sunrise and sunset in utc in order to ethier it is in daytime or nighttime
        #                        o=ephem.Observer() ###observation
        #                        o.lat=str(Site_Tile['Lat_New'].iloc[site])
        #                        #print(Site_Tile[u'纬度'].iloc[site])
        #                        o.lon = str(Site_Tile['Lat_New'].iloc[site])
        #                        #print(Site_Tile[u'经度'].iloc[site])
        #                        o.date = str(DateHdf)
        #                        s=ephem.Sun()
        #                        s.compute(o)
        #
        #                        DateRise = (datetime.strptime(str(o.previous_rising(s)), "%Y/%m/%d %H:%M:%S"))
        #                        DateSet = (datetime.strptime(str(o.next_setting(s)), "%Y/%m/%d %H:%M:%S"))
        #                       
                    Sites = Sites.append([[DateHdf2,DateHdf.year,DateHdf.month,DateHdf.day,Site_Tile['Station_Id_C'].iloc[site],Parameter,RTP_data_Site]])
                       
                RTP = None
                  
        print(csv_size)
        Sites.columns = ['date','Year','Mon','Day','Station_Id_C','Parameter','data']
        Excel_full_path = excelpath+excelname
        Sites.to_csv(Excel_full_path,index=False)
        print("finished")
