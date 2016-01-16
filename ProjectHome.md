> # **Exaile-cn** #
## 项目介绍 ##
Exaile-cn是一个对Exaile进行扩展的项目，通过对Exaile进行扩展，使Exaile功能上更加丰富，更加符合中国用户的使用习惯，给国内Linuxer提供一个更加本土化的播放器.


# **注意：因个人原因，exaile-cn暂时停止开发** #
## 安装方法: ##
**注意：Exaile-cn现在只支持Exaile0.3.2.0，如果你的Exaile不是0.3.2.0，可能会无法正常使用。**

先运行whereis exaile，查找exaile的位置，下面假设exaile位于/usr/lib/exaile/下
### 1.解决乱码问题方法 ###
将\_id3.py覆盖到/usr/lib/exaile/xl/metadata目录下(需要root权限）
### 2.豆瓣封面插件安装方法 ###
将doubancovers复制到～/.local/share/exaile/plugins/(如果没有目录，先创建目录）下，然后启动exaile，选中插件选项即可
### 3.歌词同步显示插件安装方法 ###
先把engine\_unified.py和engine\_normal.py覆盖到/usr/lib/exaile/xl/player，再将LyricDisp目录复制到~/.local/share/exaile/plugins下，然后启动Exaile，选中插件选项即可
### 4.面板标签竖行显示 ###
将init.py覆盖到/usr/lib/exaile/xlgui/目录下(需要root权限）
### 5.豆瓣电台插件安装方法 ###
将track.py覆盖到/usr/lib/exaile/xl/trax/目录下(需要root权限），将doubanfm复制到～/.local/share/exaile/plugins/,启动exaile，选中插件选项，然后在Douban.FM插件的设置里面填写用户名和密码，重启exaile，在文件菜单里面会显示豆瓣电台列表

## 补丁 ##
### 谷歌音乐歌词支持 ###
clyfish针对lyricdisp不能正常显示使用gmbox下载的歌词对lrcmod.py做了修改

安装方法：下载[lrcmod.py](http://code.google.com/p/exaile-cn/downloads/detail?name=lrcMod.py)
，放在~/.local/share/exaile/plugins/LyricDisp/下