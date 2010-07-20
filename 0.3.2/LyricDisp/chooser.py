# coding=utf8

import gtk
from lrcMod import lrcDic,lrcurldown
GUI = r"""<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy project-wide -->
  <object class="GtkVBox" id="vbox1">
    <property name="visible">True</property>
    <property name="border_width">2</property>
    <property name="orientation">vertical</property>
    <child>
      <object class="GtkHBox" id="hbox2">
        <property name="visible">True</property>
        <property name="spacing">3</property>
        <child>
          <object class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="label" translatable="yes">&#x6B4C;&#x66F2;&#x540D;&#xFF1A;</property>
          </object>
          <packing>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkEntry" id="tit">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="invisible_char">&#x2022;</property>
          </object>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="label2">
            <property name="visible">True</property>
            <property name="label" translatable="yes">&#x6B4C;&#x624B;&#x540D;&#xFF1A;</property>
          </object>
          <packing>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkEntry" id="art">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="invisible_char">&#x2022;</property>
          </object>
          <packing>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="search">
            <property name="label" translatable="yes">&#x641C;&#x7D22;</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
          </object>
          <packing>
            <property name="position">4</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="padding">6</property>
        <property name="position">0</property>
      </packing>
    </child>
    <child>
      <object class="GtkHPaned" id="hpaned1">
        <property name="visible">True</property>
        <property name="can_focus">True</property>
        <child>
          <object class="GtkTreeView" id="treeview1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
          </object>
          <packing>
            <property name="resize">False</property>
            <property name="shrink">True</property>
          </packing>
        </child>
        <child>
          <object class="GtkScrolledWindow" id="scrolledwindow1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="hscrollbar_policy">automatic</property>
            <property name="vscrollbar_policy">automatic</property>
            <child>
              <object class="GtkTextView" id="textview1">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="resize">True</property>
            <property name="shrink">True</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="position">1</property>
      </packing>
    </child>
  </object>
</interface>
"""


class lrcSearchWin(object):
    def __init__(self):
        self.dlg = gtk.Dialog(None,None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OK, gtk.RESPONSE_OK))
        self.dlg.set_title('选择歌词')
        self.guiMan = gtk.Builder()
        self.guiMan.add_from_string(GUI)
        self.vbox = self.guiMan.get_object('vbox1')
        self.treeview = self.guiMan.get_object('treeview1')
        self.textview = self.guiMan.get_object('textview1')
        self.textview.set_editable(False)
        self.SearchButton = self.guiMan.get_object('search')
        self.art = self.guiMan.get_object('art')
        self.tit = self.guiMan.get_object('tit')
        self.LyricBuffer = gtk.TextBuffer()
        self.textview.set_buffer(self.LyricBuffer)
        self.model = gtk.ListStore(int, str, str, str, str)
        self.treeview.set_model(self.model)
        self.treeview.append_column(gtk.TreeViewColumn('', gtk.CellRendererText(), text = 0))
        self.treeview.append_column(gtk.TreeViewColumn('Artist', gtk.CellRendererText(), text = 1))
        self.treeview.append_column(gtk.TreeViewColumn('Title', gtk.CellRendererText(), text = 2))
        self.treeview.append_column(gtk.TreeViewColumn('Source', gtk.CellRendererText(), text = 3))
        self.SearchButton.connect('released', self.set_lyricsList)
        self.treeview.connect('row-activated', self.double_clicked)
        self.treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)
        self.treeview.get_selection().connect('changed', self.selectchange)
        self.dlg.vbox.pack_start(self.vbox)
        self.dlg.set_default_size(200, 250)
    def set_lyricsList(self,button):
        self.model.clear()
        art = self.art.get_text()
        tit = self.tit.get_text()
        ttl = lrcDic(art, tit, 'TT')
        sgl = lrcDic(art, tit, 'Sogou')
        count = 1
        for i in ttl:
            self.model.append([count, ttl[i]['artist'], ttl[i]['title'], '千千静听', ttl[i]['id']])
            count = count + 1
        for i in sgl:
            self.model.append([count, sgl[i]['artist'], sgl[i]['title'], '搜狗音乐', sgl[i]['id']])
            count = count + 1
    def run(self, art ,tit):
        self.art.set_text(art)
        self.tit.set_text(tit)
        ttl = lrcDic(art, tit, 'TT')
        sgl = lrcDic(art, tit, 'Sogou')
        count = 1
        for i in ttl:
            self.model.append([count, ttl[i]['artist'], ttl[i]['title'], '千千静听', ttl[i]['id']])
            count = count + 1
        for i in sgl:
            self.model.append([count, sgl[i]['artist'], sgl[i]['title'], '搜狗音乐', sgl[i]['id']])
            count = count + 1
        self.dlg.show_all()
        if gtk.RESPONSE_OK == self.dlg.run():
            (model, iter) = self.treeview.get_selection().get_selected()
            if iter:
                result = model.get(iter, 1, 2, 3, 4)
                (art, tit, source, id) = model.get(iter, 1, 2, 3, 4)
                result = self.downloadlyric(id, art, tit, source)
            else:
                result = None
        else:
            result = None
        self.dlg.hide_all()
        
        return result
    
    def double_clicked(self, view, path, view_column):
        self.treeview.get_selection().unselect_all()
        self.treeview.get_selection().select_path(path)
        self.dlg.response(gtk.RESPONSE_OK)

    def downloadlyric(self, id, art, tit, source):
        sources={'千千静听' : 'TT', '搜狗音乐' : 'Sogou'}
        lyric = lrcurldown(id, art, tit, sources[source])
        return lyric

    def selectchange(self, tree):
        try:
            (model, iter) = self.treeview.get_selection().get_selected()
            (art, tit, source, id) = model.get(iter, 1, 2, 3, 4)
            lyric = self.downloadlyric(id, art, tit, source)
            self.LyricBuffer.set_text(lyric)
        except TypeError:
            pass
