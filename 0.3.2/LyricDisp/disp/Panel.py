# coding=utf-8

from xl import event,player
from xl.nls import gettext as _

import gtk, gobject, gtk.gdk
import os
import lrcMod
import chooser
TIMER = None
PLUGIN = None

class Panel(gtk.VBox):
    def __init__(self, exaile, options):
        self.ops = {'artist-title.lrc' : lambda art, tit, locname: '%s-%s' %(art, tit), \
                    'title-artist.lrc': lambda art, tit, locname: '%s-%s' %(tit, art), \
                    '与歌曲文件名相同': lambda art, tit, locname: locname.replace('.mp3','').replace('.wmv','')}

        self.exaile = exaile
        self.options = options
        gtk.VBox.__init__(self)
        self.scroller = gtk.ScrolledWindow()
        self.scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.pack_start(self.scroller, True, True, 0)

        self.TagTable = gtk.TextTagTable()
        self.textview = gtk.TextView()
        self.textview.set_cursor_visible(False)
        self.textview.set_editable(False)
        self.textview.set_wrap_mode(gtk.WRAP_WORD)
        self.textview.set_justification(gtk.JUSTIFY_LEFT)
        self.textview.set_left_margin(4)
        self.scroller.add(self.textview)

        self.LyricBuffer = gtk.TextBuffer()
        self.textview.set_buffer(self.LyricBuffer)
        color = gtk.gdk.Color(self.options['LyricColor']).to_string()
        self.colortag = self.LyricBuffer.create_tag(foreground=color)

        self.lrcDic = {}
        self.lrcLines = {}
        self.lyric = ''
        self.timeChange = 0
        self.isLrcFound = False
        
        event.add_callback(self.playTrack, 'playback_track_start')
        event.add_callback(self.stopTrack, 'playback_player_end')
        event.add_callback(self.timeSeek, 'seek')
        event.add_callback(self.colorChange, 'color_change')
        event.add_callback(self.nameChange, 'name_change')
        self.menu = gtk.Menu()
        self.lrcsearch = gtk.MenuItem('手动搜索')
        self.scrollable = gtk.CheckMenuItem('歌词微调')
        self.savechange = gtk.MenuItem('保存修改')
        self.menu.append(self.lrcsearch)
        self.menu.append(self.scrollable)
        self.menu.append(self.savechange)
        self.scrollable.set_active(False)
        self.scrollable.show()
        self.menu.show()
        self.savechange.show()
        self.lrcsearch.show()
        self.textview.connect('event', self.TVE)
        self.savechange.connect('activate', self.SaveChange)
        self.lrcsearch.connect('activate', self.lrcList)

        if bool(self.exaile.player.current):
            artist = self.exaile.player.current.get_tag_display('artist')
            title = self.exaile.player.current.get_tag_display('title')
            try:
                locname = os.path.basename(self.exaile.player.current.local_file_name())
            except AttributeError:
                locname = '-'.join([artist, title])
            self.lrcSearch(artist, title, locname)
            self.InfoPlay('play')
            if self.isLrcFound:
                self.timeSeek()
        else:
            self.InfoPlay(OP = 'stop')

    def SaveChange(self,*args):
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
        self.lrcLines = {}
        self.timeLines = []
        self.lyric = ''
        self.timeChange = 0
        self.isLrcFound = False
        self.removetags()
        try:
            gobject.source_remove(TIMER)
        except:
            pass

    def lrcSearch(self, art, tit, locname):
        if not lrcMod.ifLrcExist(self.options['LyricFolder'], self.ops[self.options['Filename']](art, tit, locname)):
            self.lyric = lrcMod.lrcGet(art, tit, 'TT')
            if self.lyric:
                self.isLrcFound = True
                lrcMod.saveLrc(self.lyric, self.options['LyricFolder'], self.ops[self.options['Filename']](art, tit, locname))
            else: self.isLrcFound = False
        else:
            self.lyric = lrcMod.readLrc(self.options['LyricFolder'], self.ops[self.options['Filename']](art, tit, locname))
            self.isLrcFound = True
        if self.isLrcFound:
            (self.lrcLines,self.timeLines) = lrcMod.lrcAny(self.lyric)
            if len(self.timeLines) == 0:
                self.isLrcFound = False
        if self.isLrcFound:
            self.timeSeek()

    def lrcPlay(self):
        time = int(self.exaile.player.get_position() / 10000000) + self.timeChange
        if self.lrcLines.has_key(time):
            self.removetags()
            linenum = self.timeLines.index(time)
            self.start = self.LyricBuffer.get_iter_at_line(linenum)
            if linenum < len(self.timeLines) - 1:
                self.end = self.LyricBuffer.get_iter_at_line(linenum + 1)
            else:
                self.end = self.LyricBuffer.get_end_iter()
            self.LyricBuffer.apply_tag(self.colortag, self.start, self.end)
            self.textview.scroll_to_iter(self.start, 0.1)
        return True

    def timeSeek(self,*args):
        if self.isLrcFound:
            self.removetags()
            time = int(self.exaile.player.get_position() / 10000000) + self.timeChange
            if time > self.timeLines[-1]:
                self.end = self.LyricBuffer.get_end_iter()
                self.start = self.LyricBuffer.get_iter_at_line(len(self.timeLines) - 1)
                self.LyricBuffer.apply_tag(self.colortag, self.start, self.end)
                self.textview.scroll_to_iter(self.start, 0.1)
            elif time < self.timeLines[0]:
                self.start = self.LyricBuffer.get_start_iter()
                self.end = self.LyricBuffer.get_iter_at_line(1)
                self.LyricBuffer.apply_tag(self.colortag, self.start, self.end)
                self.textview.scroll_to_iter(self.start, 0.1)
            else:
                for i in range(len(self.timeLines)):
                    if time > self.timeLines[i] and time < self.timeLines[i+1] or time == self.timeLines[i]:
                        self.start = self.LyricBuffer.get_iter_at_line(i)
                        self.end = self.LyricBuffer.get_iter_at_line(i + 1)
                        self.LyricBuffer.apply_tag(self.colortag, self.start, self.end)
                        self.textview.scroll_to_iter(self.start, 0.1)

    def InfoPlay(self,OP = 'play'):
        if OP == 'play':
            if self.isLrcFound:
                global TIMER
                self.text = '\n'.join([self.lrcLines[i] for i in self.timeLines])
                self.LyricBuffer.set_text(self.text)
                TIMER = gobject.timeout_add(10,self.lrcPlay) 
            else:
                self.LyricBuffer.set_text('No Lyrics')
        elif OP == 'stop':
            self.LyricBuffer.set_text('Player Stop')
            
    def playTrack(self, type, player, track):
        self.reset()
        artist = track.get_tag_display('artist')
        title = track.get_tag_display('title')
        try:
            locname = os.path.basename(self.exaile.player.current.local_file_name())
        except AttributeError:
            locname = '-'.join([artist, title])
        self.lrcSearch(artist, title, locname)
        self.InfoPlay('play')

    def stopTrack(self,*args):
        self.reset()
        self.InfoPlay('stop')
    
    def removetags(self):
        start = self.LyricBuffer.get_start_iter()
        end = self.LyricBuffer.get_end_iter()
        self.LyricBuffer.remove_all_tags(start,end)

    def colorChange(self, type, player, value):
        value = gtk.gdk.Color(value).to_string()
        self.colortag.set_property('foreground', value)

    def nameChange(self, type, player, value):
        self.options['Filename'] = value

    def TVE(self, widget, event, data = None):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 3:
                self.menu.popup(None, None, None, event.button, event.time)
                return True
        if event.type == gtk.gdk.SCROLL:
            if self.scrollable.get_active():
                if event.direction == gtk.gdk.SCROLL_UP:
                    self.timeChange -= 200
                elif event.direction == gtk.gdk.SCROLL_DOWN:
                    self.timeChange += 200
            else:
                return True
        else:return False

    def lrcList(self,*args):
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
            self.text = '\n'.join([self.lrcLines[i] for i in self.timeLines])
            self.LyricBuffer.set_text(self.text)
            self.timeChange = 0
            self.timeSeek()

def disable(exaile):
    global PLUGIN, TIMER
    if PLUGIN:
        exaile.gui.remove_panel(PLUGIN)
        PLUGIN = None
    if TIMER:
        gobject.source_remove(TIMER)

def enable(exaile, options):
    global PLUGIN
    PLUGIN = Panel(exaile, options)
    PLUGIN.show_all()
    exaile.gui.add_panel(PLUGIN, _('歌词显示'))
