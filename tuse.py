# strB2Q method: https://blog.csdn.net/sparkexpert/java/article/details/82749207
import re
import os
import sys
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import misc,ndimage
from scipy.spatial import ConvexHull
import os
from os import walk
from PIL import Image, ImageDraw,ImageColor
import cv2

#箱内属性
inside_prop = []
inside_prop.append('container')
inside_prop.append('slightly rusting')
inside_prop.append('serious rusting')
inside_prop.append('slightly deformation')
inside_prop.append('serious deformation')
inside_prop.append('damage floor')
inside_prop.append('oil contamination')
inside_prop.append('bad sealing')
inside_prop.append('novel object')
inside_prop.append('damage floor')

#箱体背面属性
outside_backview_prop = []
outside_backview_prop.append('background')
outside_backview_prop.append('container')
outside_backview_prop.append('slightly rusting')
outside_backview_prop.append('serious rusting')
outside_backview_prop.append('slightly deformation')
outside_backview_prop.append('serious deformation')
outside_backview_prop.append('container number')


#箱体侧面属性
outside_sideview_prop = []
outside_sideview_prop.append('background')
outside_sideview_prop.append('container')
outside_sideview_prop.append('slightly rusting')
outside_sideview_prop.append('serious rusting')
outside_sideview_prop.append('slightly deformation')
outside_sideview_prop.append('serious deformation')

#对箱内属性涂色
def inside(iterator):
    count = 0
    object_list = []
    
    is_object = True
    i = next(iterator)
    width = None
    height = None
    
    try:
     while i != None:
        tag = i.tag
        if tag == 'width':
                width = i.text
                i = next(iterator)
                tag = i.tag
        elif tag == 'height':
                height = i.text
                i = next(iterator)
                tag = i.tag
        elif tag == 'object':
            object_list.append([])
            tag = i.tag
            i = next(iterator)
            tag = i.tag
            
            while not tag == 'object':
               object_list[count].append(i)
               i = next(iterator)
               tag = i.tag
            count = count+1
        else:
            i = next(iterator)
    
    except StopIteration:
     pass
    
    print("length of object_list", len(object_list))
        
    x = []
    y = []
    o_indexs=[]
    count = 0
    
    for i in range(len(object_list)):
        for j in range(len(object_list[i])):
            if object_list[i][j].tag == 'name' and object_list[i][j].text in inside_prop:
                o_index = inside_prop.index(object_list[i][j].text)
                o_indexs.append(o_index)
                j=j+5
                x.append([])
                y.append([])
                for z in range(j,len(object_list[i])):
                    if z%2 == 1:
                        x[count].append(object_list[i][z].text)
                    else:
                        y[count].append(object_list[i][z].text)
                count = count+1
    
    return x,y,o_indexs,width,height                       

#对箱体背面属性涂色
def outside_backview(iterator):
    count = 0
    object_list = []
    
    is_object = True
    i = next(iterator)
    width = None
    height = None
    
    try:
     while i != None:
        tag = i.tag
        if tag == 'width':
                width = i.text
                i = next(iterator)
                tag = i.tag
        elif tag == 'height':
                height = i.text
                i = next(iterator)
                tag = i.tag
        elif tag == 'object':
            object_list.append([])
            tag = i.tag
            i = next(iterator)
            tag = i.tag
            
            while not tag == 'object':
               object_list[count].append(i)
               i = next(iterator)
               tag = i.tag
            count = count+1
        else:
            i = next(iterator)
    
    except StopIteration:
     pass

    print("length of object_list", len(object_list))
        
    x = []
    y = []
    o_indexs=[]
    count = 0
    
    for i in range(len(object_list)):
        for j in range(len(object_list[i])):
            if object_list[i][j].tag == 'list' and object_list[i][j].text in outside_backview_prop:
                o_index = outside_backview_prop.index(object_list[i][j].text)
                o_indexs.append(o_index)
                j=j+5
                x.append([])
                y.append([])
                for z in range(j,len(object_list[i])):
                    if z%2 == 1:
                        x[count].append(object_list[i][z].text)
                    else:
                        y[count].append(object_list[i][z].text)
                count = count+1
    
    return x,y,o_indexs,width,height 

