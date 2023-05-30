import requests
import urllib3


class Roots:
    root_user_feeds = "api/getfeed/"


class HttpManager:
    @staticmethod
    def get(url):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        result = requests.get(url, headers={"content-type": "application/json"}, cookies="")
        return result


class JSONFixtures:
    pass
