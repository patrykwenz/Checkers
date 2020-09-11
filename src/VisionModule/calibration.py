import cv2.cv2 as cv2
import numpy as np
import os
import json


def nothing(x):
    pass


def path_to_src(dir, filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', dir, filename))


def load_image(filename):
    return cv2.imread(path_to_src("pictures/newtest2", filename), cv2.IMREAD_COLOR)


def save_configs(filename):
    return path_to_src('configs/', filename)


def resize(scale_percent, image):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def load_configs(filename="config.txt"):
    conf = json.load(open(path_to_src("configs/", filename)))
    return conf["param1"], conf["param2"]


def find_circles(img, BOARD):
    param1, param2 = load_configs()
    blocksizes = get_block_size(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.medianBlur(gray, 5)
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1, 30, param1=param1,
                                        param2=param2, minRadius=0, maxRadius=int(img.shape[0] / 8))

    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for (x, y, r) in detected_circles[0, :]:
            output = img.copy()
            cv2.circle(output, (x, y), r, (0, 255, 0), 2)
            cv2.destroyAllWindows()
            BOARD[get_block_id_by_cords((x, y), blocksizes=blocksizes)]["Piece"] = img[y, x]


def calibrate_params(filename="planszafullborder.jpg"):
    WINDOW_NAME = "Config"
    cv2.namedWindow(WINDOW_NAME)

    cv2.createTrackbar('param1', WINDOW_NAME, 10, 255, nothing)
    cv2.createTrackbar('param2', WINDOW_NAME, 10, 255, nothing)
    switch = ' \n1 : SAVE Config'
    cv2.createTrackbar(switch, WINDOW_NAME, 0, 1, nothing)

    img = load_image(filename)
    # img = resize(20, img)

    output = img.copy
    while (1):
        param1 = cv2.getTrackbarPos('param1', WINDOW_NAME)
        param2 = cv2.getTrackbarPos('param2', WINDOW_NAME)
        s = cv2.getTrackbarPos(switch, WINDOW_NAME)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.medianBlur(gray, 5)
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, 30, param1=param1,
                                            param2=param2, minRadius=0, maxRadius=int(img.shape[0] / 8))

        if detected_circles is not None:
            output = img.copy()
            detected_circles = np.uint16(np.around(detected_circles))
            for (x, y, r) in detected_circles[0, :]:
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)

        cv2.imshow(WINDOW_NAME, output)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        if s == 1:
            d = dict()
            d["param1"] = param1
            d["param2"] = param2
            json.dump(d, open(save_configs("config.txt"), 'w'))
            break

    cv2.destroyAllWindows()


def find_first_last_white_pixel(image):
    white_pixels = np.array(np.where(image == 255))
    first_white_pixel = white_pixels[:, 0]
    last_white_pixel = white_pixels[:, -1]
    return first_white_pixel, last_white_pixel


def crop_border(image):
    f, l = find_first_last_white_pixel(image)
    h_start, w_start, _ = f
    h_stop, w_stop, _ = l
    return image[h_start + 1:h_stop, w_start + 1:w_stop]


def generate_chessboard():
    chessboard = list()
    for i in range(8):
        for j in range(8):
            FIELD = {"ID": i * 8 + j, "Color": None, "Piece": None}
            if (i + j) % 2 == 0:
                FIELD["Field"] = "White"
                chessboard.append(FIELD)
            else:
                FIELD["Field"] = "Black"
                chessboard.append(FIELD)
    return chessboard


def get_block_size(image):
    height, width, _ = image.shape
    h = int(height / 8)
    w = int(width / 8)
    return h, w


def get_block_id_by_cords(cords, blocksizes):
    x, y = cords
    h, w = blocksizes
    i = int(x / h)
    j = int(y / w)
    return i + j * 8


def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        print(x,y)
        points.append([x, y])


def calibrate_image(img):
    global points
    pts2 = np.float32([[0, 0], [800, 0], [0, 800], [800, 800]])

    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", mouse_drawing)

    while len(points) != 4:
        cv2.imshow("Frame", img)
        key = cv2.waitKey(1)

        if key == 27:
            break
    pts1 = np.float32([points[0], points[1], points[2], points[3]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (800, 800))
    cv2.imshow("Frame", result)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()
    return result

def get_board_from_border(img):
    pts2 = np.float32([[0, 0], [800, 0], [0, 800], [800, 800]])

    pts1 = np.float32([points[0], points[1], points[2], points[3]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (800, 800))
    cv2.imshow("Frame", result)
    cv2.waitKey(100)
    cv2.destroyAllWindows()
    return result


# if __name__ == '__main__':
#     points = []
#     calibrate_params("028.png")
#     # img = load_image("damki.png")
#     # img = resize(10, img)
#     # cv2.imwrite("../pictures/damkiresize.png", img)
#     # calibrate_image(img)
#     # b = generate_chessboard()
#     # find_circles(img, b)
#     # for line in b:
#     #     print(line)
#     # res = calibrate_image(img)
#     # cv2.imwrite(path_to_src('pictures', "calib.png"), res)
#     # pip = load_image("calib.png")
#     # calibrate_params("calib.png")