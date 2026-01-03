# -*- encoding: utf-8 -*-

"""
Author: Hmily
GitHub: https://github.com/ihmily
Date: 2023-07-15 23:15:00
Update: 2025-10-23 18:28:00
Copyright (c) 2023-2025 by Hmily, All Rights Reserved.
Function: Get live stream data.
"""

import hashlib
import random
import subprocess
import time
import uuid
import tempfile
import os
import sys
from operator import itemgetter
import urllib.parse
import urllib.error
from typing import List, Optional, Dict
import httpx
import ssl
import re
import json
import execjs
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from . import JS_SCRIPT_PATH, utils
from .utils import trace_error_decorator, generate_random_string
from .logger import script_path
from .room import get_sec_user_id, get_unique_id, UnsupportedUrlError
from .http_clients.async_http import async_req
from .ab_sign import ab_sign


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
OptionalStr = str | None
OptionalDict = dict | None


def get_params(url: str, params: str) -> OptionalStr:
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    if params in query_params:
        return query_params[params][0]


async def get_play_url_list(m3u8: str, proxy: OptionalStr = None, header: OptionalDict = None,
                            abroad: bool = False) -> List[str]:
    resp = await async_req(url=m3u8, proxy_addr=proxy, headers=header, abroad=abroad)
    play_url_list = []
    for i in resp.split('\n'):
        if i.startswith('https://'):
            play_url_list.append(i.strip())
    if not play_url_list:
        for i in resp.split('\n'):
            if i.strip().endswith('m3u8'):
                play_url_list.append(i.strip())
    bandwidth_pattern = re.compile(r'BANDWIDTH=(\d+)')
    bandwidth_list = bandwidth_pattern.findall(resp)
    url_to_bandwidth = {url: int(bandwidth) for bandwidth, url in zip(bandwidth_list, play_url_list)}
    play_url_list = sorted(play_url_list, key=lambda url: url_to_bandwidth[url], reverse=True)
    return play_url_list


