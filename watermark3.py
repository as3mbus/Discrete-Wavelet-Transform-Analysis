#!/usr/bin/env python

import sys


import gi

from DWT2 import *
from PSNR import *
from embed import *
from WatermarkComparison import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# print pygtk._get_available_versions()
# we can call it just about anything we want


class Watermark:

    # This first define is for our on_window1_destroy signal we created in the
    # Glade designer. The print message does just that and prints to the terminal
    # which can be useful for debugging. The 'object' if you remember is the signal
    # class we picked from GtkObject.
    def on_window1_destroy(self, object, data=None):
        print ("quit with cancel")
        Gtk.main_quit()

# This is the same as above but for our menu item.
    def on_gtk_quit_activate(self, menuitem, data=None):
        print ("quit from menu")
        Gtk.main_quit()

# This is our init part where we connect the signals
    def __init__(self):
        self.gladefile = "Watermark.glade"  # store the file name
        self.builder = Gtk.Builder()  # create an instance of the gtk.Builder
        # add the xml file to the Builder
        self.builder.add_from_file(self.gladefile)

# This line does the magic of connecting the signals created in the Glade3
# builder to our defines above. You must have one def for each signal if
# you use this line to connect the signals.
        self.builder.connect_signals(self)

        self.window = self.builder.get_object(
            "window1")  # This gets the 'window1' object
        self.window.show()  # this shows the 'window1' object
        self.window.connect("delete-event", Gtk.main_quit)

        self.builder.get_object("BtnOriginal").connect(
            "clicked", self.loadOriginal)
        self.ImageOriginal = self.builder.get_object("ImageOriginal")
        self.EntryOriginal = self.builder.get_object("EntryOriginal")
        self.ImageWatermark = self.builder.get_object("ImageWatermark")
        self.EntryWatermark = self.builder.get_object("EntryWatermark")
        self.builder.get_object("BtnWatermark").connect(
        "clicked", self.loadWatermark)
        self.builder.get_object("BtnEmbed").connect(
            "clicked", self.embedWatermark)

    def loadOriginal(self, widget):
        dialog = Gtk.FileChooserDialog("Pilih Gambar ", self.window, Gtk.FileChooserAction.OPEN, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.EntryOriginal.set_text(dialog.get_filename())
            self.ImageOriginal.set_from_file(dialog.get_filename())
            self.window.resize(400, 200)
            self.window.set_gravity(Gdk.Gravity.CENTER)
            print("File Selected", dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def loadWatermark(self, widget):
        dialog = Gtk.FileChooserDialog("Pilih Gambar ", self.window, Gtk.FileChooserAction.OPEN, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.EntryWatermark.set_text(dialog.get_filename())
            self.ImageWatermark.set_from_file(dialog.get_filename())
            self.window.resize(400, 200)
            print("File Selected", dialog.get_filename())
        elif response == Gtk.ResponseType.NORTH:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image File")
        filter_image.add_mime_type("image/*")
        dialog.add_filter(filter_image)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def embedWatermark(self, widget):

        ImageOriginal = cv2.imread(self.EntryOriginal.get_text())
        print ("sedang DWT")
        ImageOriginalDWT = waveleteTransform(ImageOriginal)
        height, width = ImageOriginal.shape[:2]
        ImageWatermark = cv2.imread(self.EntryWatermark.get_text())
        waterHeight, waterWidth = ImageWatermark.shape[:2]
        if width / 2 < waterWidth or height / 2 < waterHeight:
            if waterHeight > waterWidth:
                print (waterHeight / (height / 2))
                ImageWatermark = cv2.resize(ImageWatermark, (0, 0), fx=float(
                    height) / 2 / waterHeight, fy=float(height) / 2 / waterHeight)
            else:
                # print  str(w) + "/" + str(waterWidth) +" = "+
                # str(float(w)/waterWidth)
                ImageWatermark = cv2.resize(ImageWatermark, (0, 0), fx=float(width) / 2 / waterWidth, fy = float(width) / 2 / waterWidth)
        waterHeight, waterWidth=ImageWatermark.shape[:2]
        print("sedang embedding")
        alpha=float(self.builder.get_object("EntryIntensity").get_text())
        print(alpha)
        ImageWatermarkedDWT=embed(ImageOriginalDWT, ImageWatermark, 0, 0, waterWidth, waterHeight, alpha)
        print("sedang embedding2")
        ImageWatermarked=inverseWaveleteTransform(ImageWatermarkedDWT)
        print ("sedang ekstrak1")
        imageWatermarkedDDWT=waveleteTransform(ImageWatermarked)
        print ("sedang Ekstrak2")
        ImageExtract=extract(imageWatermarkedDDWT[0:waterHeight, 0:waterWidth],
                            ImageOriginalDWT[0:waterHeight, 0:waterWidth], alpha)
        print ("sedang nyetak")
        cv2.imwrite("/tmp/ImageOriginal.jpeg",ImageOriginal)
        cv2.imwrite("/tmp/ImageWatermarked.jpeg",ImageWatermarked)
        cv2.imwrite("/tmp/ImageWatermark.jpeg",ImageWatermark)
        cv2.imwrite("/tmp/ImageExtract.jpeg",ImageExtract)
        compare = WatermarkCompare("/tmp/ImageOriginal.jpeg","/tmp/ImageWatermarked.jpeg","/tmp/ImageWatermark.jpeg","/tmp/ImageExtract.jpeg")



if __name__ == '__main__':
    # win = MyWindow()
    # win.connect("delete-event", Gtk.main_quit)
    # win.show_all()
    wtm=Watermark()
    Gtk.main()
