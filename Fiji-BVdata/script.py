import sys
import imagej
import numpy as np
from BVMoudle import BVReader
import scyjava as sj

# initiate ImageJ
# fiji_path = r'E:\reading\BV_project\fiji-win64-pure\Fiji.app'
fiji_path = ''
BV_config_path = 'E:/ZHM_RES/sumplementary/zhm_res/CropImg_BV/config.cfg'
level = 0
min_x = 10136
max_x = min_x + 512
min_y = 8591
max_y = min_y + 512
min_z = 831
max_z = min_z + 512

ij = imagej.init(fiji_path, mode='interactive')
def process_image():
    reader = BVReader()
    img = reader.loadROI(BV_config_path, level, min_x, max_x, min_y, max_y, min_z, max_z)
    expand_img = np.expand_dims(img, axis=2).transpose(0, 2, 1, 3)
    processed_img = ij.py.to_imageplus(expand_img)
    while True:
        try:
            ij.ui().show(processed_img)
        except KeyboardInterrupt:
            break


# load images:
process_image()
