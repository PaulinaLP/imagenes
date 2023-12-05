import cv2
import numpy as np

img=cv2.imread(r"S:\VBI HUB\Interna BI\BI_ML\imagenes\03e6ab00-6160-484d-a845-0c1d9aeba1af_0001-2.png")
width = 800
height = 1200
img = cv2.resize(img, (width, height))
kernel1 = np.ones((1,2),np.uint8)
kernel2 = np.ones((4,8),np.uint8)
kernel_derecha = np.zeros((1, 9), np.uint8)
kernel_derecha[0, :] = 1
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBW=cv2.threshold(imgGray, 150, 255, cv2.THRESH_BINARY_INV)[1]
shift = 100
roi = imgBW[:, shift:]
img1=cv2.erode(roi, kernel1, iterations=1)
img2=cv2.dilate(img1, kernel2, iterations=3)
img3 = cv2.dilate(img2, kernel_derecha, iterations=100)

cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\rpruebag.png", imgGray)
cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\rpruebab.png", imgBW)
cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\rprueba1.png", img1)
cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\rprueba2.png", img2)
cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\rprueba3.png", img3)

contornos, _ = cv2.findContours(img3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
min_height = 20  # Ajusta este valor según tus necesidades
coor_contornos = [cv2.boundingRect(contorno) for contorno in contornos if
                      cv2.boundingRect(contorno)[3] > min_height
                      ]
coor_contornos_ajustados = [(1, y, 799, h) for (x, y, w, h) in coor_contornos]
for (x, y, w, h) in coor_contornos_ajustados:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
cv2.imwrite(r"S:\VBI HUB\Interna BI\BI_ML\temporal\rprueba.png", img)
