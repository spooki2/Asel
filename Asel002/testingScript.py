import cv2
import base64
from PIL import Image
import numpy as np
import io
import cv2
import base64
import numpy as np
import json



def imageEncode(frameImage): # Convert the image to a base64 string
    camValidVal, buffer = cv2.imencode('.jpg', frameImage)
    base64_image_str = base64.b64encode(buffer)
    return base64_image_str

def imageDecode(bytesImage): # Convert the base64 string back to an image
    img_bytes = base64.b64decode(bytesImage)
    img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
    decoded_img = cv2.imdecode(img_arr, flags=cv2.IMREAD_COLOR)
    return decoded_img
''' 
# Start video capture
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Capture one frame
    camValid, frame = vid.read()

    if camValid:
        imgBytes = imageEncode(frame)
        decoded_img = imageDecode(imgBytes)


        # Display the original and decoded images
        cv2.imshow('Original', frame)
        cv2.imshow('Decoded', decoded_img)
        cv2.waitKey(1)



'''
 
# show image
#cv2.imshow('Decoded', decoded_img)
#cv2.waitKey(0)