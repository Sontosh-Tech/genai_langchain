import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

train_dir = 'F:/Python3/ILT/archive_small/train'
test_dir = 'F:/Python3/ILT/archive_small/test'

img_size = 224  # MobileNetV2 expects 224x224
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

num_classes = train_generator.num_classes

# -----------------------
# Step 3: Load MobileNetV2 Base
# -----------------------
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(img_size, img_size, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False  # Freeze base initially

# -----------------------
# Step 4: Build Model
# -----------------------
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(model.summary())

# -----------------------
# Step 5: Train Model
# -----------------------
epochs = 5

history = model.fit(
    train_generator,
    validation_data=test_generator,
    epochs=epochs
)

# -----------------------
# Step 6: Fine-tune (Unfreeze part of MobileNetV2)
# -----------------------
base_model.trainable = True

# Fine-tune from this layer onwards
fine_tune_at = 100

for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

fine_tune_epochs = 3

history_fine = model.fit(
    train_generator,
    validation_data=test_generator,
    epochs=fine_tune_epochs
)

# -----------------------
# Step 7: Save Model
# -----------------------
model.save('F:/Python3/ILT/emotion_mobilenetv2.h5')
print("✅ Model saved as emotion_mobilenetv2.h5")