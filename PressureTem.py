import os
import numpy as np
from osgeo import gdal

# Extract RTP subdataset values
def extract_rtp_values(dataset):
    rtp_data = dataset.ReadAsArray()
    return rtp_data

# Calculate air temperature pixel by pixel using the formula
def estimate_air_temperature(rtp_data, pressures, target_pressure):
    height, width = rtp_data.shape[1:]
    estimated_temperatures = np.full((height, width), np.nan)  # Initialize to NaN

    for i in range(height):
        for j in range(width):
            # Extract temperature profile data for the pixel
            listtoarray = rtp_data[:, i, j]
            Validity_index = np.where(listtoarray != -32768)

            if len(Validity_index[0]) >= 2:  # Ensure there are at least two valid values
                p1 = pressures[Validity_index[0][-1]]
                t1 = (listtoarray[Validity_index[0][-1]] * 0.01) - 273.16
                p2 = pressures[Validity_index[0][-2]]
                t2 = (listtoarray[Validity_index[0][-2]] * 0.01) - 273.16

                if p1 != p2:
                    t_target = t1 + (t2 - t1) * (target_pressure - p1) / (p2 - p1)
                    estimated_temperatures[i, j] = t_target / 3 + 55
                else:
                    estimated_temperatures[i, j] = np.nan  # Pressure difference is zero, cannot calculate
            else:
                estimated_temperatures[i, j] = np.nan  # No valid values, set to NaN

    return estimated_temperatures

# Save result as a new TIF file
def save_to_tif(data, input_tif_path, output_tif_path):
    input_dataset = gdal.Open(input_tif_path)
    driver = gdal.GetDriverByName("GTiff")

    output_dataset = driver.Create(
        output_tif_path,
        input_dataset.RasterXSize,
        input_dataset.RasterYSize,
        1,  # Single band
        gdal.GDT_Float32,
    )
    output_dataset.SetGeoTransform(input_dataset.GetGeoTransform())
    output_dataset.SetProjection(input_dataset.GetProjection())
    band = output_dataset.GetRasterBand(1)
    band.WriteArray(data)
    band.SetNoDataValue(np.nan)  # Set NoData value to NaN
    output_dataset.FlushCache()
    print(f"Estimated air temperatures have been saved to {output_tif_path}")

# Main function
def main(rtp_tif_dir, output_folder):
    pressures = [5, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 400, 500, 620, 700, 780, 850, 920, 950, 1000]
    target_pressures = [700, 780, 850, 920, 950, 1000]
    
    # Get a list of all TIF files in the directory
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
                    
                    for target_pressure in target_pressures:
                        estimated_air_temperature = estimate_air_temperature(rtp_data, pressures, target_pressure)
                        output_tif_path = os.path.join(output_folder, f'rtp8_{target_pressure}hPa_{file_name}')
                        save_to_tif(estimated_air_temperature, rtp_tif_path, output_tif_path)
                
                except Exception as e:
                    print(f"An error occurred while processing file {rtp_tif_path}: {e}")

# Input TIF directory path and output TIF folder path
rtp_tif_dir = r"D:\A-Projects\UrbanHeatIsland\GeoTiff"
output_folder = r"D:\A-Projects\UrbanHeatIsland\PressureTem"

# Create output folder (if it doesn't exist)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Run the main function
if __name__ == "__main__":
    main(rtp_tif_dir, output_folder)
