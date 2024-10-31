import cv2
import matplotlib.pyplot as plt
import numpy as np

# 1. 读取图像
image = cv2.imread('./output_image.png')

# 2. 转为灰度图
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. 边缘检测
edges = cv2.Canny(gray_image, 120, 255)

# 4. 创建白色背景图像
output_image = np.ones_like(gray_image) * 255  # 白色背景

# 5. 将边缘绘制在白色背景上
output_image[edges == 255] = 0  # 将边缘位置设为黑色

# 6. 可视化结果
plt.figure(figsize=(10, 8), dpi=600)
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(output_image, cmap='gray', vmin=0, vmax=255)  # 确保只使用黑白色调
plt.axis('off')
plt.title('Detected Edges')

plt.show()
