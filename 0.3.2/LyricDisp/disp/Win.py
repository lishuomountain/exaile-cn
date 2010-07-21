# coding=utf-8

from xl import event, player, settings

import gtk, gobject, gtk.gdk
import os
import lrcMod
import chooser

GUI = r"""<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy toplevel-contextual -->
  <object class="GtkUIManager" id="uimanager1"/>
  <object class="GtkWindow" id="lrcWin">
    <property name="visible">True</property>
    <property name="title" translatable="yes">Exaile&#x6B4C;&#x8BCD;&#x63D2;&#x4EF6;</property>
    <property name="window_position">center</property>
    <property name="type_hint">dialog</property>
    <property name="skip_pager_hint">True</property>
    <property name="accept_focus">False</property>
    <property name="focus_on_map">False</property>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkMenuBar" id="menu">
            <property name="visible">True</property>
            <child>
              <object class="GtkMenuItem" id="playerMan">
                <property name="visible">True</property>
                <property name="label" translatable="yes">&#x64AD;&#x653E;&#x5668;</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu2">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkMenuItem" id="playerSS">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&#x5F00;&#x59CB;/&#x505C;&#x6B62;</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="playerNext">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&#x4E0B;&#x4E00;&#x9996;</property>
                        <property name="use_underline">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="playerPrev">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&#x4E0A;&#x4E00;&#x9996;</property>
                        <property name="use_underline">True</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="lrcMan">
                <property name="visible">True</property>
                <property name="label" translatable="yes">&#x6B4C;&#x8BCD;</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu1">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkMenuItem" id="lrcSearch">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&#x91CD;&#x65B0;&#x641C;&#x7D22;</property>
                        <property name="use_underline">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="lrcSaveChange">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&#x4FDD;&#x5B58;&#x6B4C;&#x8BCD;&#x6539;&#x53D8;</property>
                        <property name="use_underline">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="lrcSet">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&#x8C03;&#x6574;&#x6B4C;&#x8BCD;</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu3">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="slower1">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">&#x6162;&#x4E00;&#x79D2;</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="slower2">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">&#x6162;0.5&#x79D2;</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Reset">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">&#x53D6;&#x6D88;&#x4FEE;&#x6539;</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="quicker2">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">&#x5FEB;0.5&#x79D2;</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="quicker1">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">&#x5FEB;&#x4E00;&#x79D2;</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <placeholder/>
        </child>
      </object>
    </child>
  </object>
</interface>"""


PLUGIN = None
MENU_ITEM = None
TIMER = None

def disable(exaile):
    global PLUGIN, MENU_ITEM, TIMER
    if PLUGIN:
        PLUGIN.window.destroy()
        PLUGIN = None
    if MENU_ITEM:
        MENU_ITEM.hide()
        MENU_ITEM.destroy()
        MENU_ITEM = None
    if TIMER:
        gobject.source_remove(TIMER)

def enable(exaile, options):
    global MENU_ITEM, PLUGIN
    MENU_ITEM = gtk.MenuItem(label = "歌词窗口")
    MENU_ITEM.connect('activate', lrcWinShow, exaile, options)
    try:
        exaile.gui.builder.get_object('view_menu').append(MENU_ITEM)
        MENU_ITEM.show()
    except:
        exaile.gui.xml.get_widget('view_menu').append(MENU_ITEM)
    if not PLUGIN:
        PLUGIN = lrcWin(exaile, options)

