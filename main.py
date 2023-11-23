#!/usr/bin/env python3

import subprocess
import requests
from bs4 import BeautifulSoup
import sys
import yaml
import uuid
import os

# Load YAML data from a file


CONFIG_FOLDER = "~/.config/organilist"


def get_config_data():
    # try:
    with open(f"{CONFIG_FOLDER}/config.yaml", "r") as yaml_file:
        config_data = yaml.safe_load(yaml_file)
        return config_data
    # except FileNotFoundError:
    # print("Config file not found. Create one at ~/.config/organilist/config.yaml")


def get_xclip_content():
    return subprocess.check_output(["xclip", "-o", "-selection", "primary"]).decode(
        "utf-8"
    )


def add_to_bookmarks(bm_file_path, url, title, tags=None):
    if tags is None:
        tags = []

    bookmark_id = str(uuid.uuid4())
    bookmark = {"id": bookmark_id, "url": url, "title": title, "tags": tags}

    with open(bm_file_path, "a") as file:
        yaml.dump({bookmark_id: bookmark}, file, default_flow_style=False)
        file.write("\n")


def get_webpage_title(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the title tag
            title_tag = soup.find("title")

            if title_tag:
                # Get the title text
                title = title_tag.get_text()
                return title
            else:
                return "No title found on the webpage"

        else:
            return "Failed to fetch the webpage (status code {})".format(
                response.status_code
            )

    except Exception as e:
        return ""


def list_bookmarks(file_path):
    with open(file_path, "r") as file:
        for line in file:
            url, title = line.strip().split("\t")
            print(f"Title: {title}, URL: {url}")


def open_file_with_neovim(file_path):
    try:
        subprocess.run(["nvim", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # config_data = get_config_data()
    bm_file_path = (
        "/home/rick/Notes/organilist/bookmark.yaml"  # config_data["bm_file_path"]
    )

    # ~/Notes/organilist/bookmark.yaml"  # config_data["bm_file_path"]

    # TODO: Restruture management of bookmark file
    # List bookmarks
    if "-l" in sys.argv:
        # List bookmakrs
        list_bookmarks(bm_file_path)
    # Edit bookmarks
    elif "-e" in sys.argv:
        # Edit bookmark file
        open_file_with_neovim(bm_file_path)
    else:
        # Get selected text
        selected_text = get_xclip_content()
        print("New bookmark:")
        print(selected_text)

        if "-t" in sys.argv:
            # Add to bookmark_file with tags
            tags = sys.argv[sys.argv.index("-t") + 1 :]
            add_to_bookmarks(
                bm_file_path, selected_text, get_webpage_title(selected_text), tags
            )
        else:
            # Add to bookmark_file
            add_to_bookmarks(
                bm_file_path, selected_text, get_webpage_title(selected_text)
            )
