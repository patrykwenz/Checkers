import cv2.cv2 as cv2
import numpy as np
from sklearn.cluster import KMeans
import os
import warnings
import matplotlib.pyplot as plt

def warn(*args, **kwargs):
    pass
warnings.warn = warn


class ImageProcessor():
    def __init__(self):
        self.BLACK_FIELD = []
        self.WHITE_FIELD = []
        self.CATEGORY_ONE_PIECE = []
        self.CATEGORY_TWO_PIECE = []

    @staticmethod
    def load_image(filename):
        dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','pictures/', filename))
        return cv2.imread(dir_path, cv2.IMREAD_COLOR)

    @staticmethod
    def show_off_image(img):
        cv2.imshow('image', img)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()

    @staticmethod
    def display_few_img(img1, img2):
        numpy_horizontal = np.hstack((img1, img2))
        cv2.imshow('image', numpy_horizontal)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def resize(scale_percent, image):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    def create_histogram(self, cluster):
        labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
        hist, _ = np.histogram(cluster.labels_, bins=labels)
        hist = hist.astype('float')
        hist /= hist.sum()
        return hist

    def rgb_color(self, color):
        red, green, blue = int(color[2]), int(color[1]), int(color[0])
        return [red, green, blue]

    def k_means_image_colors(self, image, number_of_clusters=4):
        clusters = KMeans(n_clusters=number_of_clusters)
        clusters.fit(image)
        return clusters

    def get_image_colors(self, image, number_of_clusters=4):
        clusters = self.k_means_image_colors(image, number_of_clusters=number_of_clusters)
        hist = self.create_histogram(clusters)
        combined = zip(hist, clusters.cluster_centers_)
        combined = sorted(combined, key=lambda x: x[0], reverse=True)

        to_return = []
        for index, row in enumerate(combined):
            comb = dict()
            comb["index"] = index + 1
            comb["%"] = round(row[0], 2)
            comb["RGB"] = self.rgb_color(row[1])
            to_return.append(comb)
        return to_return

    def set_default_colors(self, ranking):
        sorted_ranking_fields = sorted(ranking[0:2], key=lambda x: sum(x["RGB"]), reverse=True)
        sorted_ranking_pieces = sorted(ranking[2:4], key=lambda x: sum(x["RGB"]), reverse=False)
        self.WHITE_FIELD = sorted_ranking_fields[0]["RGB"]
        self.BLACK_FIELD = sorted_ranking_fields[1]["RGB"]
        self.CATEGORY_ONE_PIECE = sorted_ranking_pieces[0]["RGB"]
        self.CATEGORY_TWO_PIECE = sorted_ranking_pieces[1]["RGB"]

    def tolerance_comparsion(self, a, b, tolerance=100):
        a = np.array(a)
        b = np.array(b)
        return (abs(a - b) <= tolerance).all()

    def is_black_field(self, RGB):
        return self.tolerance_comparsion(RGB, self.BLACK_FIELD)

    def is_white_field(self, RGB):
        return self.tolerance_comparsion(RGB, self.WHITE_FIELD)

    def is_category_one(self, RGB):
        return self.tolerance_comparsion(RGB, self.CATEGORY_ONE_PIECE)

    def is_category_two(self, RGB):
        return self.tolerance_comparsion(RGB, self.CATEGORY_TWO_PIECE)

    def choose_field(self, RGB):
        if self.is_black_field(RGB):
            return {"Field": "BLACK"}
        if self.is_white_field(RGB):
            return {"Field": "WHITE"}
        if self.is_category_one(RGB):
            return {"PIECE": "CAT#1"}
        if self.is_category_two(RGB):
            return {"PIECE": "CAT#2"}

    def convert_results(self, results):
        fields = []
        for field in results:
            if field["%"] > 0.1:
                fields.append(self.choose_field(field["RGB"]))
        return fields

    def iterate_through_image(self, image):
        height, width, _ = image.shape
        height_step = round(height / 8)
        width_step = round(width / 8)

        prep = image.reshape((height * width, 3))
        # set default colors, scan whole image
        self.set_default_colors(self.get_image_colors(prep, number_of_clusters=4))

        count = 0
        BOARD = []
        for i in range(0, height, height_step):
            for j in range(0, width, width_step):
                FIELD = dict()
                height_to_crop = i + height_step
                width_to_crop = j + width_step

                if height_to_crop > height:
                    break
                if width_to_crop > width:
                    break

                temp = image[i:height_to_crop, j:width_to_crop]
                t_height, t_width, _ = temp.shape

                tempo = temp.reshape((t_height * t_width, 3))
                results = self.get_image_colors(tempo)
                results = self.convert_results(results)
                count += 1
                FIELD["ID"] = count
                FIELD["DATA"] = results
                BOARD.append(FIELD)
        return BOARD


if __name__ == '__main__':
    img_proc = ImageProcessor()
    image = img_proc.load_image("planszafull.png")
    image = img_proc.resize(16, image)
    b = img_proc.iterate_through_image(image)
    for c in b:
        print(c)
