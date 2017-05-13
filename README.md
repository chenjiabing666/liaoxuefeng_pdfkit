# python制作pdf电子书

## 准备

>*制作电子书使用的是`python`的`pdfkit`这个库，`pdfkit`是 `wkhtmltopdf` 的`Python`封装包，因此在安装这个之前要安装`wkhtmltopdf`*

### 安装wkhtmltopdf

>* `sudo apt-get install wkhtmltopdf`  (`ubantu`下，不过这里安装的时候可能对应的版本不同，会出现错误，如果不行的话还请自己百度下，我安装的时候是可以的)

>* `windows`下的用户直接到`wkhtmltopdf`官网下载稳定版本，然后直接安装即可，但是安装之后需要注意的是一定要将其添加到环境变量中，否则会出现找不到路径的问题

### python安装依赖包
>**以下都是我们需要用到的库**

>* `pip install requests`
>* `pip install BeautifulSoup4`
>* `pip install pdfkit`


## pdfkit的用法
### 初级了解函数
>* `pdfkit.from_url([url,],'demo.pdf')`  这个是直接传入一个`url`或者一个`url`列表，然后通过这个函数直接将其网页转换成`demo.pdf`,注意这里只能转换静态文本，如果使用js一些脚本的话是不能直接转换的
>* `pdfkit.from_string("<h1><a href="https://chenjiabing666.gituhb.io">陈加兵的博客</a></h1>",'demo.pdf')` 这个是直接讲一个字符串转换成`pdf`格式的电子书，里面可以直接传一个字符串，也可以用`html`标签包裹这个字符串
>* `pdfkit.from_file([file_name,],'demo.pdf')`  这个是直接传入一个文件或者一个列表即是多个文件，不过这里传入的文件一般都是html格式的文件

### 进阶
>*当然知道这个是多么枯燥，生成的电子书书也不能添加各种的样式，下面我们将会介绍一些添加的样式的方法*

#### options
>**这个参数是上面函数的可选参数，其中制定了一些选项，详情请见[http://wkhtmltopdf.org/usage/wkhtmltopdf.txt](http://wkhtmltopdf.org/usage/wkhtmltopdf.txt), 你可以移除选项名字前面的 '--' .如果选项没有值, 使用`None`, `Falseor` ,`*` 作为字典值，例子如下：**

```python
    options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
```

#### cover
>**这个参数是用来制作封面的，也是函数中的一个参数，如果想要实现的话可以先写一个html文本，在其中嵌入几张图片或者文字作为封面，然后写入出传入函数即可**

```python
options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
cover='demo.html'
pdfkit.from_file('demo.html','demo.pdf',cover=cover,options=options)
```

#### css
>**这里的css也是函数中的一个可选参数，这个参数主要的作用作用就是在其中定义自己喜欢的样式，当然这里也可以传入一个列表，定义多个样式css文件，当然没有这个参数也可以实现定义自己的样式，只需要在自己的html模板中定义内嵌的样式，或者直接用`<link>`引用外面的样式即可，本人亲试是可以的，具体的使用如下**

```python
css='demo.css'
pdfkit.from_file('demo.html','demo.pdf',options=options,cover=cover,css=css)
```

## 注意

>* 这里生成`pdf`的时候可能出现中文的乱码，请一定在`html`模板开头指定字体`utf-8`-> `<meta charset="UTF-8">`

>* 可能在爬取生成的时候会出现`ascii`错误，只需要在`py`文件开头写下：

```python
import sys
import threading
reload(sys)
sys.setdefaultencoding('utf8')
```

>* 写入文件的时候不想`python3`一样可以指定编码格式，这里我使用的是`codecs`库，可以向python3一样指定其中的编码格式


## 实战

>*本人爬了廖雪峰老师的`python2.7`的教程，并且做成了电子书，截图如下*

>![python教程](http://ono60m7tl.bkt.clouddn.com/liaoxuefeng.png)

### 注意

>* 这里并没有使用框架，如果有兴趣的朋友可以用框架写一个爬取全站的
>* 这里的主要用到的是`BeautifulSoup`和`requests`,详情可以看我的博客中的[BeautifulSoup用法](https://chenjiabing666.github.io/2017/04/29/python%E7%88%AC%E8%99%AB%E4%B9%8BBeautifulSoup/),后续还会更新requests的用法

>* 源代码请见[https://github.com/chenjiabing666/liaoxuefeng_pdfkit](https://github.com/chenjiabing666/liaoxuefeng_pdfkit)


## 参考文章

>* [http://mp.weixin.qq.com/s/LH8nEFfVH4_tvYWo46CF5Q](http://mp.weixin.qq.com/s/LH8nEFfVH4_tvYWo46CF5Q)
>* [http://www.cnblogs.com/taceywong/p/5643978.html](http://www.cnblogs.com/taceywong/p/5643978.html)
>* [http://beautifulsoup.readthedocs.io/zh_CN/latest/#id44](http://beautifulsoup.readthedocs.io/zh_CN/latest/#id44)


