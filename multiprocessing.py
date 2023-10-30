import os
import multiprocessing
import requests
from bs4 import BeautifulSoup

HEADERS={"User-Agent": "Mozilla/5.0"}

def create_directory(folder: str) -> str:
    if not os.path.exists(folder):
        os.makedirs(folder)


def make_list(url: str) -> list:
    list_url = []
    for pages in range(5):
        url_new = url[:-1]
        url_pages: str = f"{url_new}{pages}"
        html = requests.get(url_pages, headers=HEADERS)
        soup = BeautifulSoup(html.text, "lxml")
        images = soup.findAll('img', class_='serp-item__thumb justifier__thumb')
        for link in images:
            r = link.get("src")
            if r != None:
                list_url += [r]
            if r == None:
                continue
    print(list_url)
    return list_url


def download(url: str) -> None:
    response = requests.get(url)
    create_directory("image")
    count_files = len(os.listdir("image"))
    with open(os.path.join("image", f"{count_files+1:04}.jpg"), "wb") as file:
        file.write(response.content)


if __name__ == "__main__":
    url = input("Введите ссылку на страницу с изображениями\n")
    r = make_list(url)
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        p.map(download, r)

