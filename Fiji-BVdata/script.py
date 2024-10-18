import sys
import imagej
import numpy as np
from BVMoudle import BVReader
import scyjava as sj

# initiate ImageJ
ij = imagej.init(r'E:\reading\BV_project\fiji-win64-pure\Fiji.app', mode='interactive')

def process_image(image_path):
    reader = BVReader()
    img = reader.loadROI("E:/ZHM_RES/sumplementary/zhm_res/CropImg_BV/config.cfg", 0, 10136, 10136 + 512, 8591, 8591 + 512, 831, 831 + 512)
    #img = reader.loadROI("E:/ZHM_RES/sumplementary/zhm_res/CropImg_BV/config.cfg", 3, 0, 12288, 0, 10240, 0, 2048)
    expand_img = np.expand_dims(img, axis=2).transpose(0, 2, 1, 3)
    processed_img = ij.py.to_imageplus(expand_img)
    while True:
        try:
            ij.ui().show(processed_img)
        except KeyboardInterrupt:
            break

# 运行图像处理
image_path = r'E:\reading\BV_project\FIG4\1.png'
process_image(image_path)
