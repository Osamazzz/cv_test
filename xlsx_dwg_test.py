import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
df = pd.read_excel(r'./xlsx/110kV自忠站-14_dwg.xlsx')
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'  # 选择你系统上安装的中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
matplotlib.rcParams['font.size'] = 10  # 设置全局字体大小
matplotlib.use('Qt5agg')

# 检查必要的列是否存在
required_columns = {'Layer', 'ID', 'ParentID', 'Point'}
if not required_columns.issubset(df.columns):
    missing_columns = required_columns - set(df.columns)
    raise ValueError(f"Missing required columns: {missing_columns}")


def clean_and_split_points(start_points, end_points):
    # 去掉方括号，并按空格分隔，转换为浮动数字
    start_points_cleaned = start_points.str.replace('[', '', regex=False).str.replace(']', '', regex=False)
    end_points_cleaned = end_points.str.replace('[', '', regex=False).str.replace(']', '', regex=False)

    # 分割字符串并转换为浮动数字，忽略 z 坐标（如果只关心 x 和 y）
    start_points_cleaned = start_points_cleaned.str.split(' ', expand=True).astype(float)
    end_points_cleaned = end_points_cleaned.str.split(' ', expand=True).astype(float)

    # 只取前两列：x 和 y，忽略 z
    start_points_cleaned = start_points_cleaned.iloc[:, :2]
    end_points_cleaned = end_points_cleaned.iloc[:, :2]

    # 设置列名为 x, y
    start_points_cleaned.columns = ['x', 'y']
    end_points_cleaned.columns = ['x', 'y']

    return start_points_cleaned, end_points_cleaned


# 创建图形窗口
plt.figure(figsize=(40, 20))

# 获取所有唯一的图层
layers = df['Layer'].unique()

# 为每个图层绘制多段线
for layer in layers:
    # 筛选出当前图层的数据
    layer_data = df[df['Layer'] == layer]
    # print(layer_data['End Point'])

    # 按 ParentID 分组，并为每个分组绘制多段线
    for parent_id, group in layer_data.groupby('ParentID'):
        # 如果 StartPoint 或 EndPoint 列为空，跳过该组
        if group['Start Point'].dropna().empty or group['End Point'].dropna().empty:
            print('ok')
            continue  # 如果 'StartPoint' 或 'EndPoint' 列为空，跳过该组
        print(group['End Point'])
        # 清理并拆分 StartPoint 和 EndPoint 列
        start_points_cleaned, end_points_cleaned = clean_and_split_points(group['Start Point'], group['End Point'])
        print(start_points_cleaned)

        # 在绘制时添加 label，每个图层仅添加一次标签
        plt.plot(start_points_cleaned['x'], start_points_cleaned['y'], marker='o', label=layer)  # 绘制 StartPoint
        plt.plot(end_points_cleaned['x'], end_points_cleaned['y'], marker='o')  # 绘制 EndPoint

        # 连接第一个和最后一个点，形成封闭的形状
        if len(start_points_cleaned) > 0 and len(end_points_cleaned) > 0:
            first_point = start_points_cleaned.iloc[0]
            last_point = end_points_cleaned.iloc[-1]
            plt.plot([first_point['x'], last_point['x']], [first_point['y'], last_point['y']], 'ro-')

# 设置图形标题和坐标轴标签
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('CAD Drawing with All Layers')
plt.axis('equal')  # 设置 x 和 y 轴的比例相同
# plt.legend()  # 添加图例，显示各个图层
plt.show()
