from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(html_text, base_url):
    result = []
    soup = BeautifulSoup(html_text, 'html.parser')
    
    for tag in soup.find_all('a'):
        href = tag.get('href')
        
        if not href or href.startswith('#'):
            continue
            
        full_url = urljoin(base_url, href)
        result.append(full_url)
        
    return result