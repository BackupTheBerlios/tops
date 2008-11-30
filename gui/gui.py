#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: gui/gui.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import gobject
import gtk
import gtk.glade
import pango
import os

#from .. import models

models = {
    'Leica TCR 1205' : 'leica_tcr_1205',
    'Zeiss Elta R55' : 'zeiss_elta_r55',
    'Nikon Npl 350' : 'nikon_npl_350',
    'Custom' : 'generic'
    }
GLADEFILE = "tops.glade"

class AboutDialog(object):
    def __init__(self):
        self.gladefile = GLADEFILE
        self.widgetTree1 = gtk.glade.XML(self.gladefile,'aboutdialog1')
        self.aboutdialog1 = self.widgetTree1.get_widget('aboutdialog1')
        self.aboutdialog1.run()
        self.aboutdialog1.destroy()

class ExportDialog(object):
    def __init__(self):
        self.gladefile = GLADEFILE
        self.widgetTree1 = gtk.glade.XML(self.gladefile,'export_dialog1')
        self.export_dialog1 = self.widgetTree1.get_widget('export_dialog1')
        self.modelsListStore = gtk.ListStore(gobject.TYPE_STRING)
        for m, n in models.items():
            self.modelsListStore.append([m])
        self.combobox_input = self.widgetTree1.get_widget('combobox_input')
        self.combobox_input.set_model(model=self.modelsListStore)
        cell = gtk.CellRendererText()
        self.combobox_input.pack_start(cell, True)
        self.combobox_input.add_attribute(cell, 'text', 0)

        self.export_dialog1.run()
        self.export_dialog1.destroy()

class TotalOpenGUI(object):
    '''Implements the main program window.'''
    
    def __init__(self):
        
        self.gladefile = GLADEFILE
        self.widgetTree = gtk.glade.XML(self.gladefile,'window1')
        self.widgetTree.signal_autoconnect(self)
        self.window1 = self.widgetTree.get_widget('window1')
        self.window1.show_all()
        
        self.textView = self.widgetTree.get_widget('textview1')
        self.textBuffer = gtk.TextBuffer()
        self.textView.set_buffer(self.textBuffer)
        mono_font_desc = pango.FontDescription("monospace")
        self.textView.modify_font(mono_font_desc)
    
    def gtk_main_quit(self, widget, event=None):
        gtk.main_quit()
    
    def on_open_menuitem_activate(self, widget):
        file_open = gtk.FileChooserDialog(title="Select file to open"
                    , action=gtk.FILE_CHOOSER_ACTION_OPEN
                    , buttons=(gtk.STOCK_CANCEL
                        , gtk.RESPONSE_CANCEL
                        , gtk.STOCK_OPEN
                        , gtk.RESPONSE_OK))
        if file_open.run() == gtk.RESPONSE_OK:
            result = file_open.get_filename()
        file_open.destroy()
        self.textBuffer.set_text(open(result).read())
    
    def on_save_menuitem_activate(self, widget):
        file_save = gtk.FileChooserDialog(title="Select destination file"
                    , action=gtk.FILE_CHOOSER_ACTION_SAVE
                    , buttons=(gtk.STOCK_CANCEL
                        , gtk.RESPONSE_CANCEL
                        , gtk.STOCK_SAVE
                        , gtk.RESPONSE_OK))
        if file_save.run() == gtk.RESPONSE_OK:
            result = file_save.get_filename()
        file_save.destroy()
        iterstart = self.textBuffer.get_start_iter()
        iterend = self.textBuffer.get_end_iter()
        
        # FIXME handle overwriting an existing file (ask the user)
        e = open(result, 'w')
        e.write(self.textBuffer.get_text(iterstart, iterend))
        e.close()
    
    def export_dialog(self, widget):
        ExportDialog()
    
    def about_dialog(self, widget):
        AboutDialog()

TotalOpenGUI()
gtk.main()
