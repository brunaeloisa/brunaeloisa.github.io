import cv2
import numpy as np


def on_trackbar(val):
    global img_final

    slider_altura = cv2.getTrackbarPos(
        'altura', 'Tiltshift')  # altura da região central
    slider_centro = cv2.getTrackbarPos(
        'centro', 'Tiltshift')  # posição vertical do centro
    slider_decaimento = cv2.getTrackbarPos(
        'decaimento', 'Tiltshift')  # intensidade de decaimento

    l1 = slider_centro - int(slider_altura/2)
    l2 = slider_centro + int(slider_altura/2)

    if l1 >= 0 and l2 <= 100:
        l1 = l1*height/100
        l2 = l2*height/100
    else:
        return

    aux = img1.copy()
    cv2.rectangle(aux, (0, int(l1)), (width, int(l2)), (0, 0, 0), 2)

    x = np.arange(height, dtype=np.float32)

    alpha = 0.5 * (np.tanh((x - l1)/(slider_decaimento+0.001)) -
                   np.tanh((x - l2)/(slider_decaimento+0.001)))

    for i, element in enumerate(alpha):
        aux[i] = cv2.addWeighted(img1[i], element, img2[i], 1 - element, 0.0)

    cv2.imshow('Tiltshift', aux)
    img_final = aux


slider_inicial = 0
slider_max = 100
mask = np.repeat(0.04, 25).reshape(5, 5)

img1 = cv2.imread('cidade.jpg', cv2.IMREAD_COLOR)
height, width = img1.shape[:-1]

img2 = img1.copy()
img_final = img1.copy()

cv2.namedWindow('Tiltshift')
cv2.createTrackbar('altura', 'Tiltshift', slider_inicial,
                   slider_max, on_trackbar)
cv2.createTrackbar('centro', 'Tiltshift', slider_inicial,
                   slider_max, on_trackbar)
cv2.createTrackbar('decaimento', 'Tiltshift',
                   slider_inicial, slider_max, on_trackbar)

img_32f = np.float32(img2)
for n in range(3):
    img_32f = cv2.filter2D(img_32f, -1, mask)
img2 = np.uint8(img_32f)

on_trackbar(0)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('img_tiltshift.png', img_final)
    print('Imagem salva como img_tiltshift.png')
