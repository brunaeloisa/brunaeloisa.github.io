import cv2
import sys
import numpy as np

nClusters = 8
nRodadas = 1

arquivo = 'jardim.jpg'
img = cv2.imread(arquivo, cv2.IMREAD_COLOR)
img = cv2.resize(img, (640, 450))

if not img.data:
    print('Erro ao abrir a imagem.')
    sys.exit()

rows, cols = img.shape[:-1]
samples = np.zeros((rows*cols, 3), dtype=np.float32)

for y in range(rows):
    for x in range(cols):
        for z in range(3):
            samples[y + x*rows][z] = img[y, x][z]

criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)

for n in range(1, 11):
    _, rotulos, centros = cv2.kmeans(samples, nClusters, None, criteria, nRodadas, cv2.KMEANS_RANDOM_CENTERS)

    centros = np.uint8(centros)

    rotulada = np.zeros(img.shape, dtype=img.dtype)
    for y in range(rows):
        for x in range(cols):
            indice = rotulos[y + x*rows, 0]
            for z in range(3):
                rotulada[y, x][z] = centros[indice][z]

    cv2.imwrite(f'clustered_img{n}.png', rotulada)
    print(f'Imagem salva como clustered_img{n}.png')

    k = cv2.waitKey(0)
    if k == 27:
        sys.exit()
