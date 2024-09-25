import json
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import shape
import matplotlib.ticker as mticker

# 读取 GeoJSON 文件
with open('四川省.json', 'r', encoding='utf-8') as file:
    geojson_data = json.load(file)

# 设置等面积投影
equal_area_crs = ccrs.AlbersEqualArea(central_longitude=104.0, central_latitude=30.0)  # 中心设置为四川省
fig = plt.figure(figsize=(12, 6))

# 创建子图
ax = fig.add_subplot(1, 1, 1, projection=equal_area_crs)
ax.set_extent([96.3504, 109.3466, 25.4422, 36.2002], crs=ccrs.PlateCarree())  # 四川省的经纬度范围

# 绘制多边形
for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'MultiPolygon':
        for coords in feature['geometry']['coordinates']:
            polygon = shape({'type': 'Polygon', 'coordinates': coords})  # 创建 shapely 多边形对象
            ax.add_geometries([polygon], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='gray', linewidth=2)

# 只显示下方和左侧的经纬度
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color="none")
gl.top_labels = False  # 关闭顶部经度标签
gl.right_labels = False  # 关闭右侧纬度标签
gl.xlocator = mticker.FixedLocator([97, 100, 105, 110, 115, 120])  # 设置经度刻度
gl.ylocator = mticker.FixedLocator([30, 31, 32, 33, 34])  # 设置纬度刻度
gl.rotate_labels = False  # 不旋转标签

# 设置刻度标签的样式
gl.xlabel_style = {'rotation': 0}  # X轴刻度标签横向
gl.ylabel_style = {'rotation': 90}  # Y轴刻度标签竖向

# 设置标题
ax.set_title('四川省 Polygons from GeoJSON', fontsize=24)

# 保存图像
plt.savefig("data/polygons.png")
plt.show()
