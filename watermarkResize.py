#!/usr/bin/env python

import sys


import gi

from DWT2 import *
from PSNR import *
from embed import *
from WatermarkComparison import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
Gdk.threads_init()
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
        print "quit from menu"
        Gtk.main_quit()

# This is our init part where we connect the signals
    def __init__(self):
        self.gladefile = "WatermarkResize.glade"  # store the file name
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
        self.BoxOriginal = self.builder.get_object("BoxOriginal")
        self.ImageOriginal = self.builder.get_object("ImageOriginal")
        self.EntryOriginal = self.builder.get_object("EntryOriginal")
        self.ImageWatermark = self.builder.get_object("ImageWatermark")
        self.EntryWatermark = self.builder.get_object("EntryWatermark")
        self.builder.get_object("BtnWatermark").connect(
        "clicked", self.loadWatermark)
        self.builder.get_object("BtnEmbed").connect(
            "clicked", self.embedWatermark)

    def loadOriginal(self, widget):
        dialog = Gtk.FileChooserDialog("Pilih Gambar ", self.window, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.EntryOriginal.set_text(dialog.get_filename())

            allocation = self.BoxOriginal.get_allocation()
            desired_width = 400
            desired_height = 500


            pixbuf = GdkPixbuf.Pixbuf.new_from_file(dialog.get_filename())
            pixbuf_width  = (float) (pixbuf.get_width())
            pixbuf_height = (float) (pixbuf.get_height())
            if desired_width < pixbuf_width or desired_height < pixbuf_height:
                if pixbuf_height > pixbuf_width:
                    target_scale  = desired_height/pixbuf_height
                    target_width  = (int) (pixbuf_width *  target_scale)
                    target_height = (int) (pixbuf_height * target_scale)
                else:
                    target_scale  = desired_width/pixbuf_width
                    target_width  = (int) (pixbuf_width * target_scale)
                    target_height = (int) (pixbuf_height * target_scale)
                    # print  str(w) + "/" + str(waterWidth) +" = "+
                    # str(float(w)/waterWidth)
                print(str(pixbuf_width)+ " * () " +str(desired_width)+ "/"+str(pixbuf_width) )
                pixbuf = pixbuf.scale_simple(target_width, target_height, GdkPixbuf.InterpType.BILINEAR)
                # pixbuf = pixbuf.scale(0,0,target_width, target_height,0,0,target_scale,target_scale, GdkPixbuf.InterpType.BILINEAR)
            self.ImageOriginal.set_from_pixbuf(pixbuf)
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
            allocation = self.ImageWatermark.get_allocation()
            desired_width = allocation.width
            desired_height = allocation.height


            pixbuf = GdkPixbuf.Pixbuf.new_from_file(dialog.get_filename())
            pixbuf_width=pixbuf.get_width()
            pixbuf_height=pixbuf.get_height()
            if desired_width < pixbuf_width or desired_height < pixbuf_height:
                if pixbuf_height > pixbuf_width:
                    target_width  = pixbuf_width * (desired_height/pixbuf_height)
                    target_height = pixbuf_height * (desired_height/pixbuf_height)
                    target_scale  = (desired_height/pixbuf_height)
                else:
                    target_width  = pixbuf_width * (desired_width/pixbuf_width)
                    target_height = pixbuf_height * (desired_width/pixbuf_width)
                    target_scale  = (desired_width/pixbuf_width)
                    # print  str(w) + "/" + str(waterWidth) +" = "+
                    # str(float(w)/waterWidth)
                # pixbuf = pixbuf.scale_simple(target_width, target_height, GdkPixbuf.InterpType.BILINEAR)
                pixbuf = pixbuf.scale(0,0,target_width, target_height,0,0,target_scale,target_scale, GdkPixbuf.InterpType.BILINEAR)
                # print(str(target_width)+ " " +str(target_height) )
            self.ImageWatermark.set_from_pixbuf(pixbuf)
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
        print "sedang DWT"
        ImageOriginalDWT = waveleteTransform(ImageOriginal)
        height, width = ImageOriginal.shape[:2]
        ImageWatermark = cv2.imread(self.EntryWatermark.get_text())
        waterHeight, waterWidth = ImageWatermark.shape[:2]
        if width / 2 < waterWidth or height / 2 < waterHeight:
            if waterHeight > waterWidth:
                print waterHeight / (height / 2)
                ImageWatermark = cv2.resize(ImageWatermark, (0, 0), fx=float(
                    height) / 2 / waterHeight, fy=float(height) / 2 / waterHeight)
            else:
                # print  str(w) + "/" + str(waterWidth) +" = "+
                # str(float(w)/waterWidth)
                ImageWatermark = cv2.resize(ImageWatermark, (0, 0), fx=float(width) / 2 / waterWidth, fy = float(width) / 2 / waterWidth)
        waterHeight, waterWidth=ImageWatermark.shape[:2]
        print "sedang embedding"
        alpha=float(self.builder.get_object("EntryIntensity").get_text())
        print alpha
        ImageWatermarkedDWT=embed(ImageOriginalDWT, ImageWatermark, 0, 0, waterWidth, waterHeight, alpha)
        print "sedang embedding2"
        ImageWatermarked=inverseWaveleteTransform(ImageWatermarkedDWT)
        print "sedang ekstrak1"
        imageWatermarkedDDWT=waveleteTransform(ImageWatermarked)
        print "sedang Ekstrak2"
        ImageExtract=extract(imageWatermarkedDDWT[0:waterHeight, 0:waterWidth],
                            ImageOriginalDWT[0:waterHeight, 0:waterWidth], alpha)
        print "sedang nyetak"
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
