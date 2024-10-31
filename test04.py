import ezdxf

# 读取 DXF 文件
doc = ezdxf.readfile("./dxf/drawing14-28.dxf")
msp = doc.modelspace()

# 遍历所有实体
for entity in msp:
    # 检查文本实体
    if entity.dxftype() in ('TEXT', 'MTEXT'):
        if '' in entity.dxf.text or 'Scale' in entity.dxf.text:
            msp.delete_entity(entity)  # 删除比例尺文本
    # 检查线条和块实体
    elif entity.dxftype() in ('LINE', 'POLYLINE', 'INSERT'):
        if entity.dxftype() == 'INSERT' and entity.dxf.name.startswith('TABLE_'):
            msp.delete_entity(entity)  # 删除表格块
        # 可以添加更多条件以过滤表格
    # 其他可能的条件
    elif entity.dxftype() == 'LWPOLYLINE':
        # 根据其他条件进一步过滤
        pass

# 检查图层并删除
for layer in doc.layers:
    if "TABLE" in layer.dxf.name:  # 使用 dxf.name 获取图层名
        msp.delete_layer(layer.dxf.name)

# 保存修改后的 DXF 文件
doc.saveas("./dxf/drawing14-28_new.dxf")
