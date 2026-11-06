import requests
from urllib.parse import urlparse, parse_qs, urlencode,urlunparse

def check_xss(url):
    parsed_url = urlparse(url)

    if not parsed_url.query:
        return

    content_dic = parse_qs(parsed_url.query)

    payload = "<script>alert('XSS-Test')</script>"

    for entry in content_dic:
        content_dic[entry] = payload

    dic_string = urlencode(content_dic, doseq=True)

    attacking_url = urlunparse((
            parsed_url.scheme, 
            parsed_url.netloc, 
            parsed_url.path, 
            parsed_url.params, 
            dic_string, 
            parsed_url.fragment
        ))
    
    try:
        response = requests.get(attacking_url, timeout=5)

        if payload in response.text:
            print(f"[!] Found XSS security gap at: {attacking_url}")
        else:
            print(f"[-] Didn't find a security gap at: {url}")
            
    except requests.exceptions.RequestException:
        print("[-] Connection failed during XSS check.")