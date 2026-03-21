import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Load Dataset (Using TensorFlow built-in dataset for Cats vs Dogs)
(train_ds, val_ds) = tf.keras.utils.image_dataset_from_directory(
    "path_to_train_folder",  # E.g., ./cats_vs_dogs/train
    validation_split=0.2,
    subset="both",
    seed=123,
    image_size=(180, 180),
    batch_size=32,
)

# 2. Build CNN Model
model = models.Sequential([
    layers.Rescaling(1./255, input_shape=(180, 180, 3)),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(128, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Binary classification
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 3. Train Model
model.fit(train_ds, validation_data=val_ds, epochs=5)

# 4. Save Model
model.save("cats_dogs_classifier.h5")

# 5. Predict New Image
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(180, 180))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

    prediction = model.predict(img_array)
    class_label = "Dog" if prediction[0][0] > 0.5 else "Cat"

    plt.imshow(img)
    plt.title(f"Predicted: {class_label}")
    plt.axis('off')
    plt.show()
    print(f"Prediction Score: {prediction[0][0]:.4f} ({class_label})")

# Example usage
# predict_image("path_to_new_image.jpg")