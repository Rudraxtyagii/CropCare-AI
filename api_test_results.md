# API Evidence: /predict endpoint

## 1. Valid Image Upload
**Request:** `POST /predict` with `test_img.jpg` (image/jpeg)
**HTTP Status Code:** 200
**Response:**
```json
{
  "success": true,
  "prediction": {
    "class_name": "Tomato___Tomato_mosaic_virus",
    "plant": "Tomato",
    "disease": "Tomato Mosaic Virus",
    "confidence": 82.21,
    "confidence_level": "Medium",
    "description": "Causes mottling (light and dark green patches) on leaves, stunting, and reduced fruit yield.",
    "causes": [
      "Tobamovirus",
      "Spread mechanically via hands, tools, or infected debris"
    ],
    "treatment": [
      "No cure; destroy infected plants"
    ],
    "prevention": [
      "Wash hands and tools thoroughly",
      "Do not use tobacco products near plants",
      "Plant resistant varieties"
    ],
    "is_mock": true
  }
}
```

## 2. Invalid File Upload (.txt)
**Request:** `POST /predict` with `test_file.txt` (text/plain)
**HTTP Status Code:** 400
**Response:**
```json
{
  "detail": "Invalid file type. Only JPG, JPEG, and PNG are allowed."
}
```

## 3. Oversized File Upload (>5MB)
**Request:** `POST /predict` with `test_large.jpg` (6MB image/jpeg)
**HTTP Status Code:** 400
**Response:**
```json
{
  "detail": "File is too large. Maximum size is 5MB."
}
```

## 4. Missing File Upload
**Request:** `POST /predict` without file
**HTTP Status Code:** 422
**Response:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "file"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

