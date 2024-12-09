import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images_from_url(url, output_dir="images"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    img_tags = soup.find_all('img')
    if not img_tags:
        print("Cannot Find Image.")
        return

    os.makedirs(output_dir, exist_ok=True)

    for i, img_tag in enumerate(img_tags):
        img_url = img_tag.get('src') or img_tag.get('data-src')
        if not img_url:
            continue

        img_url = urljoin(url, img_url)

        try:
            img_data = requests.get(img_url, headers=headers).content
            file_name = os.path.join(output_dir, f"image_{i + 1}.jpg")

            with open(file_name, 'wb') as img_file:
                img_file.write(img_data)

            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Download Failed: {img_url}, Error: {e}")

        time.sleep(1)

# 실행 예시
blog_url = "" # URL Here
download_images_from_url(blog_url)
