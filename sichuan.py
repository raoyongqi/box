import json
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import shape
from matplotlib.patches import Wedge, Rectangle, Patch

# 从本地读取 GeoJSON 文件
with open('四川省.json', 'r', encoding='utf-8') as file:
    geojson_data = json.load(file)

# 计算 global_max_pl_value 函数
def calculate_global_max_pl_value(capitals):
    max_value = 0
    for capital in capitals:
        pl_values = list(capital['PL'].values())
        max_value = max(max_value, *pl_values)  # 更新最大值
    return max_value

# 创建绘图函数
def create_pie_series_on_map(capitals, global_max_pl_value, ax):
    for capital in capitals:
        center = capital['center']
        pl_values = list(capital['PL'].values())

        # 绘制主矩形
        size = 0.6  # 矩形大小
        rect = Rectangle((center[0] - size / 2, center[1] - size / 2), size, size,
                         linewidth=1, edgecolor='black', facecolor='none',
                         transform=ccrs.PlateCarree())
        ax.add_patch(rect)

        # 计算小正方形中心
        small_square_size = size / 2
        small_centers = [
            (center[0] - small_square_size / 2, center[1] - small_square_size / 2),  # 左下
            (center[0] + small_square_size / 2, center[1] - small_square_size / 2),  # 右下
            (center[0] - small_square_size / 2, center[1] + small_square_size / 2),  # 左上
            (center[0] + small_square_size / 2, center[1] + small_square_size / 2),  # 右上
        ]

        # 绘制扇形
        start_angle = -90
        for i, value in enumerate(pl_values):
            if i >= len(small_centers):
                break
            end_angle = start_angle + (value / global_max_pl_value) * 360
            wedge = Wedge(small_centers[i], 0.15, start_angle, end_angle, color='red', alpha=0.8,
                          transform=ccrs.PlateCarree())
            ax.add_patch(wedge)
            start_angle = end_angle

# 从文件中读取 capitals 数据
import re
def load_capitals_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 使用正则表达式提取 JSON 部分
    match = re.search(r'export const capitals = (\[.*?\]);', content, re.DOTALL)
    if match:
        capitals_json = match.group(1)
        return json.loads(capitals_json)
    else:
        raise ValueError("No valid capitals data found.")

# 从文件中读取数据
file_path = 'site2.js'  # 替换为您的文件路径
capitals = load_capitals_from_file(file_path)

# 过滤出内蒙古自治区的数据
inner_mongolia_capitals = [capital for capital in capitals if capital['province'] == '四川省']
global_mongolia_capitals = [capital for capital in capitals]

# 计算 global_max_pl_value
global_max_pl_value = calculate_global_max_pl_value(global_mongolia_capitals)

# 设置等面积投影
equal_area_crs = ccrs.AlbersEqualArea(central_longitude=110.0, central_latitude=40.0)
fig = plt.figure(figsize=(12, 6))

# 创建子图
ax = fig.add_subplot(1, 1, 1, projection=equal_area_crs)
ax.set_extent([91 ,109, 25.4422, 34.2002], crs=ccrs.PlateCarree())

# 绘制多边形
for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'MultiPolygon':
        for coords in feature['geometry']['coordinates']:
            polygon = shape({'type': 'Polygon', 'coordinates': coords})  # 创建 shapely 多边形对象
            ax.add_geometries([polygon], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='gray', linewidth=2)

import matplotlib.ticker as mticker
# from cartopy.mpl.gridliner import LongitudeFormatter
# lon_formatter = LongitudeFormatter(zero_direction_label=True)
# ax.xaxis.set_major_formatter(lon_formatter)
# 只显示下方和左侧的经纬度
# 只显示下方和左侧的经纬度
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color="black")
gl.top_labels = False  # 关闭顶部经度标签
gl.right_labels = False  # 关闭右侧纬度标签gl.top_labels = False  # 关闭顶部经度标签
gl.right_labels = False  # 关闭右侧纬度标签
gl.xlocator = mticker.FixedLocator([90, 100, 110, 120])  # 设置经度刻度
gl.ylocator = mticker.FixedLocator([25,30,35,40, 45, 50])  # 设置纬度刻度
gl.rotate_labels = False  # 不旋转标签
gl.xlines = False
gl.ylines = False
# 设置刻度标签的样式
gl.xlabel_style = {'rotation': 0}  # X轴刻度标签横向
gl.ylabel_style = {'rotation': 90}  # Y轴刻度标签竖向
# 绘制扇形图
import numpy as np
# 自定义显示整10的刻度
# xticks = np.arange(100, 130, 10)  # 设定经度刻度
# yticks = np.arange(40, 60, 10)     # 设定纬度刻度
# print(yticks)
# ax.set_xticks(xticks)
# ax.set_yticks(yticks)
create_pie_series_on_map(inner_mongolia_capitals, global_max_pl_value, ax)

