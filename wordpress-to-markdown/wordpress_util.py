#coding=utf-8
import pinyin
import traceback

def parse_title(title):
    """ 处理标题 """
    dest = ''
    try:
        src = title
        dest = src.replace('"','\'')
    except Exception, e:
        print('parse_title error:')
        traceback.print_exc()
        dest = ''
    return dest


def parse_content(content):
    """ 处理正文 """
    dest = ''
    try:
        src = content
        # Jekyll 中设置摘要分隔符为 <!-- more -->，所以要替换一下
        dest = src.replace('<!--more-->', '<!-- more -->')
    except Exception, e:
        print('parse_content error:')
        traceback.print_exc()
        dest = ''
    return dest
    
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
        src = src.replace('/','-')
        src = src.replace('\\','-')
        src = src.replace(':','-')
        src = src.replace('"','-')
        src = src.replace('\n','-')
        src = src.replace('\*','-')
        src = src.replace('\<','-')
        src = src.replace('\>','-')
        src = src.replace('\|','-')
        src = src.replace('“','-')
        src = src.replace('”','-')
        src = src.replace('\&','-')
        dest = pinyin.get(src, format="strip", delimiter="")
    except Exception, e:
        print('translate_to_pinyin error:')
        traceback.print_exc()
        dest = ''
    return dest
