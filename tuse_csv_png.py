# strB2Q method: https://blog.csdn.net/sparkexpert/java/article/details/82749207
import re
import os
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import misc,ndimage
from scipy.spatial import ConvexHull
import os
from os import walk
from PIL import Image, ImageDraw,ImageColor
import cv2
import csv
import pandas as pd
import json
from xml.dom.minidom import Document
import shutil


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
    object_list = []
    o_indexs = []

    i = next(iterator)
    width = None
    height = None
    
    x=[]
    y=[]
    
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
        elif tag == 'class':
            o_indexs.append(int(i.text))
            i = next(iterator)
            i = next(iterator)
            zuobiao = i.text
            #print(isinstance(zuobiao,str))
            #print(isinstance(zuobiao,list))
            object_list.append(json.loads(zuobiao))
            i = next(iterator)
        else:
            i = next(iterator)
    except StopIteration:
     pass

    print("length of object_list", len(object_list))
    #print(object_list)
    
    for i in range(len(object_list)):
        x.append([])
        y.append([])
        for j in range(len(object_list[i])):
              #print(object_list[i][j])
              x[i].append(object_list[i][j][0])
              y[i].append(object_list[i][j][1])
    
    return x,y,o_indexs,width,height                   

#对箱体背面属性涂色
def outside_backview(iterator):

    object_list = []
    o_indexs = []

    i = next(iterator)
    width = None
    height = None
    
    x=[]
    y=[]
    
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
        elif tag == 'class':
            o_indexs.append(int(i.text))
            i = next(iterator)
            i = next(iterator)
            zuobiao = i.text
            #print(isinstance(zuobiao,str))
            #print(isinstance(zuobiao,list))
            object_list.append(json.loads(zuobiao))
            i = next(iterator)
        else:
            i = next(iterator)
    except StopIteration:
     pass

    print("length of object_list", len(object_list))

    for i in range(len(object_list)):
        x.append([])
        y.append([])
        for j in range(len(object_list[i])):
              
              #print(object_list[i][j])
              x[i].append(object_list[i][j][0])
              y[i].append(object_list[i][j][1])
    
    return x,y,o_indexs,width,height 

#对箱体侧面属性涂色
def outside_sideview(iterator):
    object_list = []
    o_indexs = []

    i = next(iterator)
    width = None
    height = None
    
    x=[]
    y=[]
    
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
        elif tag == 'class':
            o_indexs.append(int(i.text))
            i = next(iterator)
            i = next(iterator)
            zuobiao = i.text
            #print(isinstance(zuobiao,str))
            #print(isinstance(zuobiao,list))
            object_list.append(json.loads(zuobiao))
            i = next(iterator)
        else:
            i = next(iterator)
    except StopIteration:
     pass

    print("length of object_list", len(object_list))
    #print(object_list)
    
    for i in range(len(object_list)):
        x.append([])
        y.append([])
        for j in range(len(object_list[i])):
              #print(object_list[i][j])
              x[i].append(object_list[i][j][0])
              y[i].append(object_list[i][j][1])
    
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
def tuse(path1,photopath,pngpath,prop):
     print("while inside tuse method:")
     #检查文件是否存在
     if prop == None:
        print("File Type Not Found")
        return

     #读取xml文件和图片
     path1 = path1
     prop = prop
     text=open(path1,'r',encoding='utf-8')
     im1 = Image.open(photopath)
      
     print("original_path",path1)
     print(prop)
     print(pngpath)

     #根据xml文件对图片进行分类后涂色
     parser=ET.fromstring(text.read())
     
     iterator1 = parser.iter()
     x = None
     y = None
     o_indexs = None
     
     width = None
     height = None
     depth = 3
     if prop == 'inside':
         x,y,o_indexs,width,height = inside(iterator1)
     elif prop == 'outside_backview':
         x,y,o_indexs,width,height = outside_backview(iterator1)
     elif prop == 'outside_sideview':
         x,y,o_indexs,width,height = outside_sideview(iterator1)
     
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
      pngpath_new = pngpath+"0"+str(list_set_o_indexs[i])+".png"
      print(pngpath_new)
      cv2.imwrite(pngpath_new,img)
      img1 = Image.open(pngpath_new)
      img1 = img1.convert('RGBA')
      img1.putalpha(0)
      img11 = ImageDraw.Draw(img1)
      for j in range(len(result)):
       if o_indexs[j] == list_set_o_indexs[i]:          
        img11.polygon(result[j],fill=(0,0,0))
      img1.save(pngpath_new)
      
      #将01属性的图标出区域涂成透明色,背景涂成白色
      if 1 in list_set_o_indexs:
       img = np.ones((im1._size[1], im1._size[0], 3), np.uint8)
       img=img*255
       new_path = pngpath+"00.png"
       cv2.imwrite(new_path,img)
       img1 = Image.open(new_path)
       #将图片转换为4通道图片并增加透明度
       img1 = img1.convert('RGBA')
       img11 = ImageDraw.Draw(img1)
       for j in range(len(result)):
        if o_indexs[j] == 1:
         img11.polygon(result[j],fill=(0,0,0,0))
       img1.save(new_path)

