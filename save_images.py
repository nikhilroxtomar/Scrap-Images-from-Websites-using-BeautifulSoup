
import os
import requests
from bs4 import BeautifulSoup
import cv2
from skimage import io

def create_dir(path):
    """ Create folders """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error")

def create_file(path):
    """ Create a file """
    try:
        if not os.path.exists(path):
            f = open(path, "w")
            f.write("Name,Alt\n")
            f.close()
    except OSError:
        print("Error")

def save_image(search_term, page_num=1):
    ## URL and headers
    url = "https://www.freepik.com/search?dates=any&format=search&page="+str(page_num)+"&query="+str(search_term)+"&selection=1&sort=popular&type=photo"
    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

    ## making a GET request to the website and getting the information in response.
    result = requests.get(url, headers=header)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
    else:
        print("Error")
        exit()

    ## Paths and file for saving the images and data.
    dir_path = f"Downloads/{search_term}/"
    file_path = f"Downloads/{search_term}/{search_term}.csv"

    create_dir(dir_path)
    create_file(file_path)

    f = open(file_path, "a")

    for tag in soup.find_all("a", class_="showcase__link"):
        if tag.img:
            try:
                src = tag.img["data-src"]
                alt = tag.img["alt"]
            except Exception as e:
                alt = None

            try:
                if alt:
                    image = io.imread(src)
                    name = src.split("/")[-1].split("?")[0]
                    data = f"{name},{alt}\n"
                    f.write(data)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(dir_path + name, image)
                    print(name, ": ", alt)
            except Exception as e:
                pass


if __name__ == "__main__":
    terms = ['dog', 'cat', 'tree']
    for term in terms:
        save_image(term, page_num=1)
        save_image(term, page_num=2)
