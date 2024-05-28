#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import math
import json
import os
import random

# 对现有样本数据进行小样本生成，分别是1%，10%，30%
current_path = os.getcwd()
dir_name_array = ["nky-chicken", "nky-chickenpig", "nky-pig"]
percent_array = [1, 10, 30]
for dir_name in dir_name_array:
    text_dir_path = os.path.join(current_path, "data", "dataset", "NER", dir_name)
    input_text_path = os.path.join(text_dir_path, "all.txt")
    # 打开原始文件
    with open(input_text_path, 'r') as file:
        lines = file.readlines()

    for percent in percent_array:
        percent_text_dir_path = os.path.join(text_dir_path, "percent_{}".format(percent))
        print(percent_text_dir_path)
        if not os.path.exists(percent_text_dir_path):
            os.makedirs(percent_text_dir_path)
        # 计算前百分之多少的行数
        percentage = percent / 100
        number_of_lines_to_get = int(len(lines) * percentage)

        # 获取前百分之多少的行
        selected_lines = lines[:number_of_lines_to_get]

        # 将选取的行保存到新文件
        new_txt_file_path = os.path.join(percent_text_dir_path, "all.txt")
        with open(new_txt_file_path, 'w') as file:
            file.writelines(selected_lines)
