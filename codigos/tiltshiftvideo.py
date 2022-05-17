import cv2
import numpy as np

def on_trackbar_line(val):
    global l1, l2
    
    slider_altura = cv2.getTrackbarPos('altura', 'Padrao') # altura da região central
    slider_centro = cv2.getTrackbarPos('centro', 'Padrao') # posição vertical do centro
    slider_decaimento = cv2.getTrackbarPos('decaimento', 'Padrao') # intensidade de decaimento

    faixa = slider_altura*height/100
    
    aux1 = slider_centro - int(slider_altura/2)
    aux2 = slider_centro + int(slider_altura/2)

    if aux1 >= 0 and aux2 <= 100:
        l1 = aux1*height/100
        l2 = aux2*height/100
    
    aux = frame1.copy()
    cv2.rectangle(aux, (0,int(l1)), (width,int(l2)), (0,0,0), 2)
   
    x = np.arange(height, dtype=np.float32)
    alpha = (np.tanh((x - l1) / (slider_decaimento + 0.001)) - np.tanh((x - l2) / (slider_decaimento + 0.001))) / 2
    
    for i, element in enumerate(alpha):
        aux[i] = cv2.addWeighted(frame1[i], element, frame2[i], 1 - element, 0.0)
    
    cv2.imshow('Padrao', aux)

l1, l2 = 0, 0
slider_padrao = 0
slider_max = 100
mask = np.repeat(0.04,25).reshape(5,5) 

cv2.namedWindow('Padrao')
cap = cv2.VideoCapture('praia.mp4')

height, width = 480, 720

cv2.createTrackbar('altura', 'Padrao', slider_padrao, slider_max, on_trackbar_line)
cv2.createTrackbar('centro', 'Padrao', slider_padrao, slider_max, on_trackbar_line)
cv2.createTrackbar('decaimento', 'Padrao', slider_padrao, slider_max, on_trackbar_line)

taxa = 5
descarta = 0

while True:
    ret, frame1 = cap.read()
    frame1 = cv2.resize(frame1, (width, height))
    frame2 = frame1.copy()
    if ret:
        if descarta == 0:
            frame_32f = np.float32(frame2)
            for n in range(5):
                frame_32f = cv2.filter2D(frame_32f, -1, mask)
            frame2 = np.uint8(frame_32f)

            on_trackbar_line(0)

            descarta += 1
            descarta = descarta % taxa
        else:
            descarta += 1
            descarta = descarta % taxa
    else:
        print("Erro na captura do frame.")
        break

    key = cv2.waitKey(15)
    if key == 27:
        break

cv2.destroyAllWindows()