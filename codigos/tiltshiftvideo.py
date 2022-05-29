import cv2
import numpy as np
import sys

def on_trackbar(val):
    global l1, l2, alpha

    slider_altura = cv2.getTrackbarPos('altura', 'Tiltshift')  # altura da região central
    slider_centro = cv2.getTrackbarPos('centro', 'Tiltshift')  # posição vertical do centro
    slider_decaimento = cv2.getTrackbarPos('decaimento', 'Tiltshift')  # intensidade de decaimento

    tmp1 = slider_centro - int(slider_altura/2)
    tmp2 = slider_centro + int(slider_altura/2)

    if tmp1 >= 0 and tmp2 <= 100:
        l1 = tmp1*height/100
        l2 = tmp2*height/100

    x = np.arange(height, dtype=np.float32)
    alpha = (np.tanh((x - l1) / (slider_decaimento + 0.001)) - np.tanh((x - l2) / (slider_decaimento + 0.001))) / 2

    aux = tiltshift(frame1, frame2)
    cv2.imshow('Tiltshift', aux)

    
def tiltshift(frame1, frame2):
    img = frame1.copy()

    for i, element in enumerate(alpha):
        img[i] = cv2.addWeighted(
            frame1[i], element, frame2[i], 1 - element, 0.0)

    return img


def salvarvideo(video):
    taxa = 15
    descarta = 0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('video_tiltshift.mp4', fourcc, 12, (width, height))

    cap = cv2.VideoCapture(video)

    while True:
        ret, frame1 = cap.read()
        if ret:
            if descarta == 0:
                frame2 = frame1.copy()

                # aplica borramento
                frame_32f = np.float32(frame2)
                for _ in range(5):
                    frame_32f = cv2.filter2D(frame_32f, -1, mask)
                frame2 = np.uint8(frame_32f)

                novo_frame = tiltshift(frame1, frame2)
                out.write(novo_frame)

                descarta += 1
                descarta = descarta % taxa
            else:
                descarta += 1
                descarta = descarta % taxa
        else:
            break

    out.release()
    print("Vídeo salvo como video_tiltshift.mp4")


l1, l2 = 0, 0
slider_padrao = 0
slider_max = 100
mask = np.repeat(0.04, 25).reshape(5, 5)
arq_video = 'video.mp4'

cap = cv2.VideoCapture(arq_video)

# lê primeiro frame para ajustar parâmetros do tilt-shift
ret, frame1 = cap.read()

if not ret:
    print("Erro na captura do frame.")
    sys.exit()

height, width = frame1.shape[:-1]

alpha = np.zeros(height, dtype=np.float32)

frame1 = cv2.resize(frame1, (width, height))
frame2 = frame1.copy()

cv2.namedWindow('Tiltshift')
cv2.createTrackbar('altura', 'Tiltshift', slider_padrao, slider_max, on_trackbar)
cv2.createTrackbar('centro', 'Tiltshift', slider_padrao, slider_max, on_trackbar)
cv2.createTrackbar('decaimento', 'Tiltshift', slider_padrao, slider_max, on_trackbar)

frame_32f = np.float32(frame2)
for n in range(5):
    frame_32f = cv2.filter2D(frame_32f, -1, mask)
frame2 = np.uint8(frame_32f)

on_trackbar(0)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    salvarvideo(arq_video)
    cv2.destroyAllWindows()
