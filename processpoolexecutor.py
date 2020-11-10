'''多进程版'''
import requests
import time
# from urllib.parse import quote
import math
from urllib.request import urlretrieve
from urllib.request import quote
import pathlib
import os
import re
from concurrent.futures import ProcessPoolExecutor
url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&pn={num}&word={word}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
}
root = pathlib.Path.cwd()
image_name = '奥特曼_10p_t_exe2'
if not os.path.exists(image_name):
    os.mkdir(image_name)
i_path =os.path.join(root, image_name)
def down_images(page_num=0, file_path = i_path, word='表情包',p=0):
    inum = 0
    p_n = get_page_num(word)
    step = math.ceil(p_n/p)
    start_step = page_num*step
    end_step = page_num*step +step
    for i in range(start_step, end_step):
        res = requests.get(url.format(num=i*30, word=word), headers=headers).text
        image_url_list = re.findall('.*?"thumbURL":"(.*?)"', res)
        if image_url_list:
            for _ in image_url_list:
                # print("正在下载  {}".format(_))
                i_name = _.split('/')[-1]
                image_dir_i = os.path.join(file_path, i_name)
                urlretrieve(_, image_dir_i)
                inum += 1
        else:
            print("地址为 {} :没有图片".format(url.format(num=i*30, word=quote(word))))

    print("进程{}已经下载了 {}图片".format(os.getpid(), inum))

def get_page_num(word):
    url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&pn=0&word={}'.format(word)
    res = requests.get(url, headers=headers).json()
    listnum= res['listNum']
    page_num = math.ceil(listnum/30)
    return page_num

def my_process():
    with ProcessPoolExecutor() as executor:
        p_nums = 10
        for i in range(p_nums):
            executor.submit(down_images, i, word='奥特曼',p=p_nums)
            # print(i_path, i,)

if __name__ =='__main__':
    start_time = time.time()
    print("start time : {}".format(time.ctime()))
    my_process()
    spend_time = time.time() - start_time
    print("end time :{}".format(time.ctime()))
    print("spend time {} sec".format(spend_time))#40秒左右
    # print("一共下载了{}张图片".format(inum))
    #进程中没有全局变量
