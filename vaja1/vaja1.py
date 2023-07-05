from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

def jp2_to_nparray(filename):
    img = Image.open(filename)
    img.load()
    data = np.asarray(img, dtype="int32")
    data = data
    return data


def nparray_to_tiff(data, filename):
    #data = data / 255
    #data = data/np.max(data)
    #data = data * 255
    img = Image.fromarray(data)
    img.save(filename)
    
    
#get the smallest jp2 image resolution in the folder and return it
def get_smallest_resolution(folder):
    files = os.listdir(folder)
    files = [f for f in files if f.endswith(".jp2")]
    min_x = 100000000
    min_y = 100000000
    for f in files:
        img = Image.open(folder + "/" + f)
        img.load()
        data = np.asarray(img, dtype="int32")
        if data.shape[0] < min_x:
            min_x = data.shape[0]
        if data.shape[1] < min_y:
            min_y = data.shape[1]
    return min_x, min_y
    
#as an argument recieve an array of jp2 images, find the biggest image in the array and resize all the images in the array to the size of the biggest image. then save them back to the array and return the array
def resize_images(data):
    #find the biggest image in the array
    max_x = 0
    max_y = 0
    for i in range(len(data)):
        if data[i].shape[0] > max_x and data[i].shape[1] > max_y:
            max_x = data[i].shape[0]
            max_y = data[i].shape[1]
                
    
    for i in range(len(data)):
        img = Image.fromarray(data[i])
        img = img.resize((max_x,max_y),Image.Resampling.LANCZOS)
        data[i] = np.asarray(img, dtype="int32")
    return data    




#show the user a folder selection dialog and parse all .jp2 files in the folder using jp2_to_nparray
def folder_to_nparray():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    resx,resy = get_smallest_resolution(folder_selected)
    files = os.listdir(folder_selected)
    files = [f for f in files if f.endswith(".jp2")]
    data = []
    for f in files:
        data.append(jp2_to_nparray(folder_selected + "/" + f))
        
    #resize the images in data to the size of the biggest image in the data array

    return data

#compute the EVI index from the data and save it as a tiff image
def compute_evi(data):
    evi = (data[7]-data[3])/(data[7]+6*data[3]-7.5*data[1]+1)
    nparray_to_tiff(evi,"evi.tiff")

#compute the NDVI index from the data and save it as a tiff image
def compute_ndvi(data):
    ndvi = (data[7]-data[3])/(data[7]+data[3])
    nparray_to_tiff(ndvi,"ndvi.tiff")

#compute the GNDVI index from the data and save it as a tiff image
def compute_gndvi(data):
    gndvi = (data[7]-data[2])/(data[7]+data[2])
    nparray_to_tiff(gndvi,"gndvi.tiff")
    
#compute the MSI index from the data and save it as a tiff image
def compute_msi(data):
    msi = data[11]/data[7]
    nparray_to_tiff(msi,"msi.tiff")
    
#compute the NDWI index from the data and save it as a tiff image
def compute_ndwi(data):
    ndwi = (data[2]-data[11])/(data[2]+data[11])
    nparray_to_tiff(ndwi,"ndwi.tiff")

#compute the NDBI index from the data and save it as a tiff image
def compute_ndbi(data):
    ndbi = (data[10]-data[7])/(data[10]+data[7])
    nparray_to_tiff(ndbi,"ndbi.tiff")
    
#compute the NDMI index from the data and save it as a tiff image
def compute_ndmi(data):
    ndmi = (data[8]-data[7])/(data[8]+data[7])
    nparray_to_tiff(ndmi,"ndmi.tiff")

def compute_savi(data,L):
    ndvi = (data[7]-data[3])/(data[7]+data[3]+L)*(1+L)
    nparray_to_tiff(ndvi,"savi.tiff")

def compute_nbr(data):
    ndvi = (data[7]-data[11])/(data[7]+data[11])
    nparray_to_tiff(ndvi,"nbr.tiff")

def compute_uai(data):
    ndvi = (data[11]-data[7])/(data[11]+data[7])
    nparray_to_tiff(ndvi,"uai.tiff")

def compute_bsi(data):
    ndvi = (data[12]-data[7])/(data[12]+data[7])
    nparray_to_tiff(ndvi,"bsi.tiff")

data = folder_to_nparray()

data = resize_images(data)

compute_evi(data)
compute_gndvi(data)
compute_msi(data)
compute_ndbi(data)
compute_ndmi(data)
compute_ndvi(data)
compute_ndwi(data)

compute_savi(data,2) #SAVI is a modification of NDVI that accounts for soil brightness. It introduces the parameter L to adjust for soil background reflectance.
compute_nbr(data) #NBR is often used to assess burn severity and monitor post-fire vegetation recovery. It compares the near-infrared (NIR) and shortwave infrared (SWIR) bands.
compute_uai(data) #UAI is used to identify urban areas by comparing the shortwave infrared (SWIR) and near-infrared (NIR) bands.
compute_bsi(data) #BSI is used to identify areas of bare soil by comparing the shortwave infrared (SWIR1) and near-infrared (NIR) bands.
