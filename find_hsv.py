'''
选取图上两点,返回其hsv值
'''
import cv2
import numpy as np

def find_hsv_value(wait_to_read_path, x, y, display_picture):
    image = cv2.imread(wait_to_read_path)
    if image is None:
        print("图像加载失败")
        return None
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_value = hsv_image[y, x]
    
    if display_picture:
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return hsv_value




click_data = {
    "first": {"pos": None, "hsv": None, "color": (0, 255, 0)},   # 绿色标记第一次点击
    "second": {"pos": None, "hsv": None, "color": (255, 0, 0)}  # 蓝色标记第二次点击
}
current_click = 1  # 当前点击次数计数器

def mouse_callback(event, x, y, flags, param):
    global current_click, img_display
    
    if event == cv2.EVENT_LBUTTONDOWN and current_click <= 2:
        # 获取BGR颜色并转换为HSV
        bgr = img[y, x]
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        # 存储数据
        key = "first" if current_click == 1 else "second"
        click_data[key]["pos"] = (x, y)
        click_data[key]["hsv"] = hsv
        
        # 绘制标记
        cv2.circle(img_display, (x, y), 8, click_data[key]["color"], 2)
        text = f"Click{current_click}: H:{hsv[0]} S:{hsv[1]} V:{hsv[2]}"
        cv2.putText(img_display, text, (x+15, y-15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, click_data[key]["color"], 2)
        
        # 更新显示
        cv2.imshow("HSV Picker", img_display)
        current_click += 1

        # 保存到文件
        with open("hsv_values.txt", "a") as f:
            f.write(f"[Click {current_click-1}] Position: ({x}, {y}), HSV: {hsv}\n")
        
        # 两次点击后显示完成提示
        if current_click > 2:
            cv2.putText(img_display, "Selection Complete! Press ESC to exit", 
                       (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
            cv2.imshow("HSV Picker", img_display)

# 主程序
if __name__ == "__main__":
    # 读取图片
    img = cv2.imread("input.jpg")
    if img is None:
        print("Error: Failed to load image")
        exit()
    
    # 创建显示副本
    img_display = img.copy()
    
    # 创建窗口并绑定回调
    cv2.namedWindow("HSV Picker")
    cv2.setMouseCallback("HSV Picker", mouse_callback)
    
    # 显示初始图像
    cv2.imshow("HSV Picker", img_display)
    print("请依次点击两个目标位置")
    
    # 主循环
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC退出
            break
            
    # 销毁窗口
    cv2.destroyAllWindows()
    
    # 终端输出最终结果
    print("\n=== 采集结果 ===")
    print(f"第一次点击 - 位置 {click_data['first']['pos']}:")
    print(f"  H: {click_data['first']['hsv'][0]}")
    print(f"  S: {click_data['first']['hsv'][1]}")
    print(f"  V: {click_data['first']['hsv'][2]}")
    
    print(f"\n第二次点击 - 位置 {click_data['second']['pos']}:")
    print(f"  H: {click_data['second']['hsv'][0]}")
    print(f"  S: {click_data['second']['hsv'][1]}")
    print(f"  V: {click_data['second']['hsv'][2]}")