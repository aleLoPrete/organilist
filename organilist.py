#!/usr/bin/env python3

import subprocess
import requests
from bs4 import BeautifulSoup
import sys
import yaml
import uuid
import os
from test import *
import os

# Load YAML data from a file


def get_config_data():
    # Get the user's home directory
    home_directory = os.path.expanduser("~")
    config_file_path = os.path.join(
        home_directory, ".config", "organilist", "config.yaml"
    )

    try:
        with open(config_file_path, "r") as yaml_file:
            config_data = yaml.safe_load(yaml_file)
            return config_data
    except FileNotFoundError:
        print(f"{config_file_path} file not found. Create one at {config_file_path}")
        exit(1)


def get_bm_path(config_data):
    if config_data["bm_file_path"] == None:
        print("Bookmark file not found. Specify one in config file")
        exit(1)
    return config_data["bm_file_path"]


def get_xclip_content():
    return subprocess.check_output(["xclip", "-o", "-selection", "primary"]).decode(
        "utf-8"
    )


def add_to_bookmarks(bm_file_path, url, title, tags=None, reading_time=None):
    if tags is None:
        tags = []

    bookmark_id = str(uuid.uuid4())
    bookmark = {
        "id": bookmark_id,
        "url": url,
        "title": title,
        "tags": tags,
        "reading_time": reading_time,
    }

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
        return "Falied to fetch webpage Title"


def get_reading_time(url, words_per_minute=200):
    # TODO: fix, not working
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the content of the article
            article_content = ""
            for paragraph in soup.find_all("p"):
                article_content += paragraph.get_text() + " "

            # Clean the text by removing HTML tags and extra whitespaces
            article_content = response.sub(r"\s+", " ", article_content)

            # Count the number of words in the article
            word_count = len(article_content.split())

            # Calculate the reading time in minutes
            reading_time = int(word_count / words_per_minute) + 1

            return reading_time
        else:
            return "Failed to fetch the webpage (status code {})".format(
                response.status_code
            )
    except Exception as e:
        return "Failed to fetch reading time"


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


def add_bookmark():
    selected_text = get_xclip_content()
    print("New bookmark:")
    print(selected_text)

    input("[Enter to save]")

    # Retrieve tags
    # TODO: test no tags
    tags = sys.argv[sys.argv.index("-t") + 1 :]
    add_to_bookmarks(
        bm_file_path, selected_text, get_webpage_title(selected_text), tags
    )


def choice_manager(bm_file_path):
    # List bookmakrs
    if "-l" in sys.argv:
        list_bookmarks(bm_file_path)
    # Edit bookmarks
    elif "-e" in sys.argv:
        open_file_with_neovim(bm_file_path)
    # Add new bookmark
    else:
        add_bookmark()


# TODO: Add support for bookmark navigation
# TODO: Restruture management of bookmark file


if __name__ == "__main__":
    config_data = get_config_data()

    bm_file_path = get_bm_path(config_data)

    choice_manager(bm_file_path)
