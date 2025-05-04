import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import utils

def find_ellipse(img_path, resize_to):
    image = cv2.imread(img_path)
    if image is None:
        raise FileNotFoundError(f"Failed to read image: {img_path}")
    image = cv2.resize(image, resize_to)

    brown_mask = utils.brown_filter(img_path, resize_to=resize_to)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(brown_mask, (5, 5), 0)
    plt.imshow(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    # Edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_ellipse = None
    max_area = 0

    for contour in contours:
        if len(contour) >= 5:  # fitEllipse requires at least 5 points
            ellipse = cv2.fitEllipse(contour)
            (center, axes, angle) = ellipse
            area = np.pi * (axes[0]/2) * (axes[1]/2)  # approximate ellipse area
            # if area > max_area:
            #     max_area = area
            #     largest_ellipse = ellipse
            if (area > 300 and area < 1500):
                if (axes[0] > 30 or axes[1] > 30):
                    continue
                if (center[0] < (image.shape[0] * 3 / 10)):
                    continue
                if (center[0] > (image.shape[0] * 8.5 / 10)):
                    continue
                # cv2.ellipse(image, ellipse, (0, 255, 0), 2)
                if (area > max_area):
                    max_area = area
                    largest_ellipse = ellipse

    if largest_ellipse is not None:
        cv2.ellipse(image, largest_ellipse, (0, 255, 0), 2)
    else:
        print("No valid ellipse found.")

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[ERROR] Please provide the filename (without extension) of the test image in data_imgs/pos/")
        sys.exit(1)

    HOG_SIZE = (256, 512)
    POS_DIR = 'data_imgs/pos'
    NEG_DIR = 'data_imgs/neg'
    MODEL_PATH = 'hog_color_svm.pkl'
    TEST_IMAGE = f"data_imgs/pos/{sys.argv[1]}.jpg"

    find_ellipse(TEST_IMAGE, resize_to=HOG_SIZE)
    
