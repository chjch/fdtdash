import os
import base64
import requests
import json
from bs4 import BeautifulSoup

USGS_SERVER_URL = (
    "https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation"
    "/LPC/Projects/FL_Peninsular_FDEM_2018_D19_DRRA"
    "/FL_Peninsular_FDEM_Duval_2018/LAZ/"
)
BLUEDRIVE_PATH = "/Volumes/uf-fiber/chj.chen/JAXDTLIDAR"

soup = BeautifulSoup(requests.get(USGS_SERVER_URL).text, "html.parser")
links = soup.find_all('a')  # find all <a> tags

laz_urls = []

for link in links:
    href = link.get('href')
    if href and href.endswith('.laz'):
        if not href.startswith('http'):
            href = USGS_SERVER_URL + href
        laz_urls.append(href)


def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        print(response.headers)
        with open(filename, 'wb') as file:
            # Write the content of the response to the file
            file.write(response.content)
        print(f"File '{filename}' downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


for url in laz_urls[:1]:
    download_file(url, os.path.join(BLUEDRIVE_PATH, os.path.basename(url)))
# for url in laz_urls:
#     filename = os.path.basename(url)
#     download_file(url, os.path.join(BLUEDRIVE_PATH, filename))


# def download_file_with_size(url, filename):
#     # Send a GET request to the URL
#     response = requests.get(url, stream=True)
#
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Try to extract the file size from Content-Length header
#         file_size = response.headers.get('Content-Length')
#         if file_size:
#             file_size = int(file_size)
#             print(f"File size is {file_size} bytes.")
#         else:
#             print("Could not retrieve file size.")
#
#         # Download the file in chunks to avoid loading it all in memory
#         with open(filename, 'wb') as file:
#             for chunk in response.iter_content(chunk_size=8192):
#                 file.write(chunk)
#         print(f"File '{filename}' downloaded successfully.")
#     else:
#         print(f"Failed to download file. Status code: {response.status_code}")