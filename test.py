import yaml
import webbrowser
from tabulate import tabulate

def load_urls_from_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = yaml.safe_load(file)
            return urls
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

def display_urls_table(urls):
    if not urls:
        print("No URLs found.")
        return

    headers = ["Index", "URL"]
    table_data = [(index + 1, url) for index, url in enumerate(urls)]
    table = tabulate(table_data, headers=headers, tablefmt="grid")
    print(table)

def open_url_in_browser(url):
    webbrowser.open(url)

def main():
    file_path = "home/rick/Notes/organilist/bookmark.yaml"  # Replace with the path to your YAML file
    urls = load_urls_from_yaml(file_path)

    while True:
        display_urls_table(urls)

        try:
            choice = int(input("Enter the index of the URL to open (0 to exit): ")) - 1
            if choice == -1:
                break
            elif 0 <= choice < len(urls):
                open_url_in_browser(urls[choice])
            else:
                print("Invalid index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")

if __name__ == "__main__":
    main()