async def get_douyin_web_stream_data(url: str, proxy_addr: OptionalStr = None, cookies: OptionalStr = None):
    # 设置headers（保持与原代码一致）
    headers = {
        'cookie': 'ttwid=1%7C2iDIYVmjzMcpZ20fcaFde0VghXAA3NaNXE_SLR68IyE%7C1761045455'
                  '%7Cab35197d5cfb21df6cbb2fa7ef1c9262206b062c315b9d04da746d0b37dfbc7d',
        'referer': 'https://live.douyin.com/335354047186',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/116.0.5845.97 Safari/537.36 Core/1.116.567.400 QQBrowser/19.7.6764.400',
    }
    if cookies:
        headers['cookie'] = cookies

    try:
        # 使用Selenium获取页面HTML源码
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
        
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--user-agent={headers["user-agent"]}')
        
        # 设置代理（如果有）
        if proxy_addr:
            chrome_options.add_argument(f'--proxy-server={proxy_addr}')
        
        # 启动浏览器
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # 访问URL
            driver.get(url)
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            from selenium.common.exceptions import TimeoutException

            # ... 之前的代码（启动浏览器、访问URL）...

            driver.get(url)

            # 替换原来的 time.sleep(5) 为以下智能等待策略：
            try:
                # 策略1：等待页面基础结构加载完成（如 body 标签）
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print("✅ 页面基础结构加载完成")

                # 策略2：等待一个更具体的、表明页面已准备就绪的元素出现。
                # 例如，等待包含直播数据的脚本标签或特定的CSS类。这里需要根据实际页面调整。
                # 下面是一个示例，您可以尝试搜索页面中更具代表性的标志：
                # WebDriverWait(driver, 15).until(
                #     EC.presence_of_element_located((By.CLASS_NAME, "ZGg-n1ZU"))
                # )

                # 策略3（关键）：等待 JavaScript 的 document.readyState 变为 'complete'
                WebDriverWait(driver, 15).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                print("✅ 页面JavaScript执行完毕，已准备就绪")

            except TimeoutException:
                print("⚠️ 页面加载超时，但继续执行后续步骤...")



            
            # 获取页面源码
            html_content = driver.page_source


            # +++ 新增：诊断代码 +++
            try:
                with open("douyin_page_dump.html", "w", encoding="utf-8") as f:
                    f.write(html_content)
                print("✅ 页面源码已保存至：douyin_page_dump.html")
    
                # 可选：同时检查页面标题和URL，辅助判断页面状态
                print(f"   页面标题: {driver.title}")
                print(f"   当前URL: {driver.current_url}")
            except Exception as e:
                print(f"⚠️ 保存调试文件时出错: {e}")
            # +++ 诊断代码结束 +++



            
        finally:
            driver.quit()

        # ... （前面您已经获取到 html_content 的代码保持不变）

        # ========== 以下是需要替换/新增的代码块 ==========
        # 从HTML中提取直播流数据
        import re
        import json

        stream_data = None
        json_str_to_parse = None

        # 模式1：尝试寻找包含"stream"和"origin"等关键字的大型JSON对象（这是最可能成功的方式）
        pattern_large_json = r'<script id="RENDER_DATA" type="application/json">(.*?)</script>'
        match = re.search(pattern_large_json, html_content, re.DOTALL)

        if match:
            json_str_to_parse = match.group(1)
            print("✅ 模式1：找到 RENDER_DATA 脚本标签。")
        else:
            # 模式2：尝试搜索包含直播流URL的JSON片段
            pattern_stream_json = r'\"origin\"\s*:\s*\{\s*\"main\"\s*:\s*\{[^}]+\"flv\"\s*:\s*\"([^\"]+)\"[^}]+\"hls\"\s*:\s*\"([^\"]+)\"'
            match = re.search(pattern_stream_json, html_content)
            if match:
                flv_url = match.group(1).replace(r'\u0026', '&')
                hls_url = match.group(2).replace(r'\u0026', '&')
                # 手动构建一个结构化的stream_data
                stream_data = {
                    "origin": {
                        "main": {
                            "flv": flv_url,
                            "hls": hls_url
                        }
                    }
                }
                print("✅ 模式2：直接提取FLV/HLS URL成功。")

        if json_str_to_parse:
            try:
                # 处理转义字符
                json_str_cleaned = json_str_to_parse.replace(r'\u0026', '&')
                # 将JSON字符串解析为Python字典
                page_data = json.loads(json_str_cleaned)
        
                # 定义可能的路径来查找stream数据
                possible_paths = [
                    ['app', 'store', 'roomStore', 'roomInfo', 'room', 'stream_url', 'data', 'origin'],
                    ['app', 'store', 'RoomStore', 'roomInfo', 'room', 'stream_url', 'data', 'origin'],
                    ['store', 'roomStore', 'roomInfo', 'room', 'stream_url', 'data', 'origin'],
                    ['stream']  # 直接根路径
                ]
        
                for path in possible_paths:
                    current_data = page_data
                    try:
                        for key in path:
                            current_data = current_data[key]
                        stream_data = current_data
                        print(f"✅ 通过路径 {path} 找到直播流数据。")
                        break
                    except (KeyError, TypeError):
                        continue
                
            except json.JSONDecodeError as e:
                print(f"❌ 解析RENDER_DATA JSON时出错: {e}")

        # 最终检查
        if not stream_data:
            # 如果所有模式都失败，保存页面源码以供详细分析
            with open("failed_page_dump.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            raise Exception("所有提取模式均失败。页面源码已保存至 'failed_page_dump.html'，请检查页面结构或是否触发了反爬机制。")
        else:
            print("🎉 直播流数据提取成功！")


# ========== 替换代码块结束 ==========
        
        # 构建返回数据（保持与原结构一致）
        room_data = {
            'anchor_name': '',
            'status': 2,  # 假设直播中
            'stream_url': stream_data
        }
        
        # 尝试从HTML中提取主播名
        anchor_pattern = r'"nickname"\s*:\s*"([^"]+)"'
        anchor_match = re.search(anchor_pattern, html_content)
        if anchor_match:
            room_data['anchor_name'] = anchor_match.group(1)
        
        return room_data

    except Exception as e:
        print(f"Error message: {e} Error line: {e.__traceback__.tb_lineno}")
        room_data = {'anchor_name': ""}
    return room_data


@trace_error_decorator
async def get_douyin_app_stream_data(url: str, proxy_addr: OptionalStr = None, cookies: OptionalStr = None) -> dict:
    # 设置headers（保持与原代码一致）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://live.douyin.com/',
        'Cookie': 'ttwid=1%7CB1qls3GdnZhUov9o2NxOMxxYS2ff6OSvEWbv0ytbES4%7C1680522049%7C280d802d6d478e3e78d0c807f7c487e7ffec0ae4e5fdd6a0fe74c3c6af149511; my_rd=1; passport_csrf_token=3ab34460fa656183fccfb904b16ff742; passport_csrf_token_default=3ab34460fa656183fccfb904b16ff742; d_ticket=9f562383ac0547d0b561904513229d76c9c21; n_mh=hvnJEQ4Q5eiH74-84kTFUyv4VK8xtSrpRZG1AhCeFNI; store-region=cn-fj; store-region-src=uid; LOGIN_STATUS=1; __security_server_data_status=1; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; pwa2=%223%7C0%7C3%7C0%22; download_guide=%223%2F20230729%2F0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.6%7D; strategyABtestKey=%221690824679.923%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1691443863751%2C%22type%22%3Anull%7D; home_can_add_dy_2_desktop=%221%22; __live_version__=%221.1.1.2169%22; device_web_cpu_core=8; device_web_memory_size=8; xgplayer_user_id=346045893336; csrf_session_id=2e00356b5cd8544d17a0e66484946f28; odin_tt=724eb4dd23bc6ffaed9a1571ac4c757ef597768a70c75fef695b95845b7ffcd8b1524278c2ac31c2587996d058e03414595f0a4e856c53bd0d5e5f56dc6d82e24004dc77773e6b83ced6f80f1bb70627; __ac_nonce=064caded4009deafd8b89; __ac_signature=_02B4Z6wo00f01HLUuwwAAIDBh6tRkVLvBQBy9L-AAHiHf7; ttcid=2e9619ebbb8449eaa3d5a42d8ce88ec835; webcast_leading_last_show_time=1691016922379; webcast_leading_total_show_times=1; webcast_local_quality=sd; live_can_add_dy_2_desktop=%221%22; msToken=1JDHnVPw_9yTvzIrwb7cQj8dCMNOoesXbA_IooV8cezcOdpe4pzusZE7NB7tZn9TBXPr0ylxmv-KMs5rqbNUBHP4P7VBFUu0ZAht_BEylqrLpzgt3y5ne_38hXDOX8o=; msToken=jV_yeN1IQKUd9PlNtpL7k5vthGKcHo0dEh_QPUQhr8G3cuYv-Jbb4NnIxGDmhVOkZOCSihNpA2kvYtHiTW25XNNX_yrsv5FN8O6zm3qmCIXcEe0LywLn7oBO2gITEeg=; tt_scid=mYfqpfbDjqXrIGJuQ7q-DlQJfUSG51qG.KUdzztuGP83OjuVLXnQHjsz-BRHRJu4e986'
    }
    if cookies:
        headers['Cookie'] = cookies

    try:
        # 使用Selenium获取页面HTML源码（模拟移动端）
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
        
        # 配置Chrome选项（模拟移动端）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 设置移动端User-Agent
        mobile_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        chrome_options.add_argument(f'--user-agent={mobile_user_agent}')
        
        # 设置窗口大小为手机尺寸
        chrome_options.add_argument('--window-size=375,812')
        
        # 设置代理（如果有）
        if proxy_addr:
            chrome_options.add_argument(f'--proxy-server={proxy_addr}')
        
        # 启动浏览器
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # 访问URL
            driver.get(url)
            time.sleep(5)  # 等待页面加载
            
            # 添加Cookie（如果有）
            if cookies:
                cookie_list = cookies.split(';')
                for cookie in cookie_list:
                    if '=' in cookie:
                        name, value = cookie.strip().split('=', 1)
                        driver.add_cookie({'name': name, 'value': value})
                driver.refresh()
                time.sleep(3)
            
            # 获取页面源码
            html_content = driver.page_source
            
        finally:
            driver.quit()

        # 从HTML中提取直播间信息
        import re
        import json
        
        # 查找包含直播间信息的JSON数据
        room_pattern = r'"room"\s*:\s*(\{.*?\})\s*,\s*"'
        room_match = re.search(room_pattern, html_content, re.DOTALL)
        
        if not room_match:
            # 尝试其他可能的数据结构
            room_pattern = r'"roomInfo"\s*:\s*(\{.*?\})\s*,\s*"'
            room_match = re.search(room_pattern, html_content, re.DOTALL)
        
        if room_match:
            room_data_str = room_match.group(1)
            room_data = json.loads(room_data_str)
            
            # 确保数据结构一致
            if 'owner' in room_data and 'nickname' in room_data['owner']:
                room_data['anchor_name'] = room_data['owner']['nickname']
            
            return room_data
        else:
            raise Exception("无法从HTML中提取直播间数据")

    except Exception as e:
        print(f"Error message: {e} Error line: {e.__traceback__.tb_lineno}")
        room_data = {'anchor_name': ""}
    return room_data


