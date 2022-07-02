import cv2
import numpy as np
import sys


def pontilhismo(image):
    STEP = 4
    JITTER = 4
    RAIO = 3

    points = image.copy()
    rows, cols = image.shape[:-1]

    xrange = np.arange(0, rows-STEP, STEP) + STEP//2
    yrange = np.arange(0, cols-STEP, STEP) + STEP//2

    np.random.shuffle(xrange)

    for i in xrange:
        np.random.shuffle(yrange)
        for j in yrange:
            x = i + np.random.randint(2*JITTER) - JITTER + 1
            y = j + np.random.randint(2*JITTER) - JITTER + 1
            color = tuple(map(int, image[x, y]))
            points = cv2.circle(points, (y, x), RAIO,
                                color, -1, lineType=cv2.LINE_AA)
    return points


def on_trackbar_canny(slider):
    global img_final
    img_final = pontos.copy()

    for n in range(4, 0, -1):
        bordas = cv2.Canny(img, (5-n)*slider, (5-n)*slider)

        x, y = np.where(bordas == 255)

        for i in range(len(x)):
            color = tuple(map(int, img[x[i], y[i]]))
            img_final = cv2.circle(
                img_final, (y[i], x[i]), n, color, -1, lineType=cv2.LINE_AA)

    cv2.imshow('canny', img_final)


arquivo = 'jardim.jpg'
img = cv2.imread(arquivo, cv2.IMREAD_COLOR)
img = cv2.resize(img, (700, 440))

if not img.data:
    print('Erro ao abrir a imagem.')
    sys.exit()

pontos = pontilhismo(img)

cv2.namedWindow('canny')
cv2.createTrackbar('threshold', 'canny', 0, 200, on_trackbar_canny)
on_trackbar_canny(0)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('pontilhismo.png', img_final)
    print('Imagem salva como pontilhismo.png')
