#test_api.py
'''
this file contains a function that help you to test the api for both uploaded files and manually typed content
All the files you want to compare must be  in the same directory where you’ll run your Python test script.
'''
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_compare_texts():
    url = f"{BASE_URL}/compare-texts/"
    data = {
        "text1": "Hello world",
        "text2": "Hello there",
        "method": "tfidf"  # change to "semantic" to test semantic similarity
    }
    response = requests.post(url, data=data)
    print("Compare texts response:", response.json())

def test_compare_files():
    url = f"{BASE_URL}/compare-files/"
    files = {
        "file1": open("file1.txt", "rb"),
        "file2": open("file2.txt", "rb"),
    }
    data = {
        "method": "semantic"  # or "tfidf"
    }
    response = requests.post(url, files=files, data=data)
    print("Compare files response:", response.json())

if __name__ == "__main__":
    test_compare_texts()
    test_compare_files()
