import urllib
import urllib.request
import os
import requests
from contextlib import closing
import progressbar

try:
    from color_print import *
    from config import *
except ImportError:
    from .color_print import *
    from .config import *


# 创建下载文件夹目录文件目录
def create_keep_path(title):
    folder_path = keep_path + title
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        print(title + ' exit ------')


# 下载图片
def download_image(link, path):
    try:
        urllib.request.urlretrieve(link, path, call_back)
    except:
        pass
        # print("Download_fail "+link+" "+path )


# 下载回显
def call_back(blocknum, blocksize, totalsize):
    # @blocknum: 已经下载的数据块    @blocksize: 数据块的大小    @totalsize: 远程文件的大小
    percent = 100.0 * blocknum * blocksize / totalsize
    sys.stdout.write("\rDownloading : %.2f%%\r" % percent)
    sys.stdout.flush()
    if percent >= 100:
        sys.stdout.write("\rDownloading : %.2f%% -> " % 100)
        print('Download_Success ')


# 下载一组图片 一个连接下所有图片
def down_group_img(img_down_list, title):
    create_keep_path(title)
    pool = multiprocessing.Pool(processes=pool_num)
    for img_down_link in img_down_list:
        down_path = keep_path + title + '\\' + os.path.basename(img_down_link)
        pool.apply_async(download_image, (img_down_link, down_path))
    pool.close()
    pool.join()


# 获取已经下载的图片链接
def get_has_down_by_txt():
    file = open(has_down_path, 'r', encoding='utf-8')
    has_down = [line.split('<|>')[0].strip() for line in file]
    return has_down


# 保存已经下载的链接到
def keep_has_down_to_txt(meizi):
    has_down_txt = open(has_down_path, 'a', encoding='utf-8')
    split_text = '\t' + '<|>' + '\t'
    has_down_txt.write(
        meizi.link + split_text +
        meizi.title + split_text +
        meizi.category + split_text +
        meizi.date + '\n')
    has_down_txt.close()


# 设置请求头
def get_header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'image-test/webp,image-test/apng,image-test/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers


# 使用reqursts下载图片
def down_image_list(down_link_list, title):
    create_keep_path(title)
    for down_link in down_link_list:
        down_path = keep_path + title + '\\' + os.path.basename(down_link)
        print('Download   ' + down_link)
        with open(down_path, "wb+") as file:
            file.write(requests.get(down_link, headers=get_header(down_link)).content)