class lrcWin:
    def __init__(self, exaile, options):
        self.exaile = exaile

        event.add_callback(self.colorChange, 'color_change')
        event.add_callback(self.colorChange, 'name_change')
        event.add_callback(self.playTrack, 'playback_track_start')
        event.add_callback(self.stopTrack, 'playback_player_end')
        event.add_callback(self.timeSeek, 'seek')
        
        self.ops = {'artist-title.lrc' : lambda art, tit, locname: '%s-%s' %(art, tit), \
                    'title-artist.lrc': lambda art, tit, locname: '%s-%s' %(tit, art), \
                    '与歌曲文件名相同': lambda art, tit, locname: locname.replace('.mp3','').replace('.wmv','')}

        self.lrcLines = {}
        self.lyric = ''
        self.timeChange = 0
        self.isLrcFound = False
        self.options = options
        self.lastcolor=None
        self.guiMan = gtk.Builder()
        self.guiMan.add_from_string(GUI)
        self.window = self.guiMan.get_object('lrcWin')
        self.window.connect('delete_event',self.winclose)
        self.window.set_opacity(self.options['Opacity'])
        if not self.options['WindowPositionx']=='centre':
            self.window.move(self.options['WindowPositionx'],self.options['WindowPositiony'])
        self.layout = gtk.Layout()
        self.vbox = self.guiMan.get_object('vbox1')
        self.vbox.pack_start(self.layout)

        self.vbox2 = gtk.VBox(homogeneous = True, spacing = int(self.options['LyricSpacing']))
        self.layout.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        self.x = 20
        self.y = 97
        self.window.resize(320,300)
        self.layout.put(self.vbox2, self.x, self.y)
        self.window.show_all()

        self.playerSS = self.guiMan.get_object('playerSS')
        self.playerNext = self.guiMan.get_object('playerNext')
        self.playerPrev = self.guiMan.get_object('playerPrev')
        self.Slower1 = self.guiMan.get_object('slower1')
        self.Quick1 = self.guiMan.get_object('quicker1')
        self.Slower2 = self.guiMan.get_object('slower2')
        self.Quick2 = self.guiMan.get_object('quicker2')
        self.lrcreset = self.guiMan.get_object('Reset')
        self.lrcSaveChange = self.guiMan.get_object('lrcSaveChange')
        self.lrcreSearch = self.guiMan.get_object('lrcSearch')
        self.playerSS.connect('activate',self.pSS)
        self.playerNext.connect('activate',self.pNext)
        self.playerPrev.connect('activate',self.pPrevious)
        self.Slower1.connect('activate',self.lrcSlower1)
        self.Quick1.connect('activate',self.lrcQuicker1)
        self.Slower2.connect('activate',self.lrcSlower2)
        self.Quick2.connect('activate',self.lrcQuicker2)
        self.lrcreset.connect('activate',self.lrcReset)
        self.lrcSaveChange.connect('activate',self.SaveChange)
        self.lrcreSearch.connect('activate',self.lrcList)

        if bool(self.exaile.player.current):
            artist = self.exaile.player.current.get_tag_display('artist')
            title = self.exaile.player.current.get_tag_display('title')
            try:
                locname = os.path.basename(self.exaile.player.current.local_file_name())
            except AttributeError:
                locname = '-'.join([artist, title])
                
            self.playTrack(None, None, self.exaile.player.current)
        else:
            self.stopTrack() 
    def pSS(self,*args):
        if self.exaile.player.is_playing():
            self.exaile.player.pause()
        else:
            self.exaile.player.play()
    def pNext(self,*args):
        self.exaile.queue.next()
    def pPrevious(self,*args):
        self.exaile.queue.prev()
    def lrcSlower1(self,*args):
        self.timeChange -= 100
    def lrcQuicker1(self,*args):
        self.timeChange += 100
    def lrcSlower2(self, *args):
        self.timeChange -= 50
    def lrcQuicker2(self,*args):
        self.timeChange += 50
    def lrcReset(self,*args):
        self.timeChange = 0
    def SaveChange(self, *args):
        if self.timeChange <> 0:
            lrc = lrcMod.writeLrc(self.lrcLines,self.timeLines,self.timeChange)
            art = self.exaile.player.current.get_tag_display('artist')
            tit = self.exaile.player.current.get_tag_display('title')
            try:
                locname = os.path.basename(self.exaile.player.current.local_file_name())
            except AttributeError:
                locname = '-'.join([art, tit])
            lrcMod.saveLrc(lrc,self.options['LyricFolder'], self.ops[self.options['Filename']](art, tit, locname))

    def reset(self):
        global TIMER
        self.lastcolor=None
        self.lrcLines = {}
        self.timeLines = []
        self.lyric = ''
        self.timeChange = 0
        self.isLrcFound = False
        try:
            gobject.source_remove(TIMER)
        except:
            pass
        try:
            for i in self.labels.keys():
                self.labels[i].destroy()
        except:
            pass
        self.labels={}
        self.x = 20
        self.y = 80
        self.layout.move(self.vbox2, self.x, self.y)
    def lrcSearch(self, art, tit, locname):
        if not lrcMod.ifLrcExist(self.options['LyricFolder'], self.ops[self.options['Filename']](art, tit, locname)):
            try:
                self.lyric = lrcMod.lrcGet(art, tit, 'TT')
                if self.lyric:
                    self.isLrcFound = True
                    lrcMod.saveLrc(self.lyric, self.options['LyricFolder'], self.ops[self.options['Filename']](art, tit, locname))
            except:
                pass
        else:
            self.lyric = lrcMod.readLrc(self.options['LyricFolder'], self.ops[self.options['Filename']](art, tit, locname))
            self.isLrcFound = True
        if self.isLrcFound ==True:
            (self.lrcLines,self.timeLines) = lrcMod.lrcAny(self.lyric)
    def lrcPlay(self):
        time = int(self.exaile.player.get_position() / 10000000) + self.timeChange
        if self.lrcLines.has_key(time):
            if self.lastcolor:
                self.lastcolor.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
            t = self.labels[time].get_allocation().y
            self.layout.move(self.vbox2, self.x, self.vbox2.get_allocation().y-t+80)
            self.labels[time].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.options['LyricColor']))
            self.lastcolor = self.labels[time]
        return True
    def setupTIMER(self):
        global TIMER
        TIMER = gobject.timeout_add(10,self.lrcPlay) 
    def timeSeek(self,*args):
        if self.isLrcFound and len(self.timeLines) > 0:
            time = int(self.exaile.player.get_position() / 10000000) + self.timeChange
            if time > self.timeLines[-1]:
                if self.lastcolor:
                    self.lastcolor.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                t = self.labels[self.timeLines[-1]].get_allocation().y
                self.layout.move(self.vbox2, self.x, 80 - (len(self.timeLines)-2)*(17 + int(self.options['LyricSpacing'])))
                self.labels[self.timeLines[-1]].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.options['LyricColor']))
                self.lastcolor = self.labels[self.timeLines[-1]]
            elif time < self.timeLines[0]:
                if self.lastcolor:
                    self.lastcolor.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                t = self.labels[self.timeLines[0]].get_allocation().y
                self.layout.move(self.vbox2, self.x, 80)
                self.labels[self.timeLines[0]].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.options['LyricColor']))
                self.lastcolor = self.labels[self.timeLines[0]]
            else:
                for i in range(len(self.timeLines)):
                    if (time > self.timeLines[i] and time < self.timeLines[i+1]) or time == self.timeLines[i]:
                        if self.lastcolor:
                            self.lastcolor.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                        self.layout.move(self.vbox2, self.x, 80 - i * (17 + int(self.options['LyricSpacing'])))
                        self.labels[self.timeLines[i]].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.options['LyricColor']))
                        self.lastcolor = self.labels[self.timeLines[i]]
    def winclose(self,*arg):
        settings.set_option('plugin/LyricDisp/windowpositionx', self.window.get_position()[0])
        settings.set_option('plugin/LyricDisp/windowpositiony', self.window.get_position()[1])
        global TIMER, PLUGIN
        try:gobject.source_remove(TIMER)
        except:pass
        PLUGIN = None
        return False

    def playTrack(self, type, player, track):
        self.reset()
        artist = track.get_tag_display('artist')
        title = track.get_tag_display('title')
        try:
            locname = os.path.basename(self.exaile.player.current.local_file_name())
        except AttributeError:
            locname = '-'.join([artist, title])
        self.lrcSearch(artist, title, locname)
        if self.isLrcFound and len(self.timeLines) > 0:
            max = 0
            for i in self.timeLines:
                if max<len(self.lrcLines[i]):
                    max=len(self.lrcLines[i])
                    mlabel=i
            for i in self.timeLines:
                self.labels[i]=gtk.Label(self.lrcLines[i].strip())
                self.labels[i].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                self.vbox2.pack_start(self.labels[i])
            (x,y) = self.labels[mlabel].get_layout().get_pixel_size()
            self.window.resize(x+40, y*16)
            rec = gtk.gdk.Rectangle(20,80, x+40, y*16)
            self.layout.size_allocate(rec)
            rec = gtk.gdk.Rectangle(20,80, x+40, y*16)
            self.labels[self.timeLines[0]].size_allocate(rec)
            self.layout.move(self.vbox2, 20, 80)
            self.vbox2.show_all()
            self.timeSeek()
            self.setupTIMER()
            self.window.set_title('%s - %s' % (artist,title))
        else:
            list=['歌词窗口','Exaile歌词滚动显示插件',' ','自动搜索歌词失败',' ','请尝试手动搜索']
            self.PlayInfo(list)
    def stopTrack(self,*args):
        list=['歌词窗口','Exaile歌词滚动显示插件',' ','作者：BillMa',' ','项目主页:http://exaile-cn.googlecode.com']
        self.PlayInfo(list)

    def colorChange(self, type, player, value):
        self.options['LyricColor'] = value
    def nameChange(self, type, player, value):
        self.options['Filename'] = value

    def lrcList(self, *arg):
        searchlist = chooser.lrcSearchWin()
        result = searchlist.run(self.exaile.player.current.get_tag_display('artist'), self.exaile.player.current.get_tag_display('title'))
        if result:
            self.lyric = result
            art = self.exaile.player.current.get_tag_display('artist')
            tit = self.exaile.player.current.get_tag_display('title')
            try:
                locname = os.path.basename(self.exaile.player.current.local_file_name())
            except AttributeError:
                locname = '-'.join([art, tit])
            lrcMod.saveLrc(self.lyric,self.options['LyricFolder'], self.ops[self.options['Filename']](art, tit, locname))
            (self.lrcLines,self.timeLines) = lrcMod.lrcAny(self.lyric)
            self.timeChange = 0
            try:
                for i in self.labels.keys():
                    self.labels[i].destroy()
            except:
                pass
            self.labels={}
            max = 0
            for i in self.timeLines:
                if max<len(self.lrcLines[i]):
                    max=len(self.lrcLines[i])
                    mlabel=i
            for i in self.timeLines:
                self.labels[i]=gtk.Label(self.lrcLines[i].strip())
                self.labels[i].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                self.vbox2.pack_start(self.labels[i])
            (x,y) = self.labels[mlabel].get_layout().get_pixel_size()
            self.window.resize(x+40, y*16)
            self.vbox2.show_all()
            self.timeSeek()
    def PlayInfo(self, list):
        self.window.resize(320,300)
        self.reset()
        self.window.set_title(list[0])
        self.layout.move(self.vbox2, self.x , 80)
        for i in range(1,6):
            self.labels[i]=gtk.Label(list[i])
            self.labels[i].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
            self.vbox2.pack_start(self.labels[i])
        self.vbox2.show_all()
def lrcWinShow(menuitem, exaile, options, *args):
    global PLUGIN
    if not PLUGIN:
        PLUGIN = lrcWin(exaile, options)
        if bool(exaile.player.current):
            PLUGIN.playTrack(None, None, exaile.player.current)
        else:
            PLUGIN.stopTrack() 
    else:
        PLUGIN.window.present()
