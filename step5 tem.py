# import os
# import numpy as np
# from osgeo import gdal

# # 提取RTP子数据集的值
# def extract_rtp_values(dataset):
#     rtp_data = dataset.ReadAsArray()
#     return rtp_data

# # 根据公式计算逐像元气温
# def estimate_air_temperature(rtp_data, pressures, target_pressure):
#     height, width = rtp_data.shape[1:]
#     estimated_temperatures = np.full((height, width), np.nan)  # 初始化为NaN

#     for i in range(height):
#         for j in range(width):
#             # 提取像元的气温剖面数据
#             listtoarray = rtp_data[:, i, j]
#             Validity_index = np.where(listtoarray != -32768)

#             if len(Validity_index[0]) >= 2:  # 确保有至少两个有效值
#                 p1 = pressures[Validity_index[0][-1]]
#                 t1 = (listtoarray[Validity_index[0][-1]] * 0.01) - 273.16
#                 p2 = pressures[Validity_index[0][-2]]
#                 t2 = (listtoarray[Validity_index[0][-2]] * 0.01) - 273.16

#                 if p1 != p2:
#                     t_target = t1 + (t2 - t1) * (target_pressure - p1) / (p2 - p1)
#                     estimated_temperatures[i, j] = t_target / 3 + 55
#                 else:
#                     estimated_temperatures[i, j] = np.nan  # 气压差为零，无法计算
#             else:
#                 estimated_temperatures[i, j] = np.nan  # 如果没有有效值，则设为NaN

#     return estimated_temperatures

# # 保存结果为新的tif文件
# def save_to_tif(data, input_tif_path, output_tif_path):
#     input_dataset = gdal.Open(input_tif_path)
#     driver = gdal.GetDriverByName("GTiff")

#     output_dataset = driver.Create(
#         output_tif_path,
#         input_dataset.RasterXSize,
#         input_dataset.RasterYSize,
#         1,  # 单波段
#         gdal.GDT_Float32,
#     )
#     output_dataset.SetGeoTransform(input_dataset.GetGeoTransform())
#     output_dataset.SetProjection(input_dataset.GetProjection())
#     band = output_dataset.GetRasterBand(1)
#     band.WriteArray(data)
#     band.SetNoDataValue(np.nan)  # 设置NoData值为NaN
#     output_dataset.FlushCache()
#     print(f"Estimated air temperatures have been saved to {output_tif_path}")

# # 主函数
# def main(rtp_tif_path, output_folder):
#     pressures = [5, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 400, 500, 620, 700, 780, 850, 920, 950, 1000]
#     target_pressures = [700, 780, 850, 920, 950, 1000]
    
#     rtp_dataset = gdal.Open(rtp_tif_path)
#     rtp_data = extract_rtp_values(rtp_dataset)
    
#     for target_pressure in target_pressures:
#         estimated_air_temperature = estimate_air_temperature(rtp_data, pressures, target_pressure)
#         output_tif_path = os.path.join(output_folder, f'rtp8_{target_pressure}hPa.tif')
#         save_to_tif(estimated_air_temperature, rtp_tif_path, output_tif_path)

# # 输入tif文件路径和输出tif文件夹路径
# rtp_tif_path = r"D:\A-Projects\UrbanHeatIsland\GeoTiff"
# output_folder = r"D:\A-Projects\UrbanHeatIsland\PressureTem"

# # 创建输出文件夹（如果不存在）
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # 运行主函数
# if __name__ == "__main__":
#     main(rtp_tif_path, output_folder)


import os
import re
import numpy as np
from osgeo import gdal

# 提取RTP子数据集的值
def extract_rtp_values(dataset):
    rtp_data = dataset.ReadAsArray()
    return rtp_data

