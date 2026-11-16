from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def extract_links(html_text, base_url):
    base_domain = urlparse(base_url).netloc
    soup = BeautifulSoup(html_text, 'html.parser')
    links = set()

    for tag in soup.find_all('a'):
        href = tag.get('href')

        if not href or href.startswith('#'):
            continue

        full_url = urljoin(base_url, href)

        # Only follow links that stay on the target domain.
        if urlparse(full_url).netloc == base_domain:
            links.add(full_url)

    return sorted(links)
