from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm

# HDFファイルのパス
modis_pre_path = "C:/Users/gakusei/Downloads/watch_hdf/MCD12C1.A2001001.061.2022146170409.hdf"

# HDFファイルを開く
dataset = Dataset(modis_pre_path, 'r')

# 変数を取得
lc_type1 = dataset.variables['Majority_Land_Cover_Type_1']
data_to_plot = lc_type1[:, :]  # 2次元データとして取得

# カテゴリを定義
categories = {
    0: 'Water',
    1: 'Evergreen Needleleaf Forests',
    2: 'Evergreen Broadleaf Forests',
    3: 'Deciduous Needleleaf Forests',
    4: 'Deciduous Broadleaf Forests',
    5: 'Mixed Forests',
    6: 'Closed Shrublands',
    7: 'Open Shrublands',
    8: 'Woody Savannas',
    9: 'Savannas',
    10: 'Grasslands',
    11: 'Permanent Wetlands',
    12: 'Croplands',
    13: 'Urban and Built-up Lands',
    14: 'Cropland/Natural Vegetation Mosaics',
    15: 'Permanent Snow and Ice',
    16: 'Barren or Sparsely Vegetated',
    255: 'Unclassified'
}

# カラーマップを定義
colors = plt.get_cmap('tab20', len(categories))

# ノルムと境界を定義
bounds = sorted(categories.keys())
norm = BoundaryNorm(bounds, colors.N)
print(f"Colormap limits: {bounds}")

# データの範囲と座標系の確認
lon_min, lon_max = 0, data_to_plot.shape[1]
lat_min, lat_max = 0, data_to_plot.shape[0]

print(f"Longitude range: {lon_min} to {lon_max}")
print(f"Latitude range: {lat_min} to {lat_max}")

# ユニークな値の確認
unique_values = np.unique(data_to_plot)
print(f"Unique values in data: {unique_values}")
"""
# 一部データのプロット（サンプル）
fig, ax = plt.subplots(figsize=(12, 6))
im = ax.imshow(data_to_plot[::100, ::100], origin='upper', cmap=colors, norm=norm)
plt.title('Sample Data')
plt.colorbar(im)
plt.show()
"""
# 全体データのプロット
fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# データをプロット
extent = [-180, 180, -90, 90]  
im = ax.imshow(data_to_plot, origin='upper', cmap=colors, norm=norm, interpolation='nearest', extent=extent)

# 地図の特徴を追加
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# カラーバーを追加
cbar = plt.colorbar(im, ax=ax, orientation='vertical', ticks=bounds)
cbar.ax.set_yticklabels([categories.get(b, 'Unknown') for b in bounds])

# タイトルと表示
plt.title('MODIS Land Cover Type 1')
plt.show()
