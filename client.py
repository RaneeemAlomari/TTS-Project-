import requests

API_URL = "http://localhost:8080/process_image"  # Update with your actual server address
FILE_PATH = r"C:\Users\GTS\Downloads\philadelphia-mouzon.jpg"  # Update with the path to your image file

def process_image(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(API_URL, files=files)
        return response.text

# if __name__ == "__main__":
    # result =
process_image(FILE_PATH)
print(FILE_PATH)
#     print(result)