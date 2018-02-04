#coding=utf-8
import codecs
import datetime
import mysql.connector
import time
import os
import progressbar
import traceback
from wordpress_util import *

def main():
    """ 将 Wordpress 数据库数据导出生成 Markdown 文件 """
    try:
        import sys
        reload(sys)
        sys.setdefaultencoding('gb18030')
        
        # 当前目录路径  
        curr_path = os.path.abspath('.')
        
        # md 目录不存在，则创建
        dir_name = curr_path + os.path.sep + 'md'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            
        # 读取 Wordpress 配置文件
        wp_db_host = '127.0.0.1'
        wp_db_port = 3306
        wp_db_user = ''
        wp_db_pass = ''
        wp_db_name = ''
        try:
            conf_file = open(curr_path + os.path.sep + 'wordpress_config.txt', 'r')
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
                if key == 'wp_db_host':
                    wp_db_host = value
                elif key == 'wp_db_port':
                    wp_db_port = value
                elif key == 'wp_db_user':
                    wp_db_user = value
                elif key == 'wp_db_pass':
                    wp_db_pass = value
                elif key == 'wp_db_name':
                    wp_db_name = value
            conf_file.close()
        except Exception, e:
            traceback.print_exc()
        wp_db_info = {
            'host': wp_db_host, 
            'port': int(wp_db_port), 
            'user': wp_db_user, 
            'password': wp_db_pass, 
            'database': wp_db_name, 
            'use_unicode': True, 
            'charset': 'utf8'
        }

        # 从 Wordpress 数据库读取文章、处理并写入 Markdown 文件
        conn = mysql.connector.connect(**wp_db_info)
        cursor = conn.cursor()
        cursor.execute("SELECT ID, post_title, post_date, post_content FROM wp_posts WHERE post_title != '' AND post_status=%s AND post_type='post'", ('publish',))
        rows = cursor.fetchall()
        count = 0
        progress_bar = progressbar.ProgressBar()
        for row in progress_bar(rows):
            post_id = row[0]
            post_title = row[1]
            post_date = row[2]
            post_content = row[3]
            
            # 将文章标题转为拼音，用于 Markdown 文件名
            post_title_pinyin = translate_to_pinyin(post_title)
            # 处理文章标题，用于 Markdown 文件头中 title 属性值
            post_title_parsed = parse_title(post_title)
            # 获取文章发布年月日，用于 Markdown 文件名
            post_date_date = datetime.datetime.strftime(post_date, "%Y-%m-%d")
            # 获取文章发布年月日时分秒，用于 Markdown 文件头中 date 属性值
            post_date_datetime = datetime.datetime.strftime(post_date, "%Y-%m-%d %H:%M:%S")
            # 完整的 Markdown 文件名
            post_title_long = post_date_date + '-' + post_title_pinyin
            # 处理文章正文，用于 Markdown 文件中内容体
            post_content = parse_content(post_content)
            
            # 要生成的 Markdown 文件绝对路径
            filename = curr_path + os.path.sep + 'md' + os.path.sep + post_title_long + '.md'
            if os.path.exists(filename):
                continue
            
            # 将解析出的字段按要求写入 md 文件
            try:
                # 文件名含有 & 字符，会报错：不是内部或外部命令，也不是可运行的程序
                # os.system(r'touch %s' % filename)
                md_file = codecs.open(filename, 'a', 'utf-8')
                md_file.write('---\n')
                md_file.write('layout: post\n')
                md_file.write('title: "' + post_title_parsed + '"\n')
                md_file.write('date: ' + post_date_datetime + ' +0800\n')
                # 分类处理
                md_file.write('categories:\n')
                cat_cursor = conn.cursor()
                cat_cursor.execute("SELECT t3.name,t3.slug FROM `wp_term_relationships` t1,`wp_term_taxonomy` t2,`wp_terms` t3 WHERE t1.`term_taxonomy_id`=t2.`term_taxonomy_id` AND t2.`taxonomy`='category' AND t2. `term_id`=t3.`term_id` AND t1.`object_id`=%s", (post_id,))
                cat_rows = cat_cursor.fetchall()
                for cat_row in cat_rows:
                    cat_name = cat_row[0]
                    md_file.write('  - ' + cat_name + '\n')
                cat_cursor.close()
                # 标签处理
                md_file.write('tags:\n')
                tag_cursor = conn.cursor()
                tag_cursor.execute("SELECT t3.name,t3.slug FROM `wp_term_relationships` t1,`wp_term_taxonomy` t2,`wp_terms` t3 WHERE t1.`term_taxonomy_id`=t2.`term_taxonomy_id` AND t2.`taxonomy`='post_tag' AND t2. `term_id`=t3.`term_id` AND t1.`object_id`=%s", (post_id,))
                tag_rows = tag_cursor.fetchall()
                for tag_row in tag_rows:
                    tag_name = tag_row[0]
                    md_file.write('  - ' + tag_name + '\n')
                tag_cursor.close()
                # 内容处理
                md_file.write('---\n')
                md_file.write('\n')
                md_file.write(post_content)
                md_file.write('\n')
                md_file.close()
            except Exception, e:
                traceback.print_exc()
                # 写 md 失败时，删除 md
                if os.path.exists(filename):
                    os.remove(filename)
                    
            time.sleep(0.01)
        cursor.close()
        conn.close()
    except:
        traceback.print_exc()
        pass
    
if __name__ == "__main__":
    main()
