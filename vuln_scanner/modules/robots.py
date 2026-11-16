import requests
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser


def load_rules(base_url, session):
    """Fetch and parse robots.txt. An empty parser allows everything,
    so a missing or unreachable robots.txt means 'no restrictions'."""
    robots_url = urljoin(base_url, '/robots.txt')
    parser = RobotFileParser()

    try:
        response = session.get(robots_url, timeout=5)
    except requests.exceptions.RequestException:
        return parser

    if response.status_code == 200:
        parser.parse(response.text.splitlines())

    return parser
