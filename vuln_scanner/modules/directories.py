import random
import string

import requests


def _random_path():
    name = ''.join(random.choices(string.ascii_lowercase, k=16))
    return '/' + name


def _get_baseline(clean_url, session):
    """Request a path that almost certainly does not exist. Some sites answer
    a missing page with status 200 and an error page ('soft 404'). Knowing how
    that looks lets us tell a real page apart from such an error page."""
    try:
        response = session.get(clean_url + _random_path(), timeout=5)
        return response.status_code, len(response.content)
    except requests.exceptions.RequestException:
        return 404, None


def _looks_real(response, baseline_status, baseline_length):
    if response.status_code != 200:
        return False

    # If missing pages also answer with 200, compare the body size. A real
    # page usually differs clearly from the generic error page.
    if baseline_status == 200 and baseline_length is not None:
        if abs(len(response.content) - baseline_length) < 50:
            return False

    return True


def check_hidden_paths(base_url, session):
    paths = ['/admin', '/.git/config', '/.env', '/robots.txt']

    clean_url = base_url.rstrip('/')
    found = {}
    hidden = {}

    baseline_status, baseline_length = _get_baseline(clean_url, session)

    for path in paths:
        target_path = clean_url + path

        try:
            response = session.get(target_path, timeout=5)
        except requests.exceptions.RequestException:
            hidden[target_path] = "Request failed"
            continue

        if _looks_real(response, baseline_status, baseline_length):
            found[target_path] = "Critical path found"
        else:
            hidden[target_path] = "Nothing found"

    return found, hidden
