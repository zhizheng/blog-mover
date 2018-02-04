从网易博客搬家到 Typecho
========

因网易博客间歇性不能访问或超时，所以有了将网易博客搬家的想法。使用前请备份数据！

## 版本说明

* OS: Windows 10 中文版
* Python 2.7.14
* BeautifulSoup 4.6.0
* pinyin 0.4.0

## 环境准备

安装 BeautifulSoup 软件包
```
pip install beautifulsoup4
```

安装 pinyin 软件包
```
pip install pinyin
```

## 操作步骤

1. 修改 blog_163_config.txt

> 打开你的博客页面并查看源码，搜索 userId 和 userName，将对应的值填入文件 blog_163_config.txt 中

2. 执行 blog_163_index.py

> 下载你所有的博文地址到文件 blog_163_url_list.txt 中，每行一个地址

3. 执行 blog_163_download.py

> 按文件 blog_163_url_list.txt 中博文地址下载博文内容到本地 txt 文件中（txt/*.txt），每篇博文放到一个文件里

4. 执行 blog_163_to_typecho.py

> 脚本中文章和分类、标签编号默认都是从 2 开始，如果你的 Typecho 不是全新安装的并且已经有文章了，请按实际情况修改 cid 和 mid 的初始值，执行本脚本会从本地 txt 文件中读取博文内容并生成可以导入 Typecho 的 sql 文件 blog_163_to_typecho.sql

5. 将 blog_163_to_typecho.sql 文件导入 Typecho 数据库

## 特殊情况

1. 如果网易博客访问不稳定，可以将博文页面下载后放到本地目录，如 html，然后在文件 blog_163_url_list.txt 中写入博文路径，如“C:\blog-mover\blog-163-to-typecho\html\测试 - 测试的日志 - 网易博客.html”，每行一个路径，然后忽略步骤 1 和 2，直接从步骤 3 开始执行

## TODO

1. 不支持登录网易博客，只支持读取公共博文
2. 博文内容可能会丢失分段换行
3. 不支持下载图片
4. 不支持下载评论
5. 不支持登录到 Typecho 或其所在数据库导入数据，只是生成了 sql 文件，要手工导入

## 参考资料

* https://github.com/crifan/BlogsToWordpress
