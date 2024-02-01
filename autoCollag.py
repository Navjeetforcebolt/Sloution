import cv2
import os
import uuid
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def select_image():
    Tk().withdraw()  # Hide the Tkinter root window
    file_path = askopenfilename()  # Ask the user to select an image file
    return file_path

def detect_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Error: Cascade classifier not loaded properly.")
        return None

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        return (x, y, w, h)
    else:
        return None

def crop_to_1_2_aspect_ratio(image_path, x, y, w, h):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    center_x = x + w // 2
    center_y = y + h // 2

    crop_width = min(width, int(1 / 2 * height))
    crop_height = min(height, int(2 / 1 * width))

    x1 = max(0, center_x - crop_width // 2)
    y1 = max(0, center_y - crop_height // 2)
    x2 = min(width, center_x + crop_width // 2)
    y2 = min(height, center_y + crop_height // 2)

    cropped_img = img[y1:y2, x1:x2]
    return cropped_img

if __name__ == "__main__":
    # Select Image 1
    print("Select Image 1")
    image1_path = select_image()

    # Select Image 2
    print("Select Image 2")
    image2_path = select_image()

    # Detect faces and crop to 1:2 aspect ratio for image 1
    face1 = detect_face(image1_path)
    if face1 is not None:
        x1, y1, w1, h1 = face1
        cropped_photo1 = crop_to_1_2_aspect_ratio(image1_path, x1, y1, w1, h1)

    # Detect faces and crop to 1:2 aspect ratio for image 2
    face2 = detect_face(image2_path)
    if face2 is not None:
        x2, y2, w2, h2 = face2
        cropped_photo2 = crop_to_1_2_aspect_ratio(image2_path, x2, y2, w2, h2)

    # Combine the cropped images side by side
    # Existing code...

if face1 is not None and face2 is not None:
    # ... (existing code remains the same)

    # Resize images to have the same height
    min_height = min(cropped_photo1.shape[0], cropped_photo2.shape[0])
    cropped_photo1_resized = cv2.resize(cropped_photo1, (int(cropped_photo1.shape[1] * min_height / cropped_photo1.shape[0]), min_height))
    cropped_photo2_resized = cv2.resize(cropped_photo2, (int(cropped_photo2.shape[1] * min_height / cropped_photo2.shape[0]), min_height))

    print(f"Dimensions of cropped_photo1_resized: {cropped_photo1_resized.shape}")
    print(f"Dimensions of cropped_photo2_resized: {cropped_photo2_resized.shape}")

    combined_image = cv2.hconcat([cropped_photo1_resized, cropped_photo2_resized])

    # Save the combined image to the 'static' directory
    output_directory = 'static'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_filename = os.path.join(output_directory, 'combined_image.jpg')
    cv2.imwrite(output_filename, combined_image)
    print(f"Combined image saved to {output_filename}")
else:
    print("Face not detected in one or both images.")



