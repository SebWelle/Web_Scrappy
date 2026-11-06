

def check_security_headers(response_headers):
    headers = ['Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options']

    for header in headers:
        if header in response_headers:
            print(f"[+] {header}")
        else:
            print(f"[-] {header}")    
