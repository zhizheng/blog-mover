#coding=utf-8
import os
import traceback
from blog_163_util import (write_sql, 
    translate_to_pinyin)
from datetime import datetime

def main():
    """ 将下载的文章内容转换为符合 typecho 的 sql 并写入文件 """
    # 当前目录路径
    curr_path = os.path.abspath('.')
    # 文章起始编号
    cid = 2
    # 分类或标签起始编号
    mid = 2
    # “分类名称：编号”对应关系
    cat_mid_dict = {}
    # “标签名称：编号”对应关系
    tag_mid_dict = {}
    # “分类名称：引用计数”对应关系
    cat_count_dict = {}
    # “标签名称：引用计数”对应关系
    tag_count_dict = {}

    # 如果没有待处理的 txt 文件，则直接退出程序
    files = os.listdir(curr_path + os.path.sep + 'txt')
    if(len(files) == 0):
        print('no txt file')
        exit

    # 如果 sql 文件不存在，则创建；如果存在，则清空文件内容
    file_name = curr_path + os.path.sep + 'blog_163_to_typecho.sql'
    if not os.path.exists(file_name):
        try:
            os.system(r'touch %s' % file_name)
        except Exception, e:
            print('touch sql file error:')
            traceback.print_exc()
    else:
        try:
            sql_f = open(file_name, 'w')
            sql_f.truncate()
            sql_f.close()
        except Exception, e:
            print('truncate sql file error:')
            traceback.print_exc()

    #遍历 txt 文件
    for file in files:
        try:
            # 读取 txt 文件
            txt_file = open(curr_path + os.path.sep + 'txt' + os.path.sep + file, 'r')
            iter_file = iter(txt_file)
            count = 0
            title = ''
            created_num = 0
            modified_num = 0
            category = ''
            tags = ''
            views = ''
            content = ''
            # 转换成迭代器并解析
            for line in iter_file:
                count += 1
                if count == 1:
                    title = line.strip('\n')
                if count == 2:
                    created = line.strip('\n')
                    created_num = (datetime.strptime(created, '%Y-%m-%d %H:%M:%S') - datetime(1970,1,1)).total_seconds()
                    modified = line.strip('\n')
                    modified_num = (datetime.strptime(modified, '%Y-%m-%d %H:%M:%S') - datetime(1970,1,1)).total_seconds()
                if count == 3:
                    category = line.strip('\n')
                if count == 4:
                    tags = line.strip('\n')
                if count == 5:
                    views = line.strip('\n')
                if count >= 6:
                    content = content + line.strip('\n')
            txt_file.close()
            # 将解析出的分类信息写入 sql 文件
            if category != '':
                cat_index = 0
                if not cat_mid_dict.has_key(category):
                    cat_mid_dict[category] = mid
                    cat_index = cat_mid_dict[category]
                    write_sql(file_name, "INSERT INTO `typecho_metas` (`mid`, `name`, `slug`, `type`) VALUES (" + str(cat_index) + ", '" + category + "', '" + translate_to_pinyin(category) + "', 'category');")
                    mid += 1
                cat_index = cat_mid_dict[category]
                write_sql(file_name, "INSERT INTO `typecho_relationships` (`cid`, `mid`) VALUES (" + str(cid) + ", " + str(cat_index) + ");")
                # 引用计数
                if  not cat_count_dict.has_key(category):
                    cat_count_dict[category] = 0
                cat_count_dict[category] += 1
            # 将解析出的标签信息写入 sql 文件
            if tags != '':
                tag_list = tags.split(',')
                for tag in tag_list:
                    tag_index = 0
                    if not tag_mid_dict.has_key(tag):
                        tag_mid_dict[tag] = mid
                        tag_index = tag_mid_dict[tag]
                        write_sql(file_name, "INSERT INTO `typecho_metas` (`mid`, `name`, `slug`, `type`) VALUES (" + str(tag_index) + ", '" + tag + "', '" + translate_to_pinyin(tag) + "', 'tag');")
                        mid += 1
                    tag_index = tag_mid_dict[tag]
                    write_sql(file_name, "INSERT INTO `typecho_relationships` (`cid`, `mid`) VALUES (" + str(cid) + ", " + str(tag_index) + ");")
                    # 引用计数
                    if  not tag_count_dict.has_key(tag):
                        tag_count_dict[tag] = 0
                    tag_count_dict[tag] += 1
            # 将解析出的文章信息写入 sql 文件
            write_sql(file_name, "INSERT INTO `typecho_contents` (`cid`, `title`, `slug`, `created`, `modified`, `text`, `authorId`, `type`, `status`, `allowComment`, `allowPing`, `allowFeed`, `views`) VALUES (" + str(cid) + ", '" + title + "', " + str(cid) + ", " + str(int(created_num)) + ", " + str(int(modified_num)) + ", '" + content + "', 1, 'post', 'publish', 1, 1, 1, " + views + ");")
        except:
            traceback.print_exc()
            
        cid += 1
        
    # 生成分类引用计数修正 sql
    for category in cat_count_dict:
        mid = cat_mid_dict[category]
        count = cat_count_dict[category]
        write_sql(file_name, "UPDATE `typecho_metas` SET count=" + str(count) + " WHERE mid=" + str(mid) + ";")
        
    # 生成标签引用计数修正 sql
    for tag in tag_count_dict:
        mid = tag_mid_dict[tag]
        count = tag_count_dict[tag]
        write_sql(file_name, "UPDATE `typecho_metas` SET count=" + str(count) + " WHERE mid=" + str(mid) + ";")

if __name__ == '__main__':
    main()
    