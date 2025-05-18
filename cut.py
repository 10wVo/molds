'''
裁剪图片
'''
import cv2
import os


def cut_images(folder_path, cut_img_path, x, y, w, h):
    os.makedirs(cut_img_path, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"无法读取图片: {img_path}. 跳过该文件。")
            continue
            
        cropped_img = img[y:y+h, x:x+w]
        output_path = os.path.join(cut_img_path, os.path.splitext(filename)[0] + ".jpg")
        cv2.imwrite(output_path, cropped_img)
        print(f"已保存裁剪后的图片: {output_path}")


if __name__ == "__main__":
    folder_path = "C:\\Users\\Administrator\\Desktop\\molds\\picture"
    cut_img_path = "C:\\Users\\Administrator\\Desktop\\molds\\picture_aftercut"
    x, y, w, h = 1020, 53, 1021, 1022
    cut_images(folder_path, cut_img_path, x, y, w, h)
    