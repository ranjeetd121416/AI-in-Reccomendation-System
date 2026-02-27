import cv2
import numpy as np
import base64
from tensorflow.keras.models import load_model
import os

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "emotion_model.h5")

emotion_model = load_model(MODEL_PATH, compile=False)

emotion_labels = [
    "angry",
    "disgust",
    "fear",
    "happy",
    "sad",
    "surprise",
    "neutral"
]

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_mood(base64_image: str | None = None):

    if base64_image is None:
        return "neutral"

    try:
        # Decode image
        image_data = base64.b64decode(base64_image.split(",")[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Improved face detection
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(30, 30)
        )

        if len(faces) == 0:
            print("No face detected.")
            return "neutral"

        (x, y, w, h) = faces[0]
        face = gray[y:y+h, x:x+w]

        face = cv2.resize(face, (48, 48))
        face = face / 255.0
        face = np.reshape(face, (1, 48, 48, 1))

        prediction = emotion_model.predict(face, verbose=0)

        print("Raw prediction:", prediction)

        mood_index = np.argmax(prediction)
        mood = emotion_labels[mood_index]

        print("Detected mood:", mood)

        return mood

    except Exception as e:
        print("Emotion detection error:", e)
        return "neutral"