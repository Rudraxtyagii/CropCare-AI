# Technical Report: CropCare AI

## 1. Introduction
CropCare AI is an end-to-end Machine Learning application designed to detect and classify plant diseases from leaf images. Early detection of plant diseases is critical for reducing crop losses, improving agricultural productivity, and ensuring food security. 

## 2. Engineering Justification

### 2.1 Problem Selection
**Justification:** The project targets the "Agriculture & Intelligent Supply Chains" track. According to the Food and Agriculture Organization (FAO), plant diseases cost the global economy billions annually. Automating the detection of these diseases using computer vision significantly accelerates the diagnosis process, enabling farmers to take preventive measures promptly.

### 2.2 Dataset Selection
**Dataset:** PlantVillage Dataset (Huggingface / Kaggle)
**Justification:** PlantVillage is a widely recognized standard benchmark in agricultural AI. It contains over 50,000 images of healthy and diseased leaves spanning 14 crop species and 38 classes, providing a robust, diverse, and well-labeled foundation for training a supervised computer vision model.

### 2.3 Data Preprocessing
**Techniques Used:** Resizing (224x224), Center Cropping, Normalization, Random Horizontal Flips (Augmentation).
**Justification:** 
- Resizing to 224x224 matches the input dimensions expected by the chosen CNN architecture (MobileNetV2).
- Normalization using ImageNet statistics ensures faster convergence during transfer learning.
- Data augmentation (flips, random crops) mitigates overfitting and improves the model's ability to generalize to images taken in varying conditions.

### 2.4 Model Selection
**Model:** MobileNetV2 (Transfer Learning via PyTorch)
**Justification:** While heavier models like ResNet50 or EfficientNet might yield slightly higher raw accuracy, MobileNetV2 is specifically designed for mobile and resource-constrained environments. It provides an optimal trade-off between inference speed, model size, and accuracy, making it highly suitable for a real-time web application or potential future deployment on edge devices. Transfer learning leverages pre-trained weights from ImageNet to achieve high accuracy with a fraction of the computational cost and training time.

### 2.5 Technology Stack
**Justification:**
- **AI/ML:** PyTorch and TorchVision. PyTorch offers dynamic computational graphs and extensive support for computer vision tasks, making prototyping and debugging highly efficient.
- **Backend:** FastAPI. It is built on modern Python features (asyncio) and provides extremely fast request handling, automatic data validation (Pydantic), and out-of-the-box API documentation (Swagger UI).
- **Frontend:** Vanilla HTML, CSS, and JS. To meet the stringent aesthetic requirements (glassmorphism, micro-animations) without the overhead of heavy frameworks, vanilla web technologies provide maximum control over the DOM and styles, ensuring a highly responsive and visually stunning interface.

### 2.6 Evaluation Metrics
**Metrics:** Accuracy and Cross-Entropy Loss
**Justification:** Given the multi-class nature of the dataset (38 classes), Cross-Entropy Loss is the standard objective function. Top-1 Accuracy is the primary metric to evaluate whether the model correctly identified the exact disease, providing a clear, interpretable measure of performance.

### 2.7 System Architecture
**Architecture:** Client-Server Monolith (decoupled layers)
**Justification:** 
- The Frontend layer operates in the browser and sends asynchronous HTTP POST requests containing multipart form-data (images).
- The Backend API receives the image, loads it into memory, and passes the byte stream to the PyTorch inference module.
- The Inference Module transforms the byte stream into a normalized tensor, performs a forward pass, and returns the top predicted class and confidence score to the API.
- The API responds with JSON, which the frontend renders dynamically.
This decoupled approach ensures that the ML model, backend server, and frontend UI can be scaled, maintained, or replaced independently.

## 3. Implementation Details
The project is organized into modular components:
1. `model/`: Contains `train.py` for fine-tuning MobileNetV2, and `inference.py` for handling predictions.
2. `backend/`: Contains `main.py`, a FastAPI application handling routing, CORS, and HTTP request parsing.
3. `frontend/`: Contains the presentation logic with extensive use of CSS transitions, blur filters, and asynchronous JavaScript `fetch()` API calls.

## 4. Conclusion
CropCare AI successfully demonstrates the end-to-end lifecycle of an AI application. From problem identification to model training, API integration, and frontend presentation, it fulfills all major project requirements while delivering a premium user experience and solving a tangible real-world problem in the agricultural domain.
