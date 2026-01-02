import cv2
import numpy as np

def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def reduce_noise(gray_image):
    return cv2.GaussianBlur(gray_image, (5, 5), 0)

def binarize_image(blur_image):
    return cv2.adaptiveThreshold(
        blur_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        4
    )

def deskew_image(image):
    coords = cv2.findNonZero(image)
    rect = cv2.minAreaRect(coords)
    angle = rect[-1] - 90

    if angle < -45:
        angle = -(90 + angle)

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated

def preprocess_image(image_path: str):
    image = cv2.imread(image_path)
    gray = convert_to_grayscale(image)
    blur = reduce_noise(gray)
    binary = binarize_image(blur)
    deskewed = deskew_image(binary)
    return deskewed
