# coding:utf-8
import requests
import time
from bs4 import BeautifulSoup
import pdfkit
import sys
import threading
reload(sys)
sys.setdefaultencoding('utf8')
import lxml
import Queue
import codecs


# #url="http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431756919644a792ee4ead724ef7afab3f7f771b04f5000"
# #url='http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014317799226173f45ce40636141b6abc8424e12b5fb27000'
# url='http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431608990315a01b575e2ab041168ff0df194698afac000'
# headers={"User-Agent":'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Mobile Safari/537.36'}
# res=requests.get(url=url,headers=headers)
# #pdfkit.from_string((str(res.content)).encode('utf-8'),'demo.pdf')
#
# options = {
#     'page-size': 'Letter',
#     'margin-top': '0.75in',
#     'margin-right': '0.75in',
#     'margin-bottom': '0.75in',
#     'margin-left': '0.75in',
#     'encoding': "UTF-8",
#     'custom-header': [
#         ('Accept-Encoding', 'gzip')
#     ],
#     'cookie': [
#         ('cookie-name1', 'cookie-value1'),
#         ('cookie-name2', 'cookie-value2'),
#     ],
#     'outline-depth': 10,
# }
#
# html_template="""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
# </head>
# <body>
# {0}
# </body>
# </html>
# """
#
#
# soup=BeautifulSoup(res.text,'lxml')
#
# title=soup.find("div",class_='x-content').find("h4").get_text() #标题
# center_tag=soup.new_tag('center')
# title_tag=soup.new_tag("h1")
# title_tag.string=title
# center_tag.insert(1,title_tag)
# content=soup.find("div",class_='x-wiki-content')  #内容
# content.insert(1,center_tag)
# img_tag=content.find_all("img")
# for img_url in img_tag:
#     img_url['src']='http://www.liaoxuefeng.com'+img_url['src']
# #img_tag['src']='http://www.baidu.com'
# html_template=html_template.format(content)
# pdfkit.from_string(html_template,'demo.pdf',options=options)


class crawl:
    def __init__(self):
        self.file=codecs.open("python.txt",'w',encoding='utf-8')
        self.html_template = """
        <!DOCTYPE html>
<html lang="en">
<head>
     <meta charset="UTF-8">
     <link rel="stylesheet" type="text/css" href="demo.css">
 </head>
 <body>
 {0}
 </body>
 </html>"""
        self.options = {
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
        self.files=[]

        self.q = Queue.Queue()
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Mobile Safari/537.36'}
        self.lock=threading.Lock()

    def parse_url(self):
        """
        得到所有的章节链接，并且将章节的链接存储在队列中
        :return: 
        """
        url = 'http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000'
        res = requests.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'lxml')
        lis = soup.find("div", class_='x-sidebar-left-content').find_all("ul", class_='uk-nav uk-nav-side')[1].find_all(
            "li")
        for li in lis:
            url = "http://www.liaoxuefeng.com" + li.find('a').get('href')
            self.q.put(url)

    def parse_html(self):
        """
        提取队列中的URL，请求获得其中的内容，然后写入模板、
        title:提取文章中的标题
        center_tag：使用BeautifulSoup新创建的节点，用于居中显示
        title_tag:新创建的h1标签，用于包裹提取的标题
        content：提取的正文内容，这里其他的包括评论都没有提取，这个用不到
        :return: 
        """
        while not self.q.empty():
            url = self.q.get()
            print url
            self.lock.acquire()
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'lxml')
            self.lock.release()
            try:

                title = soup.find("div", class_='x-content').find("h4").get_text()  # 标题
                center_tag = soup.new_tag('center')
                title_tag = soup.new_tag("h1")
                title_tag.string = title
                center_tag.insert(1, title_tag)
                content = soup.find("div", class_='x-wiki-content')  # 内容
                content.insert(1, center_tag)
                img_tag = content.find_all("img")  #获取内容的中的所有img标签
                for img_url in img_tag:
                    #修改内容中的img标签的src，将其补全为绝对路径，否则不能正常显示
                    img_url['src'] = 'http://www.liaoxuefeng.com' + img_url['src']
                file_name = url.split('/')[-1] + '.html'
                html = self.html_template.format(content)  # 得到的每一章节的内容
                self.files.append(file_name)      #这里将每一章节的内容写入到文件中，以便后面直接提取
                print file_name

                with codecs.open(file_name, 'wb', encoding='utf-8') as f:
                    f.write(html)





            except:
                print '**************************************************'





    def write_pdf(self):
        pdfkit.from_file(self.files,'demo.pdf',options=self.options)


if __name__ == '__main__':
    demo = crawl()


    threads=[]
    demo.parse_url()
    for i in range(0,40):

        t2=threading.Thread(target=demo.parse_html,args=[])
        threads.append(t2)


    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print "chen"

    demo.write_pdf()

