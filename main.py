import requests
import os
import datetime

# --- 配置区：这里填入所有人的ID和城市代码 ---
# 1. 让爸爸、妈妈、姐姐分别扫你的测试号二维码
# 2. 扫完后，在测试号后台列表里找到他们的 OpenID，填入下方列表
FAMILY_MEMBERS = [
    {"name": "舍友", "user": "op_Zv3NDp0wcrfYSBvPVipE90H3c", "city_code": "130281"},
    {"name": "姐姐", "user": "op_Zv3POyuCmKVyYXatwT_5EUuYs", "city_code": "130203"} # 姐姐的城市代码
]

def get_weather(city_code, key):
    # 注意：这里改成了 extensions=all，才能获取预报数据
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={key}&extensions=all"
    res = requests.get(url).json()
    # 返回当天的预报数据
    return res['forecasts'][0]['casts'][0]

def send_wechat():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={os.getenv('APP_ID')}&secret={os.getenv('APP_SECRET')}"
    token = requests.get(token_url).json()['access_token']
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"

    for person in FAMILY_MEMBERS:
        w = get_weather(person['city_code'], os.getenv('WEATHER_KEY'))
        
        data = {
            "touser": person['user'],
            "template_id": os.getenv('TEMPLATE_ID'),
            "data": {
                "date": {"value": str(datetime.date.today())},
                "region": {"value": f"{person['name']}的城市"},
                "weather": {"value": w['dayweather']},
                "min_temp": {"value": w['nighttemp'] + "℃"},
                "max_temp": {"value": w['daytemp'] + "℃"},
                "wind_dir": {"value": w['daywind'] + w['daypower'] + "级"},
                "proposal": {"value": "今天注意温差，照顾好身体！"}
            }
        }
        requests.post(send_url, json=data)

if __name__ == "__main__":
    send_wechat()
