import requests
from lxml import etree
from urllib import request

url = "http://www.netbian.com/"
User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
headers = {
    'User_Agent': User_Agent
}
res = requests.get(url, headers=headers)
result = res.text
# print(result)
html = etree.HTML(result)
data_list = html.xpath('//*[@class="list"]//li')
print(data_list)

for i in data_list:
    pic_url = i.xpath('//img/@src')
    title = i.xpath('//img/@alt')

for i in range(0, len(pic_url)):
    r = requests.get(pic_url[i])
    open('D:\\bizhi\\{}.jpg'.format(title[i]), 'wb').write(r.content)
    del r
