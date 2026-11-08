import argparse
import requests
from modules.headers import check_security_headers
from modules.crawler import extract_links
from modules.directories import check_hidden_paths
from modules.xss import check_xss
from modules.reporter import save_json_report
from bs4 import BeautifulSoup


scan_results = []

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

text = response.text

directories_found, directories_hidden = check_hidden_paths(args.url)
if directories_found:
    scan_results.append(directories_found)
    

found_links = extract_links(text, args.url)

for link in found_links:
    print(f"\n[*] Check for: {link}")
    try:
        response = requests.get(link, timeout=5)


        xss_result = check_xss(link)
        if xss_result:  
            scan_results.append(xss_result)

        if directories_hidden:
            scan_results.append(directories_hidden)

        headers_result = check_security_headers(response.headers)
        if headers_result:
            scan_results.append(headers_result)

        

        save_json_report(scan_results)
            
        
    except requests.exceptions.RequestException as e:
        print("[-] Url wasn't found or timed out.")
            