#根据csv文件生成xml简单格式并调用tuse方法
def tuse_method(folderpath):
    
    for (root, dirs, files) in os.walk(folderpath):
        for file in files:
            filetype=file.split(".")
            #读取每一个xml文件
            if filetype[1] == 'csv':

               #对每个文件涂色
               filepath= os.path.join(root, file)
               #print(filepath)
               try:
                  data_frame = pd.read_csv( filepath,encoding='utf-8')
               except:
                  data_frame = pd.read_csv( filepath,encoding='gbk')
               
               c = 0
               final_result = data_frame["标注结果"].tolist()
               material_id = data_frame["文件名称"].tolist()
               
               
               
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
                    
               #对每一个图片生成xml文件并保存
               for mi, fi in zip(final_result, material_id):
                   mi = json.loads(mi)
                   fi = str(fi)  
                   point_list = []
                   
                   doc = Document()
                   dataRoot = doc.createElement("xml_file")
                   doc.appendChild(dataRoot)
                   unpack(fi,mi,dataRoot,doc)
                   xmlpath = root[:-3]+"csv\\"+str(fi)+'.xml'
                   xmlFile = open(xmlpath,'w',encoding = 'utf-8')
                   doc.writexml(xmlFile,indent='',addindent='\t',newl='\n',encoding = 'utf-8')
                   xmlFile.close()
                   c=c+1
                   #选相应图片
                   try:
                     photopath=root[:-3]+"JPEGImages\\"+str(fi)+".jpg"
                   except:
                     photopath=root[:-3]+"JPEGImages\\"+str(fi)+".png"
                   
                   #进行涂色
                   
                   try:
                      os.makedirs(root[:-3]+"PNGImages")
                   except OSError as e:
                     pass
                    
                   pngfolder = root[:-3]+"PNGImages\\"
                   csvfolder = root[:-3]+"csv\\"
                   for f in os.listdir(csvfolder):
                     if f.endswith(".png"):
                        try:
                          shutil.move(csvfolder+f,pngfolder)
                        except OSError as e:
                          print(e)
                   
                   pngpath=root[:-3]+"PNGImages\\"+str(fi)
                   
                   print(photopath)
                   print(xmlpath)
                   print(pngpath)
                   tuse(xmlpath,photopath,pngpath,prop)
                   
                   try:
                     os.remove(xmlpath)
                   except OSError as e:
                     print(e)
                   else:
                     print("xmlFile is deleted successfully")
            
#对csv文件中的数据进行涂色所需的解析   
def unpack(fi,mi,dataRoot,doc):
    if isinstance(mi,dict):
        for key, value in mi.items():
            unpack(key,value,dataRoot,doc)
    else:
            #print(isinstance(mi,dict),mi)
            #print(isinstance(mi,list),mi)
            #print(isinstance(mi,str),mi)
            #print(isinstance(mi,int),mi)
            dataElt = doc.createElement(fi)
            text=doc.createTextNode(str(mi))
            dataElt.appendChild(text)
            dataRoot.appendChild(dataElt)
            return


#对csv文件中的数据进行正确解析
def unpack_advanced(fi,mi,dataRoot,doc,prop,datasize):
    
    if isinstance(mi,dict):
        for key, value in mi.items():
            unpack_advanced(key,value,dataRoot,doc,prop,datasize)
    else:   
            if fi == "class":
                dataElt = doc.createElement("object")
                dataRoot.appendChild(dataElt)
                text=doc.createTextNode(str(mi))
                
                dataElt = doc.createElement("class")
                dataElt.appendChild(text)
                dataRoot.appendChild(dataElt)
                n = None
                if "inside"== prop:
                   n=inside_prop[int(mi)]
                elif "outside_backview"== prop:
                   n=outside_backview_prop[int(mi)]
                elif "outside_sideview"== prop:
                   n=outside_sideview_prop[int(mi)]
                else:
                    print("Property Type Not Found")
                    
                dataElt = doc.createElement("name")
                text=doc.createTextNode(n)
                dataElt.appendChild(text)
                dataRoot.appendChild(dataElt)
               
            elif fi == "name" or fi == "url":
                pass
            elif fi == "list":
                dataElt = doc.createElement("segment")
                dataRoot.appendChild(dataElt)
                for i in range(len(mi)):
  
                   x_c = doc.createElement("x"+str(i))
                   text=doc.createTextNode(str(mi[i][0]))
                   x_c.appendChild(text)
                   dataElt.appendChild(x_c)
                   
                   y_c = doc.createElement("y"+str(i))
                   text=doc.createTextNode(str(mi[i][1]))
                   y_c.appendChild(text)
                   dataElt.appendChild(y_c)
            elif fi == "width":
                dataEltt = doc.createElement("width")
                datasize.appendChild(dataEltt)
                text=doc.createTextNode(str(mi))
                dataEltt.appendChild(text)
                
            elif fi == "height":
                dataEltt = doc.createElement("height")
                datasize.appendChild(dataEltt)
                text=doc.createTextNode(str(mi))
                dataEltt.appendChild(text)
                
            elif fi == "depth":
                dataEltt = doc.createElement("depth")
                datasize.appendChild(dataEltt)
                text=doc.createTextNode(str(mi))
                dataEltt.appendChild(text)
                
                
            else:
                #print(isinstance(mi,dict),mi)
                #print(isinstance(mi,list),mi)
                #print(isinstance(mi,str),mi)
                #print(isinstance(mi,int),mi)
                dataElt = doc.createElement(fi)
                text=doc.createTextNode(str(mi))
                dataElt.appendChild(text)
                dataRoot.appendChild(dataElt)

            return
