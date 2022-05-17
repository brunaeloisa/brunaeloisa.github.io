import cv2 
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not (cap.isOpened()):
  print("Erro ao abrir a câmera.")

while(True):
    _, frame = cap.read()
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    frame_eq = cv2.equalizeHist(frame)
    
    cv2.imshow('normal', frame)
    cv2.imshow('equalizado', frame_eq)
    
    hist_size = 256
    hist_w, hist_h = 720, 540 #980, 720
    bin_w = int(round(hist_w/hist_size))
    
    # calcula histograma normal
    histImage = np.zeros((hist_h, hist_w), dtype=np.uint8)
    hist = cv2.calcHist([frame], [0], None, [hist_size], (0, 256)) 
    cv2.normalize(hist, hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)

    # calcula histograma equalizado
    histImage2 = np.zeros((hist_h, hist_w), dtype=np.uint8)
    hist_eq = cv2.calcHist([frame_eq], [0], None, [hist_size], (0, 256)) 
    cv2.normalize(hist_eq, hist_eq, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)

    for i in range(hist_size):
        cv2.line(histImage, (bin_w*i, hist_h - int(hist[i])),
            (bin_w*i, hist_h),
            255, thickness=2)
        cv2.line(histImage2, (bin_w*i, hist_h - int(hist_eq[i])),
            (bin_w*i, hist_h),
            255, thickness=2)
    
    cv2.imshow('histograma normal', histImage)
    cv2.imshow('histograma equalizado', histImage2)

    if cv2.waitKey(1) & 0xFF == 27:
        break