# 根据公式计算逐像元气温
def estimate_air_temperature(rtp_data, pressures, target_pressure):
    height, width = rtp_data.shape[1:]
    estimated_temperatures = np.full((height, width), np.nan)  # 初始化为NaN

    for i in range(height):
        for j in range(width):
            # 提取像元的气温剖面数据
            listtoarray = rtp_data[:, i, j]
            Validity_index = np.where(listtoarray != -32768)

            if len(Validity_index[0]) >= 2:  # 确保有至少两个有效值
                p1 = pressures[Validity_index[0][-1]]
                t1 = (listtoarray[Validity_index[0][-1]] * 0.01) - 273.16
                p2 = pressures[Validity_index[0][-2]]
                t2 = (listtoarray[Validity_index[0][-2]] * 0.01) - 273.16

                if p1 != p2:
                    t_target = t1 + (t2 - t1) * (target_pressure - p1) / (p2 - p1)
                    estimated_temperatures[i, j] = t_target / 3 + 55
                else:
                    estimated_temperatures[i, j] = np.nan  # 气压差为零，无法计算
            else:
                estimated_temperatures[i, j] = np.nan  # 如果没有有效值，则设为NaN

    return estimated_temperatures

# 保存结果为新的tif文件
def save_to_tif(data, input_tif_path, output_tif_path):
    input_dataset = gdal.Open(input_tif_path)
    driver = gdal.GetDriverByName("GTiff")

    output_dataset = driver.Create(
        output_tif_path,
        input_dataset.RasterXSize,
        input_dataset.RasterYSize,
        1,  # 单波段
        gdal.GDT_Float32,
    )
    output_dataset.SetGeoTransform(input_dataset.GetGeoTransform())
    output_dataset.SetProjection(input_dataset.GetProjection())
    band = output_dataset.GetRasterBand(1)
    band.WriteArray(data)
    band.SetNoDataValue(np.nan)  # 设置NoData值为NaN
    output_dataset.FlushCache()
    print(f"Estimated air temperatures have been saved to {output_tif_path}")

# 提取日期信息
def extract_date_from_filename(filename):
    match = re.search(r'A(\d{7})', filename)
    if match:
        date_str = match.group(1)
        year = "20" + date_str[1:3]
        day_of_year = date_str[3:6]
        return f"{year}{day_of_year}"
    return None

# 主函数
def main(rtp_tif_dir, output_folder):
    pressures = [5, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 400, 500, 620, 700, 780, 850, 920, 950, 1000]
    target_pressures = [700, 780, 850, 920, 950, 1000]

    # 处理所有TIF文件
    processed_dates = {}
    for root, _, files in os.walk(rtp_tif_dir):
        for file_name in files:
            if file_name.endswith('.tif'):
                rtp_tif_path = os.path.join(root, file_name)
                print(f"Processing file: {rtp_tif_path}")

                try:
                    rtp_dataset = gdal.Open(rtp_tif_path)
                    if rtp_dataset is None:
                        print(f"Failed to open file: {rtp_tif_path}")
                        continue

                    rtp_data = extract_rtp_values(rtp_dataset)
                    date_str = extract_date_from_filename(file_name)

                    if date_str:
                        if date_str not in processed_dates:
                            processed_dates[date_str] = 0
                        processed_dates[date_str] += 1
                        suffix = f"_{processed_dates[date_str]}" if processed_dates[date_str] > 1 else ""

                        for target_pressure in target_pressures:
                            output_tif_path = os.path.join(output_folder, f'{target_pressure}hPa_{date_str}{suffix}.tif')
                            estimated_air_temperature = estimate_air_temperature(rtp_data, pressures, target_pressure)
                            save_to_tif(estimated_air_temperature, rtp_tif_path, output_tif_path)
                
                except Exception as e:
                    print(f"An error occurred while processing file {rtp_tif_path}: {e}")

# 输入tif文件路径和输出tif文件夹路径
rtp_tif_dir = r"D:\A-Projects\UrbanHeatIsland\GeoTiff"
output_folder = r"D:\A-Projects\UrbanHeatIsland\PressureTem"

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 运行主函数
if __name__ == "__main__":
    main(rtp_tif_dir, output_folder)
