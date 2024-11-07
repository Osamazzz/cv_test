import ezdxf

# 读取 DXF 文件
doc = ezdxf.readfile("./dxf/woodworking-plant.dxf")
msp = doc.modelspace()

# 存储图层及其对应的实体
layers = {}
s = set()

# 遍历所有实体
for entity in msp:
    layer_name = entity.dxf.layer  # 获取实体的图层名称
    dtyp = entity.dxftype()
    s.add(dtyp)
    if layer_name not in layers:
        layers[layer_name] = []
    layers[layer_name].append(entity)

# 打印所有图层及其对应的实体数量
for layer, entities in layers.items():
    print(f"Layer: {layer}, Number of Entities: {len(entities)}")

print(s)