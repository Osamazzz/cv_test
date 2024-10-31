import cv2
import numpy as np

# 1. 创建画布
canvas_width, canvas_height = 800, 600
canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255  # 白色背景

# 2. 读取图像
image = cv2.imread('output_image.png')

# 3. 调整图像大小（例如缩放到适合画布的尺寸）
scale_factor = 0.05  # 根据需要调整缩放比例
image = cv2.resize(image, (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor)))

# 4. 设定比例尺
scale_length = 100  # 比例尺长度（像素）
scale_position = (50, canvas_height - 50)  # 比例尺的起始位置

# 5. 绘制比例尺
cv2.line(canvas, scale_position, (scale_position[0] + scale_length, scale_position[1]), (0, 0, 0), 2)
cv2.putText(canvas, "100 units", (scale_position[0] + scale_length + 10, scale_position[1] + 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# 6. 将图像放到指定坐标
image_height, image_width = image.shape[:2]
image_position = (100, 50)  # 图像放置位置

# 确保图像放置在画布内
if (image_position[1] + image_height <= canvas_height) and (image_position[0] + image_width <= canvas_width):
    canvas[image_position[1]:image_position[1] + image_height,
           image_position[0]:image_position[0] + image_width] = image
else:
    print("Image is too large to fit on the canvas.")

# 7. 显示和保存结果
cv2.imshow('Canvas with Image and Scale', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('final_output.png', canvas)
