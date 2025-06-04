from time import sleep

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

    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpdmFuQGdtYWlsLmNvbSIsImV4cCI6MTc0NzI0MjgxNn0.494kqlHZAwwsQ8IlFiUWEKhl4YaxXc2xQK6--qv63s4',
    }

    result = requests.post("http://localhost:8080/binary_image", files=files, data=data, headers=headers, stream=True)

    print(result.json())

    task_id = result.json()['task_id']

    done = True
    while done:
        result = requests.get(f"http://localhost:8080/task/{task_id}")

        if result.headers['content-type'] == 'image/png':
            print('Downloading...')

            with open("images/result_image.png", "wb") as f:
                for chunk in result.iter_content(chunk_size=8192):
                    f.write(chunk)
                done = True
                break
        elif result.headers['content-type'] == 'application/json':
            print(result.json())

            if 'status' in result.json():
                sleep(0.5)
                continue

            if 'error' in result.json() or 'detail' in result.json():
                break
        else:
            print(result.status_code, result.headers['content-type'], result)

    print('Binarization request has been successfully performed.')


if __name__ == "__main__":
    # register()
    # login()
    process_image()
