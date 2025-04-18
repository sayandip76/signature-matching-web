# ✍️ Signature Matching Web App

A web-based signature verification system that compares two signatures using image processing techniques like SSIM (Structural Similarity Index) and contour matching. Built using **FastAPI** for the backend and **HTML/CSS/JavaScript + Bootstrap** for a smooth and responsive frontend.

---

## 📌 Features

- Upload or capture two signature images
- View signature image previews instantly
- Intelligent similarity scoring using SSIM and shape matching
- Visual debugging of normalized and processed signatures
- Easy-to-use web interface with Bootstrap styling

---

## 💠 Tech Stack

### 🔹 Frontend

- HTML5 / CSS3
- JavaScript (vanilla)
- [Bootstrap 5](https://getbootstrap.com/) for responsive UI

### 🔹 Backend

- [FastAPI](https://fastapi.tiangolo.com/) for building the REST API
- [OpenCV](https://opencv.org/) for image processing and computer vision
- [scikit-image](https://scikit-image.org/) for SSIM similarity scoring
- `uvicorn` as ASGI server

---

## 🚀 How to Run the App Locally

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/signature-matcher.git
cd signature-matcher
```

### 2. Set Up Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
npm i
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

### 5. Access the Web App

Open your browser and go to:

```
http://127.0.0.1:8000
```

---

## 🖼️ How to Use

1. Upload two signature images (JPEG/PNG).
2. Preview them before comparing.
3. Click **Compare**.
4. The result shows how similar they are based on both:
   - Visual similarity (SSIM)
   - Shape similarity (contour-based)
5. Debug output and processed images are saved in `debug_ss/` for inspection.

---

## 📁 Folder Structure

```
├── main.py                # FastAPI backend
├── signature.py           # Image processing and comparison logic
├── static/
│   ├── index.html         # Web frontend
│   ├── script.js          # JS logic for upload and preview
│   ├── styles.css         # Optional custom styling
├── debug_ss/              # Saves intermediate image processing steps
├── requirements.txt       # Python dependencies
```

---

## 📌 To-Do / Future Features

- ✅ Webcam capture support
- ☑️ Save match history to a database
- ☑️ Admin interface for signature verification logs
- ☑️ Deep learning-based matching using Siamese networks

---

## 🧑‍💻 Author

Developed by [Sayandip Kar]\
Inspired by real-world signature verification problems.

