from urllib import request
import re
# 全书网  盗墓笔记
first_Url = 'http://www.quanshuwang.com/book/9/9055/'
html = request.urlopen(first_Url).read().decode('gbk')
novel_Info = {}
novel_Info['title'] = re.findall(r'<span class="r">.*?</span><strong>(.*?)</strong>', html)[0]
novel_Info['author'] = re.findall(r'<span class="r">(.*?)</span><strong>(.*?)</strong>', html)[0][0]
novel_Div = re.findall(r'<div class="clearfix dirconone(.*?)</div>', html, re.S | re.I)[0]
chapter = re.findall(r'<a.*?</a>', novel_Div)
chapter_Url = []
chapter_Title = []
i = 0
for chapter_One in chapter:
    chapter_Url.append(first_Url + re.findall(r'href="(.*?)"', chapter_One)[0])
    chapter_Title.append(re.findall(r'title="(.*?)"', chapter_One)[0])
    i += 1
print(novel_Info['title'])
print(novel_Info['author'])
print('共%d章' % i)
article = novel_Info['title'] + '\n' + novel_Info['author'] + '\n'
page = open(r'C:\Users\Administrator\Desktop\盗墓笔记.txt', 'w')
page.write(article+'\n\n\n')
for one_Url, one_Title in zip(chapter_Url, chapter_Title):
       print(one_Title + '  正在下载...  ', end='  ')
       one_Html = request.urlopen(one_Url).read().decode('gbk')
       one_Chapter = re.findall(r'&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />', one_Html, re.S)
       one_Passage = one_Title + '\n'
       for cc in one_Chapter:
           one_Passage += str(cc)+'\n'
       article += one_Passage
       page.write(one_Passage)
       print('  下载成功！')
page.close()