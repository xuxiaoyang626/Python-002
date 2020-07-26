学习笔记

pip使用：
    pip freeze > requirements.txt
    pip uninstall -r requirements.txt -y
    pip install -r requirements.txt

cookies：
    maoyan网站要使用cookie，否则要有滑块验证
    使用chrome插件cookies.txt可以下载当前页面的cookies文件

xpath:
    可以使用 scrapy shell 可以在命令行中尝试各种xpath组合，方便调试
    e.g: scrapy shell https://maoyan.com/films/344990
