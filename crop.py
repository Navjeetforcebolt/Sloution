from flask import Flask, render_template, request, redirect, url_for, jsonify
import cv2
import os
import numpy as np
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['CROPPED_FOLDER'] = 'static/'

# Function to crop the image based on specified dimensions
def crop_image(image_path, top, bottom, left, right):
    try:
        img = cv2.imread(image_path)
        height, width = img.shape[:2]

        # Calculate the intersection points of the four lines
        top_x = int((left * width) / 100)
        top_y = int((top * height) / 100)
        bottom_x = int((right * width) / 100)
        bottom_y = int((bottom * height) / 100)

        # Ensure the points are within the image bounds
        top_x = max(0, min(top_x, width))
        top_y = max(0, min(top_y, height))
        bottom_x = max(0, min(bottom_x, width))
        bottom_y = max(0, min(bottom_y, height))

        # Crop the square defined by the intersection points
        cropped_img = img[top_y:bottom_y, top_x:bottom_x]

        cropped_filename = f'cropped_{str(uuid.uuid4())}.jpg'
        cropped_path = os.path.join(app.config['CROPPED_FOLDER'], cropped_filename)
        cv2.imwrite(cropped_path, cropped_img)
        return cropped_filename
    except Exception as e:
        print(f"Error cropping image: {e}")
        return None


# Function to save cropped image from frontend
def save_cropped_image(cropped_image_data):
    try:
        nparr = np.frombuffer(cropped_image_data, np.uint8)
        cropped_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if cropped_image is None or cropped_image.size == 0:  # Check if the image is empty
            raise ValueError("Empty or invalid image data")

        cropped_filename = f'cropped_{str(uuid.uuid4())}.jpg'
        cropped_path = os.path.join(app.config['CROPPED_FOLDER'], cropped_filename)
        cv2.imwrite(cropped_path, cropped_image)
        return cropped_filename
    except Exception as e:
        print(f"Error saving cropped image: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            cropped_filename = crop_image(file_path)
            if cropped_filename:
                cropped_image = url_for('static', filename=cropped_filename)
                return render_template('index.html', cropped_image=cropped_image)
            else:
                return "Error cropping the image."
    return render_template('index.html', cropped_image=None)

@app.route('/update_frame', methods=['POST'])
def update_frame():
    if request.method == 'POST':
        try:
            file = request.files['file']
            top = int(request.form['top'])
            bottom = int(request.form['bottom'])
            left = int(request.form['left'])
            right = int(request.form['right'])

            if file:
                file_data = file.read()
                cropped_filename = crop_image(file_data, top, bottom, left, right)

                if cropped_filename:
                    cropped_image = url_for('static', filename=cropped_filename)
                    return jsonify({'cropped_image': cropped_image})
        except Exception as e:
            print(f"Error processing the image: {e}")

    return jsonify({'error': 'Error processing the image'})



if __name__ == '__main__':
    app.run(debug=True)
