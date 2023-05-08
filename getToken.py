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


def test():
    positive_data = []
    negative_data = []
    pos = open('positive1.txt', 'r', encoding='utf-8')
    neg = open('negative1.txt', 'r', encoding='utf-8')
    for line in pos:
        positive_data.append([' '.join(eval(line.strip()))])
    for line in neg:
        negative_data.append([' '.join(eval(line.strip()))])
    pos.close()
    neg.close()

    pos = open('positive1.txt', 'w', encoding='utf-8')
    for line in positive_data:
        pos.write(str(line))
        pos.write('\n')

    neg = open('negative1.txt', 'w', encoding='utf-8')
    for line in negative_data:
        neg.write(str(line))
        neg.write('\n')

    pos.close()
    neg.close()


def print_num():
    with open('positive1.txt', 'r', encoding='utf-8') as f:
        pos = f.readlines()
    with open('negative1.txt', 'r', encoding='utf-8') as f:
        neg = f.readlines()
    print(f'积极{len(pos)}条，消极{len(neg)}')


def test2():
    pos_data = []
    pos = open('positive.txt', 'r', encoding='utf-8')
    for line in pos:
        line = eval(line.strip())
        pos_data.append(line[0])

    neg_data = []
    neg = open('negative.txt', 'r', encoding='utf-8')
    for line in neg:
        line = eval(line.strip())
        neg_data.append(line[0])
    pos.close()
    neg.close()

    pos = open('positive.txt', 'w', encoding='utf-8')
    for line in pos_data:
        pos.write(line)
        pos.write('\n')

    neg = open('negative.txt', 'w', encoding='utf-8')
    for line in neg_data:
        neg.write(line)
        neg.write('\n')

    pos.close()
    neg.close()


def test3():
    lst = ['a', 'b', 'c']
    s = ' '.join(lst)
    print(s)


def test4():
    with open('positive1.txt', 'r', encoding='utf-8') as f:
        pos_data = f.readlines()
    print(len(pos_data), '1')
    pos_data = set(pos_data)
    print(len(pos_data), '2')
    with open('positive1.txt', 'w', encoding='utf-8') as f:
        f.writelines(pos_data)

    with open('negative1.txt', 'r', encoding='utf-8') as f:
        neg_data = f.readlines()
    print(len(neg_data), '1')
    neg_data = set(neg_data)
    print(len(neg_data), '2')
    with open('negative1.txt', 'w', encoding='utf-8') as f:
        f.writelines(neg_data)


if __name__ == '__main__':
    # get_token()
    # analyse()
    # test()
    # print_num()
    # test2()
    # test3()
    test4()
