import cv2
import numpy as np
import sys

def on_trackbar(val):
    pass


def filtro_homomorfico():
    '''Implementação da filtragem homomórfica'''
    gammaH = cv2.getTrackbarPos('gama H', 'filtro homomorfico') / 100
    gammaL = cv2.getTrackbarPos('gama L', 'filtro homomorfico') / 100
    D0 = cv2.getTrackbarPos('D0', 'filtro homomorfico')
    c = cv2.getTrackbarPos('c', 'filtro homomorfico') / 10

    tmp = np.zeros((dft_M, dft_N), dtype=np.float32)
    v = np.array(range(dft_N))

    for u in range(dft_M):
        D = np.sqrt((u-dft_M/2)**2 + (v-dft_N/2)**2)
        tmp[u] = (gammaH-gammaL)*(1-np.exp(-c*(D**2)/(0.0001+D0**2))) + gammaL

    # exibe em janela
    cv2.imshow('filtro', tmp)

    # cria a matriz com as componentes do filtro e junta ambas em uma matriz multicanal complexa
    comps = [tmp, tmp]
    filtro_h = cv2.merge(comps)

    return filtro_h


def menu():
    print("\nMENU\n\ne : habilita/desabilita interferencia\nm : habilita/desabilita o filtro mediano\ng : habilita/desabilita o filtro gaussiano")
    print("p : realiza uma amostra das imagens\ns : habilita/desabilita subtração de fundo\nb : realiza uma amostra do fundo da cena\nn : processa o negativo\n")


def deslocaDFT(image):
    '''Troca os quadrantes da imagem da DFT'''
    # se a imagem tiver tamanho ímpar, recorta a regiao para evitar cópias de tamanho desigual
    image = image[0:(image.shape[0] & -2), 0:(image.shape[1] & -2)]

    cy = int(image.shape[0] / 2)
    cx = int(image.shape[1] / 2)

    # reorganiza os quadrantes da transformada
    # A B   ->  D C
    # C D       B A
    A = image[:cy, :cx].copy()
    B = image[:cy, cx:].copy()
    C = image[cy:, :cx].copy()
    D = image[cy:, cx:].copy()

    # A <-> D
    image[:cy, :cx] = D
    image[cy:, cx:] = A

    # C <-> B
    image[:cy, cx:] = C
    image[cy:, :cx] = B

    return image


noise = True # habilita/desabilita ruido
median = False # habilita filtro da mediana
gaussian = False # habilita o filtro gaussiano
negative = False # habilita o negativo da imagem
sample = False # realiza amostragem da imagem
background = False # captura background
subtract = False # subtrai fundo da imagem

# frequência do ruído
freq = 10

# ganho do ruído
gain_int = 0
gain_max = 100
gain = 1.0

# abre a câmera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not (cap.isOpened()):
    print("Erro ao abrir a câmera.")
    sys.exit()

# exibe o menu
menu()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# captura uma imagem para recuperar as informações de gravação
ret, image = cap.read()

if not ret:
    print("Erro na captura do frame.")
    sys.exit()

rows, cols = image.shape[:-1]

# identifica os tamanhos ótimos para cálculo da FFT
dft_M = cv2.getOptimalDFTSize(rows)
dft_N = cv2.getOptimalDFTSize(cols)

# trackbars referentes ao ruído
freq_max = dft_M//2 - 1
cv2.namedWindow('original')
cv2.createTrackbar("frequencia", "original", freq, freq_max, on_trackbar)
cv2.createTrackbar("amp. ruido", "original", gain_int, gain_max, on_trackbar)

# define parâmetros iniciais do filtro homomórfico
gammaH = 0
gammaL = 0
D0 = 0
c = 0

# cria as trackbars
cv2.namedWindow('filtro homomorfico')
cv2.createTrackbar("gama H", "filtro homomorfico", gammaH, 100, on_trackbar)
cv2.createTrackbar("gama L", "filtro homomorfico", gammaL, 100, on_trackbar)
cv2.createTrackbar("D0", "filtro homomorfico", D0, 100, on_trackbar)
cv2.createTrackbar("c", "filtro homomorfico", c, 100, on_trackbar)

# realiza o padding da imagem
padded = cv2.copyMakeBorder(image, 0, dft_M-rows, 0, dft_N-cols, cv2.BORDER_CONSTANT, value=0)

