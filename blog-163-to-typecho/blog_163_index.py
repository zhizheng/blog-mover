#coding=utf-8
import os
import traceback
from blog_163_util import get_url_list

def main():
    """ 根据博客地址获取文章列表 """
    # 当前目录路径  
    curr_path = os.path.abspath('.')

    # 读取博客配置文件
    user_id = ''
    user_name = ''
    try:
        conf_file = open(curr_path + os.path.sep + 'blog_163_config.txt', 'r')
        lines = conf_file.readlines()
        for line in lines:
            if line == '\n':
                print('read blog config over!')
                break
            line = line.strip('\n')
            line = unicode(line,'utf-8')
            key_value = line.split(':')
            key = key_value[0].strip()
            value = key_value[1].strip()
            if key == 'userId':
                user_id = value
            elif key == 'userName':
                user_name = value
        conf_file.close()
        
        # 获取文章地址列表并写入文件 blog_163_url_list.txt 中
        url_list = get_url_list(user_id, user_name)
        list_file = open(curr_path + os.path.sep + 'blog_163_url_list.txt', 'a')
        list_file.truncate()
        for url in url_list: 
            list_file.write(url)
            list_file.write('\n')
        list_file.close()
    except Exception, e:
        traceback.print_exc()
        
if __name__ == '__main__':
    main()
    