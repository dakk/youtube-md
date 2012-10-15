#!/usr/bin/env python2

# YoutubeMusicDownload
# Copyright (C) 2012,  Davide Gessa
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pygtk
pygtk.require('2.0')
import gtk
import httplib
import urlparse
from threading import Thread
import os

gtk.gdk.threads_init()

license = """
YoutubeMusicDownload
Copyright (C) 2012,  Davide Gessa

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


def getServerStatusCode(url):
	host, path = urlparse.urlparse(url)[1:3]
	
	try:
		conn = httplib.HTTPConnection(host)
		conn.request('HEAD', path)
		return conn.getresponse().status
	except StandardError:
		return None
		

def checkUrl(url):
	codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
	return getServerStatusCode(url) in codes
	
    

class YoutubeMusicDownlaod:
	queue = []
	youtube_dl = "youtube-dl"
	folderUri = "~/"
	icon = gtk.Image().set_from_stock(gtk.STOCK_GO_DOWN, 16)
	thread = None
	
	
	def __init__(self):
		pass
		
		
	def checkExternalProgram(self):
		pass
		
		
	def destroy(self, widget, data = None):
		gtk.main_quit()
	
	
	def addUrlDialog(self, widget):
		d = gtk.Dialog()

		d.add_button("Cancel", 0)
		d.add_button("Add", 1)
		content_area = d.get_content_area()
		entry = gtk.Entry();
		entry.set_text("http://")

		content_area.add(gtk.Label("Url"))
		content_area.add(entry);

		d.show_all()

		if d.run() == 1:
			value = entry.get_text();
		else:
			value = None
			
		d.destroy()
		return value
		
		
	def addUrlEvent(self, window):
		value = self.addUrlDialog(window)
		
		if checkUrl(value):
			self.urlList.append(["Queued", value])
			self.queue.append(value)
			
		else:
			d = gtk.MessageDialog(None, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_CLOSE, message_format="Invalid url")
			d.set_title("Warning")
			d.run()
			d.destroy()
		
	
	def removeUrlEvent(self, window):
		pass
		
		
	def aboutEvent(self, widget):
		d = gtk.AboutDialog()
		d.set_authors(["Davide Gessa"])
		d.set_license(license)
		d.set_wrap_license(True)
		d.set_name("YoutubeMD")
		d.set_logo(self.icon)
		d.run()
		d.destroy()
		
	
	def downloadThread(self):
		if len(self.queue) == 0:
			return 
			
		self.down_button.set_visible(False)
		step = 1.0 / len(self.queue)
		progress = 0.0
		
		for link in self.queue:				
			self.progressBar.set_text("Downloading "+link)
			os.system(self.youtube_dl+" "+link+" --extract-audio --audio-format mp3 -t"])
			progress += step
			self.progressBar.set_fraction(progress)
				
			time.sleep(2)
			
		self.progressBar.set_text("Completed")
		self.down_button.set_visible(True)
		
		
	def downloadEvent(self, window):
		if self.thread == None:
			self.thread = Thread(target=self.downloadThread)
			
		self.thread.start()
		
	
	def chooseFolderEvent(self, window):
		d = gtk.FileChooserDialog(	title = "Select a directory to save downloaded music", 
									action = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
									buttons = (("Select", 1)))
		if d.run() == 1:
			self.folderUri = d.get_uri().replace("file://", "")
			self.folder.set_text(self.folderUri)
			d.destroy()
			
	  
	def main(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.window.set_title("YoutubeMD")
		self.window.set_default_size(400, 500)
		self.window.set_icon(self.icon)
		
		vbox = gtk.VBox()
		self.window.add(vbox)
		
		
		# Button toolbar
		toolbar = gtk.Toolbar()

		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_ADD, 16)
		add_button = toolbar.append_item("Add", "Add another url", "Private", iconw, self.addUrlEvent)
   
   		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_REMOVE, 16)
		remove_button = toolbar.append_item("Remove", "Remove selected url", "Private", iconw, self.removeUrlEvent)
		
   		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_GO_DOWN, 16)
		self.down_button = toolbar.append_item("Download", "Start the download", "Private", iconw, self.downloadEvent)
		
   		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_ABOUT, 16)
		about_button = toolbar.append_item("About", "About this app", "Private", iconw, self.aboutEvent)
		
		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_QUIT, 16)
		close_button = toolbar.append_item("Quit", "Closes this app", "Private", iconw, self.destroy)


		vbox.pack_start(toolbar, False, False, 0)
		
		# Destination folder
		hbox = gtk.HBox()
		self.folder = gtk.Entry()
		self.folder.set_text(self.folderUri)
		button = gtk.Button("Choose folder")
		button.connect_object("clicked", self.chooseFolderEvent, self.window)
		
		hbox.pack_start(self.folder, True, True, 0)
		hbox.pack_start(button, False, False, 0)
		vbox.pack_start(hbox, False, False, 0)
		
		
		# ListView with links
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw, True, True, 0)
		
		self.urlList = gtk.ListStore(str, str)

		self.urlListView = gtk.TreeView(self.urlList)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("State", rendererText, text=0)
		column.set_sort_column_id(0)    
		self.urlListView.append_column(column)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Url", rendererText, text=1)
		column.set_sort_column_id(1)
		self.urlListView.append_column(column)
  
		sw.add(self.urlListView)
		
		
		
		# Progress bar
		self.progressBar = gtk.ProgressBar()
		vbox.pack_start(self.progressBar, False, False, 0)
		
				
		
		self.window.show_all()
		gtk.main()
	
		
if __name__ == "__main__":
	ymd = YoutubeMusicDownlaod()
	ymd.main()
