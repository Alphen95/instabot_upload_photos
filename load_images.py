from PIL import Image

import requests
import os
import urllib

def load_image(filepath, links):
    for link_id in range(len(links)):
        link = links[link_id]
        response = requests.get(link)
        response.raise_for_status()
        with open(os.path.splitext(filepath)[0] + str(link_id) + os.path.splitext(filepath)[1], 'wb') as file:
            file.write(response.content)


def fetch_spacex_last_launch():
    spacexdata_url = "https://api.spacexdata.com/v4/launches/latest"
    response = requests.get(spacexdata_url)
    response.raise_for_status()
    full_response = response.json()
    load_image("images/image.jpeg", full_response["links"]["flickr"]["original"])


def fetch_hubble_telescope_images(img_id):
    hubble_site_url = "http://hubblesite.org/api/v3/image/{}".format(img_id)
    response = requests.get(hubble_site_url)
    response.raise_for_status()
    full_response = response.json()
    links = []
    if not(isinstance(full_response["image_files"], str)):
        for image_params in full_response["image_files"]:
            links.append("https:" + image_params['file_url'])
    else:
        links = "https:" + image_params['file_url']
    return links


def split_links_to_filenames(img_id, links):
    filenames = []
    for link in links:
        path = urllib.parse.unquote(os.path.split(urllib.parse.urlsplit(link)[2])[1])
        filenames.append(str(img_id) + "_" + path)
    return filenames


def resize_image(filepath):
    image = Image.open(filepath)
    image.thumbnail((1080, 768))
    image.convert('RGB')
    image.save(os.path.splitext(filepath)[0] + ".jpg")


def download_hublle_telescope_images(img_id):
    links = fetch_hubble_telescope_images(img_id)
    filenames = split_links_to_filenames(img_id, links)
    for link_id in range(len(links)):
        response = requests.get(links[link_id], verify=False)
        with open("images/" + filenames[link_id], 'wb') as file:
            file.write(response.content)


def download_hubble_telescope_images_by_collection_name(collection_name):
    hubble_site_url = "http://hubblesite.org/api/v3/images/{}".format(collection_name)
    response = requests.get(hubble_site_url)
    response.raise_for_status()
    full_response = response.json()
    image_ids = []
    for image_params in full_response:
        download_hublle_telescope_images(image_params['id'])


if __name__ == "__main__":
    if not(os.path.exists("images")):
        os.mkdir("images")

    fetch_spacex_last_launch()
    download_hubble_telescope_images_by_collection_name("news")
    files = os.listdir(str(os.getcwd()).replace("\\", "/") + "/images")
    for img_file in files:
        try:
            resize_image(str(os.getcwd()).replace("\\", "/") + "/images/" + img_file)
        except:
            pass
