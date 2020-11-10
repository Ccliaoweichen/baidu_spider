'''多进程版'''
import requests
import time
# from urllib.parse import quote
from urllib.request import urlretrieve
import pathlib
import os
import math
import re
from multiprocessing import Pool
url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&pn={num}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
}
root = pathlib.Path.cwd()
image_name = '奥特曼_10mp-5'
if not os.path.exists(image_name):
    os.mkdir(image_name)
i_path =os.path.join(root, image_name)
def down_images(page_num=0, file_path = i_path):
        params = {
            "word": "奥特曼"
        }
        inum = 0
        p_n = get_page_num('奥特曼')
        step = math.ceil(p_n/10)
        start_step = page_num*step
        end_step = page_num*step +step
        for i in range(start_step, end_step):
            res = requests.get(url.format(num=i*30), params=params,  headers=headers).text
            image_url_list = re.findall('.*?"thumbURL":"(.*?)"', res)
            if image_url_list:
                for _ in image_url_list:
                    print("正在下载  {}".format(_))
                    i_name = _.split('/')[-1]
                    image_dir_i = os.path.join(file_path, i_name)
                    urlretrieve(_, image_dir_i)
                    inum += 1
        print("线程{}已经下载了 {}图片".format(os.getpid(), inum))

def get_page_num(word):
    url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&pn=0&word={}'.format(word)
    res = requests.get(url, headers=headers).json()
    listnum= res['listNum']
    page_num = math.ceil(listnum/30)
    return page_num

def my_pool():
    pool = Pool()
    pool.map(down_images, [i for i in range(10)])

if __name__ =='__main__':
    start_time = time.time()
    my_pool()
    # print("一起下载了{}张图片".format(count)) #进程池中不能使用全局变量
    print("start time : {}".format(time.ctime()))
    spend_time = time.time() - start_time
    print("end time :{}".format(time.ctime()))
    print("spend time {} sec".format(spend_time))
    # print("一共下载了{}张图片".format(count))
    #进程中没有全局变量
