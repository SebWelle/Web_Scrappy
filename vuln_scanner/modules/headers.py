import re


def check_missing_headers(headers):
    important_headers = [
        'Strict-Transport-Security',
        'X-Frame-Options',
        'X-Content-Type-Options',
        'Content-Security-Policy',
        'Referrer-Policy',
        'Permissions-Policy',
        'Cross-Origin-Opener-Policy',
        'Cross-Origin-Resource-Policy',
    ]

    missing = []
    for header in important_headers:
        if header not in headers:
            missing.append(header)

    # frame-ancestors in the CSP does the same job as X-Frame-Options
    csp = headers.get('Content-Security-Policy', '')
    if 'frame-ancestors' in csp and 'X-Frame-Options' in missing:
        missing.remove('X-Frame-Options')

    return missing


def check_weak_headers(headers):
    weak = []

    hsts = headers.get('Strict-Transport-Security')
    if hsts:
        max_age = re.search(r'max-age=(\d+)', hsts)
        one_year = 31536000
        if not max_age or int(max_age.group(1)) < one_year:
            weak.append(f"HSTS max-age is too short: {hsts}")

    content_type = headers.get('X-Content-Type-Options')
    if content_type and content_type.lower() != 'nosniff':
        weak.append(f"X-Content-Type-Options should be nosniff: {content_type}")

    frame = headers.get('X-Frame-Options')
    if frame and frame.upper() not in ['DENY', 'SAMEORIGIN']:
        weak.append(f"X-Frame-Options should be DENY or SAMEORIGIN: {frame}")

    csp = headers.get('Content-Security-Policy', '')
    if "'unsafe-inline'" in csp:
        weak.append("CSP allows 'unsafe-inline'")
    if "'unsafe-eval'" in csp:
        weak.append("CSP allows 'unsafe-eval'")
    if ' * ' in f" {csp.replace(';', ' ')} ":
        weak.append("CSP allows everything (*)")

    if headers.get('Access-Control-Allow-Origin') == '*':
        if headers.get('Access-Control-Allow-Credentials', '').lower() == 'true':
            weak.append("CORS allows every origin with credentials")
        else:
            weak.append("CORS allows every origin")

    return weak


def check_info_leaks(headers):
    leaky_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-AspNetMvc-Version']

    leaks = []
    for header in leaky_headers:
        if header in headers:
            leaks.append(f"{header}: {headers[header]}")

    return leaks


def check_cookies(response):
    problems = []

    # requests merges multiple Set-Cookie headers into one,
    # so we read them from the raw response instead
    for cookie in response.raw.headers.getlist('Set-Cookie'):
        name = cookie.split('=')[0]
        cookie = cookie.lower()

        missing_flags = []
        for flag in ['secure', 'httponly', 'samesite']:
            if flag not in cookie:
                missing_flags.append(flag)

        if missing_flags:
            problems.append(f"{name} is missing: {', '.join(missing_flags)}")

    return problems


def check_security_headers(response):
    headers = response.headers

    result = {
        'url': response.url,
        'missing': check_missing_headers(headers),
        'weak': check_weak_headers(headers),
        'info_leak': check_info_leaks(headers),
        'cookies': check_cookies(response),
    }

    return result
