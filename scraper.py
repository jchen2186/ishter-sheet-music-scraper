import requests
from bs4 import BeautifulSoup


URL = 'http://www.theishter.com/sheet-music.html'


def get_pdf_links():
    """Returns a list of links to the sheet music located in Google Drive."""
    tmp = requests.get(URL)
    soup = BeautifulSoup(tmp.text, 'html.parser')
    links = []

    # filter for Google Drive links
    for anchor in soup.find_all('a'):
        link = anchor.get('href')
        if link and 'drive.google.com' in link:
            links.append(link)

    return links


def download_pdfs(links_to_pdfs):
    pass


def main():
    links = get_pdf_links()
    print(links)
    print(len(links))
    

if __name__ == '__main__':
    main()
