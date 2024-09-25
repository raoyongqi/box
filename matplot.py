import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle
import numpy as np

def create_pie_series(capitals, global_max_pl_value):
    fig, ax = plt.subplots()
    
    for capital in capitals:
        # 获取每个 capital 的中心
        center = capital['center']
        pl_values = list(capital['PL'].values())

        # 绘制主矩形
        size = 32
        rect = Rectangle((center[0] - size / 2, center[1] - size / 2), size, size,
                         linewidth=1, edgecolor='black', facecolor='none')
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
            wedge = Wedge(small_centers[i], 8, start_angle, end_angle, color='red', alpha=0.8)
            ax.add_patch(wedge)
            start_angle = end_angle  # 更新开始角度

    # 设置坐标轴比例和显示范围
    ax.set_aspect('equal')
    ax.set_xlim(0, 100)  # 根据数据调整范围
    ax.set_ylim(0, 100)  # 根据数据调整范围
    ax.axis('off')  # 隐藏坐标轴

    plt.show()

# 示例数据
capitals = [
    {'site': 'Capital 1', 'center': (20, 20), 'PL': {'PL_1': 10, 'PL_2': 20, 'PL_3': 30, 'PL_4': 15}},
    {'site': 'Capital 2', 'center': (60, 60), 'PL': {'PL_1': 15, 'PL_2': 5, 'PL_3': 25, 'PL_4': 10}},
]

global_max_pl_value = 30
create_pie_series(capitals, global_max_pl_value)
