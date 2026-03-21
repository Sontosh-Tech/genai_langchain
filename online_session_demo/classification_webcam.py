import cv2
import numpy as np
import tensorflow as tf

# Load pretrained MobileNetV2 model (fine-tuned for emotion detection)
# You must have a trained model; for now, assuming it's saved as 'emotion_mobilenetv2.h5'
model = tf.keras.models.load_model('F:/Python3/ILT/emotion_mobilenetv2.h5')

# Emotion labels (adjust depending on your dataset)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Load face detector (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (224, 224))
        face = face / 255.0
        face = np.expand_dims(face, axis=0)

        # Predict emotion
        preds = model.predict(face)
        emotion = emotion_labels[np.argmax(preds)]

        # Draw rectangle and emotion label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    cv2.imshow('Emotion Detection', frame)

    # Exit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()