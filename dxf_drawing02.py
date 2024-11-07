import re

import ezdxf
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.widgets import CheckButtons

# 设置字体为支持中文的字体，例如 SimHei
matplotlib.rcParams['font.family'] = 'SimSun'  # 选择你系统上安装的中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
matplotlib.rcParams['font.size'] = 4  # 设置全局字体大小
matplotlib.use('Qt5agg')

# 读取 DXF 文件
doc = ezdxf.readfile("./dxf/zizong.dxf")
msp = doc.modelspace()

# 存储图层及其对应的实体
layers = {}
for entity in msp:
    layer_name = entity.dxf.layer  # 获取实体的图层名称
    # print(f"图层名称: {layer_name}")
    if layer_name not in layers:
        layers[layer_name] = []
    layers[layer_name].append(entity)

# 初始化图层选择
layer_names = list(layers.keys())
checked = [False] * len(layer_names)  # 默认全部勾选

# 创建图像，设置 dpi
fig, ax = plt.subplots(dpi=200)  # 设置 DPI 值
plt.subplots_adjust(left=0.2, right=0.8)  # 调整布局


# 绘制实体函数
def plot_entities():
    ax.clear()  # 清除当前图像
    for i, layer in enumerate(layer_names):
        if checked[i]:  # 根据勾选状态绘制图层
            for entity in layers[layer]:
                # print(f'dtype: {entity.dxftype()}')  # 打印实体类型
                if entity.dxftype() == 'LINE':
                    start = entity.dxf.start
                    end = entity.dxf.end
                    ax.plot([start.x, end.x], [start.y, end.y], color='black')
                elif entity.dxftype() == 'LWPOLYLINE':
                    points = entity.get_points()  # 获取 LWPOLYLINE 的顶点
                    for i in range(len(points) - 1):
                        ax.plot([points[i][0], points[i + 1][0]], [points[i][1], points[i + 1][1]], color='black', linewidth=0.5)
                elif entity.dxftype() == 'POLYLINE':
                    points = [vertex.dxf.location for vertex in entity.vertices]
                    for i in range(len(points) - 1):
                        ax.plot([points[i].x, points[i + 1].x], [points[i].y, points[i + 1].y], color='black')
                elif entity.dxftype() == 'CIRCLE':
                    circle = plt.Circle(entity.dxf.center, entity.dxf.radius, fill=False, color='black')
                    ax.add_artist(circle)
                elif entity.dxftype() == 'ARC':
                    arc = patches.Arc(entity.dxf.center, entity.dxf.radius * 2, entity.dxf.radius * 2,
                                      theta1=entity.dxf.start_angle, theta2=entity.dxf.end_angle, color='black')
                    ax.add_patch(arc)  # 使用 add_patch()
                elif entity.dxftype() == 'TEXT':
                    ax.text(entity.dxf.insert.x, entity.dxf.insert.y, entity.dxf.text, fontsize=3, color='black')
                elif entity.dxftype() == 'MTEXT':
                    ax.text(entity.dxf.insert.x, entity.dxf.insert.y, entity.dxf.text, fontsize=3, color='black')
                elif entity.dxftype() == 'INSERT':  # 处理块引用 (INSERT)
                    block_name = entity.dxf.name
                    insert_position = entity.dxf.insert
                    # print(f"块引用: {block_name}, 插入位置: {insert_position}")
                    # 获取块定义
                    block = doc.blocks.get(block_name)
                    # 遍历块定义中的实体，绘制几何图形
                    for block_entity in block:
                        # print('block_entity.dxftype:' + block_entity.dxftype())
                        if block_entity.dxftype() == 'LINE':
                            start = block_entity.dxf.start + insert_position
                            end = block_entity.dxf.end + insert_position
                            ax.plot([start.x, end.x], [start.y, end.y], color='black')
                        elif block_entity.dxftype() == 'CIRCLE':
                            circle = plt.Circle((block_entity.dxf.center.x + insert_position.x,
                                                 block_entity.dxf.center.y + insert_position.y),
                                                block_entity.dxf.radius, fill=False, color='black')
                            ax.add_artist(circle)
                        elif block_entity.dxftype() == 'ARC':
                            arc = patches.Arc(block_entity.dxf.center, block_entity.dxf.radius * 2,
                                              block_entity.dxf.radius * 2,
                                              theta1=block_entity.dxf.start_angle, theta2=block_entity.dxf.end_angle,
                                              color='black')
                            ax.add_patch(arc)  # 使用 add_patch()
                        elif block_entity.dxftype() == 'SPLINE':
                            # 获取样条曲线的离散点
                            fit_points = block_entity.fit_points  # 使用 fit_points 获取拟合点
                            for i in range(len(fit_points) - 1):
                                ax.plot([fit_points[i][0], fit_points[i + 1][0]],
                                        [fit_points[i][1], fit_points[i + 1][1]], color='black')
                        elif block_entity.dxftype() == 'MTEXT':
                            print("ok " + block_entity.dxf.text)
                            ax.text(block_entity.dxf.insert.x + insert_position[0],
                                    block_entity.dxf.insert.y + insert_position[1],
                                    re.sub(r'\\[a-zA-Z]+[^;]*;|[{}]', '', block_entity.dxf.text),
                                    fontsize=4,
                                    color='black')

    ax.set_title('DXF Layers')
    ax.axis('equal')
    ax.relim()
    ax.autoscale_view()
    plt.draw()


# 创建勾选框，调整位置和大小
check = CheckButtons(plt.axes((0.01, 0.4, 0.15, 0.5)), layer_names, checked)


# 勾选框回调函数
def label_selected(label):
    index = layer_names.index(label)
    checked[index] = not checked[index]
    plot_entities()


check.on_clicked(label_selected)

# 初始绘制所有实体
plot_entities()

# 显示图形
plt.show()
