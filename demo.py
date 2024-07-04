import glob,sys,os
from osgeo import gdal


MOD07Path_HDF=r"D:\A-Projects\UrbanHeatIsland\Day_Hdf\MOD07_L2.A2023001.0210.061.2023136142747.hdf""D:\A-Projects\UrbanHeatIsland\Day_Hdf\MOD07_L2.A2023001.0215.061.2023136142736.hdf"

for root, dirs, files in os.walk(MOD07Path_HDF):
    for name in files:
        try:
            fullfilepath=os.path.join(root,name)
            print(fullfilepath)
            hdf = gdal.Open(fullfilepath,gdal.GA_ReadOnly)
            hdf_metadata=hdf.GetMetadata()
            hdf_Sub=hdf.GetSubDatasets()
            inputname_sf=hdf_Sub[14][0]
            outputname_sf=os.path.join("D:\A-Projects\UrbanHeatIsland\GeoTiff/"+name+'.tif')
            os.system("gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326"+' -tr 0.05 0.05'+' -r near'+' ' + inputname_sf + ' ' +  outputname_sf)
        except:
            pass
            continue
        

# import os
# from osgeo import gdal

# # Define the paths to the HDF files
# MOD07Paths_HDF = [
#     r"D:\A-Projects\UrbanHeatIsland\Day_Hdf\MOD07_L2.A2023001.0210.061.2023136142747.hdf",
#     r"D:\A-Projects\UrbanHeatIsland\Day_Hdf\MOD07_L2.A2023001.0215.061.2023136142736.hdf"
# ]

# # Iterate over each file path
# for file_path in MOD07Paths_HDF:
#     try:
#         print(f"Processing file: {file_path}")
        
#         # Open the HDF file
#         hdf = gdal.Open(file_path, gdal.GA_ReadOnly)
#         if hdf is None:
#             print(f"Failed to open file: {file_path}")
#             continue

#         # Get metadata and subdatasets
#         hdf_metadata = hdf.GetMetadata()
#         hdf_subdatasets = hdf.GetSubDatasets()
        
#         # Check if there are subdatasets
#         if not hdf_subdatasets:
#             print(f"No subdatasets found in file: {file_path}")
#             continue
        
#         # Select the desired subdataset (index 14, assuming it exists)
#         inputname_sf = hdf_subdatasets[14][0]
#         outputname_sf = os.path.join(r"D:\A-Projects\UrbanHeatIsland\GeoTiff", os.path.basename(file_path) + '.tif')
        
#         # Use gdalwarp to convert the subdataset to GeoTIFF
#         gdalwarp_command = f"gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326 -tr 0.05 0.05 -r near {inputname_sf} {outputname_sf}"
#         print(f"Running command: {gdalwarp_command}")
#         os.system(gdalwarp_command)
        
#     except Exception as e:
#         print(f"An error occurred while processing file {file_path}: {e}")
