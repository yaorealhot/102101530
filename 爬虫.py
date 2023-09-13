import collections
import re
import json
import time
import requests
import warnings
import wordcloud
from collections import Counter
import pandas as pd
import openpyxl
import jieba
from matplotlib import pyplot as plt
import PIL
import numpy

# 请求头
headers = {
    "cookie": 'buvid3=0375A456-07FE-C312-D4B3-36D2F803CD7F18354infoc; b_nut=1674884018; i-wanna-go-back=-1; _uuid=101074DFF5-7FC7-558C-C7DA-E5D3C831295D19039infoc; nostalgia_conf=-1; CURRENT_FNVAL=4048; rpdid=|(u))kk))l|m0J\'uY~R))R|JY; buvid_fp_plain=undefined; header_theme_version=CLOSE; b_ut=5; hit-dyn-v2=1; buvid4=E86AFAC7-8E6F-FD51-C944-E05A5E1BBF1119453-023012813-Sfw%2Bq8N2F38Nzbq0ojJXwQ%3D%3D; CURRENT_PID=8ef22160-ca2f-11ed-a546-3126efa05357; hit-new-style-dyn=1; CURRENT_QUALITY=80; FEED_LIVE_VERSION=V8; LIVE_BUVID=AUTO8216813753672881; home_feed_column=5; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ0ODE4MTEsImlhdCI6MTY5NDIyMjYxMSwicGx0IjotMX0.83cYJbNV-2Bc-rs3MOB5Vsz26S60A_UqokrwRMft0Q8; bili_ticket_expires=1694481811; SESSDATA=f864407e%2C1709774611%2C55fb1%2A92; bili_jct=9b8ff6546ff6d9b113bbbb6e110f5262; DedeUserID=433458894; DedeUserID__ckMd5=e3a34f4dcd795465; sid=4qfwc8iu; bp_video_offset_433458894=839646332364783636; fingerprint=db37aebaceed0fedd9f7e2b08ab5fc88; PVID=1; buvid_fp=db37aebaceed0fedd9f7e2b08ab5fc88; innersign=0; b_lsid=5C618134_18A86D7A5E9; browser_resolution=1528-258',
    "origin": 'https://www.bilibili.com',
    "referer": 'https://www.bilibili.com/video/BV1yF411C7ZJ/?spm_id_from=333.337.search-card.all.click&vd_source=6364b9fc01d71238e3bed6767b84f5e2',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76'
}


# 获取oid
def get_oid(page, video_num):
    # 获取bvid
    bvid_url = f'http://api.bilibili.com/x/web-interface/search/all/v2?page={page + 1}&keyword=日本核污染水排海'
    bvid_res = requests.get(url=bvid_url, headers=headers, verify=False).text
    bvid_json_dict = json.loads(bvid_res)
    bvid = bvid_json_dict["data"]["result"][11]["data"][video_num]["bvid"]

    # 获取cid
    cid_url = f'http://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp'
    cid_res = requests.get(url=cid_url, headers=headers, verify=False).text
    cid_json_dict = json.loads(cid_res)
    return cid_json_dict["data"][0]["cid"]


# 获取弹幕
def get_danmu(cid):
    # 请求网址
    url = f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={cid}&date=2023-09-05'
    # 获取响应
    res = requests.get(url=url, headers=headers)
    # 正则表达式提取中文字符
    text = re.findall('.*?([\u4e00-\u9fa5]+).*?', res.text)
    # 将弹幕输出到txt文件中
    with open('弹幕.txt', 'a', encoding='utf-8') as f:
        for index in text:
            f.write(index)
            f.write('\n')


# 排序
def danmu_sort(n):
    wb = openpyxl.Workbook()
    wb.save('排名前20弹幕.xlsx')
    danmu_list = []
    with open('弹幕.txt', mode='r', encoding='utf-8') as d:
        for index in d:
            danmu_list.append(index.strip())
    top20_danmu = Counter(danmu_list).most_common(n)
    df = pd.DataFrame(top20_danmu, index=list(range(1, n + 1)), columns=['弹幕内容', '出现次数'])
    df.to_excel('排名前20弹幕.xlsx')


# 生成词云
def draw_word_cloud():
    pic = numpy.array(PIL.Image.open('词云样式.png'))
    wc = wordcloud.WordCloud(mask=pic, background_color='white', font_path='C:\\Windows\\Fonts\\FZSTK.TTF', colormap='Reds')
    papers = open('弹幕.txt', 'r', encoding='utf-8').read().replace('\n', '')
    result = jieba.lcut(papers)
    danmu = ' '.join(result)
    wc.generate(danmu)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

def main():
    count = 300
    warnings.filterwarnings("ignore")
    # 主程序
    # for page in range(0, 15):
    #     for video_num in range(0, 20):
    #         get_danmu(get_oid(page, video_num))
    #         time.sleep(0.3)
    #         print(count)
    #         count -= 1
    # danmu_sort(20)
    draw_word_cloud()


main()
