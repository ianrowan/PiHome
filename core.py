import requests

def get_web_data():
    url = "http://mindbuilderai.com/validate"
    params = {"key":"GANs256ian"}

    data = requests.post(url=url, data=params)

    return data.text["unique"], data.text["daily"]
