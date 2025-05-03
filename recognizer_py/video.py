import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

def brown_filter(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower_blue = np.array([90, 50, 50])
    # upper_blue = np.array([130, 255, 255])

    lower_brown = np.array([5, 0, 0])
    upper_brown = np.array([70, 255, 60])

    mask = cv2.inRange(hsv, lower_brown, upper_brown)

    # save img
    cv2.imwrite('brown_filter_result.png', mask)
    return mask

def find_ellipse(img):
    brown_mask = brown_filter(img)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(brown_mask, (5, 5), 0)

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
            if area > max_area:
                max_area = area
                largest_ellipse = ellipse
    
    return cv2.ellipse(img, largest_ellipse, (0, 255, 0), 2) if largest_ellipse is not None else img

def video_cockroach(resize_to):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to HOG_SIZE
        frame_resized = cv2.resize(frame, resize_to)

        # Apply brown filter
        img_ellipse = find_ellipse(frame_resized)

        # Display the result
        cv2.imshow('frame', img_ellipse)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[ERROR] Please provide the filename (without extension) of the test image in data_imgs/pos/")
        sys.exit(1)

    HOG_SIZE = (128, 256)

    # find_ellipse(TEST_IMAGE, resize_to=HOG_SIZE)
    video_cockroach(resize_to=HOG_SIZE)