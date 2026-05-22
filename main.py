import requests
import os
import datetime

def get_weather():
    # 从 GitHub Secrets 获取 Key
    key = os.getenv('WEATHER_KEY')
    # 遵化市的 city_code 是 130281，你可以根据需要修改
    city_code = "130281" 
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={key}"
    res = requests.get(url).json()
    # 高德的实时天气在 lives 列表中
    w = res['lives'][0]
    return w

def send_wechat():
    # 1. 获取Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={os.getenv('APP_ID')}&secret={os.getenv('APP_SECRET')}"
    token = requests.get(token_url).json()['access_token']
    
    # 2. 获取天气
    w = get_weather()
    
    # 3. 发送模板消息 (对应你配置的模板格式)
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    data = {
        "touser": os.getenv('USER_ID'),
        "template_id": os.getenv('TEMPLATE_ID'),
        "data": {
            "date": {"value": str(datetime.date.today())},
            "region": {"value": w['city']},
            "weather": {"value": w['weather']},
            "min_temp": {"value": "暂无数据"}, # 高德实时接口通常不提供预报温差
            "max_temp": {"value": w['temperature'] + "℃"},
            "wind_dir": {"value": w['winddirection'] + w['windpower'] + "级"},
            "pm2p5": {"value": "暂无"},
            "category": {"value": "良好"},
            "sunrise": {"value": "暂无"},
            "sunset": {"value": "暂无"},
            "proposal": {"value": "出门请查看实时天气"}
        }
    }
    requests.post(send_url, json=data)

if __name__ == "__main__":
    send_wechat()
