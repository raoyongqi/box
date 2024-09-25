import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.patches import Wedge, Rectangle
from cartopy import config

def create_pie_series_on_map(capitals, global_max_pl_value):
    # 创建地图
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # 绘制海岸线
    # ax.coastlines()
    
    # 开启经纬度网格
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False,color = "None")

    # 添加经纬度标签格式
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}°E' if x >= 0 else f'{-x:.1f}°W'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}°N' if y >= 0 else f'{-y:.1f}°S'))

    for capital in capitals:
        # 获取每个 capital 的中心
        center = capital['center']
        pl_values = list(capital['PL'].values())

        # 绘制主矩形
        size = 4
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
            wedge = Wedge(small_centers[i], 1, start_angle, end_angle, color='red', alpha=0.8,
                          transform=ccrs.PlateCarree())  # 添加 transform 以匹配地图投影
            ax.add_patch(wedge)
            start_angle = end_angle  # 更新开始角度

    # 设置坐标轴比例和显示范围
    ax.set_aspect('equal')
    ax.set_xlim(0, 100)  # 根据数据调整范围
    ax.set_ylim(0, 100)  # 根据数据调整范围
    ax.axis('on')  # 显示坐标轴

    plt.title('Pie Series on Map with Longitude and Latitude')
    plt.show()

# 示例数据
capitals = [
    {'site': 'Capital 1', 'center': (20, 20), 'PL': {'PL_1': 10, 'PL_2': 20, 'PL_3': 30, 'PL_4': 15}},
    {'site': 'Capital 2', 'center': (60, 60), 'PL': {'PL_1': 15, 'PL_2': 5, 'PL_3': 25, 'PL_4': 10}},
]

global_max_pl_value = 20
create_pie_series_on_map(capitals, global_max_pl_value)
