import cv2.cv2 as cv2
import numpy as np

image = cv2.imread('../pictures/planszafullborder.jpg')
#
# scale_percent = 20  # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
# # resize image
# image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# thresh = cv2.threshold(gray, 0, 255,
#                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
ret, thresh = cv2.threshold(gray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, 1, 2)

print(len(contours))
for cnts in contours:
    rect = cv2.minAreaRect(cnts)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    image = cv2.drawContours(image, [box], 0, (0, 0, 255), 2)

cv2.imshow("Output", image)
cv2.waitKey(0)
