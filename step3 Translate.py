import glob, sys, os
from osgeo import gdal

MOD07Path_HDF = r"D:\A-Projects\UrbanHeatIsland\Day_Hdf"
output_tif_path = r"D:\A-Projects\UrbanHeatIsland\GeoTiff"

os.makedirs(output_tif_path, exist_ok=True)

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
                outputname_temp = os.path.join(output_tif_path, f"{name}_Temperature.tif")
                print(f"Converting {inputname_temp} to {outputname_temp}")
                os.system(f"gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326 -tr 0.05 0.05 -r near {inputname_temp} {outputname_temp}")
                
            except Exception as e:
                print(f"Error processing file {fullfilepath}: {e}")
                continue

print("Conversion completed.")



# import glob
# import sys
# import os
# from osgeo import gdal
# import numpy as np

# MOD07Path_HDF = r"D:\A-Projects\UrbanHeatIsland\Day_Hdf"
# output_tif_path = r"D:\A-Projects\UrbanHeatIsland\Daytime_Tif"

# os.makedirs(output_tif_path, exist_ok=True)

# # Function to get date from filename
# def get_date_from_filename(filename):
#     parts = filename.split('.')
#     return parts[1]

# # Dictionary to hold file paths by date
# files_by_date = {}

# # Organize files by date
# for root, dirs, files in os.walk(MOD07Path_HDF):
#     for name in files:
#         if name.endswith('.hdf'):
#             date = get_date_from_filename(name)
#             if date not in files_by_date:
#                 files_by_date[date] = []
#             files_by_date[date].append(os.path.join(root, name))

# # Process each date
# for date, filepaths in files_by_date.items():
#     try:
#         print(f"Processing date: {date}")
#         datasets = []
        
#         # Open and read all HDF files for the same date
#         for fullfilepath in filepaths:
#             print(f"Opening file: {fullfilepath}")
#             hdf = gdal.Open(fullfilepath, gdal.GA_ReadOnly)
#             if hdf is None:
#                 print(f"Failed to open file: {fullfilepath}")
#                 continue

#             hdf_Sub = hdf.GetSubDatasets()
#             inputname_temp = hdf_Sub[14][0]
            
#             # Read the temperature subdataset
#             dataset = gdal.Open(inputname_temp)
#             if dataset is None:
#                 print(f"Failed to open subdataset: {inputname_temp}")
#                 continue
            
#             datasets.append(dataset.ReadAsArray())

#         # Calculate average if there are multiple datasets
#         if len(datasets) > 0:
#             average_array = np.mean(datasets, axis=0)

#             # Get geotransform and projection from one of the datasets
#             geotransform = dataset.GetGeoTransform()
#             projection = dataset.GetProjection()

#             # Create output TIF
#             outputname_temp = os.path.join(output_tif_path, f"MOD07_{date}_RTP.tif")
#             driver = gdal.GetDriverByName("GTiff")
#             out_raster = driver.Create(outputname_temp, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)
#             out_raster.SetGeoTransform(geotransform)
#             out_raster.SetProjection(projection)
#             out_raster.GetRasterBand(1).WriteArray(average_array)
#             out_raster.FlushCache()
#             out_raster = None
#             print(f"Created TIF: {outputname_temp}")
#         else:
#             print(f"No valid datasets found for date: {date}")

#     except Exception as e:
#         print(f"Error processing files for date {date}: {e}")
#         continue

# print("Conversion completed.")