@trace_error_decorator
async def get_douyin_stream_data(url: str, proxy_addr: OptionalStr = None, cookies: OptionalStr = None) -> dict:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://live.douyin.com/',
        'Cookie': 'ttwid=1%7CB1qls3GdnZhUov9o2NxOMxxYS2ff6OSvEWbv0ytbES4%7C1680522049%7C280d802d6d478e3e78d0c807f7c487e7ffec0ae4e5fdd6a0fe74c3c6af149511; my_rd=1; passport_csrf_token=3ab34460fa656183fccfb904b16ff742; passport_csrf_token_default=3ab34460fa656183fccfb904b16ff742; d_ticket=9f562383ac0547d0b561904513229d76c9c21; n_mh=hvnJEQ4Q5eiH74-84kTFUyv4VK8xtSrpRZG1AhCeFNI; store-region=cn-fj; store-region-src=uid; LOGIN_STATUS=1; __security_server_data_status=1; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; pwa2=%223%7C0%7C3%7C0%22; download_guide=%223%2F20230729%2F0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.6%7D; strategyABtestKey=%221690824679.923%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1691443863751%2C%22type%22%3Anull%7D; home_can_add_dy_2_desktop=%221%22; __live_version__=%221.1.1.2169%22; device_web_cpu_core=8; device_web_memory_size=8; xgplayer_user_id=346045893336; csrf_session_id=2e00356b5cd8544d17a0e66484946f28; odin_tt=724eb4dd23bc6ffaed9a1571ac4c757ef597768a70c75fef695b95845b7ffcd8b1524278c2ac31c2587996d058e03414595f0a4e856c53bd0d5e5f56dc6d82e24004dc77773e6b83ced6f80f1bb70627; __ac_nonce=064caded4009deafd8b89; __ac_signature=_02B4Z6wo00f01HLUuwwAAIDBh6tRkVLvBQBy9L-AAHiHf7; ttcid=2e9619ebbb8449eaa3d5a42d8ce88ec835; webcast_leading_last_show_time=1691016922379; webcast_leading_total_show_times=1; webcast_local_quality=sd; live_can_add_dy_2_desktop=%221%22; msToken=1JDHnVPw_9yTvzIrwb7cQj8dCMNOoesXbA_IooV8cezcOdpe4pzusZE7NB7tZn9TBXPr0ylxmv-KMs5rqbNUBHP4P7VBFUu0ZAht_BEylqrLpzgt3y5ne_38hXDOX8o=; msToken=jV_yeN1IQKUd9PlNtpL7k5vthGKcHo0dEh_QPUQhr8G3cuYv-Jbb4NnIxGDmhVOkZOCSihNpA2kvYtHiTW25XNNX_yrsv5FN8O6zm3qmCIXcEe0LywLn7oBO2gITEeg=; tt_scid=mYfqpfbDjqXrIGJuQ7q-DlQJfUSG51qG.KUdzztuGP83OjuVLXnQHjsz-BRHRJu4e986'
    }
    if cookies:
        headers['Cookie'] = cookies

    try:
        origin_url_list = None
        
        # 使用Selenium获取页面HTML源码
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
        
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 设置代理（如果有）
        if proxy_addr:
            chrome_options.add_argument(f'--proxy-server={proxy_addr}')
        
        # 设置User-Agent
        chrome_options.add_argument(f'--user-agent={headers["User-Agent"]}')
        
        # 启动浏览器
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # 访问URL
            driver.get(url)
            time.sleep(5)  # 等待页面加载
            
            # 添加Cookie（如果有）
            if cookies:
                cookie_list = cookies.split(';')
                for cookie in cookie_list:
                    if '=' in cookie:
                        name, value = cookie.strip().split('=', 1)
                        driver.add_cookie({'name': name, 'value': value})
                driver.refresh()  # 刷新页面应用Cookie
                time.sleep(3)
            
            # 获取页面源码
            html_str = driver.page_source
            
        finally:
            driver.quit()

        # 原有的解析逻辑保持不变
        match_json_str = re.search(r'(\{\\"state\\":.*?)]\\n"]\)', html_str)
        if not match_json_str:
            match_json_str = re.search(r'(\{\\"common\\":.*?)]\\n"]\)</script><div hidden', html_str)
        if not match_json_str:
            raise Exception("无法从HTML中提取JSON数据")
            
        json_str = match_json_str.group(1)
        cleaned_string = json_str.replace('\\', '').replace(r'u0026', r'&')
        room_store = re.search('"roomStore":(.*?),"linkmicStore"', cleaned_string, re.DOTALL).group(1)
        anchor_name = re.search('"nickname":"(.*?)","avatar_thumb', room_store, re.DOTALL).group(1)
        room_store = room_store.split(',"has_commerce_goods"')[0] + '}}}'
        json_data = json.loads(room_store)['roomInfo']['room']
        json_data['anchor_name'] = anchor_name
        
        if 'status' in json_data and json_data['status'] == 4:
            return json_data
            
        stream_orientation = json_data['stream_url']['stream_orientation']
        match_json_str2 = re.findall(r'"(\{\\"common\\":.*?)"]\)</script><script nonce=', html_str)
        
        if match_json_str2:
            json_str = match_json_str2[0] if stream_orientation == 1 else match_json_str2[1]
            json_data2 = json.loads(
                json_str.replace('\\', '').replace('"{', '{').replace('}"', '}').replace('u0026', '&'))
            if 'origin' in json_data2['data']:
                origin_url_list = json_data2['data']['origin']['main']
        else:
            html_str = html_str.replace('\\', '').replace('u0026', '&')
            match_json_str3 = re.search('"origin":\\{"main":(.*?),"dash"', html_str, re.DOTALL)
            if match_json_str3:
                origin_url_list = json.loads(match_json_str3.group(1) + '}')

        if origin_url_list:
            origin_hls_codec = origin_url_list['sdk_params'].get('VCodec') or ''
            origin_m3u8 = {'ORIGIN': origin_url_list["hls"] + '&codec=' + origin_hls_codec}
            origin_flv = {'ORIGIN': origin_url_list["flv"] + '&codec=' + origin_hls_codec}
            hls_pull_url_map = json_data['stream_url']['hls_pull_url_map']
            flv_pull_url = json_data['stream_url']['flv_pull_url']
            json_data['stream_url']['hls_pull_url_map'] = {**origin_m3u8, **hls_pull_url_map}
            json_data['stream_url']['flv_pull_url'] = {**origin_flv, **flv_pull_url}
            
        return json_data

    except Exception as e:
        print(f"First data retrieval failed: {url} Preparing to switch parsing methods due to {e}")
        return await get_douyin_app_stream_data(url=url, proxy_addr=proxy_addr, cookies=cookies)
