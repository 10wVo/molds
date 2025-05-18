import cv2
import numpy as np

# 读取图像
image = cv2.imread("C:\\Users\Administrator\Desktop\molds\picture_yellow\yellow_Image_230201412409631.jpg")

# 检查图像是否加载成功
if image is None:
    print("图像加载失败")
    exit()

# 将图像从 BGR 转换为 HSV 色彩空间
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 输入要查找的像素点坐标 (x, y)，注意索引从 0 开始
x = 382  # 这里输入你想查找的 x 坐标
y = 342  # 这里输入你想查找的 y 坐标

# 获取该点的 HSV 值
hsv_value = hsv_image[y, x]

# 打印 HSV 值
print(f"像素点 ({x}, {y}) 的 HSV 值是: H={hsv_value[0]}, S={hsv_value[1]}, V={hsv_value[2]}")

# 如果需要，您可以通过 cv2.imshow() 显示图像，以便确认目标点
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
