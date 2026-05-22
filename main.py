import requests
import os
import datetime

# 🎯 1. 接收消息的群发白名单（直接从你测试号后台复制的真实 OpenID）
USER_LIST = [
    "op_Zv3Mm29FVZbdPNCjbtXtnZkmo",  # 释然（你自己的微信）
    "op_Zv3POyuCmKVyyXatwT_5EUuYs",  # 西柚（姐姐的微信）
    "op_Zv3NDp0wcrFYSBvPVipE90H3c"   # 🧠㤘（舍友/爸妈的微信）
]

def get_weather(city_code, key):
    # 使用 extensions=all 获取天气预报，确保能拿到最高温和最低温
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={key}&extensions=all"
    res = requests.get(url).json()
    if res.get('forecasts'):
        return res['forecasts'][0]['casts'][0]
    return None

def send_wechat():
    # 获取微信 Access Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={os.getenv('APP_ID')}&secret={os.getenv('APP_SECRET')}"
    token = requests.get(token_url).json()['access_token']
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"

    weather_key = os.getenv('WEATHER_KEY')
    
    # 🎯 2. 同时抓取两个城市的天气预报
    zh_weather = get_weather("130281", weather_key)  # 遵化市
    lb_weather = get_weather("130203", weather_key)  # 唐山路北区

    if not zh_weather or not lb_weather:
        print("天气数据获取失败，请检查高德 KEY 或城市代码")
        return

    # 🎯 3. 将两地数据完美揉合，精准对应你现有的模板字段（完全不需要去微信后台改模板！）
    template_data = {
        "date": {"value": str(datetime.date.today())},
        "region": {"value": "遵化 ＆ 唐山路北"},
        "weather": {"value": f"遵化({zh_weather['dayweather']}) | 路北({lb_weather['dayweather']})"},
        "max_temp": {"value": f"遵化 {zh_weather['daytemp']}℃ | 路北 {lb_weather['daytemp']}℃"},
        "min_temp": {"value": f"遵化 {zh_weather['nighttemp']}℃ | 路北 {lb_weather['nighttemp']}℃"},
        "wind_dir": {"value": f"遵化 {zh_weather['daywind']}风{zh_weather['daypower']}级 | 路北 {lb_weather['daywind']}风{lb_weather['daypower']}级"},
        "proposal": {"value": "全家天气合集播报，多地温差大，记得早晚添衣！"}
    }

    # 🎯 4. 循环遍历名单，确保每一个人都能收到这份一模一样的全家天气合集
    for user_id in USER_LIST:
        payload = {
            "touser": user_id,
            "template_id": os.getenv('TEMPLATE_ID'),
            "data": template_data
        }
        response = requests.post(send_url, json=payload).json()
        print(f"发送给 {user_id} 结果: {response}")

if __name__ == "__main__":
    send_wechat()
