# from flask import Flask, render_template, request, redirect, url_for, jsonify
# import cv2
# import os
# import uuid

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['CROPPED_FOLDER'] = 'static/'

# def detect_face(image_path):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     if face_cascade.empty():
#         print("Error: Cascade classifier not loaded properly.")
#     # Handle the error (e.g., raise an exception, log the error, etc.)

#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
#     if len(faces) > 0:
#         (x, y, w, h) = faces[0]
#         return (x, y, w, h)
#     else:
#         return None

# def crop_centered(image_path, crop_ratio, height_percent=50, width_percent=50):
#     face = detect_face(image_path)
#     if face is not None:
#         img = cv2.imread(image_path)
#         height, width = img.shape[:2]
#         x, y, w, h = face
#         center_x = x + w // 2
#         center_y = y + h // 2

#         crop_width, crop_height = 0, 0

#         if crop_ratio == '4:3':
#             crop_width = min(width, int(4 / 3 * height))
#             crop_height = min(height, int(3 / 4 * width))
#         # Add other crop ratio conditions similarly
        
#         # Calculate cropped dimensions based on the percentages
#         crop_width = min(width, int(width * width_percent / 100))
#         crop_height = min(height, int(height * height_percent / 100))

#         x1 = max(0, center_x - crop_width // 2)
#         y1 = max(0, center_y - crop_height // 2)
#         x2 = min(width, center_x + crop_width // 2)
#         y2 = min(height, center_y + crop_height // 2)

#         cropped_img = img[y1:y2, x1:x2]
#         cropped_filename = f'cropped_{str(uuid.uuid4())}.jpg'
#         cropped_path = os.path.join(app.config['CROPPED_FOLDER'], cropped_filename)
#         cv2.imwrite(cropped_path, cropped_img)
#         return cropped_filename
#     else:
#         return None



# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(file_path)
#             crop_ratio = request.form['crop_ratio']
#             cropped_filename = crop_centered(file_path, crop_ratio)
#             if cropped_filename:
#                 cropped_image = url_for('static', filename=cropped_filename)
#                 return render_template('crop.html', cropped_image=cropped_image)
#             else:
#                 return "No face detected in the image or an error occurred."
#     return render_template('crop.html', cropped_image=None)

# @app.route('/update_frame', methods=['POST'])
# def update_frame():
#     if request.method == 'POST':
#         file = request.files['file']
#         height_percent = int(request.form['height'])
#         width_percent = int(request.form['width'])
        
#         if file:
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(file_path)
#             crop_ratio = request.form['crop_ratio']
#             cropped_filename = crop_centered(file_path, crop_ratio, height_percent, width_percent)
#             if cropped_filename:
#                 cropped_image = url_for('static', filename=cropped_filename)
#                 return jsonify({'cropped_image': cropped_image})
#     return jsonify({'error': 'Error processing the image'})

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['CROPPED_FOLDER'] = 'static/'

def detect_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Error: Cascade classifier not loaded properly.")
    # Handle the error (e.g., raise an exception, log the error, etc.)

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        return (x, y, w, h)
    else:
        return None

def crop_centered(image_path, crop_ratio):
    face = detect_face(image_path)
    if face is not None:
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        x, y, w, h = face
        center_x = x + w // 2
        center_y = y + h // 2

        crop_width, crop_height = 0, 0

        if crop_ratio == '4:3':
            crop_width = min(width, int(4 / 3 * height))
            crop_height = min(height, int(3 / 4 * width))
        elif crop_ratio == '16:9':
            crop_width = min(width, int(16 / 9 * height))
            crop_height = min(height, int(9 / 16 * width))
        elif crop_ratio == '5:4':
            crop_width = min(width, int(5 / 4 * height))
            crop_height = min(height, int(4 / 5 * width))

        # Add more ratio cases as needed

        x1 = max(0, center_x - crop_width // 2)
        y1 = max(0, center_y - crop_height // 2)
        x2 = min(width, center_x + crop_width // 2)
        y2 = min(height, center_y + crop_height // 2)

        cropped_img = img[y1:y2, x1:x2]
        cropped_filename = f'cropped_{str(uuid.uuid4())}.jpg'
        cropped_path = os.path.join(app.config['CROPPED_FOLDER'], cropped_filename)
        cv2.imwrite(cropped_path, cropped_img)
        return cropped_filename
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            crop_ratio = request.form['crop_ratio']
            cropped_filename = crop_centered(file_path, crop_ratio)
            if cropped_filename:
                cropped_image = url_for('static', filename=cropped_filename)
                return render_template('crop.html', cropped_image=cropped_image)
            else:
                return "No face detected in the image or an error occurred."
    return render_template('crop.html', cropped_image=None)




@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            crop_ratio = request.form['crop_ratio']
            cropped_filename = crop_centered(file_path, crop_ratio)
            if cropped_filename:
                cropped_image = url_for('static', filename=cropped_filename)
                return redirect(url_for('show_cropped', filename=cropped_filename))
            else:
                return "No face detected in the image or an error occurred."
    return render_template('index.html', cropped_image=None)

@app.route('/show_cropped/<filename>')
def show_cropped(filename):
    cropped_image = url_for('static', filename=filename)
    return render_template('cropped.html', cropped_image=cropped_image)



if __name__ == '__main__':
    app.run(debug=True)





