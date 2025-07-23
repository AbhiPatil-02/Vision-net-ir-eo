# import os
# import random
# import shutil
# import mimetypes
# from flask import Flask, request, redirect, url_for, render_template, send_from_directory
# from werkzeug.utils import secure_filename
# from ultralytics import YOLO
# from PIL import Image as PILImage
# import cv2

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['PREDICTION_FOLDER'] = 'predictions'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'}

# # Load YOLO model
# model_path = os.path.join(os.path.dirname(__file__), "model", "weights", "best.pt")
# model = YOLO(model_path)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def process_image(image_path, output_dir):
#     try:
#         img = PILImage.open(image_path)
#         base_name = os.path.splitext(os.path.basename(image_path))[0]
#         output_image_path = os.path.join(output_dir, f"{base_name}.jpg")

#         if img.format.lower() != 'jpeg':
#             if img.mode != 'RGB':
#                 img = img.convert('RGB')
#             img.save(output_image_path, "JPEG")
#         else:
#             shutil.copy(image_path, output_image_path)
#         return [output_image_path]
#     except Exception as e:
#         print(f"Image processing error: {e}")
#         return []

# def process_video(video_path, output_dir, target_fps=2, duration_seconds=30):
#     extracted_image_paths = []
#     cap = cv2.VideoCapture(video_path)

#     if not cap.isOpened():
#         return []

#     original_fps = cap.get(cv2.CAP_PROP_FPS)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     video_duration = total_frames / original_fps if original_fps else 0

#     frame_interval = max(1, int(original_fps / target_fps))
#     frames_to_extract = int(target_fps * min(duration_seconds, video_duration))

#     frame_count = 0
#     saved_frame_count = 0

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 > duration_seconds:
#             break
#         if frame_count % frame_interval == 0:
#             frame_filename = os.path.join(output_dir, f"frame_{saved_frame_count + 1}.jpg")
#             cv2.imwrite(frame_filename, frame)
#             extracted_image_paths.append(frame_filename)
#             saved_frame_count += 1
#         frame_count += 1

#     cap.release()
#     return extracted_image_paths

# @app.route('/')
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return "No file part", 400
#         file = request.files['file']
#         if file.filename == '':
#             return "No selected file", 400
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#             file.save(input_path)

#             base_name = os.path.splitext(filename)[0]
#             output_dir = os.path.join(app.config['PREDICTION_FOLDER'], base_name)
#             os.makedirs(output_dir, exist_ok=True)

#             file_type, _ = mimetypes.guess_type(input_path)
#             if file_type and file_type.startswith('image'):
#                 processed = process_image(input_path, output_dir)
#             elif file_type and file_type.startswith('video'):
#                 processed = process_video(input_path, output_dir)
#             else:
#                 return "Unsupported file type", 400

#             if not processed:
#                 return "No frames/images processed", 500

#             results = model(processed, save=True, project=output_dir, name="predicted_results", exist_ok=True)
#             pred_dir = os.path.join(output_dir, "predicted_results")
#             final_folder = os.path.join(output_dir, f"predicted_{base_name}")
#             if os.path.exists(final_folder):
#                 shutil.rmtree(final_folder)
#             shutil.move(pred_dir, final_folder)

#             result_images = [img for img in os.listdir(final_folder) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
#             return render_template("result.html", images=result_images, folder=f"{base_name}/predicted_{base_name}")

#     return render_template('upload.html')

# @app.route('/predictions/<path:folder>/<filename>')
# def serve_prediction_image(folder, filename):
#     return send_from_directory(os.path.join(app.config['PREDICTION_FOLDER'], folder), filename)

# if __name__ == '__main__':
#     app.run(debug=True)



import os
import shutil
import mimetypes
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from PIL import Image as PILImage
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PREDICTION_FOLDER'] = 'predictions'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'}

# Load YOLO model
model_path = os.path.join(os.path.dirname(__file__), "model", "weights", "best_13.pt")
model = YOLO(model_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path, output_dir):
    try:
        img = PILImage.open(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_image_path = os.path.join(output_dir, f"{base_name}.jpg")

        if img.format.lower() != 'jpeg':
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output_image_path, "JPEG")
        else:
            shutil.copy(image_path, output_image_path)
        return [output_image_path]
    except Exception as e:
        print(f"Image processing error: {e}")
        return []

def process_video(video_path, output_dir, target_fps=2, duration_seconds=30):
    extracted_image_paths = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return []

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / original_fps if original_fps else 0

    frame_interval = max(1, int(original_fps / target_fps))
    frames_to_extract = int(target_fps * min(duration_seconds, video_duration))

    frame_count = 0
    saved_frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 > duration_seconds:
            break
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{saved_frame_count + 1}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_image_paths.append(frame_filename)
            saved_frame_count += 1
        frame_count += 1

    cap.release()
    return extracted_image_paths

# === New Route for Index Page ===
@app.route('/')
def index():
    return render_template('index.html')

# === Existing Upload Handling Logic ===
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(input_path)

            base_name = os.path.splitext(filename)[0]
            output_dir = os.path.join(app.config['PREDICTION_FOLDER'], base_name)
            os.makedirs(output_dir, exist_ok=True)

            file_type, _ = mimetypes.guess_type(input_path)
            if file_type and file_type.startswith('image'):
                processed = process_image(input_path, output_dir)
            elif file_type and file_type.startswith('video'):
                processed = process_video(input_path, output_dir)
            else:
                return "Unsupported file type", 400

            if not processed:
                return "No frames/images processed", 500

            model(processed, save=True, project=output_dir, name="predicted_results", exist_ok=True)
            pred_dir = os.path.join(output_dir, "predicted_results")
            final_folder = os.path.join(output_dir, f"predicted_{base_name}")
            if os.path.exists(final_folder):
                shutil.rmtree(final_folder)
            shutil.move(pred_dir, final_folder)

            result_images = [
                img for img in os.listdir(final_folder)
                if img.lower().endswith(('.jpg', '.jpeg', '.png'))
            ]
            return render_template("result.html", images=result_images, folder=f"{base_name}/predicted_{base_name}")

    return render_template('upload.html')

@app.route('/predictions/<path:folder>/<filename>')
def serve_prediction_image(folder, filename):
    return send_from_directory(os.path.join(app.config['PREDICTION_FOLDER'], folder), filename)

if __name__ == '__main__':
    app.run(debug=True)
