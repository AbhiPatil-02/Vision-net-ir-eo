# 🛰️ EO/IR Image & Video Classification for Military and Surveillance

---

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Objective](#objective)
- [Features](#features)
- [How to Run](#how-to-run)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

---

## 📁 Project Overview
This project provides a rapid classification system for **Electro-Optical (EO)** and **Infrared (IR)** imagery, primarily designed for military and surveillance applications. Leveraging a fine-tuned **YOLOv8** object detection model, the system accurately identifies key targets such as:

- 👤 Personnel
- 🚙 Vehicles
- 🛡️ Armored Units
- ✈️ Aircraft
- 🔫 Weapons

The application includes a clean, user-friendly web interface built with **Streamlit**, enabling image and video file uploads with real-time annotated detection results.

---

## 🎯 Objective
The primary goal is to enhance **real-time situational awareness** and support **critical decision-making** in defense and surveillance environments. It focuses on EO/IR image interpretation under challenging conditions such as:

- 🌙 Low-light or night operations
- 🌲 Camouflaged terrains
- 🌫️ Visual obstructions (fog, smoke, haze)

---

## ✨ Features

- 🔍 **Image Classification**
  Upload EO/IR images and detect military-relevant targets.

- 🎞️ **Video Frame Analysis**
  Automatically extract and process frames (2 FPS for first 30 seconds).

- 🧠 **YOLOv8 Model**
  Fine-tuned custom-trained object detection for high accuracy.

- 🌐 **Streamlit Web UI**
  Drag-and-drop interface for uploading files and viewing results.

- ☁️ **Google Drive Integration**
  Seamless use in Google Colab for model loading and saving outputs.

---

## 🛠️ How to Run

### 📥 1. Clone the Repository
<pre>
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
</pre>

### ▶️ 2. Run the Streamlit App

**In Google Colab:**
<pre>
!streamlit run /content/drive/MyDrive/HAL_HACKTHON/abhi/streamlit_app.py &>/dev/null&
</pre>

**Locally:**
<pre>
python3 app.py
</pre>

---

## 🧪 Usage
1. Click “Choose an image or video file” in the UI to upload a file (`.jpg`, `.jpeg`, `.png`, `.mp4`, `.avi`, `.mov`, `.webm`).
2. A preview of the image or video will appear.
3. Click the 🚀 **Run Prediction** button.
4. View the output with bounding boxes and labels rendered directly in the app.

---

## 🤝 Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:
<pre>
git checkout -b feature/your-feature-name
</pre>
3. Make your changes.
4. Commit your changes:
<pre>
git commit -m "Add new feature"
</pre>
5. Push to the branch:
<pre>
git push origin feature/your-feature-name
</pre>
6. Open a Pull Request.

---

## 📬 Contact
For questions, issues, or collaborations, feel free to:

- Open an issue on GitHub.
- Contact: abhipatilrcb@gmail.com
