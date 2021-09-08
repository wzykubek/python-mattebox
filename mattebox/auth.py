import requests
import json
from .consts import PLATFORM_ID, CLIENT_SECRET, CLIENT_ID


def login(login: str, password: str) -> str:
    s = requests.Session()

    res = s.post(
        "https://oauth.nangu.tv/oauth/username_check",
        data={
            "custom": "mattebox",
            "pair_device": "false",
            "login": "Login",
            "platform_id": PLATFORM_ID,
            "username": login,
            "password": password,
        },
    )

    oauth = s.cookies.get_dict()["oauth"]

    res = s.post(
        "https://oauth.nangu.tv/oauth/auth",
        params={
            "client_id": CLIENT_ID,
            "custom": "mattebox",
            "language": "en",
            "platform_id": PLATFORM_ID,
            "redirect_uri": "nangutv://oauth",
            "response_type": "code",
        },
        cookies={"oauth": oauth},
        allow_redirects=False,
    )

    code = res.headers["Location"].replace("nangutv://oauth?code=", "")

    res = s.post(
        "https://oauth.nangu.tv/oauth/token",
        data={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "custom": "mattebox",
            "redirect_uri": "nangutv://oauth",
        },
    )

    access_token = json.loads(res.text)["access_token"]
    return access_token
