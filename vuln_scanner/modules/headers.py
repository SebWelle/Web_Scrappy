

def check_security_headers(response_headers):
    headers = ['Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options']

    result = {}

    for header in headers:
        if header in response_headers:

             result[header] = "[+]"
        else:
            result[header] = "[-]"

    return result
