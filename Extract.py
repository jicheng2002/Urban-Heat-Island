import os
import glob
import subprocess
from osgeo import gdal

chinashp = r"D:\A-Projects\UrbanHeatIsland\shp\Bayarea.shp"
mod13a3_wrap = r"D:\A-Projects\UrbanHeatIsland\PressureTem"
mod13a3_crop = r"D:\A-Projects\UrbanHeatIsland\Bayarea_Tif"
os.makedirs(mod13a3_crop, exist_ok=True)

tiffiles = glob.glob(os.path.join(mod13a3_wrap, '*.tif'))

for tiffile in tiffiles:
    print(f"Processing {tiffile}")
    filename = os.path.join(mod13a3_crop, os.path.basename(tiffile))
    crop_command = [
        'gdalwarp',
        '-of', 'GTiff',
        '-cutline', chinashp,
        '-crop_to_cutline',
        tiffile,
        filename
    ]
    print(f"Running command: {' '.join(crop_command)}")
    
    try:
        subprocess.run(crop_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Skipping {tiffile} due to error: {e}")



