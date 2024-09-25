import json
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import shape
import matplotlib.ticker as mticker

# 从本地读取 GeoJSON 文件
with open('内蒙古自治区.json', 'r') as file:
    geojson_data = json.load(file)

# 设置等面积投影
equal_area_crs = ccrs.AlbersEqualArea(central_longitude=110.0, central_latitude=40.0)
fig = plt.figure(figsize=(12, 6))

# 创建子图
ax = fig.add_subplot(1, 1, 1, projection=equal_area_crs)
ax.set_extent([97.0, 126.0, 37.0, 53.0], crs=ccrs.PlateCarree())

# 绘制多边形
for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'Polygon':
        polygon = shape(feature['geometry'])  # 创建 shapely 多边形对象
        ax.add_geometries([polygon], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='blue', linewidth=2)

# 只显示下方和左侧的经纬度

# 只显示下方和左侧的经纬度
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color="none")
gl.top_labels = False  # 关闭顶部经度标签
gl.right_labels = False  # 关闭右侧纬度标签gl.top_labels = False  # 关闭顶部经度标签
gl.right_labels = False  # 关闭右侧纬度标签
gl.xlocator = mticker.FixedLocator([100, 110, 120])  # 设置经度刻度
gl.ylocator = mticker.FixedLocator([40, 45, 50])  # 设置纬度刻度
gl.rotate_labels = False  # 不旋转标签

# 设置刻度标签的样式
gl.xlabel_style = {'rotation': 0}  # X轴刻度标签横向
gl.ylabel_style = {'rotation': 90}  # Y轴刻度标签竖向

# 设置标题
ax.set_title('Polygons from GeoJSON', fontsize=24)

# 保存图像
plt.savefig("data/polygons.png")
plt.show()
