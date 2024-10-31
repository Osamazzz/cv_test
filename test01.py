import cv2
import matplotlib.pyplot as plt
import numpy as np

# 1. 读取图像
image = cv2.imread('./output_image.png')

# 2. 如果图像已经是黑白的，直接使用
binary_image = cv2.bitwise_not(image)  # 反转颜色（如果需要）

# 3. 边缘检测
edges = cv2.Canny(binary_image, 120, 255)

# 4. 形态学处理：膨胀和腐蚀
kernel = np.ones((2, 2), np.uint8)  # 使用更大的内核
morphed_image = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# 5. 提取轮廓
contours, _ = cv2.findContours(morphed_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# 6. 创建白色背景图像
output_image = np.ones_like(binary_image) * 255  # 白色背景

# 7. 筛选和绘制墙体轮廓
for contour in contours:
    # 计算轮廓面积
    area = cv2.contourArea(contour)
    if area > 100:  # 设定最小面积以过滤小轮廓
        cv2.drawContours(output_image, [contour], -1, 0, 1)  # 绘制黑色轮廓

# 8. 可视化结果
plt.figure(figsize=(10, 8), dpi=600)
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(output_image, cmap='gray', vmin=0, vmax=255)  # 确保只使用黑白色调
plt.axis('off')
plt.title('Detected Walls')

plt.show()
