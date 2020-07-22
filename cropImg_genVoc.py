import os 
from lxml.etree import ElementTree
from xml.dom import minidom
import numpy as np
import cv2
import random
from tqdm import tqdm
import shutil

def gen_voc(parse_info,save_path,file_name):
    
    w,h = parse_info['size']
    objects = parse_info['objects']

    doc = minidom.Document()

    annotation = doc.createElement("annotation")
    doc.appendChild(annotation)
    folder = doc.createElement('folder')
    folder.appendChild(doc.createTextNode('wuxi'))
    annotation.appendChild(folder)

    filename = doc.createElement('filename')
    filename.appendChild(doc.createTextNode(file_name))
    annotation.appendChild(filename)

    source = doc.createElement('source')
    database = doc.createElement('database')
    database.appendChild(doc.createTextNode("Unknown"))
    source.appendChild(database)

    annotation.appendChild(source)

    size = doc.createElement('size')
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(str(w)))
    size.appendChild(width)
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode(str(h)))
    size.appendChild(height)
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode(str(3)))
    size.appendChild(depth)
    annotation.appendChild(size)

    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode("0"))
    annotation.appendChild(segmented)

    for obj in objects:
    
        name = obj['name']
        x_min = obj['xmin']
        y_min = obj['ymin']
        x_max = obj['xmax']
        y_max = obj['ymax']

        object = doc.createElement('object')
        nm = doc.createElement('name')
        nm.appendChild(doc.createTextNode(name))
        object.appendChild(nm)
        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode("Unspecified"))
        object.appendChild(pose)
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode("1"))
        object.appendChild(truncated)
        difficult = doc.createElement('difficult')
        difficult.appendChild(doc.createTextNode("0"))
        object.appendChild(difficult)
        bndbox = doc.createElement('bndbox')
        xmin = doc.createElement('xmin')
        xmin.appendChild(doc.createTextNode(str(x_min)))
        bndbox.appendChild(xmin)
        ymin = doc.createElement('ymin')
        ymin.appendChild(doc.createTextNode(str(y_min)))
        bndbox.appendChild(ymin)
        xmax = doc.createElement('xmax')
        xmax.appendChild(doc.createTextNode(str(x_max)))
        bndbox.appendChild(xmax)
        ymax = doc.createElement('ymax')
        ymax.appendChild(doc.createTextNode(str(y_max)))
        bndbox.appendChild(ymax)
        object.appendChild(bndbox)
        annotation.appendChild(object)
    with open(save_path, 'w') as x:
        x.write(doc.toprettyxml())
    x.close()
def ImgCrop(xml_path,crop_size=(1600,1200),style="include"):

    xmls = os.listdir(xml_path)
    crop_img_path = xml_path.replace("label","crop_img")
    crop_xml_path = xml_path.replace("label","crop_xml")
    for f in xmls:
        xml_src = xml_path+"/"+f
        img_src = xml_path.replace('label','source')+"/"+f.replace('xml','png')
        tree = ElementTree()
        tree.parse(xml_src)
        size = tree.find("size")
        w = int(size.find("width").text)
        h = int(size.find("height").text)
        obj_nodes = tree.findall("object")
        nums = len(obj_nodes)
        w_l = w
        w_r = 0
        h_t = h
        h_b = 0
        
        w_c = 0
        h_c = 0
        parse_info = {'objects':[],'size':(w,h)}
        for node in obj_nodes:
            name = node.find("name").text
            bndbox = node.find("bndbox")
            xmin = int(float(bndbox.find("xmin").text))
            ymin = int(float(bndbox.find("ymin").text))
            xmax = int(float(bndbox.find("xmax").text))
            ymax = int(float(bndbox.find("ymax").text))
            if xmin<w_l:
                w_l=xmin
            if xmax>w_r:
                w_r=xmax
            if ymin<h_t:
                h_t=ymin
            if ymax>h_b:
                h_b=ymax
            w_c += (xmin+xmax)/2
            h_c += (ymin+ymax)/2
            loc = {'xmin':xmin,'ymin':ymin,'xmax':xmax,'ymax':ymax,'name':name} 
            parse_info['objects'].append(loc)
        img = cv2.imread(img_src)
        ww = w_r-w_l
        hh = h_b-h_t
        w_c /=nums
        h_c /=nums
        w_c = min(max((w_r+w_l)/2,crop_size[0]/2+4),w-crop_size[0]/2-4) if (ww<=crop_size[0]) else min(max(w_c,crop_size[0]/2+4),w-crop_size[0]/2-4)
        h_c = min(max((h_t+h_b)/2,crop_size[1]/2+4),h-crop_size[1]/2-4) if (hh<=crop_size[1]) else min(max(h_c,crop_size[1]/2+4),h-crop_size[1]/2-4)
        lw = int(w_c-crop_size[0]/2)
        th = int(h_c-crop_size[1]/2)
        crop_img = img[th:th+crop_size[1],lw:lw+crop_size[0]]
        cv2.imwrite(crop_img_path+'/'+f.replace('xml','png'),crop_img)
        for loc in parse_info['objects']:
            loc['xmin'] -= lw
            loc['xmax'] -= lw
            loc['ymin'] -= th
            loc['ymax'] -= th
        save_path = crop_xml_path+"/"+f
        gen_voc(parse_info,save_path,f.split('.')[0])
if __name__ == "__main__":
    xml_path = 'wxn/small/label'
    ImgCrop(xml_path)
