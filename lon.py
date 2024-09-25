import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.patches import Wedge, Rectangle
import json
import re

def create_pie_series_on_map(capitals, global_max_pl_value):
    # 创建地图
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # 开启经纬度网格
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

    # 添加经纬度标签格式
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}°E' if x >= 0 else f'{-x:.1f}°W'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}°N' if y >= 0 else f'{-y:.1f}°S'))

    for capital in capitals:
        # 获取每个 capital 的中心
        center = capital['center']
        pl_values = list(capital['PL'].values())

        # 绘制主矩形
        size = 1
        rect = Rectangle((center[0] - size / 2, center[1] - size / 2), size, size,
                         linewidth=1, edgecolor='black', facecolor='none',
                         transform=ccrs.PlateCarree())
        ax.add_patch(rect)

        # 计算每个小正方形的中心点
        small_square_size = size / 2  # 每个小正方形的大小
        small_centers = [
            (center[0] - small_square_size / 2, center[1] - small_square_size / 2),  # 左下
            (center[0] + small_square_size / 2, center[1] - small_square_size / 2),  # 右下
            (center[0] - small_square_size / 2, center[1] + small_square_size / 2),  # 左上
            (center[0] + small_square_size / 2, center[1] + small_square_size / 2),  # 右上
        ]

        # 绘制扇形
        start_angle = -90  # 从顶部开始
        for i, value in enumerate(pl_values):
            if i >= len(small_centers):
                break  # 如果扇形数量超过小正方形数量则跳出
            end_angle = start_angle + (value / global_max_pl_value) * 360  # 计算结束角度
            wedge = Wedge(small_centers[i], 0.25, start_angle, end_angle, color='red', alpha=0.8,
                          transform=ccrs.PlateCarree())  # 添加 transform 以匹配地图投影
            ax.add_patch(wedge)
            start_angle = end_angle  # 更新开始角度

    # 设置坐标轴比例和显示范围
    ax.set_aspect('equal')
    ax.set_xlim(100, 140)  # 根据内蒙古的经度范围调整
    ax.set_ylim(35, 70)    # 根据内蒙古的纬度范围调整
    ax.axis('on')  # 显示坐标轴

    plt.title('Pie Series on Map for Inner Mongolia')
    plt.show()

# 从文件中读取 capitals 数据
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

# 设置文件路径
file_path = 'site2.js'  # 替换为您的文件路径

# 从文件中读取数据
capitals = load_capitals_from_file(file_path)

# 过滤出内蒙古自治区的数据
inner_mongolia_capitals = [capital for capital in capitals if capital['province'] == '内蒙古自治区']
def calculate_global_max_pl_value(capitals):
    # 计算所有 PL 值的最大值
    max_value = 0
    for capital in capitals:
        pl_values = list(capital['PL'].values())
        max_value = max(max_value, *pl_values)  # 更新最大值
    return max_value
# 设置 global_max_pl_value
global_max_pl_value = calculate_global_max_pl_value(inner_mongolia_capitals)

create_pie_series_on_map(inner_mongolia_capitals, global_max_pl_value)
