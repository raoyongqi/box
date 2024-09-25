import json
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import shape
from matplotlib.patches import Wedge, Rectangle, Patch

# 从本地读取 GeoJSON 文件
with open('内蒙古自治区.json', 'r') as file:
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
inner_mongolia_capitals = [capital for capital in capitals if capital['province'] == '内蒙古自治区']
global_mongolia_capitals = [capital for capital in capitals]

# 计算 global_max_pl_value
global_max_pl_value = calculate_global_max_pl_value(global_mongolia_capitals)

# 设置等面积投影
equal_area_crs = ccrs.AlbersEqualArea(central_longitude=110.0, central_latitude=40.0)
fig = plt.figure(figsize=(12, 6))

# 创建子图
ax = fig.add_subplot(1, 1, 1, projection=equal_area_crs)
ax.set_extent([97.0, 126.0, 37.0, 53.0], crs=ccrs.PlateCarree())

# 绘制 GeoJSON 多边形
for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'Polygon':
        polygon = shape(feature['geometry'])  # 创建 shapely 多边形对象
        ax.add_geometries([polygon], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='blue', linewidth=2)

# 只显示下方和左侧的经纬度
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color="none")
gl.top_labels = False  # 关闭顶部经度标签
gl.right_labels = False  # 关闭右侧纬度标签

# 绘制扇形图
create_pie_series_on_map(inner_mongolia_capitals, global_max_pl_value, ax)

# 设置标题
ax.set_title('Polygons from GeoJSON with Pie Series', fontsize=24)

# 添加图例
legend_elements = [
    Patch(facecolor='none', edgecolor='black', label='site'),
    Wedge((0, 0), 0.15, 0, 360, color='red', alpha=0.8, label='PL')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=12, title='Legend')

# 保存图像
plt.savefig("data/polygons_with_pie_series.png")
plt.show()
