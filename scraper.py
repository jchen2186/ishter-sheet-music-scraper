import os
import requests
from bs4 import BeautifulSoup


def get_id_to_title(website_url):
    """Scrapes a website and returns a dict of ids (keys) to titles (values)
    for the Google Drive links found on the website.

    Args:
        website_url (str): URL to where to scrape links from.
    
    Returns:
        dict: Google Drive id (str) to title (str) pairs.
    """
    result = requests.get(website_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    id_to_title = {}

    # filter for Google Drive links
    for anchor in soup.find_all('a'):
        link = anchor.get('href')
        title = anchor.text.strip()

        if link and 'drive.google.com' in link:
            # get id depending on the url format
            if '?id=' in link:
                id = link.split('?id=')[-1]
            elif '/file/d' in link:
                id = link.split('/')[-2]
            
            id_to_title[id] = title

    return id_to_title


def download_pdfs(id_to_title, directory):
    """Downloads Google Drive files into a desired directory.

    Args:
        id_to_title (dict): Google Drive id (str) to title (str) pairs.
        directory (str): Local directory where files will be downloaded to.
    
    Returns:
        None.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    for id, title in id_to_title.items():
        # replace any slashes in title with a space
        title = title.replace('/', ' ')

        # download pdf if it does not already exist
        if not os.path.isfile(f'{directory}/{title}.pdf'):
            download_from_google_drive(id, f'{directory}/{title}.pdf')


# The next three functions are based on the following stack overflow answer:
# https://stackoverflow.com/a/39225272/11112248
def download_from_google_drive(id, destination):
    """Downloads content from the Google Drive file into the destination file."""
    DOWNLOAD_URL = 'https://docs.google.com/uc?export=download'
    session = requests.Session()
    response = session.get(DOWNLOAD_URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(DOWNLOAD_URL, params={'id': id}, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    """Returns token from the response."""
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    """Saves the content from the response into the destination file."""
    CHUNK_SIZE = 32768

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def main():
    ISHTER_URL = 'http://www.theishter.com/sheet-music.html'
    DIRECTORY = 'pdfs'

    links = get_id_to_title(ISHTER_URL)
    download_pdfs(links, 'pdfs')


if __name__ == '__main__':
    main()
