import pytesseract
from PIL import Image
from transformers import pipeline
import cv2

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, theshold = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    preprocess_image_path = "/".join(image_path.split('/')[:-1]) + "/preprocessed_" + image_path.split('/')[-1]
    print(preprocess_image_path)
    cv2.imwrite(preprocess_image_path, theshold)
    return preprocess_image_path

def extract_text_from_image(image_path):
    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
    print(pytesseract.pytesseract.tesseract_cmd)
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    pytesseract.imag
    return text

def main():
    image_path = "F:/Python3/ILT/Screenshot_2025-04-23-15-48-23-68.jpg"
    preprocessed_image = preprocess_image(image_path)
    extracted_text = extract_text_from_image(preprocessed_image)
    print(f"Extracted text: \n{extracted_text}")

main()