# coding: utf-8
import base64
import requests


class BaiduAPI(object):
    '''文字识别'''
    __instance = None
    text_access_token = None
    image_access_token = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.image_api_key = "zC2rZlcrf1uD0hm6yosOCV6Z"
        self.image_secret_key = "xZ2QAwUiowfiYhDNqsC6MaT2pZfMD4Zn"
        self.text_api_key = "EzfSIezrThmLo9rVniwypRne"
        self.text_secret_key = "OvKDgdHog6fWGqcN5xcuy4Lb5Sv5Vims"

    def get_access_token(self, api_key, secret_key):
        try:
            url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(api_key, secret_key)
            res = requests.post(url)
            res.encoding = 'utf-8'
            res = res.json()
            acess_token = res.get('access_token', '')
            return acess_token
        except:
            return ''

    def get_accurate_basic(self, img_str):
        '''图片文字识别'''
        if not BaiduAPI.image_access_token:
            BaiduAPI.image_access_token = self.get_access_token(self.image_api_key, self.image_secret_key)
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={}'.format(BaiduAPI.image_access_token)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'image': img_str}
        res = requests.post(url, data=data, headers=headers)
        res.encoding = 'utf-8'
        res = res.json()
        words = res.get('words_result', '')
        if words:
            word_str = ''
            for i in words:
                word_str += i['words']
            print(word_str)

    def get_antispam(self, content):
        '''敏感词鉴定'''
        if not BaiduAPI.text_access_token:
            BaiduAPI.text_access_token = self.get_access_token(self.text_api_key, self.text_secret_key)
        url = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam?access_token={}'.format(BaiduAPI.text_access_token)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'content': content}
        res = requests.post(url, data=data, headers=headers)
        res.encoding = 'utf-8'
        res = res.json()
        print(res)


def get_img_base64():
    # # 线上图片转base64
    # url = 'https://image.qiniu.chuxiaocheng.cn/icon_4020191016092728'
    # res = requests.post(url)
    # res.encoding = 'utf-8'
    # content = res.content
    # b64str = base64.b64encode(content).decode()
    # return b64str

    # 本地图片转base64
    with open('zhangdan.jpg', 'rb') as f:
        b64str = base64.b64encode(f.read())
    return b64str


if __name__ == "__main__":
    baidu = BaiduAPI()
    # baidu.get_accurate_basic(get_img_base64())
    baidu.get_antispam('狗日的')
