#coding:utf-8
import os 
import xml.dom.minidom
import numpy as np
import cv2
import math
import shutil 
from tqdm import tqdm

def makexml(img_path,xml_path,des_path,crop_path):
    
    provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', 'O']
    ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']
    files=os.listdir(img_path)
    src_xml = xml_path
    for f in tqdm(files):
        p_num = [int(cha) for cha in f.split("-")[4].split("_")]
        plate_name = provinces[p_num[0]]+alphabets[p_num[1]]+ads[p_num[2]]+ads[p_num[3]]+ads[p_num[4]]+ads[p_num[5]]+ads[p_num[6]]

        ordinate = f.split("-")[2].split("_")
        xmin,ymin = int(ordinate[0].split("&")[0]),int(ordinate[0].split("&")[1])
        xmax,ymax = int(ordinate[1].split("&")[0]),int(ordinate[1].split("&")[1])

        img_pa=os.path.join(img_path,f)
        img=cv2.imread(img_pa)
        img_h,img_w,_= img.shape

        xml_file=os.path.join(des_path,plate_name+'.xml')
        img_des = os.path.join(des_path,plate_name+'.jpg')
        DomTree = xml.dom.minidom.parse(src_xml)
        annotation = DomTree.documentElement

        filename = annotation.getElementsByTagName("filename")
        filename[0].childNodes[0].data = plate_name
        path = annotation.getElementsByTagName("path")
        path[0].childNodes[0].data = img_des
        width = annotation.getElementsByTagName("width")
        width[0].childNodes[0].data = img_w
        height = annotation.getElementsByTagName("height")
        height[0].childNodes[0].data = img_h

        plates = annotation.getElementsByTagName('object')
        for p in plates:
                
            box = p.getElementsByTagName('bndbox')[0]
            x1 =box.getElementsByTagName('xmin')
            x1[0].childNodes[0].data = xmin
            y1 = box.getElementsByTagName('ymin')
            y1[0].childNodes[0].data = ymin
            x2 = box.getElementsByTagName('xmax')
            x2[0].childNodes[0].data = xmax
            y2 = box.getElementsByTagName('ymax')
            y2[0].childNodes[0].data = ymax

            crop_img = img[ymin:ymax,xmin:xmax]
            if len(crop_img)==0:
                print(f)
            cv2.imwrite(crop_path+'/'+plate_name+".jpg",crop_img)#
        with open(xml_file,'w') as fh:
            DomTree.writexml(fh)
        shutil.move(img_pa,img_des)

                
                
            
	
if __name__=='__main__':

    img_path = './plate'
    xml_path = './train0.xml'
    des_path = './plate2'
    crop_path = './crop'
    dire = os.listdir(img_path)
    for di in dire:
        img_p = os.path.join(img_path,di)
        makexml(img_p,xml_path,des_path,crop_path)
