# This Python file uses the following encoding: utf-8
#       lyr_mod.py
#       
#       Copyright 2009 Bill Ma <billnowar@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import os
import lyricSer.TTLyric as TT
import lyricSer.SogouLyric as Sogou

def lrcGet(artist, title, Serve):
    if Serve == 'TT':
        Result = TT.SearchLyric(artist, title)
        if Result:
            lrcDic = TT.AnySearchRes(Result)
        else:return False
        if lrcDic:
            lrc = TT.DownLoadLyric(lrcDic[1]['id'], lrcDic[1]['artist'], lrcDic[1]['title'])
        else:return False
        return lrc
    elif Serve == 'Sogou':
        Result = Sogou.SearchLyric(artist, title)
        if Result:
            lrcDic = Sogou.AnySearchRes(Result)
        else:return False
        if lrcDic:
            lrc = Sogou.DownLoadLyric(lrcDic[1]['id'], lrcDic[1]['artist'], lrcDic[1]['title'])
        else:return False
        return lrc
def lrcDic(artist, title, Serve):
    if Serve == 'TT':
        Result = TT.SearchLyric(artist, title)
        if Result:
            lrcDic = TT.AnySearchRes(Result)
        else:return False
        return lrcDic
    elif Serve == 'Sogou':
        Result = Sogou.SearchLyric(artist, title)
        if Result:
            lrcDic = Sogou.AnySearchRes(Result)
        else:return False
        return lrcDic

def lrcurldown(id, artist, title, Serve):
    if Serve == 'TT':
        lrc = TT.DownLoadLyric(id, artist, title)
        return lrc
    elif Serve == 'Sogou':
        lrc = Sogou.DownLoadLyric(id, artist, title)
        return lrc
def lrcAny(lyric):
    lrcLines = {}
    lrcUni = lyric.split('\n')
    for i in lrcUni:
        timeSign = i.count(']')
        timeEnd = i.find(']')+1
        try:
            for j in range(timeSign):
                lrcStr = i[j * timeEnd : (j + 1) * timeEnd]
                time = (int(lrcStr[1:3]) * 6000 + int(lrcStr[4:6]) * 100 + int(lrcStr[7:8])*10)
                lrcLines[time] = i[timeSign * timeEnd:]
        except:
            pass
    timeLines = lrcLines.keys()
    timeLines.sort()
    return lrcLines,timeLines

def saveLrc(lrc, dic, basename):
    dic = os.path.expanduser(dic)
    if not os.path.exists(dic):
        os.mkdir(dic)
    f = file('%s//%s.lrc' %(dic, basename), 'w')
    f.write(lrc)
    f.close()

def readLrc(dic, basename):
    dic = os.path.expanduser(dic)
    f = open('%s//%s.lrc' %(dic, basename), 'r')
    lyric = f.read()
    f.close()
    return lyric

def ifLrcExist(dic, basename):
    dic = os.path.expanduser(dic)
    return os.path.isfile('%s//%s.lrc' %(dic, basename))

def writeLrc(lyrLines, timeLines, timeChange):
    lyric = ''
    timeMod = '[%s:%s.%s]%s'
    lyrStrs = []
    for i in timeLines:
        if (i-timeChange)>0:
            sec = (i-timeChange) // 100
            lyrStrs.append(timeMod % (str(sec // 60).rjust(2,'0'), \
            str(sec % 60).rjust(2,'0'), \
            str(sec % 100).ljust(2,'0'), \
            lyrLines[i]))
    lyric = '\n'.join(lyrStrs)
    return lyric
