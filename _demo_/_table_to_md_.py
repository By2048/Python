import re
from numpy import *
import numpy as np
import sys
from bs4 import BeautifulSoup
import re
import os

try:
    from markdown.config import *
except ImportError:
    from config import *

desktop_file_path = r'E:\Script\table_to_md_input.txt'

from _tool_._zh_cn_ import get_word_length, get_zh_cn_num, get_zh_code_num


# test='3.1415926'
# print(test.center(20)+'werwer')
# print(test.ljust(20,'=')+'werwer')
# print('{:10s} {:10s}'.format('Hello', 'World')+'rwerwe')


# 设置每行项目的分割方式 四个空格 或者 \t
def splite_items(line):
    splite_tab = line.split('\t')
    splite_space = line.split('    ')
    if len(splite_tab) > len(splite_space):
        items = splite_tab
    elif len(splite_tab) < len(splite_space):
        items = splite_space
    else:
        items = splite_tab
    return items


# 获取列数
def get_tab_num(input_lines):
    first_line = splite_items(input_lines[0])
    num = len(first_line)
    return num


# 获取每行的长度
def get_all_word_length(input_lines):
    lengths = []
    for each_line in input_lines:
        each_line_length = []
        split_lines = splite_items(each_line)
        # split_lines=line.split('\t')
        # if len(split_lines)==1:
        #     split_lines=line.split('    ')
        for item in split_lines:
            length = get_word_length(item)
            each_line_length.append(length)
        lengths.append(each_line_length)
    return lengths


# 获取整个输入的最大的行的长度
def get_word_max_lengths(word_lengths):
    max_lengths = []
    new_length = np.array(word_lengths)
    for num in range(tab_num):
        max_length = max(new_length[:, num])
        max_length += 4
        max_lengths.append(max_length)
    return max_lengths


# 获取主体
def get_md_lines(input_lines, word_max_lengths, tab_num):
    lines = []

    first_line = ''
    second_line = ''
    for (num, word_len) in zip(range(tab_num), word_max_lengths):
        first_line += '|   ' + ' ' * (word_len - 3 - 1) + '   '
    first_line += '|'
    for (num, word_len) in zip(range(tab_num), word_max_lengths):
        second_line += '|   ' + '-' * (word_len - 3 - 1) + '   '
    second_line += '|'
    lines.append(first_line)
    lines.append(second_line)

    for each_line in input_lines:
        items = splite_items(each_line)
        line = ''
        for (item, num) in zip(items, range(tab_num)):
            line += '|' + ' ' * 3
            line += item.ljust(
                word_max_lengths[num] - get_zh_cn_num(item) - get_zh_code_num(item) - 1)
        line += '|'
        lines.append(line)
    return lines


# 解析html文件
def get_html_lines(soup):
    lines = []
    first_th = [item.get_text() for item in soup.find('tr').find_all('th')]
    if len(first_th) != 0:
        lines.append("\t".join(first_th))
    for tr in soup.find_all('tr')[1:]:
        all_td = []
        for td in tr.find_all('td'):
            if len(tr.find_all('td')) != 0:
                if td.find('ul') != None:
                    all_li = [item.get_text() for item in td.find('ul').find_all('li')]
                    all_td.append(" ".join(all_li))
                else:
                    all_td.append(td.get_text())
        lines.append("\t".join(all_td))
    return lines


def replace_table_to_space(lines):
    return lines


if __name__ == '__main__':

    tab_num = 0
    word_max_lengths = []
    input_lines = []
    output_lines = []
    sentinel = '===='  # 输入以 ==== 结束

    file_size = os.path.getsize(desktop_file_path)
    if file_size != 0:
        print('\n')
        with open(desktop_file_path, 'r', encoding='gbk') as file:
            for line in file.readlines():
                input_lines.append(line.replace('\n', ''))
            print("\n".join(input_lines))
        print('\n')
    else:
        print('输入以 ==== 结束')
        # 输入部分
        for line in iter(input, sentinel):
            input_lines.append(line)
        print('\n')
    if input_lines[0][0:6] == '<table':
        soup = BeautifulSoup("".join(input_lines), "lxml")
        input_lines = get_html_lines(soup)
        print('\n'.join(output_lines), end='\n\n')

    # 检查输入
    for tab_line in input_lines:
        items = splite_items(tab_line)
        print(len(items), end='    ')
        print(items)
    print('\n')

    tab_num = get_tab_num(input_lines)
    word_lengths = get_all_word_length(input_lines)
    word_max_lengths = get_word_max_lengths(word_lengths)

    # 输出计算的信息
    print('tab_num             ' + str(tab_num))
    print('word_lengths        ' + str(word_lengths))
    print('word_max_lengths    ' + str(word_max_lengths))
    print('\n')

    # 获取主体
    output_lines = get_md_lines(input_lines, word_max_lengths, tab_num)
    print('\n'.join(output_lines), end='\n\n')
