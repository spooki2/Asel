import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def WTB():
    str = "WTBRET"
    return str
    '''
    ret, frame = cap.read()
    if not ret:
        return

    # convert the frame to bytes
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.array(frame)
    bytes_frame = frame.tobytes()
    return bytes_frame


cap.release()
cv2.destroyAllWindows()
'''
