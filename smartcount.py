# smartcount.py
#
# Improved algorithm to count eggs
# Uses edge/shape detection to separate the image into single eggs
# and clumps of eggs. The single eggs are counted and the average
# size computed is used to estimate the number in the remaining clumps.
#
# Written by Scott Foster

import cv2 as cv
import numpy as np
import sys

# preprocess the image with otsu binarization and erosion/dilation
def preprocess(image):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _,otsu = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    otsu = cv.bitwise_not(otsu)
    kernel = np.ones((2,2), np.uint8)
    dilated = cv.dilate(otsu, kernel, iterations=1)
    eroded = cv.erode(dilated, kernel, iterations=1)
    return eroded

# implements the algorithm to count the eggs. image is an OpenCV Matrix
def count(image):
    # find contours
    pp = preprocess(image)
    cont, _ = cv.findContours(pp, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    fgsize = np.sum(pp == 255)
    totalsize = np.sum(pp == 255) + np.sum(pp == 0)

    # find upper and lower limit of egg size
    hulls = []
    for i, c in enumerate(cont):
        # find approx poly fits and sort out the ones
        # without concave corners (likely single eggs)
        approx = cv.approxPolyDP(c, 0.02 * cv.arcLength(c, True), True)
        if cv.isContourConvex(approx):
            hulls.append(cv.contourArea(c))
    hulls.sort()
    median = hulls[int(len(hulls) / 1.8)]
    lower = median * 0.5
    upper = median * 1.5

    # draw all contours larger than upper bound on the mask
    mask = np.zeros(img.shape[:2], dtype=img.dtype)
    for c in cont:
        if cv.contourArea(c) > upper:
            x, y, w, h = cv.boundingRect(c)
            cv.drawContours(mask, [c], 0, (255), -1)

    # apply the mask to the original image
    clumps = cv.bitwise_and(pp,pp, mask= mask)
    totalclumpsize = np.sum(clumps == 255)
    singles = cv.subtract(pp, clumps)

    # get contours of clumps/small
    clumpcont, _ = cv.findContours(clumps, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    singlescont, _ = cv.findContours(singles, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    # compute average size of single eggs
    avg = 0
    sclen = 0
    for sc in singlescont:
        if cv.contourArea(sc) > lower:
            sclen += 1
            avg += cv.contourArea(sc)
    if sclen > 0:
        avg = avg / sclen

    # count is the number of singles + estimated count of clumps
    count = sclen + round(totalclumpsize / avg, 0)
    return int(count)

if __name__ == "__main__":
    path = sys.argv[1]
    img = cv.imread(path)
    print(count(img))
