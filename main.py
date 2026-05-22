import requests
import os
import datetime

def get_weather():
    # 这里用的是和风天气API，如果还没申请可以去申请一个免费的
    key = os.getenv('WEATHER_KEY')
    # 遵化市城市ID: 101090506 (请根据实际情况替换)
    url = f"https://devapi.qweather.com/v7/weather/3d?location=101090506&key={key}"
    res = requests.get(url).json()
    daily = res['daily'][0]
    return daily

def send_wechat():
    # 1. 获取Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={os.getenv('APP_ID')}&secret={os.getenv('APP_SECRET')}"
    token = requests.get(token_url).json()['access_token']
    
    # 2. 获取天气
    weather = get_weather()
    
    # 3. 发送模板消息
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    data = {
        "touser": os.getenv('USER_ID'),
        "template_id": os.getenv('TEMPLATE_ID'),
        "data": {
            "date": {"value": str(datetime.date.today())},
            "region": {"value": "遵化市"},
            "weather": {"value": weather['textDay']},
            "min_temp": {"value": weather['tempMin']},
            "max_temp": {"value": weather['tempMax']},
            "wind_dir": {"value": weather['windDirDay']},
            "pm2p5": {"value": "优"},
            "category": {"value": "良好"},
            "sunrise": {"value": weather['sunrise']},
            "sunset": {"value": weather['sunset']},
            "proposal": {"value": "记得带伞，注意保暖"}
        }
    }
    requests.post(send_url, json=data)

if __name__ == "__main__":
    send_wechat()
