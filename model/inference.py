import sys
try:
    import torch
    import torch.nn as nn
    from torchvision import models, transforms
except ImportError:
    from unittest.mock import MagicMock
    sys.modules['torch'] = MagicMock()
    sys.modules['torch.nn'] = MagicMock()
    sys.modules['torchvision'] = MagicMock()
    sys.modules['torchvision.models'] = MagicMock()
    sys.modules['torchvision.transforms'] = MagicMock()
    import torch
    import torch.nn as nn
    from torchvision import models, transforms
from PIL import Image, UnidentifiedImageError
import os
import random
import logging
import io

# Setup logger for inference module
logger = logging.getLogger("CropCare-Inference")

MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), 'plant_disease_model.pth')
NUM_CLASSES = 38

# Default classes representing the 38 classes of the PlantVillage dataset
DEFAULT_CLASSES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

class PlantDiseasePredictor:
    def __init__(self):
        """
        Initializes the model, defines the exact MobileNetV2 preprocessing pipeline,
        and handles falling back to a mock mode if weights are missing.
        """
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.class_names = DEFAULT_CLASSES
        self.is_mock = False
        
        # Exact preprocessing requirements for MobileNetV2 (ImageNet)
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        self._load_model()

    def _load_model(self):
        """
        Attempts to load the trained PyTorch model. 
        If the file does not exist, switches to mock mode for testing/UI validation.
        """
        if os.path.exists(MODEL_SAVE_PATH):
            logger.info(f"Loading trained model from {MODEL_SAVE_PATH}...")
            try:
                self.model = models.mobilenet_v2(pretrained=False)
                # Adjust final classifier layer to match NUM_CLASSES
                self.model.classifier[1] = nn.Linear(self.model.last_channel, NUM_CLASSES)
                
                checkpoint = torch.load(MODEL_SAVE_PATH, map_location=self.device)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.class_names = checkpoint.get('class_names', DEFAULT_CLASSES)
                
                self.model = self.model.to(self.device)
                self.model.eval()
                self.is_mock = False
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model weights: {e}")
                logger.warning("Falling back to mock prediction mode.")
                self.is_mock = True
        else:
            logger.warning(f"Trained model not found at {MODEL_SAVE_PATH}. Using mock prediction mode.")
            self.is_mock = True

    def predict(self, image_bytes):
        """
        Takes raw image bytes, validates them, applies preprocessing, 
        and returns the predicted class and confidence.
        """
        # Validate image bytes
        if not image_bytes:
            return {"error": "Empty image byte stream provided."}

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except UnidentifiedImageError:
            return {"error": "Cannot identify image file. It may be corrupted or in an unsupported format."}
        except Exception as e:
            return {"error": f"Error opening image: {str(e)}"}

        if self.is_mock:
            # Mock prediction simulating real inference delay and random outcomes
            import time
            time.sleep(1.5) # Simulate inference time
            mock_class = random.choice(self.class_names)
            confidence = random.uniform(0.65, 0.99)
            return {
                "disease": mock_class,
                "confidence": float(confidence),
                "is_mock": True
            }
            
        # Real prediction
        try:
            tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                confidence, predicted_idx = torch.max(probabilities, 0)
                
            predicted_class = self.class_names[predicted_idx.item()]
            
            return {
                "disease": predicted_class,
                "confidence": float(confidence.item()),
                "is_mock": False
            }
        except RuntimeError as e:
            logger.error(f"Runtime tensor error during inference: {e}")
            return {"error": f"Model inference failed: {str(e)}"}
        except Exception as e:
            logger.exception("Unexpected error during prediction pipeline.")
            return {"error": f"Unexpected error: {str(e)}"}
