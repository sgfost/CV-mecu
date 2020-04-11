import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
from scipy.spatial import distance
import imutils

img = None
refPt = []
ruler = False
refLength = 10 #default

def mouse_sizing(event, x, y, flags, param):
    global refPt, ruler, refLength
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x,y)]
        ruler = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x,y))
        ruler = False
        refLength = distance.euclidean(refPt[0], refPt[1])
        print("[INFO] egg length set to {}".format(refLength))
        compute(False)

def initialize():
    global img
    img = cv2.imread('data/images/rice2.png')
    cv2.namedWindow('CompupaVision')
    cv2.setMouseCallback('CompupaVision', mouse_sizing)
    cv2.imshow('CompupaVision', img)

def compute(flag):
    global img, refLength
    pyr = cv2.pyrMeanShiftFiltering(img, 15,40)
    ####
    if(flag):
        cv2.imshow('CompupaVision',pyr)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    ####
    gray = cv2.cvtColor(pyr,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    if(flag):
        cv2.imshow('thresh',thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # noise removal NOT USED YET
    kernel = np.ones((3,3),np.uint8)
    cleaned = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel, iterations = 1)
    if(flag):
        cv2.imshow('cleaned',cleaned)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # compute the exact Euclidean distance from every binary
    # pixel to the nearest zero pixel, then find peaks in this
    # distance map
    D = ndimage.distance_transform_edt(cleaned)
    localMax = peak_local_max(D, indices=False,labels=cleaned,footprint=np.ones(((refLength/2).astype(int),(refLength/2).astype(int))))
    # perform a connected component analysis on the local peaks,
    # using 8-connectivity, then appy the Watershed algorithm
    markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
    labels = watershed(-D, markers, mask=cleaned)
    print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

    # loop over the unique labels returned by the Watershed
    # algorithm
    for label in np.unique(labels):
            # if the label is zero, we are examining the 'background'
            # so simply ignore it
            if label == 0:
                    continue
            # otherwise, allocate memory for the label region and draw
            # it on the mask
            mask = np.zeros(cleaned.shape, dtype="uint8")
            mask[labels == label] = 255
            # detect contours in the mask and grab the largest one
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)
            # draw a circle enclosing the object
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)
            
    # show the output image
    cv2.imshow("Output", img)
    cv2.waitKey(0)

def main():
    initialize()

if __name__ == '__main__':
    main()
    

