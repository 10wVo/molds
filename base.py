'''
程序说明：
python版本: 3.11.7
Windows11
只需修改两个设置的部分，其他的尽量不要动
日期:2025.5.18
'''
import cv2
import os
import numpy as np
from cut import cut_images
from find_hsv import find_hsv_value

#————————————功能设置————————————————#
cut_picture = True #是否裁剪图片
read_picture = True #是否以第一张图片作为hsv值读取参考，关闭该功能则使用默认范围值
display_picture = True #是否显示图片


#————————————初始参数设置————————————————#
project_path = "E:\molds"#项目所在路径
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([40, 255, 255])#提取范围



#===============以下部分只要不出BUG就尽量不要修改===============#
#===============以下部分只要不出BUG就尽量不要修改===============#
#===============以下部分只要不出BUG就尽量不要修改===============#

folder_path = os.path.join(project_path,"origin_picture") #原始文件保存路径
output_image_path = os.path.join(project_path,"output")#提取后文件保存路径
if(cut_picture):
    cut_img_path = os.path.join(project_path,"picture_aftercut")#裁剪后文件保存路径
    x, y, w, h = 1020, 53, 1021, 1022
    cut_images(folder_path, cut_img_path, x, y, w, h)
    folder_path = cut_img_path
    
#读取文件夹中的指定图片，作为示例
if(read_picture):
    picture_wait_to_read = os.path.join(folder_path, "wait_to_read.jpg")
    low_x, low_y = 50, 30
    up_x, up_y = 50, 30
    lower_yellow = find_hsv_value(picture_wait_to_read, low_x, low_y, display_picture)
    upper_yellow = find_hsv_value(picture_wait_to_read, up_x, up_y, display_picture)

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.png')):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

        if img is None:
            print(f"无法读取图片: {img_path}. 跳过该文件。")
            continue

        # 如果是带有 alpha 通道的图像，分离出透明通道 (RGBA)
        if img.shape[2] == 4:
            bgr_img = img[:, :, :3]  # 提取 BGR 部分
            alpha_channel = img[:, :, 3]  # 提取 Alpha 通道
        else:
            bgr_img = img
            alpha_channel = None

        hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
        yellow_part = cv2.bitwise_and(bgr_img, bgr_img, mask=mask)

        # 如果有 alpha 通道，保留透明部分
        if alpha_channel is not None:
            # 将提取的黄色区域与 alpha 通道合并
            yellow_part_with_alpha = cv2.merge([yellow_part[:, :, 0], yellow_part[:, :, 1], yellow_part[:, :, 2], alpha_channel])
            # 保存带透明度的图片
            output_path = os.path.join(output_image_path, 'yellow_' + filename)
            cv2.imwrite(output_path, yellow_part_with_alpha)
        else:
            # 如果没有 alpha 通道，直接保存黄色区域的图片
            output_path = os.path.join(output_image_path, 'yellow_' + filename)
            cv2.imwrite(output_path, yellow_part)

        print(f"已保存黄色部分的图片: {output_path}")
        #cv2.imshow(f"Yellow part in {filename}", yellow_part)
        #cv2.waitKey(0)
cv2.destroyAllWindows()

'''
找重叠的部分，表示为红色
'''
def extract_yellow_area(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv_image,lower_yellow, upper_yellow)
    return yellow_mask


def process_images(image_folder):
    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    common_yellow_mask = None
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)
        yellow_mask = extract_yellow_area(image)
        if common_yellow_mask is None:
            common_yellow_mask = yellow_mask
        else:
            common_yellow_mask = cv2.bitwise_and(common_yellow_mask, yellow_mask)
    return common_yellow_mask


def highlight_common_yellow(image_folder, output_image_path):
    common_yellow_mask = process_images(image_folder)
    height, width = common_yellow_mask.shape
    result_image = np.ones((height, width, 3), dtype=np.uint8) * 255
    result_image[common_yellow_mask == 255] = [0, 0, 255]
    cv2.imwrite(output_image_path, result_image)
    print(f"结果已保存到：{output_image_path}")


image_folder = 'E:\\molds\\picture_aftercut'
output_image_path = 'E:\\molds\\common_yellow_highlighted.png'
highlight_common_yellow(folder_path, output_image_path)