#对箱体侧面属性涂色
def outside_sideview(iterator):
    count = 0
    object_list = []
    
    is_object = True
    i = next(iterator)
    width = None
    height = None
    
    try:
     while i != None:
        tag = i.tag
        if tag == 'width':
                width = i.text
                i = next(iterator)
                tag = i.tag
        elif tag == 'height':
                height = i.text
                i = next(iterator)
                tag = i.tag
        elif tag == 'object':
            object_list.append([])
            tag = i.tag
            i = next(iterator)
            tag = i.tag
            
            while not tag == 'object':
               object_list[count].append(i)
               i = next(iterator)
               tag = i.tag
            count = count+1
        else:
            i = next(iterator)
    
    except StopIteration:
     pass

    print("length of object_list", len(object_list))
        
    x = []
    y = []
    o_indexs=[]
    count = 0
    
    for i in range(len(object_list)):
        for j in range(len(object_list[i])):
            if object_list[i][j].tag == 'name'and object_list[i][j].text in outside_sideview_prop:
                o_index = outside_sideview_prop.index(object_list[i][j].text)
                o_indexs.append(o_index)
                j=j+5
                x.append([])
                y.append([])
                for z in range(j,len(object_list[i])):
                    if z%2 == 1:
                        x[count].append(object_list[i][z].text)
                    else:
                        y[count].append(object_list[i][z].text)
                count = count+1
    
    return x,y,o_indexs,width,height

#中英文全角半角转换
def strQ2B(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                                
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): 
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring

#根据属性涂色
def tuse(path1,photopath,prop):
     #检查文件是否存在
     if prop == None:
        print("File Type Not Found")
        return

     #读取xml文件和图片
     path1 = path1
     prop = prop
     text=open(path1).read()
     im1 = Image.open(photopath)
      
     print("original_path",path1)
     print(prop)

     #根据xml文件对图片进行分类后涂色
     parser=ET.fromstring(text)
     
     iterator1 = parser.iter()
     x = None
     y = None
     o_indexs = None
     
     width = None
     height = None
     if prop == 'inside':
         x,y,o_indexs,width,height = inside(iterator1)
     elif prop == 'outside_backview':
         x,y,o_indexs,width,height = outside_backview(iterator1)
     elif prop == 'outside_sideview':
         x,y,o_indexs,width,height = outside_sideview(iterator1)
     print(x)
     #对返回的对象进行坐标提取
     result = []
     for i in range(len(x)):
         result.append([])
         for j in range(len(x[i])):
             result[i].append(float(x[i][j]))
             result[i].append(float(y[i][j]))
     
     set_o_indexs = set(o_indexs)
     list_set_o_indexs = list(set_o_indexs)
     print(width, height)
     print(list_set_o_indexs)
    
     #将标出的区域涂为黑色,背景涂成透明色
     for i in range(len(list_set_o_indexs)):
      img = np.ones((im1._size[1], im1._size[0], 3), np.uint8)
      img=img*255
      new_path = path1[:-4]+"0"+str(list_set_o_indexs[i])+".png"
      cv2.imwrite(new_path,img)
      img1 = Image.open(new_path)
      img1 = img1.convert('RGBA')
      img1.putalpha(0)
      img11 = ImageDraw.Draw(img1)
      for j in range(len(result)):
       if o_indexs[j] == list_set_o_indexs[i]:          
        img11.polygon(result[j],fill=(0,0,0))
      img1.save(new_path)
      
      #将01属性的图标出区域涂成透明色,背景涂成白色
      if 1 in list_set_o_indexs:
       img = np.ones((im1._size[1], im1._size[0], 3), np.uint8)
       img=img*255
       new_path = path1[:-4]+"00.png"
       cv2.imwrite(new_path,img)
       img1 = Image.open(new_path)
       #将图片转换为4通道图片并增加透明度
       img1 = img1.convert('RGBA')
       img11 = ImageDraw.Draw(img1)
       for j in range(len(result)):
        if o_indexs[j] == 1:
         img11.polygon(result[j],fill=(0,0,0,0))
       img1.save(new_path)

def main():
    #文件夹路径
    folderpath = 'C:\\Users\\Administrator.SKY-20120726UJY\\Desktop\\2020_05_11-05_17\\outside'
    
    for (root, dirs, files) in os.walk(folderpath):
        for file in files:
            filetype=file.split(".")
            #读取每一个xml文件
            if filetype[1] == 'xml':
               filepath= os.path.join(root, file)
               prop = None
               if "inside" in root:
                 prop = "inside"
               elif "outside" in root:
                 if "backview" in root:
                    prop = "outside_backview"
                 elif "sideview" in root:
                    prop = "outside_sideview"
                 else:
                    print("File Type Not Found")
               #根据xml文件名称选相应图片
               try:
                photopath=root[:-3]+"JPEGImages\\"+file[:-4]+".jpg"
               except:
                photopath=root[:-3]+"JPEGImages\\"+file[:-4]+".png"
               #对每个文件涂色
               tuse(filepath,photopath,prop)
    

main()

