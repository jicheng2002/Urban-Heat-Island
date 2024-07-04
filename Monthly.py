# import os
# import glob
# import numpy as np
# from osgeo import gdal

# output_tif_path = r"D:\A-Projects\UrbanHeatIsland\tif"
# monthly_tif_path = r"D:\A-Projects\Urban Heat Island\Monthly_Day_RTP"

# os.makedirs(monthly_tif_path, exist_ok=True)

# # Function to get month from date string
# def get_month_from_date(date):
#     day_of_year = int(date[4:])
#     month = (day_of_year - 1) // 30 + 1  # Approximate month calculation
#     return f"{month:02d}"

# # Dictionary to hold file paths by month
# files_by_month = {}

# # Organize files by month
# for filepath in glob.glob(os.path.join(output_tif_path, "*.tif")):
#     filename = os.path.basename(filepath)
#     date = filename.split('_')[1]
#     month = get_month_from_date(date)
#     if month not in files_by_month:
#         files_by_month[month] = []
#     files_by_month[month].append(filepath)

# # Process each month
# for month, filepaths in files_by_month.items():
#     try:
#         print(f"Processing month: {month}")
#         datasets = []

#         # Open and read all TIF files for the same month
#         for fullfilepath in filepaths:
#             print(f"Opening file: {fullfilepath}")
#             dataset = gdal.Open(fullfilepath, gdal.GA_ReadOnly)
#             if dataset is None:
#                 print(f"Failed to open file: {fullfilepath}")
#                 continue

#             datasets.append(dataset.ReadAsArray())

#         # Calculate average if there are multiple datasets
#         if len(datasets) > 0:
#             average_array = np.mean(datasets, axis=0)

#             # Get geotransform and projection from one of the datasets
#             geotransform = dataset.GetGeoTransform()
#             projection = dataset.GetProjection()

#             # Create output TIF
#             outputname_temp = os.path.join(monthly_tif_path, f"MOD07_{month}_RTP.tif")
#             driver = gdal.GetDriverByName("GTiff")
#             out_raster = driver.Create(outputname_temp, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)
#             out_raster.SetGeoTransform(geotransform)
#             out_raster.SetProjection(projection)
#             out_raster.GetRasterBand(1).WriteArray(average_array)
#             out_raster.FlushCache()
#             out_raster = None
#             print(f"Created TIF: {outputname_temp}")
#         else:
#             print(f"No valid datasets found for month: {month}")

#     except Exception as e:
#         print(f"Error processing files for month {month}: {e}")
#         continue

# print("Monthly conversion completed.")


# import os
# import glob
# import numpy as np
# from osgeo import gdal
# from datetime import datetime, timedelta

# output_tif_path = r"D:\A-Projects\UrbanHeatIsland\tif"
# monthly_tif_path = r"D:\A-Projects\UrbanHeatIsland\Monthly_Day_RTP"

# os.makedirs(monthly_tif_path, exist_ok=True)

# # Function to get month from date string
# def get_month_from_date(date):
#     year = int(date[:4])
#     day_of_year = int(date[4:])
#     date_obj = datetime(year, 1, 1) + timedelta(day_of_year - 1)
#     return date_obj.strftime("%Y_%m")

# # Dictionary to hold file paths by month
# files_by_month = {}

# # Organize files by month
# for filepath in glob.glob(os.path.join(output_tif_path, "*.tif")):
#     filename = os.path.basename(filepath)
#     date = filename.split('.')[1][1:8]  # Extract date part (YYYYDDD) from second part of filename
#     month = get_month_from_date(date)
#     if month not in files_by_month:
#         files_by_month[month] = []
#     files_by_month[month].append(filepath)

# # Process each month
# for month, filepaths in files_by_month.items():
#     try:
#         print(f"Processing month: {month}")
#         datasets = []
#         valid_shapes = set()
        
#         # Open and read all TIF files for the same month
#         for fullfilepath in filepaths:
#             print(f"Opening file: {fullfilepath}")
#             dataset = gdal.Open(fullfilepath, gdal.GA_ReadOnly)
#             if dataset is None:
#                 print(f"Failed to open file: {fullfilepath}")
#                 continue

