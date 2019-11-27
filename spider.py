import csv
import requests
import urllib
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont


def getHTMLText(url):  # 获取网站
    try:
        userAgent = {'uesr-agent': 'Mozilla/5.0'}  # 更改UA
        r = requests.get(url, headers=userAgent)
        r.raise_for_status()  # 检测访问是否出现异常
        r.encoding = r.apparent_encoding  # 更改网页编码至可读
        return r.text
    except:
        return "产生异常"


def download_font(demo):  # 下载字体文件
    demo = BeautifulSoup(demo, "html.parser")  # 转换为BS对象
    dict_path = demo.find(type='text/css').string  # 提取字体的相对路径
    dict_link = re.findall(re.compile(r'[(](.*?)[)]', re.S), dict_path)
    dict_link = dict_link[0]
    down_link = urljoin("https://www.shixiseng.com/", dict_link)  # 拼接成绝对路径下载
    urllib.request.urlretrieve(down_link, "file.woff2")  # 下载


def font_dict():  # 处理字体文件建立反反爬字典
    font = TTFont('file.woff2')
    font.saveXML('shixi.xml')  # 转换为xml方便读写
    ccmap = font['cmap'].getBestCmap()
    # print("ccmap:\n", ccmap)
    newmap = {}
    for key, value in ccmap.items():
        key = hex(key)
        value = value.replace('uni', '')
        a = 'u' + '0' * (4 - len(value)) + value
        newmap[key] = a
    # print("newmap:\n", newmap)
    newmap.pop('0x78')
    for i, j in newmap.items():
        newmap[i] = eval("u" + "\'\\" + j + "\'")
    # print("newmap:\n", newmap)

    new_dict = {}
    for key, value in newmap.items():
        key_ = key.replace('0x', '&#x')
        new_dict[key_] = value

    return new_dict


def decrypt_text(text, new_dict):  # 根据反反爬字典将加密文本替换正确文本
    for key, value in new_dict.items():
        if key in text:
            text = text.replace(key, value)
        else:
            pass
    return text


csvFile = open("csvData.csv", "w")  # 初始化CSV对象
writer = csv.writer(csvFile)
writer.writerow(["职位", "薪水", "公司名称","区域"])  # 定义CSV字段


def buildcsv(url):
    demo = getHTMLText(url)  # 获取原网站
    download_font(demo)  # 下载字典
    newdict = font_dict()  # 编译字典
    demo = decrypt_text(demo, newdict)  # 解密
    soup = BeautifulSoup(demo, "html.parser")  # 转换为bs对象

    for li in soup.find_all(class_='intern-wrap intern-item'):
        info1 = li.find(class_='clearfix intern-detail')  # 逐级访问
        info2 = info1.find(class_='f-l intern-detail__job')
        info3 = info2.find("p")
        info4 = info1.find(class_='f-r intern-detail__company')
        location = info2.find("span",class_='city ellipsis').string
        job = info3.find("a").string  # 职位
        salary = info3.find("span").string  # 薪资
        info5 = info4.find("p")
        company = info5.find("a").string  # 公司
        writer.writerow([job, salary, company,location])  # 写入CSV


def build_url(pages):
    base_url = "https://www.shixiseng.com/interns?page=1&keyword=IT%E4%BA%92%E8%81%94%E7%BD%91&type=intern&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend="
    for page in range(1, pages + 1):
        new = []
        for s in base_url:
            new.append(s)
        new[39] = str(page)
        buildcsv(''.join(new))
        print("第 %d 页已完成" % (page))