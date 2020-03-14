import cv2
import numpy as np

# Read image
im = cv2.imread('data/images/eggs1.png', cv2.IMREAD_GRAYSCALE)
im2 = cv2.imread('15.png', cv2.IMREAD_GRAYSCALE)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 100
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 1000

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.95
    
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.0001

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else : 
	detector = cv2.SimpleBlobDetector_create(params)

detector2 = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(im)
keypoints2 = detector2.detect(im2)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
im_with_keypoints2 = cv2.drawKeypoints(im2, keypoints2, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow('Eggs', im_with_keypoints)
cv2.imshow('Eggs', im_with_keypoints2)
cv2.waitKey(0)