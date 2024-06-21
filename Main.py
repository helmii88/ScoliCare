import cv2
import sys
import os
import timeit
from YOLO import computeCobb  # Assuming computeCobb is defined in YOLO.py

path = os.path.dirname(__file__)


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def on_btn_File_clicked():
    imagePath = input("Enter the path of the image file: ")
    if os.path.exists(imagePath):
        image = cv2.imread(imagePath)
        if image is not None:
            return image
        else:
            print("Failed to read the image file.")
    else:
        print("File not found at the specified path.")
    return None


def main():
    image = on_btn_File_clicked()
    if image is not None:
        start = timeit.default_timer()
        cobbUp, cobbLow, imgCobb, result = computeCobb(image)

        if (cobbUp or cobbLow) is None:
            print("No vertebrae detected or wrong image")
            return

        if abs(cobbUp) > abs(cobbLow):
            cobbAngle = str(truncate(abs(cobbUp), 2))
        else:
            cobbAngle = str(truncate(abs(cobbLow), 2))

        print("Cobb angle:", cobbAngle)
        print("Classification:", result)

        stop = timeit.default_timer()
        print('Time:', stop - start)


if __name__ == "__main__":
    main()
