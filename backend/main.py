import sys
import os
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("CropCare-API")

# Add parent directory to path so we can import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.inference import PlantDiseasePredictor
from disease_info import get_disease_info

app = FastAPI(
    title="CropCare AI API",
    description="Production-ready API for detecting plant diseases from leaf images.",
    version="2.0.0"
)

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Initializing ML Model...")
predictor = PlantDiseasePredictor()
logger.info("ML Model Initialized Successfully.")

# Allowed file types and max size (5MB)
ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/jpg"]
MAX_FILE_SIZE = 5 * 1024 * 1024

def determine_confidence_level(confidence):
    if confidence >= 0.90:
        return "High"
    elif confidence >= 0.70:
        return "Medium"
    else:
        return "Low"

@app.get("/")
def read_root():
    return {"message": "Welcome to CropCare AI API. Use /docs for documentation."}

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    logger.info(f"Received prediction request for file: {file.filename}")
    
    # Validation: Content Type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        logger.warning(f"Invalid content type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, JPEG, and PNG are allowed.")
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Validation: File Size
        if len(contents) > MAX_FILE_SIZE:
            logger.warning(f"File size exceeded: {len(contents)} bytes")
            raise HTTPException(status_code=400, detail="File is too large. Maximum size is 5MB.")
            
        logger.info("File validated. Running inference...")
        
        # Inference
        result = predictor.predict(contents)
        
        if "error" in result:
            logger.error(f"Inference error: {result['error']}")
            raise HTTPException(status_code=500, detail=f"Inference failed: {result['error']}")
            
        class_name = result["disease"]
        confidence = result["confidence"]
        is_mock = result.get("is_mock", False)
        
        # Fetch rich info
        info = get_disease_info(class_name)
        confidence_level = determine_confidence_level(confidence)
        
        logger.info(f"Prediction successful: {class_name} ({confidence*100:.2f}%)")
        
        return {
            "success": True,
            "prediction": {
                "class_name": class_name,
                "plant": info['plant'],
                "disease": info['disease'],
                "confidence": round(confidence * 100, 2), # Return as percentage
                "confidence_level": confidence_level,
                "description": info['description'],
                "causes": info['causes'],
                "treatment": info['treatment'],
                "prevention": info['prevention'],
                "is_mock": is_mock
            }
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception("An unexpected error occurred during prediction.")
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
