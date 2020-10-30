#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import os

clouds = {
    "Amazon": "https://aws.amazon.com/",
    "Google": "https://cloud.google.com/",
    "Microsoft": "https://azure.microsoft.com/en-us/"
}


class CloudProvider():
    def __init__(self, name, url):
        self.name = name
        self.filename = os.path.join("links", self.name.lower() + ".txt")
        self.url = url
        self.create_dir()
        self.send_request()
        self.get_links()

    def create_dir(self):
        path = os.path.join(os.getcwd(), "links")
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as err:
                print("Error making dir: ", err)

    def send_request(self):
        self.response = requests.get(url)
        self.response.raise_for_status()

    def get_links(self):
        self.soup = BeautifulSoup(self.response.text, features="html.parser")
        self.links = self.soup.find_all('a')

    def print_header(self):
        print(self.name, self.url)
        for k, v in self.response.headers.items():
            print(f"    {k}: {v}")

    def write_links(self):
        print("Gettings links from:", self.url)
        with open(self.filename, "w", encoding="utf-8") as f:
            for link in self.links:
                if link.string:
                    text = str(link.string).strip()
                    if text is not None:
                        f.write(f"{text}\n")

                # href = str(link.get('href'))

                # if href is not None and href != "#" and text is not None:
                #     f.write(f"{text:20}:   {href}\n")


for name, url in clouds.items():
    p = CloudProvider(name, url)
    p.write_links()
    # p.print_header()
