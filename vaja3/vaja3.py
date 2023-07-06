import cv2
import numpy as np
from random import *
from tkinter import filedialog
height = None
width = None

#function that recieves a 2d array and convertes it to an image where each unique value represents a different color
def convert_to_color_image(arr):
    height, width = arr.shape
    colors = np.empty((0,3),dtype=np.uint8)
    for i in range(arr.min(),arr.max()+2):
        colors = np.append(colors,[[randint(0,255),randint(0,255),randint(0,255)]],axis=0)
    image = np.empty((height,width,3),dtype=np.uint8)
    
    colors[0] = [0,0,0]
    for i in range(height):
        for j in range(width):
            image[i,j] = colors[arr[i,j]]
    return image
#def a function that gets a 2d array and combines similar adjacent values into one value based on a threshold
def combine_adjacent(arr, threshold):
    height, width = arr.shape
    for x in range(height):
        for y in range(width):
            if arr[x,y] == 0:
                continue
            else:
                for p in get_ng_far_no_diagonal(x,y,arr):
                    if abs(arr[x,y] - p[0]) <= threshold:
                        arr[x,y] = p[0]
    
    return arr


def sort(img):
    global height
    global width
    coordinates = np.indices((height, width))
    flattened_image = img.flatten()
    flattened_coordinates = coordinates.reshape(2, -1).T

    combined_array = np.concatenate((flattened_image[:, np.newaxis],flattened_coordinates), axis=1)
    return combined_array[combined_array[:, 0].argsort()]

def get_ng_far_no_diagonal(x,y, img):
    height, width = img.shape
    neighbors = np.empty((0,3),dtype=np.int32)

    for i in range(-2, 3):
        for j in range(-2, 3):
            if i == 0 and j == 0:
                continue
            if i == 1 and j == 1:
                continue
            if i == -1 and j == -1:
                continue
            if i == 1 and j == -1:
                continue
            if i == -1 and j == 1:
                continue
            if i == 0 and j == 0:
                continue
            if i == 2 and j == 2:
                continue
            if i == -2 and j == -2:
                continue
            if i == 2 and j == -2:
                continue
            if i == -2 and j == 2:
                continue
            nx, ny = x + i, y + j
            nx=int(nx)
            ny=int(ny)
            if 0 <= nx < height and 0 <= ny < width:
                value = img[nx, ny]
                neighbors = np.append(neighbors,[[value, nx, ny]],axis=0)
    
    
    return neighbors

def get_ng(x,y, img):
    height, width = img.shape
    neighbors = np.empty((0,3),dtype=np.int32)
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if i == 1 and j == 1:
                continue
            if i == -1 and j == -1:
                continue
            if i == 1 and j == -1:
                continue
            if i == -1 and j == 1:
                continue
            if i == 0 and j == 0:
                continue 
            nx, ny = x + i, y + j
            nx=int(nx)
            ny=int(ny)
            if 0 <= nx < height and 0 <= ny < width:
                value = img[nx, ny]
                neighbors = np.append(neighbors,[[value, nx, ny]],axis=0)
    
    return neighbors

def flood(sortedgray):
    mask = -2
    wshed = 0
    inqueue = -3
    flag = False
    current_label = 0
    fifo = np.empty((0,3),dtype=np.int32)
    
    arr = np.full((height, width), -1)
    
    for h in range(256):
        for p in (sortedgray[sortedgray[:,0] == h]):
            arr[p[1],p[2]] = mask
            pp = get_ng(p[1],p[2],arr)
            if any(pp[:,0] >= 0):
                arr[p[1],p[2]] = inqueue
                fifo = np.append(fifo, [[arr[p[1],p[2]],p[1],p[2]]],axis=0)
        
        while len(fifo) != 0:
            p = fifo[0]
            fifo = fifo[1:]
            for pp in get_ng(p[1],p[2],arr):
                if arr[pp[1],pp[2]] > 0:
                    if arr[p[1],p[2]] == inqueue or (arr[p[1],p[2]] == wshed and flag == True):
                          arr[p[1],p[2]] = arr[pp[1],pp[2]]          
                    elif arr[p[1],p[2]] > 0 and arr[p[1],p[2]] != arr[pp[1],pp[2]]:
                        arr[p[1],p[2]] = wshed
                        flag = False           
                elif arr[pp[1],pp[2]] == wshed:
                    if arr[p[1],p[2]] == inqueue:
                        arr[p[1],p[2]] = wshed
                        flag = True
                elif arr[pp[1],pp[2]] == mask:
                    arr[pp[1],pp[2]] = inqueue
                    fifo = np.append(fifo, [[arr[pp[1],pp[2]],pp[1],pp[2]]],axis=0)
        for p in (sortedgray[sortedgray[:,0] == h]):
            if arr[p[1],p[2]] == mask:
                current_label = current_label + 1
                arr[p[1],p[2]] = current_label
                fifo = np.append(fifo, [[arr[p[1],p[2]],p[1],p[2]]],axis=0)
                while len(fifo) != 0:
                    pp = fifo[0]
                    fifo = fifo[1:]
                    for ppp in get_ng(pp[1],pp[2],arr):
                        if arr[ppp[1],ppp[2]] == mask:
                            arr[ppp[1],ppp[2]] = current_label
                            fifo = np.append(fifo, [[arr[ppp[1],ppp[2]],ppp[1],ppp[2]]],axis=0)
    print(arr)
    return arr

drawingred=False # true if mouse is pressed
drawinggreen=False

#function that shows an image and lets the user drwa a rectangle on it and returns the coordinates of the rectangle
def interactive_drawing(event,x,y,flags,param):
    global ix,iy,drawingred,drawinggreen

    if event==cv2.EVENT_LBUTTONDOWN:
        drawingred=True
        ix,iy=x,y

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawingred==True:
            cv2.line(image,(ix,iy),(x,y),(0,0,255),10)
            ix=x
            iy=y
        elif drawinggreen==True:
            cv2.line(image,(ix,iy),(x,y),(0,255,0),10)
            ix=x
            iy=y
    elif event==cv2.EVENT_LBUTTONUP:
        drawingred=False
        cv2.line(image,(ix,iy),(x,y),(0,0,255),10)
        ix=x
        iy=y
    elif event==cv2.EVENT_RBUTTONDOWN:
        drawinggreen=True
        ix,iy=x,y
    elif event==cv2.EVENT_RBUTTONUP:
        drawinggreen=False
        cv2.line(image,(ix,iy),(x,y),(0,255,0),10)
        ix=x
        iy=y
    return x,y



#get the image from file selection dialog
image = cv2.imread(filedialog.askopenfilename())

#image = cv2.imread("C:\\Users\\GTAbl\\Desktop\\AOPDZ-Vaja3\\untitled.jpg")

image = cv2.resize(image, (960, 540))

cv2.namedWindow('Selection')
cv2.setMouseCallback('Selection',interactive_drawing)
while(1):
    cv2.imshow('Selection',image)
    k=cv2.waitKey(1)&0xFF
    if k==13:
        break
cv2.destroyAllWindows()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
height, width = gray.shape

gray[gray < 100] = 0

#gray[gray > 200] = 0

gray = sort(gray)

arr = flood(gray)

#arr[arr < 10000] = 0

#arr = combine_adjacent(arr, 50000)





arr = convert_to_color_image(arr)




cv2.imshow("win2",image)
cv2.imshow("win1",arr)
cv2.waitKey(0)
cv2.destroyAllWindows()
