import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
  ret, frame = cap.read()
  print frame.shape
  cv2.imshow('frame', frame)
  # if cv2.waitKey(100) & 0xFF == ord('q'):
  #   break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
