#!/usr/bin/env python

import sys


import gi


from PSNR import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk
Gdk.threads_init()

# print pygtk._get_available_versions()
# we can call it just about anything we want


class WatermarkCompare:

    # This first define is for our on_window1_destroy signal we created in the
    # Glade designer. The print message does just that and prints to the terminal
    # which can be useful for debugging. The 'object' if you remember is the signal
    # class we picked from GtkObject.
    def on_window1_destroy(self, object, data=None):
        print "quit with cancel"
        Gtk.main_quit()

# This is the same as above but for our menu item.
    def on_gtk_quit_activate(self, menuitem, data=None):
        print "quit from menu"
        Gtk.main_quit()

# This is our init part where we connect the signals
    def __init__(self, ImageOriginal, ImageWatermarked, ImageWatermark, ImageExtract):
        self.gladefile = "Watermark-Comparison.glade"  # store the file name
        self.builder = Gtk.Builder()  # create an instance of the gtk.Builder
        # add the xml file to the Builder
        self.builder.add_from_file(self.gladefile)

        self.ImageOriginal = cv2.imread(ImageOriginal)
        self.ImageWatermarked = cv2.imread(ImageWatermarked)
        self.ImageWatermark = cv2.imread(ImageWatermark)
        self.ImageExtract = cv2.imread(ImageExtract)

        self.OriMSE, self.OriPSNR = mse(
            self.ImageOriginal, self.ImageWatermarked)
        self.WatermarkMSE, self.WatermarkPSNR = mse(
            self.ImageWatermark, self.ImageExtract)
# This line does the magic of connecting the signals created in the Glade3
# builder to our defines above. You must have one def for each signal if
# you use this line to connect the signals.
        self.builder.connect_signals(self)
        self.window = self.builder.get_object(
            "window1")  # This gets the 'window1' object
        self.window.show()  # this shows the 'window1' object
        self.builder.get_object("window1")
        self.builder.get_object("ImageOriginal").set_from_file(ImageOriginal)
        self.builder.get_object(
            "ImageWatermarked").set_from_file(ImageWatermarked)
        self.builder.get_object("ImageWatermark").set_from_file(ImageWatermark)
        self.builder.get_object("ImageExtract").set_from_file(ImageExtract)
        self.builder.get_object("EntryOriMSE").set_text(
            str(rgb2gs(self.OriMSE)))
        self.builder.get_object("EntryOriPSNR").set_text(
            str(rgb2gs(self.OriPSNR)))
        self.builder.get_object("EntryWatermarkMSE").set_text(
            str(rgb2gs(self.WatermarkMSE)))
        self.builder.get_object("EntryWatermarkPSNR").set_text(
            str(rgb2gs(self.WatermarkPSNR)))
        self.builder.get_object("BtnSave").connect(
            "clicked", self.saveWatermark)

    def saveWatermark(self, widget):
        dialog = Gtk.FileChooserDialog("Save file", self, Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        self.handle_file_dialog(dialog)

    def handle_file_dialog(self, dialog):
        response = dialog.run()
        if response == Gtk.ResponseType.OK:  # OK button was pressed or existing file was double clicked
            cansave = False
            if os.path.exists(dialog.get_filename()) == True:  # does file already exists?
                dialog2 = DialogSaveFile(self, dialog.get_filename())  # ask to confirm overwrite
                response = dialog2.run()
                if response == Gtk.ResponseType.OK:
                    cansave = True
                    dialog2.destroy()
                else:
                    dialog2.destroy()
                    # We need to re-run the file dialog to detect the buttons
                    self.handle_file_dialog(dialog)
                    return
            else:
                cansave = True
            if cansave == True:  # save new file
                open(dialog.get_filename(), "w").close
                dialog.destroy()
            else:
                pass
        else:
            dialog.destroy()

if __name__ == '__main__':
    # win = MyWindow()
    # win.connect("delete-event", Gtk.main_quit)
    # win.show_all()
    image = "/media/DATA/UDINUS/SMT 6/Advanced Image Processing/Project/index.jpeg"
    image2 = "/media/DATA/UDINUS/SMT 6/Advanced Image Processing/Project/image3.jpeg"
    wtm = WatermarkCompare(image, image2, image2, image)
    Gtk.main()
