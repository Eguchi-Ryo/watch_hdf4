from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy.ma as ma

# HDFファイルのパス
modis_pre_path = "E:/reguchi/DownloadNASAData/MCD12Q1/2001.01.01/MCD12Q1.A2001001.h00v08.061.2022146024956.hdf"

# HDFファイルを開く
dataset = Dataset(modis_pre_path, 'r')

# データセット内の変数名を取得
variables = dataset.variables.keys()
print("Available variables:", variables)

# 変数のリストを取得
desired_bands = [var for var in variables if var.startswith('LC_Type1')]

# バンドのデータを辞書に保存
bands_data = {band: dataset.variables[band][:] for band in desired_bands}

# バンドデータの内容を表示
for band_name, band_data in bands_data.items():
    print(f"{band_name} data shape: {band_data.shape}")
    print(f"{band_name} data min: {band_data.min()}")
    print(f"{band_name} data max: {band_data.max()}")

# バンドデータのプロット
for band_name, band_data in bands_data.items():
    print(f"Plotting {band_name}")
    
    # バンドデータの最初のバンドを取得（データが3次元の場合、最初のインデックスを選択）
    data_to_plot = band_data[0, :, :] if band_data.ndim == 3 else band_data
    
    #masked = ma.masked_where(band_data.mask, data_to_plot)
    #masked = np.where(~band_data.mask, data_to_plot, np.nan) #マスクのみ表示（多分不要）、imshowの第一引数をmaskedに書き換える必要あり。
    # データサイズのリサイズ
    #data_to_plot = np.interp(data_to_plot, (data_to_plot.min(), data_to_plot.max()), (0, 1))  ##<- グリッドの値を(0,1)にスケーリング
    
    # 緯度・経度範囲の設定（データの範囲に合わせて調整）
    lon_min, lon_max = 0, 2399
    lat_min, lat_max = 0, 2399

    # 可視化
    fig = plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # データをプロット
    im = ax.imshow(data_to_plot, origin='upper', extent=[lon_min, lon_max, lat_min, lat_max],
                   cmap='bwr', interpolation='nearest', vmin=band_data.min(), vmax=band_data.max())

    # 地図の特徴を追加
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    #ax.add_feature(cfeature.LAND, edgecolor='black') #大陸を緑色に塗る
    #ax.add_feature(cfeature.OCEAN) #海を青色に塗る

    # カラーバーを追加
    plt.colorbar(im, ax=ax, orientation='vertical', label='Reflectance')

    # タイトルと表示
    plt.title(f'MODIS {band_name}')
    plt.show()
