import ezdxf
import matplotlib.pyplot as plt

# 读取 DXF 文件
doc = ezdxf.readfile("./dxf/drawing14-28_new.dxf")
msp = doc.modelspace()

# 创建高分辨率图像
plt.figure(figsize=(10, 8), dpi=600)

# 遍历所有实体
for entity in msp:
    if entity.dxftype() == 'Line' or entity.dxftype() == 'Polyline':
        start = entity.dxf.start
        end = entity.dxf.end
        plt.plot([start.x, end.x], [start.y, end.y], color='black')
    elif entity.dxftype() == 'CIRCLE':
        circle = plt.Circle(entity.dxf.center, entity.dxf.radius, fill=False, color='black')
        plt.gca().add_artist(circle)
plt.axis('off')  # 隐藏坐标轴
plt.axis('equal')
plt.title('DXF to Image')
# plt.savefig('output_image.png', dpi=600)  # 保存为高分辨率图像
plt.show()
