import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt


def brown_filter(img_path, resize_to):
    image = cv2.imread(img_path)
    if image is None:
        raise FileNotFoundError(f"Failed to read image: {img_path}")
    image = cv2.resize(image, resize_to)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # lower_blue = np.array([90, 50, 50])
    # upper_blue = np.array([130, 255, 255])

    lower_brown = np.array([5, 0, 0])
    upper_brown = np.array([70, 255, 60])

    mask = cv2.inRange(hsv, lower_brown, upper_brown)
    result = cv2.bitwise_and(image, image, mask=mask)

    # save img
    cv2.imwrite('brown_filter_result.png', mask)
    return mask


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[ERROR] Please provide the filename (without extension) of the test image in data_imgs/pos/")
        sys.exit(1)

    HOG_SIZE = (128, 256)
    POS_DIR = 'data_imgs/pos'
    NEG_DIR = 'data_imgs/neg'
    MODEL_PATH = 'hog_color_svm.pkl'
    TEST_IMAGE = f"data_imgs/pos/{sys.argv[1]}.webp"

    brown_filter(TEST_IMAGE, resize_to=HOG_SIZE)
