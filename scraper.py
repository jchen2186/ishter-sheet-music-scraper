import requests
from bs4 import BeautifulSoup


ISHTER_URL = 'http://www.theishter.com/sheet-music.html'
DOWNLOAD_URL = 'https://docs.google.com/uc?export=download'


def get_pdf_links():
    """Returns a list of links to the sheet music located in Google Drive."""
    tmp = requests.get(ISHTER_URL)
    soup = BeautifulSoup(tmp.text, 'html.parser')
    link_ids = []

    # filter for Google Drive links
    for anchor in soup.find_all('a'):
        link = anchor.get('href')
        if link and 'drive.google.com' in link:
            # do different things depending on the url format
            if '?id=' in link:
                link_ids.append(link.split('?id=')[-1])
            elif '/file/d' in link:
                link_ids.append(link.split('/')[-2])

    return link_ids


# The next three functions are based on the following stack overflow answer:
# https://stackoverflow.com/a/39225272/11112248
def download_from_google_drive(id, destination):
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

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def main():
    links = get_pdf_links()
    print(links)
    print(len(links))

    download_from_google_drive(links[0], 'pdfs/test.pdf')
    

if __name__ == '__main__':
    main()
