import cv2
import numpy as np
from pdf2image import convert_from_path
import os
import imagenes

path=r"S:\VBI HUB\Interna BI\BI_Data Quality\Advanced Analitycs\documentacion_para_SuperPaulins\NS_TRAFALGAR"
output_folder = "S:/VBI HUB/Interna BI/BI_ML/imagenes"

for file in os.listdir(path):
    name=file
    pdf_path=os.path.join(path, file)
    nombre = name[:-4]
    imagenes.convertDibujo(pdf_path, output_folder, nombre)