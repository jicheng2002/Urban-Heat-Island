import os
import glob
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def read_raster(file_path):
    dataset = gdal.Open(file_path)
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()
    geotransform = dataset.GetGeoTransform()
    return array, geotransform

def plot_raster(ax, data, geotransform, title, cmap, vmin, vmax):
    x_min = geotransform[0]
    x_max = x_min + geotransform[1] * data.shape[1]
    y_max = geotransform[3]
    y_min = y_max + geotransform[5] * data.shape[0]

    extent = [x_min, x_max, y_min, y_max]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.OCEAN, edgecolor='black')
    im = ax.imshow(data, origin='upper', extent=extent, cmap=cmap, vmin=vmin, vmax=vmax, transform=ccrs.PlateCarree())
    ax.set_title(title, fontsize=8)
    plt.colorbar(im, ax=ax, orientation='horizontal', fraction=0.046, pad=0.04)

# Directory containing the TIFF files
tif_folder = r'D:\A-Projects\UrbanHeatIsland\MonthlyMeanTemperature'
output_folder = r'D:\A-Projects\UrbanHeatIsland\Plots'

os.makedirs(output_folder, exist_ok=True)

# Collect all TIFF files
tif_files = glob.glob(os.path.join(tif_folder, "*.tif"))

# Define pressure levels and months (for readability)
pressure_levels = sorted(set(int(os.path.basename(f).split('hPa_mean_')[0]) for f in tif_files), reverse=True)
pressure_levels = [f'{p}hPa' for p in pressure_levels]

months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Temperature adjustments for each month
temperature_adjustments = {
    'January': 5, 'February': 6, 'March': 7, 'April': 8, 'May': 9, 'June': 10,
    'July': 10, 'August': 9, 'September': 8, 'October': 7, 'November': 6, 'December': 5
}

# Create subplots
n_pressure_levels = len(pressure_levels)
n_months = len(months)
fig, axs = plt.subplots(n_pressure_levels, n_months, figsize=(30, 20), subplot_kw={'projection': ccrs.PlateCarree()})
fig.subplots_adjust(hspace=0.4, wspace=0.4)

# Plot each raster in the corresponding subplot
for pressure_idx, pressure in enumerate(pressure_levels):
    # Determine the common temperature range for the current pressure level
    vmin, vmax = float('inf'), float('-inf')
    for month_idx in range(n_months):
        month_str = f"{month_idx + 1:02d}"  # Convert month index to two-digit string
        file_pattern = f"{pressure}_mean_{month_str}.tif"
        matching_files = [f for f in tif_files if os.path.basename(f) == file_pattern]
        
        if matching_files:
            file_path = matching_files[0]
            data, _ = read_raster(file_path)
            # Adjust temperatures according to the month
            data = data + temperature_adjustments[months[month_idx]]
            vmin = min(vmin, np.nanmin(data))
            vmax = max(vmax, np.nanmax(data))
    
    for month_idx, month in enumerate(months):
        month_str = f"{month_idx + 1:02d}"  # Convert month index to two-digit string
        # Find the corresponding file
        file_pattern = f"{pressure}_mean_{month_str}.tif"
        matching_files = [f for f in tif_files if os.path.basename(f) == file_pattern]
        
        if matching_files:
            file_path = matching_files[0]
            data, geotransform = read_raster(file_path)
            # Adjust temperatures according to the month
            data = data + temperature_adjustments[month]
            ax = axs[pressure_idx, month_idx]
            plot_raster(ax, data, geotransform, '', cmap='inferno', vmin=vmin, vmax=vmax)
            ax.set_title('')

            # Set month labels at the top
            if pressure_idx == 0:
                ax.set_title(month, fontsize=16, fontweight='bold')
            
            # Set pressure level labels on the left
            if month_idx == 0:
                ax.annotate(pressure, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 5, 0),
                            xycoords=ax.yaxis.label, textcoords='offset points',
                            size=16, ha='right', va='center', rotation=0, fontweight='bold')

# Save the plot
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'Temperature_Monthly_Pressure_Adjusted.jpeg'), dpi=300)
plt.show()

