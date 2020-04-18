# basic watershed segmenting
# !!!!!!!!!!!!!!!!!(failed experiment)

import cv2 as cv
import numpy as np
import sys

# -.-.-.-.-.-.-.-.-.-. functions -.-.-.-.-.-.-.-.-.-.-.-.-.-
def grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def threshold(image):
    timg = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv.THRESH_BINARY, 255, 5)
    return cv.bitwise_not(timg)

def dilate_erode(image):
    ksize = 3
    diterations = 1
    eiterations = 1
    kernel = np.ones((ksize, ksize), np.uint8)
    dimg = cv.dilate(image, kernel, iterations=diterations)
    eimg = cv.erode(dimg, kernel, iterations=eiterations)
    return eimg 
# find a single egg in the image and count the white pixels
# TODO: method to find the single egg
def single_egg_pix(image):
    return np.sum(image == 255)

# count the number of white pixels in the whole image
def count_white_pix(image):
    return np.sum(image == 255)

def segment(image):
    # remove noise from the image
    kernel = np.ones((3,3), np.uint8)
    opening = cv.morphologyEx(image, cv.MORPH_OPEN, kernel, iterations=2)
    bg = cv.dilate(opening, kernel, iterations=3)
    dt = cv.distanceTransform(opening, cv.DIST_L2, 5)
    cv.imshow('d',dt)
    cv.waitKey()
    r, fg = cv.threshold(dt, 0.7*dt.max(),255,0)
    #cv.imshow('fg', fg)
    #cv.imshow('bg', bg)
    #cv.waitKey()
    fgu = np.uint8(fg)
    unk = cv.subtract(bg, fgu)
    return dt

def count(img_path):
    # manually counted 222 eggs in the frame of eggs1.png
    # open image
    img = cv.imread(img_path)

    processed = dilate_erode(threshold(grayscale(img)))
    count = count_white_pix(processed)

    # manually cropping out a single egg
    x = 366
    y = 74
    h = 45
    w = 64
    simg = processed[y:y+h, x:x+w]
    singlecount = single_egg_pix(simg)
    
    return int(count / singlecount), processed
    #print('whole img pixels :  ' + str(count))
    #print('                    ------')
    #print('single egg pixels : ' + str(singlecount))
    #print('egg estimate: ' + str(count / singlecount))

# -.-.-.-.-.-.-.-.-.-. main test -.-.-.-.-.-.-.-.-.-.-.-.-.-

img = cv.imread('../../../data/images/1.png')
img = cv.imread('water_coins.jpg')
preproc = dilate_erode(threshold(grayscale(img)))
proc = segment(img)
#cv.imshow('eggs2', preproc)
#cv.imshow('eggs3', proc)
#cv.waitKey()
