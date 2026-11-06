import argparse
import requests
from modules.headers import check_security_headers
from modules.crawler import extract_links
from modules.directories import check_hidden_paths
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', required=True)
args = parser.parse_args()


if not args.url.startswith(('http://', 'https://')):
    args.url = 'https://' + args.url

print(f"Starting scan for: {args.url}")

try:
    response = requests.get(args.url, timeout=5)
    print(f"Status-Code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Url wasn't found. Reason: {e}")

check_security_headers(response.headers)
check_hidden_paths(args.url)

text = response.text

found_links = extract_links(text, args.url)

for link in found_links:
    print(f"\n[*] Check for: {link}")
    try:
        response = requests.get(link, timeout=5)
        check_security_headers(response.headers)
        
    except requests.exceptions.RequestException as e:
        print("[-] Url wasn't found or timed out.")
            
