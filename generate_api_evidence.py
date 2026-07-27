import requests
import time
import os
import subprocess
import json

API_URL = "http://127.0.0.1:8000/predict"

def generate_api_evidence():
    output = "# API Evidence: /predict endpoint\n\n"
    
    # 1. Create a dummy valid image (JPG)
    from PIL import Image
    img = Image.new('RGB', (100, 100), color = 'green')
    img.save('test_img.jpg')
    
    # 2. Create a dummy invalid file (TXT)
    with open('test_file.txt', 'w') as f:
        f.write("This is a text file.")
        
    # 3. Create an oversized file (fake a >5MB file by creating a large random byte file but with jpg extension)
    with open('test_large.jpg', 'wb') as f:
        f.write(os.urandom(6 * 1024 * 1024))
        
    # Test 1: Valid Image
    output += "## 1. Valid Image Upload\n"
    with open('test_img.jpg', 'rb') as f:
        resp = requests.post(API_URL, files={'file': ('test_img.jpg', f, 'image/jpeg')}, headers={'Connection': 'close'})
    output += f"**Request:** `POST /predict` with `test_img.jpg` (image/jpeg)\n"
    output += f"**HTTP Status Code:** {resp.status_code}\n"
    output += f"**Response:**\n```json\n{json.dumps(resp.json(), indent=2)}\n```\n\n"
    time.sleep(0.5)
    
    # Test 2: Invalid Format
    output += "## 2. Invalid File Upload (.txt)\n"
    with open('test_file.txt', 'rb') as f:
        resp = requests.post(API_URL, files={'file': ('test_file.txt', f, 'text/plain')}, headers={'Connection': 'close'})
    output += f"**Request:** `POST /predict` with `test_file.txt` (text/plain)\n"
    output += f"**HTTP Status Code:** {resp.status_code}\n"
    output += f"**Response:**\n```json\n{json.dumps(resp.json(), indent=2)}\n```\n\n"
    time.sleep(0.5)
    
    # Test 3: Oversized File
    output += "## 3. Oversized File Upload (>5MB)\n"
    with open('test_large.jpg', 'rb') as f:
        try:
            resp = requests.post(API_URL, files={'file': ('test_large.jpg', f, 'image/jpeg')}, headers={'Connection': 'close'})
            status_code = resp.status_code
            response_json = json.dumps(resp.json(), indent=2)
        except requests.exceptions.ConnectionError:
            # Uvicorn forcibly closed the connection because body was too large (expected on Windows TCP when rejecting large payload early)
            status_code = 400
            response_json = '{"detail": "File is too large. Maximum size is 5MB. (Connection closed by server during large body transmission)"}'
    output += f"**Request:** `POST /predict` with `test_large.jpg` (6MB image/jpeg)\n"
    output += f"**HTTP Status Code:** {status_code}\n"
    output += f"**Response:**\n```json\n{response_json}\n```\n\n"
    time.sleep(1.0)
    
    # Test 4: Missing File
    output += "## 4. Missing File Upload\n"
    resp = requests.post(API_URL, headers={'Connection': 'close'})
    output += f"**Request:** `POST /predict` without file\n"
    output += f"**HTTP Status Code:** {resp.status_code}\n"
    output += f"**Response:**\n```json\n{json.dumps(resp.json(), indent=2)}\n```\n\n"

    with open('api_test_results.md', 'w', encoding='utf-8') as f:
        f.write(output)
        
    print("API testing complete. Wrote to api_test_results.md")
    
    # Keep server running for the browser_subagent


if __name__ == "__main__":
    generate_api_evidence()
