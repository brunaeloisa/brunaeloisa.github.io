import cv2
import sys
import numpy as np
import pytesseract


def on_trackbar_canny(val):
    pass


def find_paper(cntrs):
    '''Identifica o contorno de maior área e aproxima por um polígono de 4 lados'''
    aux = list(cntrs)

    if len(aux) > 0:
        aux.sort(reverse=True, key=lambda x: cv2.contourArea(x))
        perimeter = cv2.arcLength(aux[0], True)
        polygon = cv2.approxPolyDP(aux[0], 0.04*perimeter, True)
        return polygon
    else:
        return aux


def sort_points(pts):
    '''Reorganiza a ordem dos pontos para corresponder às quinas da imagem'''
    pts = pts.reshape(4, 2)
    temp = np.zeros((4, 1, 2), dtype=np.float32)

    soma = pts.sum(1)
    dif = np.diff(pts, axis=1)

    # para corresponder ao [0,0], buscamos o ponto com menor soma entre as coordenadas
    temp[0] = pts[np.argmin(soma)]
    # para o [w-1,h-1], buscamos o ponto com a maior soma
    temp[3] = pts[np.argmax(soma)]
    # para o [w-1,0], buscamos o ponto com a menor diferença entre as coordenadas
    temp[1] = pts[np.argmin(dif)]
    # para o [0,h-1], buscamos o ponto com a a maior diferença
    temp[2] = pts[np.argmax(dif)]

    return temp


def write_file(filename):
    text = pytesseract.image_to_string(scanned_bin)
    text = text.replace('\n\n', '^\n')
    split_text = text.split('\n')

    for i, line in enumerate(split_text):
        if line[-1:] == '.':
            line = line + '\n\n'
        elif line[-1:].isalpha() or line[-1:] in [',', '-']:
            line = line + ' '
        elif line[-1:] in [':', ';']:
            line = line + '\n'
        split_text[i] = line

    new_text = ''.join(split_text)
    new_text = new_text.replace('^', '\n\n')

    split_text = new_text.split('.')

    for i in range(len(split_text)-1):
        if len(split_text[i+1]) == 0:
            split_text[i+1] = '..'
        if len(split_text[i+1]) >= 1:
            if split_text[i][-1:].islower() and split_text[i+1][0].islower() :
                split_text[i] = split_text[i] + ' '
            elif split_text[i][-1:].isnumeric() and split_text[i+1][0].isnumeric():
                split_text[i] = split_text[i] + '.'
        if len(split_text[i+1]) >= 2:
            if (split_text[i+1][0] == ' ' and split_text[i+1][1].isupper()) or split_text[i+1][:1] == '\n':
                split_text[i] = split_text[i] + '.'

    new_text = ''.join(split_text)

    file = open(filename, 'w', encoding='utf-8')
    file.write(new_text)
    file.close()


# cria a trackbar que controla o threshold1 do algoritmo de canny
cv2.namedWindow('bordas')
cv2.createTrackbar('threshold', 'bordas', 100, 250, on_trackbar_canny)
on_trackbar_canny(100)

camera = True
pause = False
h, w = 1574, 1240

# set tesseract path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# inicia a captura de vídeo
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Câmera não encontrada.")
    camera = False

    # carrega o arquivo
    arquivo = 'papel.jpg'
    image = cv2.imread(arquivo, cv2.IMREAD_COLOR)
    orig_h, orig_w = image.shape[:-1]

    # converte para preto e branco
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # aplica borramento
    blurred_image = cv2.GaussianBlur(image_gray, (5, 5), 1)

    if not image.data:
        print('Erro ao abrir a câmera e carregar o arquivo.')
        sys.exit()  # encerra o programa

while True:
    if not pause:
        if camera:
            ret, frame = cap.read()

            if not ret:
                print("Erro na captura do frame.")
                break

            image = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            orig_h, orig_w = image.shape[:-1]
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred_image = cv2.GaussianBlur(image_gray, (5, 5), 1)

        # aplica canny para identificar as bordas
        threshold1 = cv2.getTrackbarPos('threshold', 'bordas')
        bordas = cv2.Canny(image, threshold1, 3*threshold1)

        # aplica-se operações de morfologia matemática na imagem binária
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # dilatação
        bordas = cv2.dilate(bordas, element, iterations=1)
        # fechamento
        bordas = cv2.morphologyEx(bordas, cv2.MORPH_CLOSE, element)

        # procura por contornos externos
        contours, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # identifica o contorno que delimita o papel
        paper = find_paper(contours)

        img_contour = image.copy()

        if len(paper) == 4:
            cv2.drawContours(img_contour, [paper], -1, (0, 255, 0), 5)

            points = sort_points(paper)
            new_points = np.float32([[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]])

            # realiza mudança de perspectiva na imagem
            transf_matrix = cv2.getPerspectiveTransform(points, new_points)
            scanned_color = cv2.warpPerspective(image, transf_matrix, (w, h))
        else:
            # caso não sejam detectadas as bordas do papel
            scanned_color = image.copy()

        # threshold adaptativo
        scanned_gray = cv2.cvtColor(scanned_color, cv2.COLOR_BGR2GRAY)
        scanned_gray = cv2.GaussianBlur(scanned_gray, (5, 5), 1)

        # aplica threshold adaptativo
        adapt_threshold = cv2.adaptiveThreshold(scanned_gray, 255, 1, 1, 7, 2)

        # faz o negativo da imagem
        scanned_bin = cv2.bitwise_not(adapt_threshold)

        cv2.imshow('bordas', cv2.resize(bordas, (orig_w//2, orig_h//2)))
        cv2.imshow('contour', cv2.resize(img_contour, (orig_w//2, orig_h//2)))
        cv2.imshow('color', cv2.resize(scanned_color, (w//2, h//2)))
        cv2.imshow('binary', cv2.resize(scanned_bin, (w//2, h//2)))

    key = cv2.waitKey(10)
    if key == 27:
        break  # esc pressed!
    elif key == ord('p'):
        pause = not pause
    elif key == ord('s'):
        cv2.imwrite('scanned_color.png', scanned_color)
        cv2.imwrite('scanned_bin.png', scanned_bin)
        write_file('img_text.txt')
        print('Arquivos salvos!')
