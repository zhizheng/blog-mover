#coding=utf-8
import os
import string
import traceback
from blog_163_util import (get_html, 
    extract_title,
    extract_date_time,
    extract_category,
    extract_tags,
    extract_views,
    extract_content)

def main():
    """ 根据文章地址下载内容 """
    # 当前目录路径  
    curr_path = os.path.abspath('.')
    # txt 文件起始编号
    count = 0

    # txt 目录不存在，则创建
    dir_name = curr_path + os.path.sep + 'txt'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    try:
        # 读取文章地址列表文件
        list_file = open(curr_path + os.path.sep + 'blog_163_url_list.txt', 'r')
        lines = list_file.readlines()
        for line in lines:
            if line == '\n':
                print('read url list over!')
                break
            url = line.strip('\n')
            url = unicode(url,'utf-8')
            
            count += 1
            file_name = curr_path + os.path.sep + 'txt' + os.path.sep + str(count) + '.txt'
            if os.path.exists(file_name):
                continue
            
            # 获取文章内容
            html = get_html(url)
            if html != '':
                # 从文章内容中解析相关字段
                title = extract_title(html)
                date_time = extract_date_time(html)
                category = extract_category(html)
                tags = extract_tags(html)
                views = extract_views(html)
                content = extract_content(html)

                # 在文章开头加些自定义内容
                prefix = u'> 本文由本人网易博客迁移而来。'
                    
                # 将解析出的字段按顺序写入 txt 文件
                try:
                    os.system(r'touch %s' % file_name)
                    txt_file = open(file_name, 'a')
                    txt_file.write(title.encode("gb18030"))
                    txt_file.write('\n')
                    txt_file.write(date_time)
                    txt_file.write('\n')
                    txt_file.write(category.encode("gb18030"))
                    txt_file.write('\n')
                    txt_file.write(','.join(tags).encode("gb18030"))
                    txt_file.write('\n')
                    txt_file.write(views)
                    txt_file.write('\n')
                    txt_file.write(prefix.encode("gb18030"))
                    txt_file.write('\n')
                    txt_file.write(content.encode("gb18030"))
                    txt_file.write('\n')
                    txt_file.close()
                except Exception, e:
                    traceback.print_exc()
                    # 写 txt 失败时，删除 txt
                    if os.path.exists(file_name):
                        os.remove(file_name)
        list_file.close()
    except Exception, e:
        traceback.print_exc()
        
if __name__ == '__main__':
    main()
    