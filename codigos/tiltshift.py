import cv2
import numpy as np

#https://mofreitas.github.io/#_exercicio_tiltshift
#http://matheuspetrovich.github.io/unidade1.html

def on_trackbar_blend(val):
    alpha = val / 100
    beta = (1 - alpha)
    dst = cv2.addWeighted(img1, alpha, img2, beta, 0.0)
    cv2.imshow('Padrao', dst)


def on_trackbar_line(val):
    faixa = slider_altura*height/100
    
    l1 = slider_centro - int(slider_altura/2)
    l2 = slider_centro + int(slider_altura/2)

    if l1 >= 0 and l2 <= 100:
        l1 = l1*height/100
        l2 = l2*height/100
    else:
        return

    aux = img1.copy()
    cv2.rectangle(aux, (0,int(l1)), (width,int(l2)), (0,0,255),2)
    imageTop = aux.copy()
    on_trackbar_blend(slider_decaimento)


def aumenta_saturacao(image):
    """Modify the saturation and value of the image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)

    saturation = np.array(saturation * 1.2, dtype=np.uint16)
    saturation = np.array(np.clip(saturation, 0, 255), dtype=np.uint8)

    value = np.array(value * 1.1, dtype=np.uint16)
    value = np.array(np.clip(value, 0, 255), dtype=np.uint8)

    return cv2.cvtColor(cv2.merge((hue, saturation, value)), cv2.COLOR_HSV2BGR)


slider_altura = 0 # altura da região central
slider_centro = 0 # posição vertical do centro
slider_decaimento = 0 # intensidade de decaimento
slider_max = 100

cv2.namedWindow('Padrao')
img1 = cv2.imread('cidade.jpg', cv2.IMREAD_COLOR)
height, width = img1.shape[:-1]
img2 = aumenta_saturacao(img1)

cv2.createTrackbar('altura', 'Padrao', slider_altura, slider_max, on_trackbar_line)
cv2.createTrackbar('centro', 'Padrao', slider_centro, slider_max, on_trackbar_line)
on_trackbar_line(0)
cv2.createTrackbar('decaimento', 'Padrao', slider_decaimento, slider_max, on_trackbar_blend)
#on_trackbar_blend(slider_decaimento)

cv2.waitKey(0)