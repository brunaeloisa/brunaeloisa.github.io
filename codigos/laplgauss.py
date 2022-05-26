import cv2
import numpy as np
import sys

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not (cap.isOpened()):
  print("Erro ao abrir a câmera.")
  sys.exit() # encerra o programa

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# define as máscaras
media = np.array([[0.1111,0.1111,0.1111], [0.1111,0.1111,0.1111], [0.1111,0.1111,0.1111]])
gauss = np.array([[0.0625,0.125,0.0625], [0.125,0.25,0.125], [0.0625,0.125,0.0625]])
horizontal = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
vertical = np.array([[-1,-2,-1], [0,0,0], [1,2,1]])
laplacian = np.array([[0,-1,0], [-1,4,-1], [0,-1,0]])
boost = np.array([[0,-1,0], [-1,5.2,-1], [0,-1,0]])

print("\nMENU\n\n'a' - módulo\n'm' - média\n'g' - gaussiano\n'h' - detector de bordas horizontais\n\
'v' - detector de bordas verticais\n'l' - laplaciano\n'f' - laplaciano do gaussiano\n'b' - boost\
\n's' - salvar imagem instantânea\nesc - encerrar programa\n")

mask = np.float32(media)
absolut = True
laplacian_gauss = False

while(True):
  ret, frame = cap.read()

  if not ret:
    print("Erro na captura do frame.")
    break

  frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  frame_gray = cv2.flip(frame_gray, 1)

  frame_32f = np.float32(frame_gray)
  filtered_frame = cv2.filter2D(frame_32f, -1, mask)

  if laplacian_gauss:
    filtered_frame = cv2.filter2D(filtered_frame, -1, laplacian)

  if absolut:
    filtered_frame = np.abs(filtered_frame)

  filtro_espacial = np.uint8(filtered_frame)

  cv2.imshow('imagem original', frame_gray)
  cv2.imshow('imagem com efeito', filtro_espacial)

  key = cv2.waitKey(10)

  if key == 27:
    break
  elif key == ord('a'):
    absolut = not absolut
  elif key == ord('m'):
    laplacian_gauss = False
    mask = np.float32(media)
  elif key == ord('g'):
    laplacian_gauss = False
    mask = np.float32(gauss)
  elif key == ord('h'):
    laplacian_gauss = False
    mask = np.float32(horizontal)
  elif key == ord('v'):
    laplacian_gauss = False
    mask = np.float32(vertical)
  elif key == ord('l'):
    laplacian_gauss = False
    mask = np.float32(laplacian)
  elif key == ord('b'):
    laplacian_gauss = False
    mask = np.float32(boost)
  elif key == ord('f'):
    laplacian_gauss = True
    mask = np.float32(gauss)
  elif key == ord('s'):
    cv2.imwrite('filtered_img.png', filtro_espacial)
