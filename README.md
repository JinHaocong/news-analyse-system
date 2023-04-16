# 计算机毕业设计

#### 软件架构

```
后端技术栈(python):
    - django <https://docs.djangoproject.com/zh-hans/4.0/>
    - django-simpleui 后台ui框架
    - mysql 数据库
    - sqlite3 数据库
数据爬虫(python):
    - scrapy 爬虫框架
    - requests 轻量爬虫工具
    - xpath 页面数据抽取
前端技术栈(nodejs+vue3):
    - vue3 <https://v3.cn.vuejs.org/guide/introduction.html>
    - element-plus vue3组件库
    - element-plus-admin 页面框架
    - postcss 样式后处理
    - tailwindcss 样式库
    - vite 打包工具
    - typescript 强类型的js
```


#### 安装教程

```
1. 安装Python3.7
    windows版python3.7下载链接: 
        https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe
    注意，安装时，一定要勾选add python to path!!!!!

2. 更新pip
    打开控制台，执行
        pip3 install --upgrade pip

3. 安装依赖包
    进入项目处，打开控制台，执行 
        pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    命令，等待下载安装完毕

4. 启动网页服务器
    进入项目处，打开控制台，执行
        python manage.py runserver
    然后浏览器打开链接即可
        http://127.0.0.1:8000/
```

#### 使用说明

```
# 第二次运行
启动网页服务器
    进入项目处，打开控制台，执行
        python manage.py runserver
    然后浏览器打开链接即可
        http://127.0.0.1:8000/
```