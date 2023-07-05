from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

def jp2_to_nparray(filename):
    img = Image.open(filename)
    img.load()
    data = np.asarray(img, dtype="int32")
    data = data+1
    return data


def nparray_to_tiff(data, filename):
    img = Image.fromarray(data.astype('uint8'))
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

#compute the NDVI index from the data and save it as a tiff image
def compute_ndvi(data):
    ndvi = (data[9]-data[5])/(data[9]+data[5])
    nparray_to_tiff(ndvi,"ndvi.tiff")
    
#compute the EVI index from the data and save it as a tiff image
def compute_evi(data):
    evi = (data[9]-data[5])/(data[9]+6*data[5]-7.5*data[3]+1)
    nparray_to_tiff(evi,"evi.tiff")

#compute the GNDVI index from the data and save it as a tiff image
def compute_gndvi(data):
    gndvi = (data[9]-data[4])/(data[9]+data[4])
    nparray_to_tiff(gndvi,"gndvi.tiff")
    
#compute the NDWI index from the data and save it as a tiff image
def compute_ndwi(data):
    ndwi = (data[4]-data[12])/(data[4]+data[12])
    nparray_to_tiff(ndwi,"ndwi.tiff")

#compute the NDBI index from the data and save it as a tiff image
def compute_ndbi(data):
    ndbi = (data[12]-data[9])/(data[12]+data[9])
    nparray_to_tiff(ndbi,"ndbi.tiff")
    
#compute the NDMI index from the data and save it as a tiff image
def compute_ndmi(data):
    ndmi = (data[10]-data[9])/(data[10]+data[9])
    nparray_to_tiff(ndmi,"ndmi.tiff")
    
#compute the MSI index from the data and save it as a tiff image
def compute_msi(data):
    msi = data[12]/data[8]
    nparray_to_tiff(msi,"msi.tiff")


data = folder_to_nparray()

data = resize_images(data)

compute_evi(data)
compute_gndvi(data)
compute_msi(data)
compute_ndbi(data)
compute_ndmi(data)
compute_ndvi(data)
compute_ndwi(data)