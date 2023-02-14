import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()
cap = cv2.VideoCapture(0)

def PoseCordGetter(landmark,*axis):
    x = pose_cords[0].landmark[landmark].x
    y = pose_cords[0].landmark[landmark].y
    if axis[0].lower() == "x":
        return x
    if axis[0].lower() == "y":
        return y
    return [x, y]
def FaceCordGetter(landmark,*axis):
    x = face_cords[0].landmark[landmark].x
    y = face_cords[0].landmark[landmark].y
    if axis[0].lower() == "x":
        return x
    if axis[0].lower() == "y":
        return y
    return [x, y]
def MediaPipeDraw():
    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())


while True:
    success, image = cap.read()
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(imgRGB)
    pose_cords = results.pose_landmarks
    face_cords = results.face_landmarks
    MediaPipeDraw()
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