def main():
    #文件夹路径
    folderpath = 'C:\\Users\\Administrator.SKY-20120726UJY\\Desktop\\qinzhen\\outside'
    print(folderpath.split("\\")[-1])
    #用tuse_method(folderpath)遍历csv文件,生成第一版xml，并根据xml用tuse(path1,photopath,pngpath,prop)进行涂色，
    #保存png格式并存在PNG文件夹里
    tuse_method(folderpath)
    #遍历csv文件生成正确格式的xml，保存在xml文件夹里并删除csv文件夹
    for (root, dirs, files) in os.walk(folderpath):
        for file in files:
            csvfolder = root[:-3]+"csv\\"
            xmlfolder = root[:-3]+"xml\\"
            filetype=file.split(".")
            #读取每一个xml文件
            if filetype[1] == 'csv':
               #对每个文件涂色
               filepath= os.path.join(root, file)
               #print(filepath)
               try:
                  data_frame = pd.read_csv( filepath,encoding='utf-8')
               except:
                  data_frame = pd.read_csv( filepath,encoding='gbk')
               
               c = 0
               final_result = data_frame["标注结果"].tolist()
               material_id = data_frame["文件名称"].tolist()

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
                    
               #生成正确格式的xml文件
               height = None
               width = None
               for mi, fi in zip(final_result, material_id):
                   mi = json.loads(mi)
                   fi = str(fi)  
                   point_list = []
                   doc = Document()
                   dataRoot = doc.createElement("annotation")
                   doc.appendChild(dataRoot)

                   dataElt = doc.createElement("folder")
                   text=doc.createTextNode(str(folderpath.split("\\")[-1]))
                   dataElt.appendChild(text)
                   dataRoot.appendChild(dataElt)
                   
                   dataElt = doc.createElement("filename")
                   text=doc.createTextNode(str(fi)+".jpg")
                   dataElt.appendChild(text)
                   dataRoot.appendChild(dataElt)
                   
                   dataElt = doc.createElement("source")
                   
                   dataEltt = doc.createElement("database")
                   text=doc.createTextNode("Unknown")
                   dataEltt.appendChild(text)
                   dataElt.appendChild(dataEltt)
                   dataRoot.appendChild(dataElt)
                   
                   dataElt = doc.createElement("path")
                   xmlsavepath=folderpath.split("\\")[-1]+"\\"+prop+"\\JPEGImages\\"+str(fi)+'.jpg'
                   xmlsavepath=xmlsavepath.replace("\\","/")
                   text=doc.createTextNode(xmlsavepath)
                   dataElt.appendChild(text)
                   dataRoot.appendChild(dataElt)
                   
                   datasize = doc.createElement("size")
                   dataRoot.appendChild(datasize)
                   unpack_advanced(fi,mi,dataRoot,doc,prop,datasize)
                   xmlpath = root[:-3]+"csv\\"+str(fi)+'.xml'
                   xmlFile = open(xmlpath,'w',encoding = 'utf-8')
                   doc.writexml(xmlFile,indent='',addindent='\t',newl='\n',encoding = 'utf-8')
                   #xmlFile.write(doc.toprettyxml(indent = '\t'))
                   xmlFile.close()
                   
                   #创建xml文件夹并放置正确的xml文件
                   try:
                      os.makedirs(root[:-3]+"xml")
                   except OSError as e:
                     pass
                   
                   
                   for f in os.listdir(csvfolder):
                     if f.endswith(".xml"):
                        #print(root[:-3]+"csv\\")
                        try:
                          shutil.move(csvfolder+f,xmlfolder)
                        except OSError as e:
                          print(e)
    
    #创建好xml后将原来的csv文件夹删除                   
    for (root, dirs, files) in os.walk(folderpath):
            csvfolder = root[:-3]+"csv\\"
            xmlfolder = root[:-3]+"xml\\"
            try:           
              shutil.rmtree(csvfolder)
            except OSError as e:
              print(e)
            else:
              print("csvfolder is deleted successfully")

main()


        

