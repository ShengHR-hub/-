import requests
import os
import datetime

# 用户和城市的映射配置
# key 是微信里的 UserID，value 是对应城市的名称和代码
USER_CONFIGS = [
    
    {"user": "op_Zv3POyuCmKVyYXatwT_5EUuYs", "city_code": "130203", "city_name": "唐山路北区"}
]

def get_weather(city_code, key):
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={key}"
    res = requests.get(url).json()
    return res['lives'][0]

def send_wechat():
    # 1. 获取Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={os.getenv('APP_ID')}&secret={os.getenv('APP_SECRET')}"
    token = requests.get(token_url).json()['access_token']
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"

    # 2. 循环给每个人发送
    for item in USER_CONFIGS:
        w = get_weather(item['city_code'], os.getenv('WEATHER_KEY'))
        
        data = {
            "touser": item['user'], # 这里获取的是配置里的对应ID
            "template_id": os.getenv('TEMPLATE_ID'),
            "data": {
                "date": {"value": str(datetime.date.today())},
                "region": {"value": item['city_name']},
                "weather": {"value": w['weather']},
                "min_temp": {"value": "未知"}, 
                "max_temp": {"value": w['temperature'] + "℃"},
                "wind_dir": {"value": w['winddirection'] + w['windpower'] + "级"},
                "proposal": {"value": "注意温差，照顾好自己！"}
            }
        }
        requests.post(send_url, json=data)

if __name__ == "__main__":
    send_wechat()
