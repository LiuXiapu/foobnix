#-*- coding: utf-8 -*-
'''
Created on 28 сент. 2010

@author: ivan
'''

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango

from foobnix.util import idle_task
from foobnix.util.const import FTYPE_RADIO
from foobnix.gui.model.signal import FControl
from foobnix.util.time_utils import convert_seconds_to_text


class SeekProgressBarControls(FControl, Gtk.Alignment):
    def __init__(self, controls, seek_bar_movie=None):
        FControl.__init__(self, controls)
        self.seek_bar_movie = seek_bar_movie
        Gtk.Alignment.__init__(self, xalign=0.5, yalign=0.5, xscale=1.0, yscale=1.0)

        self.set_padding(padding_top=7, padding_bottom=7, padding_left=0, padding_right=7)

        self.tooltip = Gtk.Window(Gtk.WindowType.POPUP)
        self.tooltip.set_position(Gtk.WindowPosition.CENTER)
        self.tooltip_label = Gtk.Label.new(None)
        self.tooltip.add(self.tooltip_label)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_ellipsize(Pango.EllipsizeMode.END)
        self.progressbar.set_property("show-text", True)
        self.progressbar.set_text("00:00 / 00:00")
        try:
            self.progressbar.set_has_tooltip(True)
        except:
            #fix debian compability
            pass

        event = Gtk.EventBox()
        event.add(self.progressbar)
        event.connect("button-press-event", self.on_seek)
        event.connect("leave-notify-event", lambda *a: self.safe_hide_tooltip())
        event.connect("motion-notify-event", self.on_pointer_motion)
        self.add(event)
        self.show_all()
        self.tooltip.hide()

    @idle_task
    def safe_hide_tooltip(self):
        self.tooltip.hide()

    @idle_task
    def on_pointer_motion(self, widget, event):
        width = self.progressbar.get_allocation().width
        x = event.x
        duration = self.controls.media_engine.duration_sec
        seek_percent = (x + 0.0) / width
        sec = int(duration * seek_percent)
        sec = convert_seconds_to_text(sec)

        self.tooltip_label.set_text(sec)
        self.tooltip.show_all()
        unknown_var, x, y, mask = Gdk.get_default_root_window().get_pointer()
        self.tooltip.move(x+5, y-15)

    def on_seek(self, widget, event):
        bean = self.controls.media_engine.bean
        if bean and bean.type == FTYPE_RADIO:
            return None

        width = widget.get_allocation().width
        x = event.x
        seek_percent = (x + 0.0) / width * 100
        self.controls.player_seek(seek_percent)

        if self.seek_bar_movie:
            self.seek_bar_movie.on_seek(widget, event)

    @idle_task
    def set_text(self, text):
        if text:
            self.progressbar.set_text(text[:200])

        if self.seek_bar_movie:
            self.seek_bar_movie.set_text(text)

    @idle_task
    def clear(self):
        self.progressbar.set_text("00:00 / 00:00")
        self.progressbar.set_fraction(0)

        if self.seek_bar_movie:
            self.seek_bar_movie.clear()

    @idle_task
    def fill_seekbar(self):
        self.progressbar.set_fraction(1)

    @idle_task
    def update_seek_status(self, position_sec, duration_sec):
        if duration_sec == 0:
            seek_text = "00:00 / 00:00"
            seek_persent = 0.999
        else:
            duration_str = convert_seconds_to_text(duration_sec)
            position_str = convert_seconds_to_text(position_sec)
            seek_persent = (position_sec + 0.0) / duration_sec
            seek_text = position_str + " / " + duration_str

        if 0 <= seek_persent <= 1:
            self.progressbar.set_text(seek_text)
            self.progressbar.set_fraction(seek_persent)

        if self.seek_bar_movie:
            self.seek_bar_movie.update_seek_status(position_sec, duration_sec)
