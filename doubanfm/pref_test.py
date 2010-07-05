import gtk
import gtk.glade

class Win:
	def __init__(self):
		self.glade = "doubanfm_mode.ui"
		self.builder = gtk.Builder()
		self.builder.add_from_file(self.glade)

		self.window = self.builder.get_object('window1')
		self.window.show()

		

if __name__ == '__main__':
	w = Win()
	gtk.main()
