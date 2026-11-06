import requests

def check_hidden_paths(base_url:str):
    paths = ['/admin', '/.git/config', '/.env', '/robots.txt']

    clean_url = base_url.rstrip('/')
    found = []
    hidden = []

    for path in paths:
        target_path =  clean_url + path

        response = requests.get(target_path)

        if response.status_code == 200:
            print("Critical directory found: " + target_path)
        elif response.status_code == 404:
            print("Didn't find: " + target_path)
