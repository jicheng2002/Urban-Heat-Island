# import os
# import glob
# import geopandas as gpd
# import rasterio
# from rasterio.mask import mask
# from shapely.geometry import box

# # 文件路径
# tif_folder = r'D:\A-Projects\UrbanHeatIsland\PressureTem'
# shp_file = r'D:\A-Projects\Urban Heat Island\shp\Bayarea.shp'
# output_folder = r'D:\A-Projects\Urban Heat Island\Bayarea_Tif'

# # 创建输出文件夹（如果不存在）
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # 读取shapefile
# shapefile = gpd.read_file(shp_file)
# geoms = shapefile.geometry.values  # 获取几何形状

# # 获取所有tif文件路径
# tif_files = glob.glob(os.path.join(tif_folder, '*.tif'))

# for tif_file in tif_files:
#     with rasterio.open(tif_file) as src:
#         # 创建tif文件的边界框
#         tif_bounds = box(*src.bounds)
        
#         # 检查shapefile的几何形状是否与tif文件重叠
#         if not shapefile.intersects(tif_bounds).any():
#             print(f"{tif_file} is not match the bay area")
#             continue

#         try:
#             # 掩膜提取
#             out_image, out_transform = mask(src, geoms, crop=True)
#             out_meta = src.meta.copy()

#             # 更新元数据
#             out_meta.update({
#                 "driver": "GTiff",
#                 "height": out_image.shape[1],
#                 "width": out_image.shape[2],
#                 "transform": out_transform
#             })

#             # 检查掩膜后文件是否为空
#             if out_image.any():
#                 output_path = os.path.join(output_folder, os.path.basename(tif_file))
#                 with rasterio.open(output_path, "w", **out_meta) as dest:
#                     dest.write(out_image)
#             else:
#                 print(f"{tif_file} 掩膜后为空，未输出该文件")
#         except ValueError as e:
#             print(f"{tif_file} 处理时发生错误: {e}")


import subprocess
import os
import glob
from osgeo import ogr, osr, gdal
import rasterio
from shapely.geometry import box

daytime_tif_path = r"D:\A-Projects\UrbanHeatIsland\PressureTem"
shapefile_path = r"D:\A-Projects\Urban Green Space\ChinaAdminDivisonSHP-master\Bayarea.shp"
output_path = r"D:\A-Projects\UrbanHeatIsland\Bayarea_Tif"

os.makedirs(output_path, exist_ok=True)

# Function to get the SRS of the shapefile using osgeo
def get_shapefile_srs(shapefile):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(shapefile, 0)  # 0 means read-only
    layer = dataset.GetLayer()
    spatial_ref = layer.GetSpatialRef()
    return spatial_ref.ExportToWkt()

# Get SRS from shapefile
shapefile_srs = get_shapefile_srs(shapefile_path)
if shapefile_srs is None:
    raise ValueError("Cannot determine the SRS of the shapefile")
print(f"Shapefile SRS: {shapefile_srs}")

# Read the shapefile using ogr
driver = ogr.GetDriverByName("ESRI Shapefile")
shapefile = driver.Open(shapefile_path, 0)
layer = shapefile.GetLayer()

# Process each TIF file
for tif_file in glob.glob(os.path.join(daytime_tif_path, "*.tif")):
    try:
        with rasterio.open(tif_file) as src:
            # Create the bounding box of the TIF file
            tif_bounds = box(*src.bounds)

            # Convert tif_bounds to an OGR geometry
            tif_bounds_geom = ogr.CreateGeometryFromWkt(tif_bounds.wkt)

            # Check if the TIF file intersects with the shapefile geometry
            intersects = False
            for feature in layer:
                geom = feature.GetGeometryRef()
                if geom.Intersects(tif_bounds_geom):
                    intersects = True
                    break
            if not intersects:
                print(f"{tif_file} does not intersect with the shapefile area. Skipping.")
                continue

        print(f"Processing {tif_file}")
        output_file = os.path.join(output_path, os.path.basename(tif_file))
        crop_command = [
            'gdalwarp',
            '-of', 'GTiff',
            '-cutline', shapefile_path,
            '-crop_to_cutline',
            '-s_srs', shapefile_srs,
            '-t_srs', shapefile_srs,
            tif_file, output_file
        ]
        print(f"Running command: {' '.join(crop_command)}")
        subprocess.run(crop_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing file {tif_file}: {e}")
        continue

print("Cropping completed.")

