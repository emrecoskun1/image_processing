import numpy as np
import matplotlib.pyplot as plt
import random
import cv2
import math


def SaltAndPaper(image, density):
    # create an empty array with same size as input image
    output = np.zeros(image.shape, np.uint8)

    # parameter for controlling how much salt and paper are added
    threshhold = 1 - density

    # loop every each pixel and decide add the noise or not base on threshhold (density)
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
    # create an empty array with same size as input image
    output = np.zeros(image.shape, np.uint8)

    # Calculate padding for the filter
    padding = filter_size // 2

    # Deal with filter size
    for j in range(padding, image.shape[0] - padding):
        for i in range(padding, image.shape[1] - padding):
            result = 0
            # Iterate over filter area and sum the values
            for y in range(-padding, padding + 1):
                for x in range(-padding, padding + 1):
                    result += image[j + y, i + x]
            # Calculate the mean value and assign it to the output pixel
            output[j][i] = int(result / (filter_size**2))

    return output


def MedianFilter(image, filter_size):
    # create an empty array with same size as input image
    output = np.zeros(image.shape, np.uint8)

    # create the kernel array of filter as same size as filter_size
    filter_array = [0] * filter_size**2

    # Calculate padding for the filter
    padding = filter_size // 2

    # Deal with filter size
    for j in range(padding, image.shape[0] - padding):
        for i in range(padding, image.shape[1] - padding):
            idx = 0
            # Iterate over filter area and fill the filter array
            for y in range(-padding, padding + 1):
                for x in range(-padding, padding + 1):
                    filter_array[idx] = image[j + y, i + x]
                    idx += 1

            # Sort the filter array
            filter_array.sort()

            # put the median number into output array
            output[j][i] = filter_array[len(filter_array) // 2]

    return output

    # def main():
    # read image
    gray_lena = cv2.imread(r"C:\Users\yunusemrecoskun\Desktop\vesikalik.jpg", 0)

    # add salt and paper (0.01 is a proper parameter)
    noise_lena = SaltAndPaper(gray_lena, 0.01)

    # # use 3x3 mean filter
    # mean_3x3_lena = MeanFilter(noise_lena, 9)

    # # use 3x3 median filter
    # median_3x3_lena = MedianFilter(noise_lena, 9)

    # use 5x5 mean filter
    mean_5x5_lena = MeanFilter(noise_lena, 25)

    # use 5x5 median filter
    median_5x5_lena = MedianFilter(noise_lena, 25)

    # set up side-by-side image display
    fig = plt.figure()
    fig.set_figheight(10)
    fig.set_figwidth(8)

    # display the oringinal image
    fig.add_subplot(2, 2, 1)
    plt.title("Original Image")
    plt.imshow(gray_lena, cmap="gray")

    # display the salt and paper image
    fig.add_subplot(2, 2, 2)
    plt.title("Adding Salt & Paper Image")
    plt.imshow(noise_lena, cmap="gray")

    # # display 3x3 mean filter
    # fig.add_subplot(3, 2, 3)
    # plt.title("3x3 Mean Filter")
    # plt.imshow(mean_3x3_lena, cmap="gray")

    # # display 3x3 median filter
    # fig.add_subplot(3, 2, 4)
    # plt.title("3x3 Median Filter")
    # plt.imshow(median_3x3_lena, cmap="gray")

    # display 5x5 median filter
    fig.add_subplot(2, 2, 3)
    plt.title("5x5 Mean Filter")
    plt.imshow(mean_5x5_lena, cmap="gray")

    # display 5x5 median filter
    fig.add_subplot(2, 2, 4)
    plt.title("5x5 Median Filter")
    plt.imshow(median_5x5_lena, cmap="gray")

    plt.show()


# if __name__ == "__main__":
#     main()