# 设置标题
tit = 'sichuan'
ax.set_title(f'{tit} site', fontsize=14)

# 添加图例
legend_elements = [
    Patch(facecolor='none', edgecolor='black', label='site'),
    Wedge((0, 0), 0.15, 0, 360, color='red', alpha=0.8, label='PL')
]
def add_scale_bar(ax, location, length=0.1):
    # 绘制比例尺
    scale_bar = Rectangle(location, length, 0.005, color='black', transform=ax.transAxes)
    ax.add_patch(scale_bar)
    ax.text(location[0] + length / 2, location[1] + 0.02, '100 km', ha='center', va='bottom', transform=ax.transAxes)

add_scale_bar(ax, location=(0.05, 0.05), length=0.1)

inset_border = Rectangle(
    (0.095, 0.42),  # left and bottom position of the inset (matching the inset position)
    0.3,  # width of the inset
    0.5,  # height of the inset
    linewidth=2,
    edgecolor='black',
    facecolor='none',
    transform=fig.transFigure  # Use figure coordinates for the rectangle
)

# 在主图中添加边框
ax.add_patch(inset_border)


from matplotlib.patches import FancyArrowPatch
from geo_northarrow import add_north_arrow

add_north_arrow(ax, scale=0.5, xlim_pos=0.925, ylim_pos=0.9, color='#000', text_scaler=2, text_yT=-1.25)

ax.legend(handles=legend_elements, loc='lower right', fontsize=12, title='Legend')
# 从本地读取中国的 GeoJSON 文件
with open('中华人民共和国.json', 'r', encoding='utf-8') as file:  # 确保使用正确的中国地图文件名
    china_data = json.load(file)
# 添加中国地图的插图，定义插图的轴和投影
fig.subplots_adjust(left=0)  # 设置左边距为0

ax_china_inset = fig.add_axes([0.095, 0.42, 0.4, 0.5], projection=equal_area_crs)  # [left, bottom, width, height]
ax_china_inset.set_extent([85.0, 126.0, 0, 56.0], crs=ccrs.PlateCarree())

# 绘制中国所有几何形状


# 存储内蒙古的几何数据
inner_mongolia_geom = None

# 遍历中国数据的所有几何形状
for feature in china_data['features']:
    geom = shape(feature['geometry'])
    
    # 检查 feature 的属性，判断是否为内蒙古
    if '四川省' in feature['properties']['name']:  # 假设属性中有 name 或类似的字段
        inner_mongolia_geom = geom  # 保存内蒙古的几何数据
    if  feature['properties']['name'] is '':  # 假设属性中有 name 或类似的字段
        ax_china_inset.add_geometries([geom], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='black', linewidth=2)
    else:
        # 先绘制其他区域
        ax_china_inset.add_geometries([geom], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='gray', linewidth=2)
        # print(feature['properties']['name'])

# 最后绘制内蒙古的几何数据
if inner_mongolia_geom:
    ax_china_inset.add_geometries([inner_mongolia_geom], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='red', linewidth=2)

        # print(feature['properties']['name'])
# 不显示中国地图的坐标轴
# ax_china_inset.set_title('China', fontsize=10)
ax_china_inset.axis('off')


add_scale_bar(ax_china_inset, location=(0.05, 0.05), length=0.1)
# 只绘制右边和下边的边框
# ax_china_inset.spines['top'].set_visible(False)
# ax_china_inset.spines['left'].set_visible(False)
# ax_china_inset.spines['right'].set_visible(True)  # 右边框可见
# ax_china_inset.spines['bottom'].set_visible(True)  # 下边框可见
# ax_china_inset.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False,color = "None")

# 保存图像
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

plt.subplots_adjust(wspace=0, hspace=0)
# 保存图像
plt.savefig(f"data/{tit}.png")
plt.show()
