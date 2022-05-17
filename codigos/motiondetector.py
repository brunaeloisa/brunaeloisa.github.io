import cv2 
import numpy as np

inicio = True
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
  print("Erro ao abrir a câmera.")

while True:
    _, frame = cap.read()

    bgr = cv2.split(frame) # separa os canais da imagem
    
    hist_size = 256
    hist_w, hist_h = 720, 540
    bin_w = int(round(hist_w/hist_size))
    histImage = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

    # calcula histograma atual (canal vermelho)
    hist_atual = cv2.calcHist(bgr, [2], None, [hist_size], (0, 256))
    cv2.normalize(hist_atual, hist_atual, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)
    
    if inicio:
      hist_anterior = hist_atual.copy() 
      inicio = False

    for i in range(hist_size):
        cv2.line(histImage, (bin_w*i, hist_h - int(hist_atual[i])),
            (bin_w*i, hist_h),
            (0, 0, 255), thickness=2)

    dif = cv2.compareHist(hist_anterior, hist_atual, cv2.HISTCMP_BHATTACHARYYA) # cv2.HISTCMP_BHATTACHARYYA retorna 0.0 para imagens iguais
    if (100 * dif > 3):
      cv2.putText(frame, "Movimento detectado!", (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255))
    
    cv2.imshow('frame', frame)
    cv2.imshow('histograma', histImage)

    hist_anterior = hist_atual.copy()
    
    if cv2.waitKey(1) & 0xFF == 27:
        break