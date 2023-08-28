# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/9 16:56
@Auth ： DingKun
@File ：start.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import datetime
import json
import time
import requests
from bs4 import BeautifulSoup
import chardet
from fake_useragent import UserAgent
from requests_html import HTMLSession
from log import log_create
from operation_sql import saveToMysql
s = requests.Session()
s.keep_alive = False


def www_tianqi_com(city: str, query_month: str):
    """
    根据查询月份，返回天气网的历史数据
    :param city: 城市， eg：xiangcheng 相城区， suzhou 苏州
    :param query_month: 查询月份，eg 202301
    :return:
    eg：
    result = []
    for i in range(1, 8):
        result += www_tianqi_com('suzhou', '2023' + '0' + str(i))
        time.sleep(1)
    result = result[0::1]
    dt = pd.DataFrame(result)
    dt.columns = ['日期','星期', '最高温度','最低温度','天气','风速']
    pd.DataFrame.to_excel(dt, 'result.xlsx', index=False)
    """
    cookies = {
        'Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2': '1692154110',
        'Hm_lvt_30606b57e40fddacb2c26d2b789efbcb': '1692154120',
        'Hm_lpvt_30606b57e40fddacb2c26d2b789efbcb': '1692154120',
        'Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2': '1692154132',
    }
    session = HTMLSession()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1692154110;
        # Hm_lvt_30606b57e40fddacb2c26d2b789efbcb=1692154120; Hm_lpvt_30606b57e40fddacb2c26d2b789efbcb=1692154120;
        # Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1692154132',
        'Referer': 'https://lishi.tianqi.com/xiangchengqu/index.html',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': UserAgent().random,
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    rqg = session.get(f'https://lishi.tianqi.com/{city}/{query_month}.html', cookies=cookies, headers=headers)
    rqg.encoding = chardet.detect(rqg.content)['encoding']
    # 初始化HTML
    html = rqg.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')  # 生成BeautifulSoup对象
    soup.prettify()
    all_reault = soup.find_all('ul', class_='thrui')
    return_data = []
    for i in all_reault:
        try:
            one_day = i.find_all('li')
            for j in one_day:
                data = j.find_all('div')
                return_data.append([])
                for index, k in enumerate(data):
                    data_str = k.get_text()
                    if "星期" in data_str:
                        return_data[-1].append(data_str.split(' ')[0])
                        return_data[-1].append(data_str.split(' ')[1])
                    elif "℃" in data_str:
                        return_data[-1].append(data_str[:-1])
                    elif "风" in data_str:
                        return_data[-1].append(data_str.split(' ')[1])
                    else:
                        return_data[-1].append(data_str)
        except Exception as e:
            print(e)

    return return_data


city_position = {"相城区": [120.64857, 31.37469], "常熟市": [120.75950, 31.65954], "姑苏区": [120.62346, 31.34183],
                 "虎丘区": [120.57847, 31.30193], "昆山市": [120.98745, 31.39086], "太仓市": [121.13560, 31.46460],
                 "吴江区": [120.65157, 31.14464], "吴中区": [120.63850, 31.26826], "张家港市": [120.56156, 31.88114]}


def The_tomorrow_io_weather(city_name, city_local: list, query_type: str):
    """
    使用tomorrow.io api 查询指定城市的天气数据
    :param city_name: 城市中文名称
    :param city_local: 城市地理位置，[所在经度、所在纬度]
    :param query_type: 历史数据——history，预测数据——forecast
    :return:天气数据列表，列表元素为字典类型，包含时间点以及相应的天气数据
    """
    if query_type == "history":
        url = f"https://api.tomorrow.io/v4/weather/history/recent?location={city_local[1]},{city_local[0]}&timesteps=1h&apikey=95uLJwaji751lMHVOVSLS37ljRDdNaB4"
    elif query_type == "forecast":
        pass
    else:
        pass
    headers = {"accept": "application/json"}
    response = s.get(url, headers=headers)
    json_data = json.loads(response.text)
    return_data = []
    for key, value in json_data.items():
        if key == "timelines":
            for key_hour, data in value.items():
                for i in data:
                    return_data.append([])
                    time_ = i["time"]
                    return_data[-1].append(city_name)
                    # temperature_values = i["values"]["temperature"]
                    return_data[-1].append(i["values"]["temperature"])
                    # humidity_values = i["values"]["humidity"]
                    return_data[-1].append(i["values"]["humidity"])
                    # dewPoint_values = i["values"]["visibility"]
                    return_data[-1].append(i["values"]["visibility"] * 1.609344)
                    # windSpeed_values = i["values"]["windSpeed"]
                    return_data[-1].append(i["values"]["windSpeed"] * 1.609344)
                    # pressureSurfaceLevel_values = i["values"]["pressureSurfaceLevel"]
                    return_data[-1].append(i["values"]["pressureSurfaceLevel"])
                    # freezingRainIntensity_values = i["values"]["freezingRainIntensity"]
                    # return_data[-1]["evapotranspiration"] = i["values"]["evapotranspiration"]
                    # rainAccumulation_values = i["values"]["rainAccumulation"]
                    return_data[-1].append(i["values"]["rainAccumulation"] * 2.54)
                    # cloudCover_values = i["values"]["cloudCover"]
                    return_data[-1].append(i["values"]["cloudCover"])
                    return_data[-1].append(time_.replace('T', ' ').replace('Z', ''))
    return return_data


if __name__ == "__main__":
    city_name = '相城区'
    while True:
        time_now = datetime.datetime.now()
        if time_now.hour == 13:
            query_region = list(city_position.keys())
            success_query_region = {}
            success_save_region = []
            needs_save_data = []
            while True:
                #  首先查询天气数据
                for city_name in query_region:
                    if city_name not in success_query_region:
                        return_data = The_tomorrow_io_weather(city_name, city_position[city_name], 'history')
                        if len(return_data) != 0:
                            success_query_region[city_name] = return_data
                            log_create.info(city_name + '天气查询成功')
                            time.sleep(5)
                        else:
                            log_create.info(city_name + '天气查询失败')
                    else:
                        continue
                #  然后保存数据
                for city_name, data in success_query_region.items():
                    if city_name not in success_save_region:
                        save_result = saveToMysql(data)
                        if save_result:
                            log_create.info(city_name + '天气数据保存成功')
                            success_save_region.append(city_name)
                            time.sleep(2)
                            needs_save_data.append(data)
                        else:
                            log_create.info(city_name + '天气数据保存失败')
                    else:
                        pass
                #  核对所有区域天气数据是否均保存
                if len(success_save_region) == len(query_region):
                    break
                else:
                    pass
                # print('当前时间07\n', return_data)
            time.sleep(5000)
        else:
            time.sleep(1)
