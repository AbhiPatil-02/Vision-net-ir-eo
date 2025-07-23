# import os
# import random
# from ultralytics import YOLO
# from PIL import Image as PILImage # Renamed to avoid conflict with IPython.display.Image
# import cv2
# import mimetypes
# import shutil # For moving files and directories
# from IPython.display import display, Image # Import display and Image from IPython

# # Load the trained model
# model = YOLO(r"C:\Users\SANSKAR M  MUDNUR\OneDrive\Desktop\TEMP\Data\Webpage\model\weights\best.pt")

# # Base directory for saving all outputs
# output_base_dir = r"C:\Users\SANSKAR M  MUDNUR\OneDrive\Desktop\TEMP\Data\Webpage\predictions"

# os.makedirs(output_base_dir, exist_ok=True)

# def process_image(image_path, output_dir):
#     """Processes an image: converts to JPG if needed, saves, and returns the path."""
#     try:
#         img = PILImage.open(image_path)
#         base_name = os.path.splitext(os.path.basename(image_path))[0]
#         output_image_path = os.path.join(output_dir, f"{base_name}.jpg")

#         if img.format.lower() != 'jpeg':
#             print(f"Converting {image_path} to JPEG...")
#             # Convert to RGB mode before saving as JPEG to handle different modes (e.g., RGBA)
#             if img.mode != 'RGB':
#                 img = img.convert('RGB')
#             img.save(output_image_path, "JPEG")
#             print(f"Converted image saved to: {output_image_path}")
#         else:
#             # If already JPEG, just copy it to the output directory
#             shutil.copy(image_path, output_image_path)
#             print(f"Image already JPEG, copied to: {output_image_path}")
#         return [output_image_path] # Return as a list for consistent processing
#     except Exception as e:
#         print(f"Error processing image {image_path}: {e}")
#         return []

# def process_video(video_path, output_dir, target_fps=2, duration_seconds=30):
#     """Extracts frames from the first 30 seconds of a video at 2 FPS."""
#     extracted_image_paths = []
#     cap = cv2.VideoCapture(video_path)

#     if not cap.isOpened():
#         print(f"Error: Could not open video {video_path}")
#         return []

#     original_fps = cap.get(cv2.CAP_PROP_FPS)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     video_duration = total_frames / original_fps

#     print(f"Video: {video_path}, Original FPS: {original_fps}, Duration: {video_duration:.2f} seconds")

#     if original_fps == 0:
#         print("Warning: Video has 0 FPS, cannot extract frames.")
#         cap.release()
#         return []

#     # Calculate the frame interval to achieve target_fps
#     frame_interval = max(1, int(original_fps / target_fps)) # Ensure at least 1

#     frames_to_extract = int(target_fps * min(duration_seconds, video_duration))
#     print(f"Attempting to extract {frames_to_extract} frames at {target_fps} FPS for the first {min(duration_seconds, video_duration):.2f} seconds.")

#     frame_count = 0
#     saved_frame_count = 0

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Stop after the desired duration
#         current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
#         if current_time_ms / 1000 > duration_seconds:
#             break

#         if frame_count % frame_interval == 0:
#             frame_filename = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_{saved_frame_count + 1}.jpg")
#             cv2.imwrite(frame_filename, frame)
#             extracted_image_paths.append(frame_filename)
#             saved_frame_count += 1

#         frame_count += 1

#     cap.release()
#     print(f"Extracted {saved_frame_count} frames from video and saved to: {output_dir}")
#     return extracted_image_paths

# # Main script execution
# if __name__ == "__main__":
#     while True:
#         input_file_path = input("Please upload an image or video file path (or type 'exit' to quit): ").strip()

#         if input_file_path.lower() == 'exit':
#             break

#         if not os.path.exists(input_file_path):
#             print("File not found. Please enter a valid path.")
#             continue

#         file_type, _ = mimetypes.guess_type(input_file_path)

#         if file_type and file_type.startswith('image'):
#             print(f"Detected image file: {input_file_path}")

#             # Create a specific directory for this input file's processing
#             input_basename = os.path.splitext(os.path.basename(input_file_path))[0]
#             current_output_dir = os.path.join(output_base_dir, input_basename)
#             os.makedirs(current_output_dir, exist_ok=True)

#             processed_files = process_image(input_file_path, current_output_dir)

#         elif file_type and file_type.startswith('video'):
#             print(f"Detected video file: {input_file_path}")

#             # Create a specific directory for this input file's processing
#             input_basename = os.path.splitext(os.path.basename(input_file_path))[0]
#             current_output_dir = os.path.join(output_base_dir, input_basename)
#             os.makedirs(current_output_dir, exist_ok=True)

#             processed_files = process_video(input_file_path, current_output_dir)

#         else:
#             print(f"Unsupported file type: {input_file_path}. Please provide an image or video.")
#             continue

#         if not processed_files:
#             print("No images were processed for inference.")
#             continue

