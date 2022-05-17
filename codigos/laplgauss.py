import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not (cap.isOpened()):
  print("Erro ao abrir a câmera.")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# define as masks
media = np.array([[0.1111,0.1111,0.1111], [0.1111,0.1111,0.1111], [0.1111,0.1111,0.1111]])
gauss = np.array([[0.0625,0.125,0.0625], [0.125,0.25,0.125], [0.0625,0.125,0.0625]])
horizontal = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
vertical = np.array([[-1,-2,-1], [0,0,0], [1,2,1]])
laplacian = np.array([[0,-1,0], [-1,4,-1], [0,-1,0]])
boost = np.array([[0,-1,0], [-1,5.2,-1], [0,-1,0]])
laplacian_gauss = np.array([[0,0,1,0,0], [0,1,2,1,0], [1,2,-16,2,1], [0,1,2,1,0], [0,0,1,0,0]])

print("\nMENU\n\n'a' - módulo\n'm' - média\n'g' - filtro gaussiano\n'h' - detector de bordas horizontais\n\
'v' - detector de bordas verticais\n'l' - filtro laplaciano\n'f' - filtro laplaciano do gaussiano\n'b' - boost\
\nesc - encerrar programa\n")

mask = np.float32(media)
absolut = True

while(True):
  _, frame = cap.read()

  frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  frame_gray = cv2.flip(frame_gray, 1)

  frame_32f = np.float32(frame_gray)
  filtered_frame = cv2.filter2D(frame_32f, -1, mask)

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
    mask = np.float32(media)
  elif key == ord('g'):
    mask = np.float32(gauss)
  elif key == ord('h'):
    mask = np.float32(horizontal)
  elif key == ord('v'):
    mask = np.float32(vertical)
  elif key == ord('l'):
    mask = np.float32(laplacian)
  elif key == ord('b'):
    mask = np.float32(boost)
  elif key == ord('f'):
    mask = np.float32(laplacian_gauss)