import numpy as np
import matplotlib.pyplot as plt
import random
import cv2
import math


def SaltAndPaper(image, density):

    output = np.zeros(image.shape, np.uint8)

    threshhold = 1 - density

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            possibility = random.random()
            if possibility < density:
                output[i][j] = 0
            elif possibility > threshhold:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


def MeanFilter(image, filter_size):

    output = np.zeros(image.shape, np.uint8)

    padding = filter_size // 2

    for j in range(padding, image.shape[0] - padding):
        for i in range(padding, image.shape[1] - padding):
            result = 0
            for y in range(-padding, padding + 1):
                for x in range(-padding, padding + 1):
                    result += image[j + y, i + x]
            output[j][i] = int(result / (filter_size**2))

    return output


def MedianFilter(image, filter_size):
    output = np.zeros(image.shape, np.uint8)

    filter_array = [0] * filter_size**2

    padding = filter_size // 2

    for j in range(padding, image.shape[0] - padding):
        for i in range(padding, image.shape[1] - padding):
            idx = 0
            for y in range(-padding, padding + 1):
                for x in range(-padding, padding + 1):
                    filter_array[idx] = image[j + y, i + x]
                    idx += 1

            filter_array.sort()

            output[j][i] = filter_array[len(filter_array) // 2]

    return output
