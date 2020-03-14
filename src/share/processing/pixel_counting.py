# basic processing test
# grayscale -> thresholding -> dilate -> erode
# -> count white pixels in whole image and divide by
#    number of white pixels in a single egg
#
# NOTE: still need to find a way to single out a lone egg to
#       count the pixels, however this is surpisingly accurate
#       when done manually on the one test image we have
#
# Written by Scott Foster

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
    ksize = 4
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

def count(img_path):
    # manually counted 222 eggs in the frame of eggs1.png
    # open image
    img = cv.imread(img_path)

    processed = dilate_erode(threshold(grayscale(img)))
    #cv.imshow('eggs', processed)
    count = count_white_pix(processed)

    # manually cropping out a single egg
    x = 366
    y = 74
    h = 45
    w = 64
    simg = processed[y:y+h, x:x+w]
    singlecount = single_egg_pix(simg)
    
    return int(count / singlecount)
    #print('whole img pixels :  ' + str(count))
    #print('                    ------')
    #print('single egg pixels : ' + str(singlecount))
    #print('egg estimate: ' + str(count / singlecount))

    #cv.waitKey()


# -.-.-.-.-.-.-.-.-.-. main test -.-.-.-.-.-.-.-.-.-.-.-.-.-

print(count(sys.argv[1]))
