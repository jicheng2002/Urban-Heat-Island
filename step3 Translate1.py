# import glob, sys, os
# from osgeo import gdal

# MOD07Path_HDF = r"D:\A-Projects\UrbanHeatIsland\Day_Hdf"
# output_tif_path = r"D:\A-Projects\UrbanHeatIsland\tif"

# os.makedirs(output_tif_path, exist_ok=True)

# def get_date_from_filename(filename):
#     parts = filename.split('.')
#     return parts[1]

# for root, dirs, files in os.walk(MOD07Path_HDF):
#     for name in files:
#         if name.endswith('.hdf'):
#             try:
#                 fullfilepath = os.path.join(root, name)
#                 print(f"Processing file: {fullfilepath}")
#                 hdf = gdal.Open(fullfilepath, gdal.GA_ReadOnly)
#                 if hdf is None:
#                     print(f"Failed to open file: {fullfilepath}")
#                     continue
                
#                 hdf_metadata = hdf.GetMetadata()
#                 hdf_Sub = hdf.GetSubDatasets()

#                 # 提取温度子数据集
#                 inputname_temp = hdf_Sub[14][0]  
#                 outputname_temp = os.path.join(output_tif_path, f"{name}_RTP.tif")
#                 print(f"Converting {inputname_temp} to {outputname_temp}")
#                 os.system(f"gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326 -tr 0.05 0.05 -r near {inputname_temp} {outputname_temp}")
                
               
#             except Exception as e:
#                 print(f"Error processing file {fullfilepath}: {e}")
#                 continue

# print("Conversion completed.")


import glob
import sys
import os
from osgeo import gdal

MOD07Path_HDF = r"D:\A-Projects\UrbanHeatIsland\Day_Hdf"
output_tif_path = r"D:\A-Projects\UrbanHeatIsland\tif"

os.makedirs(output_tif_path, exist_ok=True)

# Function to get date from filename
def get_date_from_filename(filename):
    parts = filename.split('.')
    date_str = parts[1][1:]  # Remove the leading 'A'
    year = date_str[:4]
    day_of_year = int(date_str[4:])
    return year, day_of_year

for root, dirs, files in os.walk(MOD07Path_HDF):
    for name in files:
        if name.endswith('.hdf'):
            try:
                fullfilepath = os.path.join(root, name)
                print(f"Processing file: {fullfilepath}")
                hdf = gdal.Open(fullfilepath, gdal.GA_ReadOnly)
                if hdf is None:
                    print(f"Failed to open file: {fullfilepath}")
                    continue
                
                hdf_metadata = hdf.GetMetadata()
                hdf_Sub = hdf.GetSubDatasets()

                # 提取温度子数据集
                inputname_temp = hdf_Sub[14][0]  

                # 获取年份和日期
                year, day_of_year = get_date_from_filename(name)
                outputname_temp = os.path.join(output_tif_path, f"MOD07_{year}{day_of_year:03d}_RTP.tif")

                print(f"Converting {inputname_temp} to {outputname_temp}")
                os.system(f"gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326 -tr 0.05 0.05 -r near {inputname_temp} {outputname_temp}")
                
            except Exception as e:
                print(f"Error processing file {fullfilepath}: {e}")
                continue

print("Conversion completed.")
