import cv2
import numpy as np
from pdf2image import convert_from_path
import os


# Function to prepare the image by resizing it
def prepare_image(image):
    width = 800
    height = 1200
    image = cv2.resize(image, (width, height))
    return image


# Function to detect rectangles in the image
def detect_rectangles(image):
    kernel1 = np.ones((1, 2), np.uint8)
    kernel2 = np.ones((4, 8), np.uint8)
    kernel_right = np.zeros((1, 9), np.uint8)
    kernel_right[0, :] = 1
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_bw = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV)[1]
    shift = 100
    roi = img_bw[:, shift:]
    img1 = cv2.erode(roi, kernel1, iterations=1)
    img2 = cv2.dilate(img1, kernel2, iterations=3)
    img3 = cv2.dilate(img2, kernel_right, iterations=100)
    contours, _ = cv2.findContours(img3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_height = 20
    contour_coordinates = [cv2.boundingRect(contour) for contour in contours if cv2.boundingRect(contour)[3] > min_height]
    adjusted_contour_coordinates = [(1, y, 799, h) for (x, y, w, h) in contour_coordinates]
    return adjusted_contour_coordinates


# Function to get non-overlapping rectangles
def get_non_overlapping_rectangles(rectangles):
    sorted_rectangles = sorted(rectangles, key=lambda r: r[1])
    non_overlapping_rectangles = []
    prev_bottom = float('-inf')
    for rect in sorted_rectangles:
        if rect[1] >= prev_bottom:
            non_overlapping_rectangles.append(rect)
            prev_bottom = rect[1] + rect[3]
    return non_overlapping_rectangles


# Function to detect lines in the image
def detect_lines(image):
    kernel1 = np.ones((1, 5), np.uint8)
    kernel2 = np.ones((2, 3), np.uint8)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_bw = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
    img1 = cv2.erode(img_bw, kernel1, iterations=1)
    img2 = cv2.dilate(img1, kernel2, iterations=2)
    lines = cv2.HoughLinesP(img2, 1, np.pi / 180, 40, minLineLength=300, maxLineGap=5)
    return lines


# Function to convert PDF to PNG images
def convert_pdf_to_png(name, pdf_path, output_folder):
    images = convert_from_path(pdf_path, output_folder=output_folder, fmt='png', output_file=f'{name}_')
    return images


# Function to draw rectangles and lines on images
def draw (name, images, output_folder):
    for i, image in enumerate(images):
        image = np.array(image)
        image = prepare_image(image)
        try:
            print(name)
            print(i)
            rectangles = detect_rectangles(image)
            print(rectangles)
            rectangles = get_non_overlapping_rectangles(rectangles)
            print(rectangles)
        except cv2.error as e:
            # Handle cv2.error exception
            print(f"OpenCV error occurred: {e}")
        try:
            lines = detect_lines(image)
            print(f'line {lines}')
            if lines:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    if length > 200:
                        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        except cv2.error as e:
            # Handle cv2.error exception
            print(f"OpenCV error occurred: {e}")
        try:
            for (x, y, w, h) in rectangles:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        except cv2.error as e:
            # Handle cv2.error exception
            print(f"OpenCV error occurred: {e}")

        cv2.imwrite(os.path.join(output_folder, f'{name}processed_page_{i + 1}.png'), image)


# Function to convert PDF to images and draw on them
def convert_draw (pdf_path, output_folder, name):
    images = convert_pdf_to_png(name, pdf_path, output_folder)
    draw(name, images, output_folder)