#             array = dataset.ReadAsArray()
#             shape = array.shape
#             valid_shapes.add(shape)
            
#             if len(valid_shapes) > 1:
#                 print(f"Skipping file due to shape mismatch: {fullfilepath}")
#                 continue
            
#             datasets.append(array)

#         # Calculate average if there are multiple datasets
#         if len(datasets) > 0:
#             average_array = np.mean(datasets, axis=0)

#             # Get geotransform and projection from one of the datasets
#             geotransform = dataset.GetGeoTransform()
#             projection = dataset.GetProjection()

#             # Create output TIF
#             outputname_temp = os.path.join(monthly_tif_path, f"MOD07_{month}_RTP.tif")
#             driver = gdal.GetDriverByName("GTiff")
#             out_raster = driver.Create(outputname_temp, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)
#             out_raster.SetGeoTransform(geotransform)
#             out_raster.SetProjection(projection)
#             out_raster.GetRasterBand(1).WriteArray(average_array)
#             out_raster.FlushCache()
#             out_raster = None
#             print(f"Created TIF: {outputname_temp}")
#         else:
#             print(f"No valid datasets found for month: {month}")

#     except Exception as e:
#         print(f"Error processing files for month {month}: {e}")
#         continue

# print("Monthly conversion completed.")

import os
import glob
import numpy as np
from osgeo import gdal
from datetime import datetime, timedelta

input_tif_path = r"D:\A-Projects\UrbanHeatIsland\tif"
monthly_tif_path = r"D:\A-Projects\UrbanHeatIsland\Monthly_Day_RTP"

os.makedirs(monthly_tif_path, exist_ok=True)

# Function to get month from date string
def get_month_from_date(date):
    year = int(date[:4])
    day_of_year = int(date[4:])
    date_obj = datetime(year, 1, 1) + timedelta(day_of_year - 1)
    return date_obj.strftime("%Y_%m")

# Dictionary to hold file paths by month
files_by_month = {}

# Organize files by month
for filepath in glob.glob(os.path.join(input_tif_path, "*.tif")):
    filename = os.path.basename(filepath)
    date = filename.split('_')[1]  # Extract date part (YYYYDDD)
    month = get_month_from_date(date)
    if month not in files_by_month:
        files_by_month[month] = []
    files_by_month[month].append(filepath)

# Process each month
for month, filepaths in files_by_month.items():
    try:
        print(f"Processing month: {month}")
        datasets = []
        valid_shapes = set()
        
        # Open and read all TIF files for the same month
        for fullfilepath in filepaths:
            print(f"Opening file: {fullfilepath}")
            dataset = gdal.Open(fullfilepath, gdal.GA_ReadOnly)
            if dataset is None:
                print(f"Failed to open file: {fullfilepath}")
                continue

            array = dataset.ReadAsArray()
            shape = array.shape
            valid_shapes.add(shape)
            
            if len(valid_shapes) > 1:
                print(f"Skipping file due to shape mismatch: {fullfilepath}")
                continue
            
            datasets.append(array)

        # Calculate average if there are multiple datasets
        if len(datasets) > 0:
            average_array = np.mean(datasets, axis=0)

            # Get geotransform and projection from one of the datasets
            geotransform = dataset.GetGeoTransform()
            projection = dataset.GetProjection()

            # Create output TIF
            outputname_temp = os.path.join(monthly_tif_path, f"MOD07_{month}_RTP.tif")
            driver = gdal.GetDriverByName("GTiff")
            out_raster = driver.Create(outputname_temp, dataset.RasterXSize, dataset.RasterYSize, 20, gdal.GDT_Float32)
            out_raster.SetGeoTransform(geotransform)
            out_raster.SetProjection(projection)
            for i in range(20):
                out_raster.GetRasterBand(i+1).WriteArray(average_array[i])
            out_raster.FlushCache()
            out_raster = None
            print(f"Created TIF: {outputname_temp}")
        else:
            print(f"No valid datasets found for month: {month}")

    except Exception as e:
        print(f"Error processing files for month {month}: {e}")
        continue

print("Monthly conversion completed.")
