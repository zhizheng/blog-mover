#coding=utf-8
import os
import pinyin
import re
import string
import traceback
import urllib
import urllib2
from bs4 import BeautifulSoup

def get_url_list(user_id, user_name):
    """ 获取博文列表 """
    url_list = []
    # 是否还有博文要获取
    has_more_blog = True
    # 本次获取起始博文的下标
    blog_index = 0;
    # 本次获取博文的最大个数
    batch_num = 100
    try:
        while has_more_blog:
            # http://api.blog.163.com/user_name/dwr/call/plaincall/BlogBeanNew.getBlogs.dwr
            url = 'http://api.blog.163.com/' + user_name + '/dwr/call/plaincall/BlogBeanNew.getBlogs.dwr'
            post_params = {
                'callCount': '1',
                'scriptSessionId': '${scriptSessionId}187',
                'c0-scriptName': 'BlogBeanNew',
                'c0-methodName': 'getBlogs',
                'c0-id':   '0',
                'c0-param0': "number:" + user_id,
                'c0-param1': "number:" + str(blog_index),
                'c0-param2': "number:" + str(batch_num),
                'batchId': '1',
            };
            post_data = urllib.urlencode(post_params)
            req = urllib2.Request(url, post_data);
            req.add_header('Referer', "http://api.blog.163.com/crossdomain.html?t=20100205");
            req.add_header('Content-Type', "text/plain");
            rsp = urllib2.urlopen(req);
            rsp_data = rsp.read()
            id_list = re.findall('permalink="blog/static/(\d+)"', rsp_data)
            
            get_num = len(id_list)
            if get_num < batch_num:
                has_more_blog = False
            else:
                blog_index += get_num
            
            for id in id_list:
                url_list.append('http://' + user_name + '.blog.163.com/blog/static/' + id + '/')
    except Exception, e:
        print('get_url_list error:')
        traceback.print_exc()
        url_list = []

    return url_list

def get_html(url):
    """ 获取网页 html 内容 """
    try:
        html = ''
        if(url.startswith('http:') or url.startswith('https:')):
            html = urllib.urlopen(url).read().decode('gbk')
        else:
            encoded_url = url.encode("gb18030")
            html = urllib.urlopen('file:' + os.path.sep + os.path.sep + encoded_url).read().decode('gbk')
        return html
    except Exception, e:
        print('get_html error:')
        traceback.print_exc()
        return ''

def html_to_soup(html):
    """ 将网页内容用 BeautifulSoup 解析 """
    soup = BeautifulSoup(html, 'html.parser')
    return soup
    
def extract_title(html):
    """ 从网页内容中解析出文章标题 """
    title = ""
    try:
        soup = html_to_soup(html)
        found_title = soup.find(attrs={"class": "tcnt"})
        title = found_title.string.strip()
    except Exception, e:
        print('extract_title error:')
        traceback.print_exc()
        title = ""

    return title
   
def extract_datetime(html):
    """ 从网页内容中解析出文章发布时间 """
    datetime = ''
    try:
        soup = html_to_soup(html)
        found_datetime = soup.find(attrs={"class": "blogsep"})
        datetime = found_datetime.string.strip()
    except Exception, e:
        print('extract_datetime error:')
        traceback.print_exc()
        datetime = ""
        
    return datetime

def extract_category(html):
    """ 从网页内容中解析出文章分类 """
    cat = ''
    try:
        soup = html_to_soup(html)
        found_cat = soup.find(attrs={"class": "fc03 m2a"})
        cat = found_cat.string.strip()
    except Exception, e:
        print('extract_category error:')
        traceback.print_exc()
        cat = ""

    return cat

def extract_tags(html):
    """ 从网页内容中解析出文章标签 """
    tag_list = []
    try:
        soup = html_to_soup(html)
        found_tag = soup.find('input', attrs={"name": "tag"})
        tag = found_tag['value']
        tag_list = tag.split('&nbsp;&nbsp;')
    except Exception, e:
        print('extract_tags error:')
        traceback.print_exc()
        tag_list = []

    return tag_list

def extract_views(html):
    """ 从网页内容中解析出阅读次数 """
    views = '0'
    try:
        soup = html_to_soup(html)
        found_views = soup.find(attrs={"id": "$_spaniReadCount"})
        views = found_views.string.strip()
    except Exception, e:
        print('extract_views error:')
        traceback.print_exc()
        views = '0'

    return views

def extract_content(html):
    """ 从网页内容中解析出文章内容 """
    content = ''
    try:
        soup = html_to_soup(html)
        found_content = soup.find(attrs={"class": "bct fc05 fc11 nbw-blog ztag"})
        content = found_content.text.strip()
        content = content.replace('&nbsp;','')
        content = content.replace( u'\xa0','')
    except Exception, e:
        print('extract_content error:')
        traceback.print_exc()
        content = ''

    return content
  
def write_sql(file_name, sql):
    """ 将 sql 写入到文件中 """
    try:
        sql_file = open(file_name,'a')
        sql_file.write(sql)
        sql_file.write('\n')
        sql_file.close()
    except Exception, e:
        print('write sql file error:')
        traceback.print_exc()

def translate_to_pinyin(word):
    """ 将中文转换为拼音 """
    dest = ''
    try:
        import sys
        reload(sys)
        sys.setdefaultencoding('gb18030')
        
        src = word.encode('utf-8')
        src = src.replace(' ','-')
        src = src.replace('_','-')
        dest = pinyin.get(src, format="strip", delimiter="")
    except Exception, e:
        print('write sql file error:')
        traceback.print_exc()
        dest = ''
    return dest
        