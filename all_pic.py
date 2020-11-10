'''普通版 '''
import requests
from pprint import pprint
import time
# from urllib.parse import quote
import pathlib
import os
import re

q_word = '表情包'
# q_word = quote(q_word)
url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&word={word}&pn={num}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
}
# params = {
#     'word': '表情包'
# }
def get_all_image_url(word='表情包', page_num=49):
    count=0
    images = []
    for i in range(page_num):
        print("第{}页图片".format(i+1))
        res = requests.get(url.format(word=word,num=i*30),  headers=headers).text
    # image_url_str = res.text.split("app.setData('imgData',")[1].strip().split(');')[0].strip()
        image_url_list = re.findall('.*?"thumbURL":"(.*?)"',res)
    # pprint(image_url_list)
        if image_url_list:
            for _ in image_url_list:
                count += 1
                images.append(_)
        else:
            break  #当前页面没有图片了  退出循环
    print("一共有{}页,{}张图片".format(i+1,count))
    return images

def save_images(image_name='image',images_url=[]):
    root = pathlib.Path.cwd()
    image_dir = os.path.join(root, image_name)
    if not os.path.exists(image_name):
        os.mkdir(image_name)
    count = 0
    for _ in images_url:
        i_name = _.split('/')[-1]
        image_path = os.path.join(image_dir, i_name)
        print("正在下载  {}".format(_))
        content = requests.get(_).content
        with open(image_path, 'wb')as f:
            f.write(content)
            count += 1
    print("保存完成，一起下载了{}张图片".format(count)) #1793s


if __name__ =='__main__':
    start_time = time.time()
    print("start time : {}".format(time.ctime()))
    # get_all_image_url('赛文', 3)
    # for i in get_all_image_url('赛文', 3):
    #     print(i)
    images_url = get_all_image_url('奥特曼', 49)
    # images = images_url[:7]
    save_images('奥特曼_two', images_url)
    spend_time = time.time() - start_time
    print("end time :{}".format(time.ctime()))
    print("spend time {} sec".format(spend_time))#spend time 121 sec
# pprint(res.text)