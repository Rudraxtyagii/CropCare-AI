import requests
import time
import os

API_URL = "http://127.0.0.1:8000/predict"

def test_api():
    print("Testing API...")
    
    # 1. Create a dummy valid image (JPG)
    from PIL import Image
    img = Image.new('RGB', (100, 100), color = 'green')
    img.save('test_img.jpg')
    
    # 2. Create a dummy invalid file (TXT)
    with open('test_file.txt', 'w') as f:
        f.write("This is a text file.")
        
    # 3. Create a dummy oversized file (fake a >5MB file by creating a large random byte file but with jpg extension to pass content type check)
    # Wait, the content type is determined by the FastAPI client upload (which uses mimetypes based on extension). 
    with open('test_large.jpg', 'wb') as f:
        f.write(os.urandom(6 * 1024 * 1024))
        
    # Test 1: Valid Image
    print("\n--- Test 1: Valid Image ---")
    with open('test_img.jpg', 'rb') as f:
        resp = requests.post(API_URL, files={'file': ('test_img.jpg', f, 'image/jpeg')})
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    assert resp.status_code == 200, "Valid image failed!"
    assert resp.json().get('success') == True, "Valid image missing success flag!"
    
    # Test 2: Invalid Format
    print("\n--- Test 2: Invalid Format ---")
    with open('test_file.txt', 'rb') as f:
        resp = requests.post(API_URL, files={'file': ('test_file.txt', f, 'text/plain')})
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    assert resp.status_code == 400, "Invalid format should return 400!"
    
    # Test 3: Large File
    print("\n--- Test 3: Oversized File ---")
    with open('test_large.jpg', 'rb') as f:
        resp = requests.post(API_URL, files={'file': ('test_large.jpg', f, 'image/jpeg')})
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    assert resp.status_code == 400, "Oversized file should return 400!"
    
    # Test 4: Missing File
    print("\n--- Test 4: Missing File ---")
    resp = requests.post(API_URL)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    assert resp.status_code == 422, "Missing file should return 422!"

    print("\nALL API TESTS PASSED!")

if __name__ == "__main__":
    test_api()
