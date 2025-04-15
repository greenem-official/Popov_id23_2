import requests

if __name__ == "__main__":
    files = {'image': open('images/image.jpg', 'rb')}
    data = {'algorithm': 'bradley_roth'}

    result = requests.post("http://localhost:8080/binary_image", files=files, data=data, stream=True)

    with open("images/result_image.png", "wb") as f:
        for chunk in result.iter_content(chunk_size=8192):
            f.write(chunk)