while True:
    ret, image = cap.read()
    if ret:
        imagegray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if (background):
            backgroundImage = imagegray.copy()
            background = False

        if (subtract):
            try:
                imagegray = cv2.max(imagegray - backgroundImage, 0)
            except NameError:
                print("The background image is not defined.")
                subtract = False
        
        if (negative):
            imagegray = np.invert(imagegray)

        if (median):
            image = cv2.medianBlur(imagegray, 3)
            imagegray = image.copy()

        if (gaussian):
            image = cv2.GaussianBlur(imagegray, (3, 3), 0)
            imagegray = image.copy()

        cv2.imshow("original", imagegray)

        # realiza o padding da imagem
        padded = cv2.copyMakeBorder(imagegray, 0, dft_M-rows, 0, dft_N-cols, cv2.BORDER_CONSTANT, value=0)

        # cria a componente real
        realInput = np.float32(padded)

        # parte imaginaria da matriz complexa (preenchida com zeros)
        zeros = np.zeros(padded.shape, dtype=np.float32)

        # insere as duas componentes no array de matrizes
        planos = [realInput, zeros]

        # combina o array de matrizes em uma única componente complexa
        complexImage = cv2.merge(planos)

        # calcula o dft
        cv2.dft(complexImage, complexImage)

        # realiza a troca de quadrantes
        complexImage = deslocaDFT(complexImage)

        ## OPCIONAL ##
        # # exibe o espectro e angulo de fase e armazena amostra das imagens
        # cv2.split(complexImage, planos)

        # magn, angl = cv2.cartToPolar(planos[0], planos[1], False)
        # cv2.normalize(angl, angl, 0, 255, cv2.NORM_MINMAX)
        # anglInt = np.uint8(angl)
        # cv2.imshow("Angulo de Fase", anglInt)

        # cv2.magnitude(planos[0], planos[1], planos[0])
        # magI = planos[0]

        # # soma 1 para evitar erro no log
        # magI += np.ones(magI.shape, dtype=magI.dtype)

        # cv2.log(magI, magI)
        # cv2.normalize(magI, magI, 0, 255, cv2.NORM_MINMAX)
        # magnInt = np.uint8(magI)
        # cv2.imshow("Espectro", magnInt)

        # if (sample):
        #     cv2.imwrite("dft-imagem.png", padded)
        #     cv2.imwrite("dft-espectro.png", magnInt)
        #     cv2.imwrite("dft-angl.png", anglInt)
        #     print("#### sample ok ####\n")
        #     menu()
        #     sample = False
        ## ##

        filtro = filtro_homomorfico()

        # aplica o filtro homomórfico
        complexImage = cv2.mulSpectrums(complexImage, filtro, 0)

        # separa as partes real e imaginária para modificá-las
        cv2.split(complexImage, planos)

        # usa o valor médio do espectro para dosar o ruído
        mean = np.abs(planos[0][dft_M//2][dft_N//2])

        # insere ruído coerente, se habilitado
        if (noise):
            freq = cv2.getTrackbarPos('frequencia', 'original')
            gain_int = cv2.getTrackbarPos('amp. ruido', 'original')
        
            gain = 1.0 * gain_int / gain_max

            # F(u,v) recebe ganho proporcional a F(0,0)
            planos[0][dft_M//2 + freq][dft_N//2 + freq] += gain * mean
            planos[1][dft_M//2 + freq][dft_N//2 + freq] += gain * mean

            # F*(-u,-v) = F(u,v)
            planos[0][dft_M//2-freq][dft_N//2-freq] = planos[0][dft_M//2+freq][dft_N//2+freq]
            planos[1][dft_M//2-freq][dft_N//2-freq] = -planos[1][dft_M//2+freq][dft_N//2+freq]

        # recompõe os planos em uma única matriz complexa
        complexImage = cv2.merge(planos)

        # troca novamente os quadrantes
        complexImage = deslocaDFT(complexImage)

        # calcula a DFT inversa
        cv2.idft(complexImage, complexImage)

        # separa as partes real e imaginária da imagem filtrada
        cv2.split(complexImage, planos)

        # normaliza a parte real para exibição
        cv2.normalize(planos[0], planos[0], 0, 1, cv2.NORM_MINMAX)
        cv2.imshow('filtro homomorfico', planos[0])

        key = cv2.waitKey(10)

        if key == 27:
            break  # esc pressed
        elif key == ord('e'):
            noise = not noise
        elif key == ord('m'):
            median = not median
            menu()
        elif key == ord('g'):
            gaussian = not gaussian
            menu()
        elif key == ord('p'):
            sample = True
        elif key == ord('b'):
            background = True
        elif key == ord('s'):
            subtract = not subtract
        elif key == ord('n'):
            negative = not negative
    else:
        print("Falha na captura do frame.")
        sys.exit()