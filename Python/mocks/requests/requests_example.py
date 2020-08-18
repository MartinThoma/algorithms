import requests


def get_ip():
    resp = requests.get("http://ip.jsontest.com/")
    return resp.json()


if __name__ == "__main__":
    print(get_ip())
