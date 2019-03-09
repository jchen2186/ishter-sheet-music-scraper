import os
import requests
from bs4 import BeautifulSoup


def get_pdf_links(website_url):
    """
    Returns a dict of links (key) and titles (value) to the sheet music
    located in Google Drive.
    """
    tmp = requests.get(website_url)
    soup = BeautifulSoup(tmp.text, 'html.parser')
    link_to_title = {}

    # filter for Google Drive links
    for anchor in soup.find_all('a'):
        link = anchor.get('href')
        title = anchor.text.strip()

        if link and 'drive.google.com' in link:
            # get id depending on the url format
            if '?id=' in link:
                link_to_title[link.split('?id=')[-1]] = title
            elif '/file/d' in link:
                link_to_title[link.split('/')[-2]] = title

    return link_to_title


def download_pdfs(link_to_title, directory):
    """
    Downloads files from the dictionary link_to_title.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    for link, title in link_to_title.items():
        # replace any slashes in title with a space
        title = title.replace('/', ' ')

        # download pdf if it does not already exist
        if not os.path.isfile(f'{directory}/{title}.pdf'):
            download_from_google_drive(link, f'{directory}/{title}.pdf')


# The next three functions are based on the following stack overflow answer:
# https://stackoverflow.com/a/39225272/11112248
def download_from_google_drive(id, destination):
    DOWNLOAD_URL = 'https://docs.google.com/uc?export=download'
    session = requests.Session()
    response = session.get(DOWNLOAD_URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(DOWNLOAD_URL, params={'id': id}, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def main():
    ISHTER_URL = 'http://www.theishter.com/sheet-music.html'
    DIRECTORY = 'pdfs'

    links = get_pdf_links(ISHTER_URL)
    print(links)
    print(len(links))

    download_pdfs(links, 'pdfs')

if __name__ == '__main__':
    main()
