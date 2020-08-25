import numpy as np
import cv2.cv2 as cv2


def get_corners(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    ret, dst = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

    return corners


def get_valid_corners(corners):
    corners = sorted(corners, key=lambda x: x[0])
    up_left = corners[0]
    down_right = corners[-1]
    up_right = [down_right[0], up_left[1]]
    down_left = [up_left[0], down_right[1]]

    return up_left, up_right, down_left, down_right
