import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取图像
image = cv2.imread('4-80.png')

# 2. 转为灰度图
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. 二值化处理
_, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

# 4. 边缘检测
edges_img = cv2.Canny(binary_image, 50, 150)

# 5. 轮廓提取
bin_img, contours, hierarchy = cv2.findContours(edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# 6. 创建黑色图像用于可视化
output_image = np.zeros_like(image)

for contour in contours:
    # 计算轮廓的面积
    area = cv2.contourArea(contour)

    # 通过面积过滤出墙体和门（根据具体面积阈值进行调整）
    if area > 1000:  # 假设墙体面积大于1000
        cv2.drawContours(output_image, [contour], -1, (0, 255, 0), 2)  # 画墙体（绿色）
    elif area < 500:  # 假设门的面积小于500
        cv2.drawContours(output_image, [contour], -1, (255, 0, 0), 2)  # 画门（蓝色）

# 7. 可视化结果
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.show()
