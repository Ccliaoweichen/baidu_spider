'''多线程版'''
import requests
import time
# from urllib.parse import quote
from urllib.request import urlretrieve
from urllib.request import  quote
import pathlib
import os
import re
import math
from concurrent.futures import ThreadPoolExecutor
from threading import currentThread
url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&pn={num}&word={word}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
}
root = pathlib.Path.cwd()
image_name = '奥特曼_10_t_p_e6'
if not os.path.exists(image_name):
    os.mkdir(image_name)
i_path =os.path.join(root, image_name)
def down_images(page_num=0, thread_num=5,  file_path = i_path, word='奥特曼'):
        # params = {
        #     "word": "表情包"
        # }
    # global count
    # count = 0
    page = get_page_num(word)
    step = math.ceil(page/thread_num)
    inum = 0
    start_step = page_num*step
    end_step = page_num*step + step
    # print("正在下载{}到{}".format(start_step, end_step))
    for _ in range(start_step, end_step):
        print("正在下载{}页的图片".format(_))
        res = requests.get(url.format(num=_*30, word=word), headers=headers).text
        thumburl_list = re.findall('.*?"thumbURL":"(.*?)"', res)
        if thumburl_list:
            for _ in thumburl_list:
                # print("正在下载  {}".format(_))
                i_name = _.split('/')[-1]
                image_dir_i = os.path.join(file_path, i_name)
                urlretrieve(_, image_dir_i)
                inum += 1
        else:
            print("没有图片，地址为：{}".format(url.format(num=_*30, word=quote(word))))
            # break #不能使用break 让程序无法退出来 因为有线程直接退出来了
    print("线程{}已经下载了 {}图片".format(currentThread(), inum))

def get_page_num(word):
    url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&pn=0&word={}'.format(word)
    res = requests.get(url, headers=headers).json()
    listnum= res['listNum']
    page_num = math.ceil(listnum/30)
    return page_num
def my_thread():
    with ThreadPoolExecutor() as executor:
        p_nums = 10
        for i in range(p_nums):
            executor.submit(down_images, i, p_nums)
            # print(i_path, i,)

if __name__ =='__main__':
    start_time = time.time()
    print("start time : {}".format(time.ctime()))
    my_thread()
    # print("总共下载了{}张图片".format(count))
    spend_time = time.time() - start_time
    print("end time :{}".format(time.ctime()))
    print("spend time {} sec".format(spend_time))#四十秒左右
    #线程池中没有全局变量
