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
        self.set_default_size(400, 200)

        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box1)
        self.loadimg = Gtk.Image.new_from_file('')
        self.loadimg.set_pixel_size(200)
        box1.pack_start(self.loadimg, 1, 1, 10)
        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box1.pack_start(box2, 1, 1, 10)
        self.imgbuffer = Gtk.TextBuffer()
        self.img = Gtk.TextView()
        self.img.set_buffer(self.imgbuffer)
        self.imgbuffer.set_text("")
        self.img.set_can_focus(0)
        box2.pack_start(self.img, 1, 1, 10)

        filechooser = Gtk.Button(label="...")
        filechooser.connect("clicked", self.on_image_clicked)
        box2.pack_start(filechooser, 0, 0, 5)
        self.progress_bar = Gtk.ProgressBar()
        box1.pack_start(self.progress_bar, 1, 1, 0)
        bttndwt = Gtk.Button(label="Analisa")
        bttndwt.connect("clicked", self.on_bttndwt_clicked)
        box1.pack_start(bttndwt, 1, 1, 0)

    def on_bttndwt_clicked(self, widget):
        image = cv2.imread(self.imgbuffer.get_text(
            self.imgbuffer.get_iter_at_line(0), self.imgbuffer.get_iter_at_offset(-1), 0))
        height, width = image.shape[:2]
        image2, imArray2 = waveleteTransform(image, width, height)
        self.progress_bar.set_fraction(0.284760845)
        while Gtk.events_pending():
            Gtk.main_iteration()
        image3, imArray3 = inverseWaveleteTransform(imArray2, width, height)
        self.progress_bar.set_fraction(0.56952169)
        while Gtk.events_pending():
            Gtk.main_iteration()
        cv2.imwrite('/tmp/awal.jpeg', image)
        cv2.imwrite('/tmp/prosesdwt.jpeg', image2)
        cv2.imwrite('/tmp/resultdwt.jpeg', image3)
        show = Gtk.Window()
        headerBar = Gtk.HeaderBar()
        headerBar.set_show_close_button(True)
        show.set_border_width(10)
        show.set_default_size(400, 200)
        vboxP = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.add(vboxP)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vboxP.pack_start(hbox, 1, 1, 10)
        loadawal = Gtk.Image.new_from_file('/tmp/awal.jpeg')
        hbox.pack_start(loadawal, 1, 1, 5)
        loadproses = Gtk.Image.new_from_file('/tmp/prosesdwt.jpeg')
        hbox.pack_start(loadproses, 1, 1, 5)
        loadresult = Gtk.Image.new_from_file('/tmp/resultdwt.jpeg')
        hbox.pack_start(loadresult, 1, 1, 5)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vboxP.pack_start(vbox, 1, 1, 0)
        hboxheader = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hboxheader, 1, 1, 0)

        # GLCM CITRA AWAL
        glcmaw = GLCM(image, height, width, 0, 1)
        self.progress_bar.set_fraction(0.711902113)
        while Gtk.events_pending():
            Gtk.main_iteration()
        kontrasaw, meanIaw, meanJaw, energyaw, homogenityaw = contrast(glcmaw)
        self.progress_bar.set_fraction(0.712458287)
        while Gtk.events_pending():
            Gtk.main_iteration()
        taoIaw, taoJaw = tao(glcmaw, meanIaw, meanJaw)
        self.progress_bar.set_fraction(0.713014461)
        while Gtk.events_pending():
            Gtk.main_iteration()
        korelasionaw = correlation(glcmaw, meanIaw, meanJaw, taoIaw, taoJaw)
        self.progress_bar.set_fraction(0.713570635)
        while Gtk.events_pending():
            Gtk.main_iteration()

        gskontrasaw = rgb2gs(kontrasaw)
        gsenergyaw = rgb2gs(energyaw)
        gshomogenityaw = rgb2gs(homogenityaw)
        gskorelasiaw = rgb2gs(korelasionaw)
        # GLCM CITRA DWT
        glcm = GLCM(image3, height, width, 0, 1)
        self.progress_bar.set_fraction(0.855951058)
        while Gtk.events_pending():
            Gtk.main_iteration()
        kontras, meanI, meanJ, energy, homogenity = contrast(glcm)
        self.progress_bar.set_fraction(0.856507232)
        while Gtk.events_pending():
            Gtk.main_iteration()
        taoI, taoJ = tao(glcm, meanI, meanJ)
        self.progress_bar.set_fraction(0.857063406)
        while Gtk.events_pending():
            Gtk.main_iteration()
        korelasion = correlation(glcm, meanI, meanJ, taoI, taoJ)
        self.progress_bar.set_fraction(0.85761958)
        while Gtk.events_pending():
            Gtk.main_iteration()
        gskontras = rgb2gs(kontras)
        gsenergy = rgb2gs(energy)
        gshomogenity = rgb2gs(homogenity)
        gskorelasi = rgb2gs(korelasion)

        # PSNR

        imagePSNR1 = cv2.imread("/tmp/awal.jpeg")
        imagePSNR2 = cv2.imread("/tmp/resultdwt.jpeg")
        MSE, PSNR = mse(imagePSNR1, imagePSNR2)

        gsmse = psnrrgb2gs(MSE)
        gspsnr = psnrrgb2gs(PSNR)

        labelkosong = Gtk.Label(" ")
        hboxheader.pack_start(labelkosong, 1, 1, 10)
        labeldwt = Gtk.Label("DWT")
        hboxheader.pack_end(labeldwt, 1, 1, 0)
        labelawal = Gtk.Label("Awal")
        hboxheader.pack_end(labelawal, 1, 1, 0)

        hboxhomo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hboxhomo, 1, 1, 10)

        labelhomo = Gtk.Label("Homogenitas")
        hboxhomo.pack_start(labelhomo, 1, 1, 0)

        bufferhomodwt = Gtk.TextBuffer()
        viewhomodwt = Gtk.TextView()
        viewhomodwt.set_buffer(bufferhomodwt)
        bufferhomodwt.set_text("" + str(gshomogenity))
        viewhomodwt.set_can_focus(0)
        hboxhomo.pack_end(viewhomodwt, 1, 1, 0)

        bufferhomoaw = Gtk.TextBuffer()
        viewhomoaw = Gtk.TextView()
        viewhomoaw.set_buffer(bufferhomoaw)
        bufferhomoaw.set_text("" + str(gshomogenityaw))
        viewhomoaw.set_can_focus(0)
        hboxhomo.pack_end(viewhomoaw, 1, 1, 0)

        hboxkontras = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hboxkontras, 1, 1, 10)

        labelkontras = Gtk.Label("Kontras")
        hboxkontras.pack_start(labelkontras, 1, 1, 12)

        bufferkontrasdwt = Gtk.TextBuffer()
        viewkontrasdwt = Gtk.TextView()
        viewkontrasdwt.set_buffer(bufferkontrasdwt)
        bufferkontrasdwt.set_text("" + str(gskontras))
        viewkontrasdwt.set_can_focus(0)
        hboxkontras.pack_end(viewkontrasdwt, 1, 1, 0)

        bufferkontrasaw = Gtk.TextBuffer()
        viewkontrasaw = Gtk.TextView()
        viewkontrasaw.set_buffer(bufferkontrasaw)
        bufferkontrasaw.set_text("" + str(gskontrasaw))
        viewkontrasaw.set_can_focus(0)
        hboxkontras.pack_end(viewkontrasaw, 1, 1, 0)

        hboxenergy = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hboxenergy, 1, 1, 10)

        labelenergy = Gtk.Label("Energy")
        hboxenergy.pack_start(labelenergy, 1, 1, 16)

        bufferenergydwt = Gtk.TextBuffer()
        viewenergydwt = Gtk.TextView()
        viewenergydwt.set_buffer(bufferenergydwt)
        bufferenergydwt.set_text("" + str(gsenergy))
        viewenergydwt.set_can_focus(0)
        hboxenergy.pack_end(viewenergydwt, 1, 1, 0)

        bufferenergyaw = Gtk.TextBuffer()
        viewenergyaw = Gtk.TextView()
        viewenergyaw.set_buffer(bufferenergyaw)
        bufferenergyaw.set_text("" + str(gsenergyaw))
        viewenergyaw.set_can_focus(0)
        hboxenergy.pack_end(viewenergyaw, 1, 1, 0)

        hboxkorelasi = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hboxkorelasi, 1, 1, 10)

        labelkorelasi = Gtk.Label("Korelasi")
        hboxkorelasi.pack_start(labelkorelasi, 1, 1, 12)

        bufferkorelasidwt = Gtk.TextBuffer()
        viewkorelasidwt = Gtk.TextView()
        viewkorelasidwt.set_buffer(bufferkorelasidwt)
        bufferkorelasidwt.set_text("" + str(gskorelasi))
        viewkorelasidwt.set_can_focus(0)
        hboxkorelasi.pack_end(viewkorelasidwt, 1, 1, 0)

        bufferkorelasiaw = Gtk.TextBuffer()
        viewkorelasiaw = Gtk.TextView()
        viewkorelasiaw.set_buffer(bufferkorelasiaw)
        bufferkorelasiaw.set_text("" + str(gskorelasiaw))
        viewkorelasiaw.set_can_focus(0)
        hboxkorelasi.pack_end(viewkorelasiaw, 1, 1, 0)

        hboxmse = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hboxmse, 1, 1, 10)

        labelmse = Gtk.Label("MSE")
        hboxmse.pack_start(labelmse, 0, 0, 60)

        buffermsedwt = Gtk.TextBuffer()
        viewmsedwt = Gtk.TextView()
        viewmsedwt.set_buffer(buffermsedwt)
        buffermsedwt.set_text("" + str(gsmse))
        viewmsedwt.set_can_focus(0)
        hboxmse.pack_end(viewmsedwt, 1, 1, 0)

        hboxpsnr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hboxpsnr, 1, 1, 10)

        labelpsnr = Gtk.Label("PSNR")
        hboxpsnr.pack_start(labelpsnr, 0, 0, 60)

        bufferpsnrdwt = Gtk.TextBuffer()
        viewpsnrdwt = Gtk.TextView()
        viewpsnrdwt.set_buffer(bufferpsnrdwt)
        bufferpsnrdwt.set_text("" + str(gspsnr))
        viewpsnrdwt.set_can_focus(0)
        hboxpsnr.pack_end(viewpsnrdwt, 1, 1, 0)

        self.progress_bar.set_fraction(1)
        while Gtk.events_pending():
            Gtk.main_iteration()
        show.add(vboxP)
        show.connect("delete-event", Gtk.main_quit)
        show.show_all()
        self.progress_bar.set_fraction(0)

    def on_image_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Pilih Gambar ", self, Gtk.FileChooserAction.OPEN, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.imgbuffer.set_text(dialog.get_filename())
            self.loadimg.set_from_file(dialog.get_filename())
            self.resize(400, 200)
            print("File Selected", dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
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


if __name__ == '__main__':
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
