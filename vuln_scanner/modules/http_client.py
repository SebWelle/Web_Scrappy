import requests

# Honest, identifiable user agent so the site owner can see who is scanning.
USER_AGENT = "Web_Scrappy Security Scanner"


def new_session():
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    return session
