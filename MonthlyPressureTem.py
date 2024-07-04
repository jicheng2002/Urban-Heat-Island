# import os
# import glob
# import numpy as np
# import rasterio
# from rasterio.enums import Resampling

# # Define the paths
# tif_folder = r"D:\A-Projects\UrbanHeatIsland\Bayarea_Tif"
# output_folder = r"D:\A-Projects\UrbanHeatIsland\Monthly_Mean_Temperature"

# os.makedirs(output_folder, exist_ok=True)

# # Define month ranges
# month_ranges = {
#     '01': range(0, 3),
#     '02': range(3, 6),
#     '03': range(6, 9),
#     '04': range(9, 12),
#     '05': range(12, 15),
#     '06': range(15, 18),
#     '07': range(18, 21),
#     '08': range(21, 24),
#     '09': range(24, 27),
#     '10': range(27, 30),
#     '11': range(30, 33),
#     '12': range(33, 36)
# }

# # Helper function to get the month from the filename
# def get_month_from_filename(filename):
#     month_day = int(filename.split('_')[1][5:7])
#     for month, days in month_ranges.items():
#         if month_day in days:
#             return month
#     return None

# # Process each pressure level and month
# pressure_levels = set()
# for tif_file in glob.glob(os.path.join(tif_folder, "*.tif")):
#     pressure = tif_file.split('_')[0]
#     pressure_levels.add(pressure)

# for pressure in pressure_levels:
#     for month in month_ranges.keys():
#         tif_files = [f for f in glob.glob(os.path.join(tif_folder, f"{pressure}_*.tif")) if get_month_from_filename(f) == month]
        
#         if not tif_files:
#             continue
        
#         # Read all TIFF files for the given pressure and month
#         arrays = []
#         for tif_file in tif_files:
#             with rasterio.open(tif_file) as src:
#                 arrays.append(src.read(1, masked=True))
        
#         # Calculate the mean, ignoring NaNs
#         mean_array = np.ma.mean(np.ma.stack(arrays), axis=0)

#         # Save the result to a new TIFF file
#         output_file = os.path.join(output_folder, f"{pressure}_mean_{month}.tif")
#         with rasterio.open(tif_files[0]) as src:
#             profile = src.profile
#             profile.update(dtype=rasterio.float32, count=1, compress='lzw')
        
#         with rasterio.open(output_file, 'w', **profile) as dst:
#             dst.write(mean_array.filled(np.nan), 1)

# print("Monthly mean temperature calculation completed.")

import os
import glob
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject, calculate_default_transform

# Define the paths
tif_folder = r"D:\A-Projects\UrbanHeatIsland\BayareaTif\1000hPa"
output_folder = r"D:\A-Projects\UrbanHeatIsland\MonthlyMeanTemperature"

os.makedirs(output_folder, exist_ok=True)

# Define month ranges
month_ranges = {
    '01': range(0, 3),
    '02': range(3, 6),
    '03': range(6, 9),
    '04': range(9, 12),
    '05': range(12, 15),
    '06': range(15, 18),
    '07': range(18, 21),
    '08': range(21, 24),
    '09': range(24, 27),
    '10': range(27, 30),
    '11': range(30, 33),
    '12': range(33, 36)
}

# Helper function to get the month from the filename
def get_month_from_filename(filename):
    basename = os.path.basename(filename)
    month_day = int(basename.split('_')[1][5:7])
    for month, days in month_ranges.items():
        if month_day in days:
            return month
    return None

# Helper function to get the pressure level from the filename
def get_pressure_from_filename(filename):
    basename = os.path.basename(filename)
    return basename.split('_')[0].replace('hPa', '')

# Process each pressure level and month
pressure_levels = set(get_pressure_from_filename(os.path.basename(tif_file)) for tif_file in glob.glob(os.path.join(tif_folder, "*.tif")))

for pressure in pressure_levels:
    for month in month_ranges.keys():
        tif_files = [f for f in glob.glob(os.path.join(tif_folder, "*.tif")) if get_pressure_from_filename(f) == pressure and get_month_from_filename(f) == month]
        
        # Debug: Print the pressure and month being processed
        print(f"Processing pressure: {pressure}, month: {month}, number of files: {len(tif_files)}")

        if not tif_files:
            print(f"No files found for pressure: {pressure}, month: {month}")
            continue
        
        # Read and reproject all TIFF files for the given pressure and month
        arrays = []
        reference_profile = None
        for tif_file in tif_files:
            with rasterio.open(tif_file) as src:
                if reference_profile is None:
                    reference_profile = src.profile
                    reference_profile.update(dtype=rasterio.float32, count=1, compress='lzw')
                    reference_transform = src.transform
                    reference_crs = src.crs
                    reference_shape = src.shape
                array = src.read(1, masked=True)
                
                # Reproject the array to the reference grid
                reprojected_array = np.empty(reference_shape, dtype=np.float32)
                reproject(
                    source=array,
                    destination=reprojected_array,
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=reference_transform,
                    dst_crs=reference_crs,
                    resampling=Resampling.nearest
                )
                arrays.append(np.ma.masked_invalid(reprojected_array))
        
        # Calculate the mean, ignoring NaNs
        stack = np.ma.stack(arrays)
        mean_array = np.ma.mean(stack, axis=0)

        # Save the result to a new TIFF file
        output_file = os.path.join(output_folder, f"{pressure}hPa_mean_{month}.tif")
        with rasterio.open(output_file, 'w', **reference_profile) as dst:
            dst.write(mean_array.filled(np.nan), 1)

print("Monthly mean temperature calculation completed.")





