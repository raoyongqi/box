import json
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import shape

# 从本地读取内蒙古 GeoJSON 文件
with open('内蒙古自治区.json', 'r', encoding='gbk') as file:
    inner_mongolia_data = json.load(file)

# 从本地读取中国的 GeoJSON 文件
with open('中华人民共和国.json', 'r', encoding='utf-8') as file:  # 确保使用正确的中国地图文件名
    china_data = json.load(file)

# 设置等面积投影
equal_area_crs = ccrs.AlbersEqualArea(central_longitude=110.0, central_latitude=40.0)
fig = plt.figure(figsize=(10, 10))

# 创建内蒙古的主图
ax_inner = fig.add_subplot(1, 1, 1, projection=equal_area_crs)
ax_inner.set_extent([97.0, 126.0, 37.0, 56.0], crs=ccrs.PlateCarree())  

# 绘制内蒙古所有几何形状
for feature in inner_mongolia_data['features']:
    geom = shape(feature['geometry'])
    ax_inner.add_geometries([geom], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='blue', linewidth=2)

# 不绘制内蒙古子图的坐标系
ax_inner.set_title('Inner Mongolia', fontsize=16)

# 添加中国地图的插图，定义插图的轴和投影
fig.subplots_adjust(left=0)  # 设置左边距为0

ax_china_inset = fig.add_axes([0.1, 0.36, 0.4, 0.5], projection=equal_area_crs)  # [left, bottom, width, height]
ax_china_inset.set_extent([85.0, 126.0, 0, 56.0], crs=ccrs.PlateCarree())

# 绘制中国所有几何形状


# 存储内蒙古的几何数据
inner_mongolia_geom = None

# 遍历中国数据的所有几何形状
for feature in china_data['features']:
    geom = shape(feature['geometry'])
    
    # 检查 feature 的属性，判断是否为内蒙古
    if '内蒙古自治区' in feature['properties']['name']:  # 假设属性中有 name 或类似的字段
        inner_mongolia_geom = geom  # 保存内蒙古的几何数据
    else:
        # 先绘制其他区域
        ax_china_inset.add_geometries([geom], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='green', linewidth=2)

# 最后绘制内蒙古的几何数据
if inner_mongolia_geom:
    ax_china_inset.add_geometries([inner_mongolia_geom], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='red', linewidth=2)

        # print(feature['properties']['name'])
# 不显示中国地图的坐标轴
# ax_china_inset.set_title('China', fontsize=10)
ax_china_inset.axis('off')
# ax_china_inset.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False,color = "None")

# 保存图像
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

plt.subplots_adjust(wspace=0, hspace=0)

plt.savefig("inner_mongolia_with_china_inset.png")
plt.show()
