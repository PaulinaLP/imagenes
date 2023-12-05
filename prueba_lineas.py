import cv2
import numpy as np

img=cv2.imread(r"S:\VBI HUB\Interna BI\BI_ML\imagenes\03e6ab00-6160-484d-a845-0c1d9aeba1af_0001-2.png")
width = 800
height = 1200
img = cv2.resize(img, (width, height))
kernel1 = np.ones((1, 5), np.uint8)
kernel2 = np.ones((2, 3), np.uint8)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBW = cv2.threshold(imgGray, 200, 255, cv2.THRESH_BINARY_INV)[1]
img1 = cv2.erode(imgBW, kernel1, iterations=1)
img2 = cv2.dilate(img1, kernel2, iterations=2)
lines = cv2.HoughLinesP(img2, 1, np.pi / 180, 40, minLineLength=300, maxLineGap=5)

cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\lpruebag.png", imgGray)
cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\lpruebab.png", imgBW)
cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\lprueba1.png", img1)
cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\lprueba2.png", img2)
for line in lines:
    x1, y1, x2, y2 = line[0]
    length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # Adjust the length threshold as needed
    if length > 200:  # Only draw lines longer than 150 pixels
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\lprueba.png", img)