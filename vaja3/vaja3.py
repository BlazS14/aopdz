import cv2
import numpy as np
from random import *

height = None
width = None

#function that recieves a 2d array and convertes it to an image where each unique value represents a different color
def convert_to_color_image(arr):
    height, width = arr.shape
    colors = np.empty((0,3),dtype=np.uint8)
    for i in range(arr.min()-1,arr.max()):
        colors = np.append(colors,[[randint(0,255),randint(0,255),randint(0,255)]])
    image = np.empty((height,width,3),dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            image[i,j] = colors[arr[i,j]]
    return image

def sort(img):
    global height
    global width
    coordinates = np.indices((height, width))
    flattened_image = img.flatten()
    flattened_coordinates = coordinates.reshape(2, -1).T

    combined_array = np.concatenate((flattened_image[:, np.newaxis],flattened_coordinates), axis=1)
    return combined_array[combined_array[:, 0].argsort()]

def get_ng(x,y, img):
    height, width = img.shape
    neighbors = np.empty((0,3),dtype=np.int32)
    
    for i in range(-1, 2):
        for j in range(-1, 2):
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
                if pp[0] > 0:
                    if p[0] == inqueue or (p[0] == wshed and flag == True):
                          arr[p[1],p[2]] = pp[0]          
                    elif p[0] > 0 and p[0] != pp[0]:
                        arr[p[1],p[2]] = wshed
                        flag = False           
                elif pp[0] == wshed:
                    if p[0] == inqueue:
                        arr[p[1],p[2]] = wshed
                        flag = True
                elif pp[0] == mask:
                    arr[pp[1],pp[2]] = inqueue
                    fifo = np.append(fifo, [pp],axis=0)
        for p in (sortedgray[sortedgray[:,0] == h]):
            if arr[p[1],p[2]] == mask:
                current_label = current_label + 1
                arr[p[1],p[2]] = current_label
                fifo = np.append(fifo, [[arr[p[1],p[2]],p[1],p[2]]],axis=0)
                while len(fifo) != 0:
                    pp = fifo[0]
                    fifo = fifo[1:]
                    for ppp in get_ng(pp[1],pp[2],arr):
                        if ppp[0] == mask:
                            fifo = np.append(fifo, [ppp],axis=0)
                            arr[ppp[1],ppp[2]] = current_label
    
    print(arr)
    return arr

image = cv2.imread("C:\\Users\\GTAbl\\Desktop\\AOPDZ-Vaja3\\untitled.jpg")

image = cv2.resize(image, (960, 540))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
height, width = gray.shape


gray = sort(gray)

arr = flood(gray)


# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(arr,cv2.MORPH_OPEN,kernel, iterations = 2)
# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)
# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)



arr = convert_to_color_image(arr)




cv2.imshow("win2",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("win1",arr)
cv2.waitKey(0)
cv2.destroyAllWindows()