import requests

def register():
    data = {
        'username': 'ivan',
        'email': 'ivan@gmail.com',
        'password': '1111111'
    }

    result = requests.post("http://localhost:8080/auth/register", json=data)
    print(result.json())

def login():
    data = {
        'email': 'ivan@gmail.com',
        'password': '1111111'
    }

    result = requests.post("http://localhost:8080/auth/login", json=data)
    print(result.json())

def process_image():
    files = {'image': open('images/image.jpg', 'rb')}
    data = {
        'algorithm': 'bradley_roth',
        
            }

    result = requests.post("http://localhost:8080/binary_image", files=files, data=data, stream=True)

    with open("images/result_image.png", "wb") as f:
        for chunk in result.iter_content(chunk_size=8192):
            f.write(chunk)

if __name__ == "__main__":
    # register()
    login()
    # process_image()
