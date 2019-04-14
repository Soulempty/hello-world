import os 
import xml.dom.minidom
import numpy as np
import cv2
import math

def crop(img_path,xml_path,des_path):
    files=os.listdir(img_path)
    files=[f for f in files if f.split('.')[1]=='jpg']
    txt=open('./plate_scale2.txt','a')
    name=open('./name2.txt','a')
    txt.write('min_len\tmax_len\tmean_len\twh_ratio\tpercentage\n')
    mean_len=[]
    wh_r=[]
    per=[]
    num=0
    for f in files:
        
        img=os.path.join(img_path,f)
        xml_file=os.path.join(xml_path,f.split('.')[0]+'.xml')
        DomTree = xml.dom.minidom.parse(xml_file)
        annotation = DomTree.documentElement
        img=cv2.imread(img)
        img_h,img_w,_= img.shape
        plates = annotation.getElementsByTagName('object')
        for p in plates:
                
            box = p.getElementsByTagName('bndbox')[0]
            x1 = box.getElementsByTagName('xmin')
            x1 = int(x1[0].childNodes[0].data)
            y1 = box.getElementsByTagName('ymin')
            y1 = int(y1[0].childNodes[0].data)
            x2 = box.getElementsByTagName('xmax')
            x2 = int(x2[0].childNodes[0].data)
            y2 = box.getElementsByTagName('ymax')
            y2 = int(y2[0].childNodes[0].data)
            w = x2 - x1
            h = y2 - y1
            rate = round(w/h,2)
            area = round(np.sqrt(w*h),2)
            percent = round(100*w*h/(img_w*img_h),2)
            min_p = min(w,h)
            max_p = max(w,h)
            mean_len.append(area)
            wh_r.append(rate)
            per.append(percent)
            txt.write(str(min_p)+'\t'+str(max_p)+'\t'+str(area)+'\t'+str(rate)+'\t'+str(percent)+'\n')
            crop_img = img[y1:y2,x1:x2]
            if len(crop_img)==0:
                print(f)
            name.write(f+' '+str(num)+'\n')
            cv2.imwrite(des_path+'/'+f,crop_img)
            num+=1
    print('mean_len',sorted(mean_len))
    print('wh_r',sorted(wh_r))
    print('per',sorted(per))
                
            
	
if __name__=='__main__':

    img_path = '/home/chao/NewSpace/CCPD/LPR/3/澳门出入境车牌'
    xml_path = '/home/chao/NewSpace/CCPD/LPR/3/澳门出入境车牌'
    plate_path = 'plate5'
    crop(img_path,xml_path,des_path)
