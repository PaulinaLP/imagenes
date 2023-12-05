import cv2
import numpy as np
from pdf2image import convert_from_path
import os


def prepararImagen(image):
    width = 800
    height = 1200
    image = cv2.resize(image, (width, height))
    return (image)


def rectangulos(image):
    kernel1 = np.ones((1, 2), np.uint8)
    kernel2 = np.ones((4, 8), np.uint8)
    kernel_derecha = np.zeros((1, 9), np.uint8)
    kernel_derecha[0, :] = 1
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBW = cv2.threshold(imgGray, 150, 255, cv2.THRESH_BINARY_INV)[1]
    shift = 100
    roi = imgBW[:, shift:]
    img1 = cv2.erode(roi, kernel1, iterations=1)
    img2 = cv2.dilate(img1, kernel2, iterations=3)
    img3 = cv2.dilate(img2, kernel_derecha, iterations=100)
    contornos, _ = cv2.findContours(img3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_height = 20
    coor_contornos = [cv2.boundingRect(contorno) for contorno in contornos if
                      cv2.boundingRect(contorno)[3] > min_height
                      ]
    coor_contornos_ajustados = [(1, y, 799, h) for (x, y, w, h) in coor_contornos]
    return coor_contornos_ajustados

def get_non_overlapping_rectangles(rectangles):
    # Sort the rectangles by y-coordinate in ascending order
    sorted_rectangles = sorted(rectangles, key=lambda r: r[1])

    # List to store non-overlapping rectangles
    non_overlapping_rectangles = []

    # Iterate through sorted rectangles and check for y-coordinate constraint
    prev_bottom = float('-inf')  # Initialize with negative infinity
    for rect in sorted_rectangles:
        # Check if the current rectangle starts after the bottom of the previous one
        if rect[1] >= prev_bottom:
            non_overlapping_rectangles.append(rect)
            prev_bottom = rect[1] + rect[3]  # Update the bottom of the current rectangle

    return non_overlapping_rectangles

def lineas(image):
    kernel1 = np.ones((1, 5), np.uint8)
    kernel2 = np.ones((2, 3), np.uint8)
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBW = cv2.threshold(imgGray, 200, 255, cv2.THRESH_BINARY_INV)[1]
    img1 = cv2.erode(imgBW, kernel1, iterations=1)
    img2 = cv2.dilate(img1, kernel2, iterations=2)
    lines = cv2.HoughLinesP(img2, 1, np.pi / 180, 40, minLineLength=300, maxLineGap=5)
    return lines


def convert_pdf_to_png(nombre, pdf_path, output_folder):
    images = convert_from_path(pdf_path, output_folder=output_folder, fmt='png', output_file=f'{nombre}_')
    return images


def dibujar(nombre, images, output_folder):
    for i, image in enumerate(images):
        image = np.array(image)
        image = prepararImagen(image)
        try:
            print(nombre)
            print(i)
            rect = rectangulos(image)
            print(rect)
            rect = get_non_overlapping_rectangles(rect)
            print(rect)
        except:
            pass
        try:
            lin = lineas(image)
            for line in lin:
                    x1, y1, x2, y2 = line[0]
                    length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    # Adjust the length threshold as needed
                    if length > 200:  # Only draw lines longer than 150 pixels
                        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        except:
            pass
        try:
            for (x, y, w, h) in rect:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        except:
            pass

        cv2.imwrite(os.path.join(output_folder, f'{nombre}processed_page_{i + 1}.png'), image)


def convertDibujo(pdf_path, output_folder, nombre):
    images = convert_pdf_to_png(nombre, pdf_path, output_folder)
    dibujar(nombre, images, output_folder)



