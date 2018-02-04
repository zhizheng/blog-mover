从 Wordpress 搬家到 Markdown
========

因 Wordpress 消耗资源较多，所以打算将其导出生成 Markdown 文件，使用 Jekyll 部署并托管到 GitHub 上。使用前请备份数据！

## 版本说明

* OS: Windows 10 中文版
* Python 2.7.14
* pinyin 0.4.0
* progressbar 2.3

## 环境准备

安装 MySQL 驱动
```
pip install mysql-connector-python
```

安装 pinyin 软件包
```
pip install pinyin
```

安装 progressbar 软件包
```
pip install progressbar
```

## 操作步骤

1. 修改 wordpress_config.txt 中 Wordpress 数据库信息
2. 执行 wordpress_to_markdown.py 从数据库中读取博文内容并生成 Markdown 文件
3. 将生成的 Markdown 文件（md/*.md）放到 Jekyll _posts 目录下，同步内容到 GitHub

## TODO

1. 文章内容可能会丢失分段换行
2. 不支持下载图片
3. 不支持下载评论
