# CropCare AI 🍃
**Production-Grade Plant Disease Detection System**

CropCare AI is a comprehensive, end-to-end artificial intelligence application designed to diagnose plant diseases from leaf images. Built as a final-year Major Project for the KIET Agriculture & Intelligent Supply Chains track, this application features a stunning glassmorphism UI, a robust FastAPI backend, and an optimized PyTorch inference pipeline capable of identifying 38 distinct crop diseases.

---

## 📸 Application Screenshot
![CropCare AI Dashboard](file:///C:/Users/ASUS/.gemini/antigravity/brain/80c2b640-c1db-41cf-bb9f-942749523115/cropcare_ui_mockup_1785157526955.jpg)

---

## 🚀 Features

### **1. AI-Powered Inference**
- Recognizes **38 different classes** (healthy and diseased) from the PlantVillage dataset.
- Uses **MobileNetV2** via transfer learning for an optimal balance of speed and accuracy.
- Precise preprocessing pipeline (Resize 256 -> CenterCrop 224 -> Tensor -> ImageNet Normalization).

### **2. Production-Ready Backend (FastAPI)**
- **Structured JSON Responses:** Returns plant name, disease, confidence, and rich metadata (description, causes, treatment, prevention).
- **Validation:** Strict file type (JPG/PNG) and file size (<5MB) validation.
- **Resilience:** Graceful exception handling and comprehensive logging.

### **3. Premium UI/UX**
- **Glassmorphism Design:** Beautiful translucent panels, animated background blobs, and sleek hover effects.
- **Upload Experience:** Drag-and-drop or click-to-upload with real-time file validation and image preview.
- **Analytics Dashboard:** Automatically tracks total scans, average confidence, and most frequent diseases across the session.
- **Local History:** Saves prediction history with image thumbnails natively in the browser.

---

## 🏗️ Architecture Diagram

```mermaid
graph TD
    A[Client Browser (HTML/JS)] -->|Upload Image (Multipart)| B(FastAPI Backend)
    B -->|Validate Image| C{Is Valid?}
    C -- No --> D[Return 400 Bad Request]
    C -- Yes --> E[PyTorch Inference Module]
    E -->|Preprocess| F[MobileNetV2 Model]
    F -->|Forward Pass| G[Class Index & Confidence]
    G --> H[Disease Knowledge Base]
    H -->|Enrich Data| I[Construct JSON Response]
    I -->|Return 200 OK| A
    A -->|Render| J[Glassmorphism Result Card & Stats]
```

---

## 📂 Folder Structure
```text
C:\major project
├── backend/
│   ├── main.py            # FastAPI server & endpoints
│   └── disease_info.py    # Knowledge base for all 38 classes
├── frontend/
│   ├── index.html         # Application layout
│   ├── styles.css         # Glassmorphism & animations
│   └── script.js          # DOM manipulation & API requests
├── model/
│   ├── train.py           # PyTorch training script
│   └── inference.py       # Production inference pipeline
├── docs/                  # Project reports and presentations
└── requirements.txt       # Python dependencies
```

---

## 🛠️ Installation & Setup

1. **Clone or Download the Repository**
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

**1. Start the Backend API**
```bash
python backend/main.py
```
*The server will start on `http://0.0.0.0:8000`. You can view the automatic Swagger documentation at `http://localhost:8000/docs`.*

**2. Start the Frontend**
Since it uses Vanilla HTML/JS/CSS, you can simply open `frontend/index.html` in your web browser, or use a local server like `Live Server` in VSCode.

*(Note: If the `plant_disease_model.pth` weights are not present in the `model/` folder, the backend automatically enters a "Mock Mode" simulating real predictions so you can test the UI and API instantly.)*

---

## 📡 API Endpoints

### `POST /predict`
Accepts an image file (multipart/form-data) and returns a detailed analysis.

**Example Response:**
```json
{
  "success": true,
  "prediction": {
    "class_name": "Tomato___Early_blight",
    "plant": "Tomato",
    "disease": "Early Blight",
    "confidence": 98.45,
    "confidence_level": "High",
    "description": "Characterized by brown spots with concentric rings (target spots) on older leaves.",
    "causes": [
      "Fungus Alternaria solani",
      "High humidity, heavy dew, plant stress"
    ],
    "treatment": [
      "Apply fungicides (e.g., chlorothalonil, mancozeb)",
      "Remove affected lower leaves"
    ],
    "prevention": [
      "Mulch around the base of the plant",
      "Stake or cage plants to keep foliage off soil"
    ],
    "is_mock": false
  }
}
```

---

## 🔮 Future Improvements
- Implement JWT authentication for user accounts.
- Connect to a PostgreSQL database to persistently store global statistics.
- Deploy the backend via Docker to AWS/GCP and serve the frontend via Vercel or Netlify.
- Integrate object detection to draw bounding boxes around the diseased areas on the leaf.