#         print(f"Running inference on {len(processed_files)} processed image(s)...")
#         results = model(processed_files, save=True, project=current_output_dir, name="predicted_results", exist_ok=True) # save=True will save annotated images

#         # YOLOv8 typically saves results in a 'runs/detect/predictX' folder.
#         # We need to find this folder and rename it.
#         yolo_runs_dir = os.path.join(current_output_dir, 'predicted_results')

#         # Find the actual prediction folder created by YOLOv8 (e.g., 'predict', 'predict2', etc.)
#         actual_prediction_folders = [d for d in os.listdir(yolo_runs_dir) if os.path.isdir(os.path.join(yolo_runs_dir, d)) and d.startswith('predict')]

#         final_prediction_path = None # Initialize to None

#         if actual_prediction_folders:
#             # Assuming YOLOv8 creates only one such folder for a single run
#             yolo_output_folder = os.path.join(yolo_runs_dir, actual_prediction_folders[0])

#             # Rename the folder to 'predicted_inputfilename'
#             new_prediction_folder_name = f"predicted_{input_basename}"
#             final_prediction_path = os.path.join(current_output_dir, new_prediction_folder_name)

#             if os.path.exists(final_prediction_path):
#                 # If a folder with the desired name already exists, remove it before renaming
#                 shutil.rmtree(final_prediction_path)

#             shutil.move(yolo_output_folder, final_prediction_path)
#             print(f"Predicted results saved to: {final_prediction_path}")

#             # --- Display Results Here ---
#             print("\n--- Displaying Predicted Results ---")
#             if os.path.isdir(final_prediction_path):
#                 predicted_images = [f for f in os.listdir(final_prediction_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
#                 predicted_images.sort() # Sort to display in a consistent order
#                 if predicted_images:
#                     for img_name in predicted_images:
#                         img_path_to_display = os.path.join(final_prediction_path, img_name)
#                         print(f"Displaying: {img_path_to_display}")
#                         try:
#                             display(Image(filename=img_path_to_display, width=600)) # Adjust width as needed
#                         except Exception as e:
#                             print(f"Could not display image {img_name}: {e}")
#                 else:
#                     print("No predicted images found in the output directory to display.")
#             else:
#                 print("Final prediction path does not exist, cannot display results.")
#             # --- End Display Results ---

#         else:
#             print(f"Could not find YOLOv8 prediction output folder in {yolo_runs_dir}. Results might not have been saved correctly.")

#         print("-" * 50) # Separator for next input


import os
import random
from ultralytics import YOLO
from PIL import Image as PILImage
import cv2
import mimetypes
import shutil

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
        print(f"Error processing image: {e}")
        return []

def process_video(video_path, output_dir, target_fps=2, duration_seconds=30):
    extracted_image_paths = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return []

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / original_fps if original_fps else 0

    frame_interval = max(1, int(original_fps / target_fps)) if original_fps else 1
    frames_to_extract = int(target_fps * min(duration_seconds, video_duration))

    frame_count = 0
    saved_frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        if current_time_ms / 1000 > duration_seconds:
            break

        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_{saved_frame_count + 1}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_image_paths.append(frame_filename)
            saved_frame_count += 1

        frame_count += 1

    cap.release()
    return extracted_image_paths

def run_detection(input_file_path):
    model = YOLO(r"C:\Users\SANSKAR M  MUDNUR\OneDrive\Desktop\TEMP\Data\Webpage\model\weights\best.pt")
    output_base_dir = "predictions"
    os.makedirs(output_base_dir, exist_ok=True)

    file_type, _ = mimetypes.guess_type(input_file_path)
    input_basename = os.path.splitext(os.path.basename(input_file_path))[0]
    current_output_dir = os.path.join(output_base_dir, input_basename)
    os.makedirs(current_output_dir, exist_ok=True)

    if file_type and file_type.startswith('image'):
        processed_files = process_image(input_file_path, current_output_dir)
    elif file_type and file_type.startswith('video'):
        processed_files = process_video(input_file_path, current_output_dir)
    else:
        return "Unsupported file format"

    if not processed_files:
        return "No images processed"

    results = model(processed_files, save=True, project=current_output_dir, name="predicted_results", exist_ok=True)
    yolo_runs_dir = os.path.join(current_output_dir, 'predicted_results')

    actual_prediction_folders = [
        d for d in os.listdir(yolo_runs_dir)
        if os.path.isdir(os.path.join(yolo_runs_dir, d)) and d.startswith('predict')
    ]

    if actual_prediction_folders:
        yolo_output_folder = os.path.join(yolo_runs_dir, actual_prediction_folders[0])
        new_prediction_folder_name = f"predicted_{input_basename}"
        final_prediction_path = os.path.join(current_output_dir, new_prediction_folder_name)

        if os.path.exists(final_prediction_path):
            shutil.rmtree(final_prediction_path)

        shutil.move(yolo_output_folder, final_prediction_path)
        return final_prediction_path
    else:
        return "Prediction failed or output not found"
