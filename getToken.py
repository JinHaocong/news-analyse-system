import json

import requests

proxies = {
    'http': "127.0.0.1:7890",
    'https': "127.0.0.1:7890",
}


# 获取百度aitoken
def get_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=7N7mI9U7oGUUviN43pHEOqUB&client_secret=sE4uyhL0DcmrXTp2tdFGLbpYGn5I75YU"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)

    print(response.text)


def analyse():
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.5e32b04f49903cd9e520c7a2be477c78.2592000.1684409657.282335-32554078&charset=UTF-8"

    payload = json.dumps({
        "text": "不开心呀"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)

    print(response.text)


if __name__ == '__main__':
    # get_token()
    analyse()
