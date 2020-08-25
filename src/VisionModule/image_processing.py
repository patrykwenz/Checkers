import numpy as np
import cv2.cv2 as cv2
import json
import os


# find corners on image in order to get board without layout
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


# get 4 valid corners
def get_valid_corners(corners):
    corners = sorted(corners, key=lambda x: x[0])
    up_left = corners[0]
    down_right = corners[-1]
    up_right = [down_right[0], up_left[1]]
    down_left = [up_left[0], down_right[1]]

    return up_left, up_right, down_left, down_right


# generate dict representing pieces and fields on chessboard
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


def path_to_src(dir, filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', dir, filename))


def load_image(filename):
    return cv2.imread(path_to_src("pictures/", filename), cv2.IMREAD_COLOR)


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


def get_block_size(image):
    height, width, _ = image.shape
    h = int(height / 8)
    w = int(width / 8)
    return h, w

#calculate field id by cords
def get_block_id_by_cords(cords, blocksizes):
    x, y = cords
    h, w = blocksizes
    i = int(x / h)
    j = int(y / w)
    return i + j * 8


#find all pieces by searching for circles
def find_circles(img):
    BOARD = generate_chessboard()
    param1, param2 = load_configs()
    blocksizes = get_block_size(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.medianBlur(gray, 5)
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1, 30, param1=param1,
                                        param2=param2, minRadius=0, maxRadius=int(img.shape[0] / 8))

    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        output = img.copy()
        for (x, y, r) in detected_circles[0, :]:
            cv2.circle(output, (x, y), r, (0, 255, 0), 2)
            BOARD[get_block_id_by_cords((x, y), blocksizes=blocksizes)]["Piece"] = img[y, x]
            cv2.imwrite("savecircles.png", output)
    return BOARD

def get_board_from_border(img, points):
    pts2 = np.float32([[0, 0], [800, 0], [0, 800], [800, 800]])

    pts1 = np.float32([points[0], points[1], points[2], points[3]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (800, 800))

    # cv2.imwrite("../pictures/wiadomka.png", result)

    # cv2.imshow("Frame", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return result


def run():
    #load image
    img = load_image("planszafullborder.jpg")

    #find corners
    corners = get_corners(img)

    #find valid corners
    points = get_valid_corners(corners)

    #get rid off layout
    img = get_board_from_border(img, points)

    #find circles
    board = find_circles(img)

    for line in board:
        print(line)



if __name__ == '__main__':
    run()