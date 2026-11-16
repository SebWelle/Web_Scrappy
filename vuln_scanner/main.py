import argparse

import requests

from modules.headers import check_security_headers
from modules.crawler import extract_links
from modules.directories import check_hidden_paths
from modules.xss import check_xss
from modules.reporter import save_json_report
from modules.http_client import new_session, USER_AGENT
from modules import robots


def parse_args():
    parser = argparse.ArgumentParser(description="Simple web vulnerability scanner.")
    parser.add_argument('-u', '--url', required=True, help="Target URL to scan.")
    return parser.parse_args()


def normalize_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


def main():
    args = parse_args()
    target = normalize_url(args.url)
    session = new_session()
    scan_results = []

    print(f"Starting scan for: {target}")

    try:
        response = session.get(target, timeout=5)
        print(f"Status-Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Url wasn't found. Reason: {e}")
        return

    # Scan the start page itself, otherwise its headers are never checked.
    homepage_headers = check_security_headers(response)
    if homepage_headers:
        scan_results.append(homepage_headers)

    directories_found, directories_hidden = check_hidden_paths(target, session)
    if directories_found:
        scan_results.append(directories_found)
    if directories_hidden:
        scan_results.append(directories_hidden)

    robot_rules = robots.load_rules(target, session)
    # Use response.url (the URL after any redirects, e.g. to www.) as the base
    # so the same-domain filter in extract_links does not discard every link.
    found_links = extract_links(response.text, response.url)

    for link in found_links:
        if not robot_rules.can_fetch(USER_AGENT, link):
            print(f"\n[*] Skipping (blocked by robots.txt): {link}")
            continue

        print(f"\n[*] Check for: {link}")
        try:
            response = session.get(link, timeout=5)

            xss_result = check_xss(link, session)
            if xss_result:
                scan_results.append(xss_result)

            headers_result = check_security_headers(response)
            if headers_result:
                scan_results.append(headers_result)

        except requests.exceptions.RequestException:
            print("[-] Url wasn't found or timed out.")

    save_json_report(scan_results)
    print("\n[+] Scan finished. Report saved.")


if __name__ == "__main__":
    main()
