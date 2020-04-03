from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import imutils
import cv2.cv2 as cv2

image = cv2.imread("../pictures/planszafullborder.jpg")
#
# scale_percent = 20  # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
# # resize image
# image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# image = cv2.bitwise_not(image)


shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
# convert the mean shift image to grayscale, then apply
# Otsu's thresholding
gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255,
                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=20,
                          labels=thresh)
# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

#
# for label in np.unique(labels):
# 	# if the label is zero, we are examining the 'background'
# 	# so simply ignore it
# 	if label == 0:
# 		continue
# 	# otherwise, allocate memory for the label region and draw
# 	# it on the mask
# 	mask = np.zeros(gray.shape, dtype="uint8")
# 	mask[labels == label] = 255
# 	# detect contours in the mask and grab the largest one
# 	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
# 		cv2.CHAIN_APPROX_SIMPLE)
# 	cnts = imutils.grab_contours(cnts)
# 	c = max(cnts, key=cv2.contourArea)
# 	# draw a circle enclosing the object
# 	((x, y), r) = cv2.minEnclosingCircle(c)
# 	cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
# 	cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
# 		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
# # show the output image
# cv2.imshow("Output", image)
# cv2.waitKey(0)


# for label in np.unique(labels):
#     if label == 0:
#         continue
#     mask = np.zeros(gray.shape, dtype="uint8")
#     mask[labels == label] = 255
#     cnts, hier = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
#                                   cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0]
#     rect = cv2.minAreaRect(cnts)
#     box = cv2.boxPoints(rect)
#     box = np.int0(box)
#     image = cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
# print("dasda")

for label in np.unique(labels):
    if label == 0: continue
    mask = np.zeros(gray.shape, dtype="uint8")
    mask[labels == label] = 255
    cnts, hier = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0]
    rect = cv2.minAreaRect(cnts)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    print(box)
    image = cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
    bottom_right, bottom_left, top_left, top_right = box
    print(((bottom_right[0] - bottom_left[0]) / 2))
    print(((bottom_left[1] - top_left[1]) / 2), "\n")
    cv2.putText(image, "#{}".format(label),
                (int((bottom_right[0] - bottom_left[0]) / 2) + top_left[0] - 10
                 , int((bottom_left[1] - top_left[1]) / 2) + top_left[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow("Output", image)
cv2.waitKey(0)
#####genialnypomysl wziecie obrazka, obliczenie sredniej wielkosci boxa, obliczenie liczby pikseli, ekstrakcja po kolei i sprawdzanie pojedynzco