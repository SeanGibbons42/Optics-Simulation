import numpy as np
import matplotlib.image as mpimg

class Model():
    """
    Class Model: Contains code responsible for calculations
    and data manipulation.
    """
    def __init__(self):
        self.obj_pic = None

    def fft(a):
        return np.fft.fft2(a)

    def load_img(self, path):

        img = mpimg.imread(path)
        img = self.rgb2gray(img)
        return img

    def get_fcl(self, obj):
        pass

    def get_image(self, fcl):
        pass

    def rgb2gray(self, rgb):
        return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
