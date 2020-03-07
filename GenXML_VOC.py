#coding:utf8
import os 
import xml.etree.ElementTree as ET
from lxml.etree import Element, SubElement, tostring, ElementTree
from xml.dom.minidom import parseString
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm
num = 0
def modifyxml(path,des,img_p):
    xmls = os.listdir(path)
    for f in tqdm(xmls):
        xml_src = path+"/"+f
        xml_des = des+'/'+f
        img = img_p+"/"+f[:-4]+".jpg"
        image = cv2.imread(img)
        h,w = image.shape[:2]
        doc = ET.parse(xml_src)
        root = doc.getroot()
        frame = root.find("frame")
        root.remove(frame)
        folder = Element("folder")
        folder.text = "JPEGImages"
        root.append(folder)
        filename = Element("filename")
        filename.text = f
        root.append(filename)

        size = Element("size")
        width = Element("width")
        width.text = str(w)
        height = Element("height")
        height.text = str(h)
        depth = Element("depth")
        depth.text = "3"
        size.append(width)
        size.append(height)
        size.append(depth)
        root.append(size)

        doc.write(xml_des)

def genxml(path,des,img_p):
    xmls = os.listdir(path)
    for f in tqdm(xmls):
        xml_src = path+"/"+f
        xml_des = des+'/'+f
        img = img_p+"/"+f[:-4]+".jpg"
        image = cv2.imread(img)
        h,w = image.shape[:2]
        
        tree = ElementTree()
        tree.parse(xml_src)
        obj_nodes = tree.findall("object")
           
        node_root = Element('annotation')
        node_folder = SubElement(node_root, 'folder')
        node_folder.text = "JPEGImages"

        node_filename = SubElement(node_root, 'filename')
        node_filename.text = f
        
        node_source = SubElement(node_root, 'source')
        node_source_database = SubElement(node_source, 'database')
        node_source_database.text = "VOC2007Data"

        node_size = SubElement(node_root, 'size')
           
        node_width = SubElement(node_size, 'width')
        node_width.text = str(w)
           
        node_height = SubElement(node_size, 'height')
        node_height.text = str(h)
           
        node_depth = SubElement(node_size, 'depth')
        node_depth.text = '3'
        
        for node in obj_nodes:
            node_root.append(node)
        xml = tostring(node_root,pretty_print=True)
        dom = parseString(xml)
        with open(xml_des,'w') as f:
            dom.writexml(f)
        
            
                
            
	
if __name__=='__main__':

    path = 'Annotations'
    des = 'labels'
    img_path = 'JPEGImages'
    genxml(path,des,img_path)



         
        
    
    
