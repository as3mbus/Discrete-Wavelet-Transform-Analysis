
import gi

from DWT2 import *
from GLCM import *
from PSNR import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="DWTGLCMPSNR")
        self.set_border_width(10)
        self.set_default_size(400,200)
        box1 = Gtk.Box(orientation= Gtk.Orientation.VERTICAL)
        self.add(box1)
        self.loadwatermark = Gtk.Image.new_from_file('')
        self.loadwatermark.set_pixel_size(200)
        box1.pack_start(self.loadwatermark,1,1,10)
        box2 = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box1.pack_start(box2,1,1,10)
        self.imgbuffer = Gtk.TextBuffer()
        self.img = Gtk.TextView()
        self.img.set_buffer(self.imgbuffer)
        self.imgbuffer.set_text("")
        self.img.set_can_focus(0)
        box2.pack_start(self.img,1,1,10)

        filechooser = Gtk.Button(label="...")
        # filechooser.connect("clicked",self.on_image_clicked)
        box2.pack_start(filechooser,0,0,5)
        bttndwt = Gtk.Button(label="Next")
        # bttndwt.connect("clicked",self.on_bttndwt_clicked)
        box1.pack_start(bttndwt,1,1,0)
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
