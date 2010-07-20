# coding=utf-8

import urllib,re

def SearchLyric(title, artist):
    try:
        url = 'http://mp3.sogou.com/gecisearch.so?query=%s+%s' % (artist.decode('utf-8').encode('gbk'), title.decode('utf8').encode('gbk'))
        html = urllib.urlopen(url).read()
        return html
    except:
        print 'SearchLyric failed'
        return False
def AnySearchRes(html):
    try:
        listpat = re.compile(r'downlrc\.jsp\?tGroupid=.*?&lyricId=.*?&fn=.*?\"')
        patres = re.findall(listpat, html)
        j = 1
        lrcDic = {}
        for i in patres:
            atre = re.compile('fn=.*?-.*?\"')
            idre = re.compile('lyricId=.*?&')
            at = atre.search(i).group().split('-')
            id = idre.search(i).group()[8:-1]
            lrcDic[j] = {'id' : id, 'artist' : urllib.unquote(at[1][:-1]).decode('gbk'),'title' : urllib.unquote(at[0][3:]).decode('gbk')}
            j += 1
        return lrcDic
    except:
        print 'AnySearchRes failed'
        return False
def DownLoadLyric(id, art, tit):
    try:
        url = 'http://mp3.sogou.com/downlrc.jsp?lyricId=%s&fn=%s-%s' % (id, urllib.quote(tit).encode('gbk'), urllib.quote(art).encode('gbk'))
        lrc = urllib.urlopen(url).read()
        return lrc.decode('gbk')
    except:
        print 'DownLoadLyric failed'
        return False
