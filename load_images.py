from PIL import Image

import requests
import os
import urllib
import pathlib
import platform

def load_image(filepath, links):
    for link_id, link in enumerate(links):
        response = requests.get(link)
        response.raise_for_status()
        ext = os.path.splitext(filepath)[1] if os.path.splitext(filepath)[1] != "" else ext = ".jpg"

        with open("{0}{1}{2}".format(os.path.splitext(filepath)[0], str(link_id), ext), "wb") as file:
            file.write(response.content)


def fetch_spacex_last_launch(folder_name="images"):
    spacexdata_url = "https://api.spacexdata.com/v4/launches/latest"
    response = requests.get(spacexdata_url)
    response.raise_for_status()
    full_response = response.json()
    path = os.path.join(folder_name,"")
    load_image(path.format(folder_name), full_response["links"]["flickr"]["original"])


def fetch_hubble_telescope_images(img_id):
    hubble_site_url = "http://hubblesite.org/api/v3/image/{}".format(img_id)
    response = requests.get(hubble_site_url)
    response.raise_for_status()
    full_response = response.json()
    links = []
    if not(isinstance(full_response["image_files"], str)):
        links.append("https:{}".format( full_response["image_files"][0]["file_url"]))
    else:
        links = "https:{}".format( full_response["file_url"])
    return links


def split_links_to_filenames(img_id, links):
    filenames = []
    for link in links:
        path = urllib.parse.unquote(os.path.split(urllib.parse.urlsplit(link)[2])[1])
        filenames.append("{0}{1}{2}".format(img_id, "_", path))
    return filenames


def resize_image(filepath):
    image = Image.open(filepath)
    img_size = (1080, 768)
    image.thumbnail(img_file)
    image.convert("RGB")
    image.save("{}.jpg".format(os.path.splitext(filepath)[0]))


def download_hublle_telescope_images(img_id, folder_name="images"):
    links = fetch_hubble_telescope_images(img_id)
    filenames = split_links_to_filenames(img_id, links)
    for link_id, link in enumerate(links):
        response = requests.get(link, verify=False)
        path = os.path.join(folder_name,filenames[link_id])
        with open(path, "wb") as file:
            file.write(response.content)


def download_hubble_telescope_images_by_collection_name(collection_name, folder_name="imgaes"):
    hubble_site_url = "http://hubblesite.org/api/v3/images/{}".format(collection_name)
    response = requests.get(hubble_site_url)
    response.raise_for_status()
    full_response = response.json()
    image_ids = []
    for image_params in full_response:
        download_hublle_telescope_images(image_params["id"], folder_name)


if __name__ == "__main__":
    folder_name = "images"
    os.makedirs(folder_name, exist_ok=True)

    fetch_spacex_last_launch(folder_name)
    download_hubble_telescope_images_by_collection_name("news", folder_name)
    files = os.listdir("{0}/{1}".format(str(pathlib.Path(__file__).parent.absolute()), folder_name))
    for img_file in files:
        try:
            resize_image(os.path.join(str(pathlib.Path(__file__).parent.absolute()), folder_name,img_file))
        except:
            print("По неизвестной причине  файл {} был отбракован".format(img_file)) #здесь мы ловим неудачные картинки и просто баги в программе. если таковые будут - самбиттье их мне в Issues
