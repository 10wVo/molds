import cv2
import os
import numpy as np

# 读取图像
image = cv2.imread('input_image.jpg', cv2.IMREAD_GRAYSCALE)

# 检查图像是否成功加载
if image is None:
    print("图像加载失败")
    exit()

# 创建一个结构元素，通常用矩形或者椭圆形
kernel = np.ones((5, 5), np.uint8)  # 这里用5x5的矩形结构元素

# 对图像进行膨胀操作
dilated_image = cv2.dilate(image, kernel, iterations=1)

# 对膨胀后的图像进行腐蚀操作
eroded_image = cv2.erode(dilated_image, kernel, iterations=1)

# 显示原图、膨胀后的图像和腐蚀后的图像
cv2.imshow('Original Image', image)
cv2.imshow('Dilated Image', dilated_image)
cv2.imshow('Eroded Image', eroded_image)

# 保存膨胀和腐蚀后的图像
cv2.imwrite('dilated_image.jpg', dilated_image)
cv2.imwrite('eroded_image.jpg', eroded_image)

# 等待键盘事件
cv2.waitKey(0)
cv2.destroyAllWindows()


"""
1:
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([40, 255, 255])

2:
"""