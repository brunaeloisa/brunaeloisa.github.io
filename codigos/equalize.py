import cv2 
import numpy as np
import sys

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not (cap.isOpened()):
    print("Erro ao abrir a câmera.")
    sys.exit() # encerra o programa

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

hist_size = 256
hist_w, hist_h = 512, 480
hist_range = (0, 256)

bin_w = int(round(hist_w/hist_size))

while(True):
    ret, frame = cap.read()
    
    if not ret:
        print("Erro na captura do frame.")
        break
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    frame_eq = cv2.equalizeHist(frame)

    # calcula histograma normal
    histImage = np.zeros((hist_h, hist_w), dtype=np.uint8)
    hist = cv2.calcHist([frame], [0], None, [hist_size], hist_range) 
    cv2.normalize(hist, hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)

    # calcula histograma equalizado
    histImage_eq = np.zeros((hist_h, hist_w), dtype=np.uint8)
    hist_eq = cv2.calcHist([frame_eq], [0], None, [hist_size], hist_range) 
    cv2.normalize(hist_eq, hist_eq, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)

    for i in range(hist_size):
        cv2.line(histImage, (bin_w*i, hist_h - int(hist[i])), (bin_w*i, hist_h), 255, thickness=2)
        cv2.line(histImage_eq, (bin_w*i, hist_h - int(hist_eq[i])), (bin_w*i, hist_h), 255, thickness=2)
      
    normal = cv2.hconcat([frame, histImage])
    equalizado = cv2.hconcat([frame_eq, histImage_eq])
    
    cv2.imshow('normal', normal)
    cv2.imshow('equalizado', equalizado)

    key = cv2.waitKey(10)
    
    if key == 27: 
        break # encerra se apertar ESC
    elif key == ord('s'):
        cv2.imwrite('normal.png', normal)
        cv2.imwrite('equalizado.png', equalizado)
