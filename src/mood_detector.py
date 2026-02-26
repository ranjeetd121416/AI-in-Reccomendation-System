import cv2
from deepface import DeepFace

def detect_mood():

    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        return "neutral"

    try:
        result = DeepFace.analyze(
            frame,
            actions=["emotion"],
            enforce_detection=False
        )
        return result[0]["dominant_emotion"]

    except:
        return "neutral"