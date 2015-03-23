import sys
import urllib.request
from PyQt4 import QtGui, QtCore, uic
from images_rc import *


# Load the UI
form_class = uic.loadUiType("TwieTwiet.ui")[0]

class Gui(QtGui.QMainWindow, form_class):

	def __init__(self, parent=None):
		""" initializing widgets """
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.showMaximized()

		self.header = self.tableWidget.horizontalHeader()
		self.header.setResizeMode(QtGui.QHeaderView.Stretch)
		self.header.setBackgroundRole(QtGui.QPalette.NoRole)
		
		self.url = 'http://th00.deviantart.net/fs71/PRE/f/2011/285/c/2/lol_face_by_rober_raik-d4cm1yl.png'    
		data = urllib.request.urlopen(self.url).read()
		pixmap = QtGui.QPixmap()
		pixmap.loadFromData(data)

		self.url2 = 'http://th00.deviantart.net/fs71/PRE/f/2011/285/c/2/lol_face_by_rober_raik-d4cm1yl.png'    
		data = urllib.request.urlopen(self.url2).read()
		pixmap2 = QtGui.QPixmap()
		pixmap2.loadFromData(data)

		#tweet1
		self.profile_picture = QtGui.QTableWidgetItem()
		self.profile_picture.setBackground(QtGui.QBrush(pixmap))
		self.tweet = QtGui.QTableWidgetItem("lol")
		self.name = QtGui.QTableWidgetItem("lol")
		self.time = QtGui.QTableWidgetItem("lol")

		#tweet2
		self.profile_picture2 = QtGui.QTableWidgetItem()
		self.profile_picture2.setBackground(QtGui.QBrush(pixmap2))
		self.tweet2 = QtGui.QTableWidgetItem("lol")
		self.name2 = QtGui.QTableWidgetItem("lol")
		self.time2 = QtGui.QTableWidgetItem("lol")


		self.tweet.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
		self.tweet2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
		self.tweet.setFlags(QtCore.Qt.NoItemFlags)
		self.tweet2.setFlags(QtCore.Qt.NoItemFlags)
		self.tweet.setTextAlignment(QtCore.Qt.AlignCenter)
		self.tweet2.setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.setItem(0,0,self.tweet)
		self.tableWidget.setItem(1,0,self.tweet2)

		self.pushButton.clicked.connect(self.update)
		self.tableWidget.cellClicked.connect(self.showDetails)
		self.clickable = True

	def showDetails(self):
		""" show extra tweet information """
		if self.clickable == True:
			self.tableWidget.insertColumn(1)
			self.tableWidget.insertColumn(0)
			self.tableWidget.insertColumn(0)
			self.tableWidget.setItem(0,0,self.profile_picture)
			self.header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
			self.tableWidget.setItem(0,1,self.name)
			self.header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
			self.tableWidget.setItem(0,3,self.time)
			self.header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
			self.tableWidget.setItem(1,0,self.profile_picture2)
			self.tableWidget.setItem(1,1,self.name2)
			self.tableWidget.setItem(1,3,self.time2)

			self.profile_picture.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.profile_picture.setFlags(QtCore.Qt.NoItemFlags)
			self.name.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.name.setFlags(QtCore.Qt.NoItemFlags)
			self.time.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.time.setFlags(QtCore.Qt.NoItemFlags)

			self.profile_picture2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.profile_picture2.setFlags(QtCore.Qt.NoItemFlags)
			self.name2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.name2.setFlags(QtCore.Qt.NoItemFlags)
			self.time2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.time2.setFlags(QtCore.Qt.NoItemFlags)
			self.clickable = False

	def update(self, tweet, tweet2):
		""" Update tweet data """ 
		self.profile_picture.setText(tweet.userImage)
		self.profile_picture2.setText(tweet2.userImage)

		self.name.setText(tweet.userName)
		self.name2.setText(tweet2.userName)

		self.tweet.setText(tweet.message)
		self.tweet2.setText(tweet2.message)

		self.time.setText(tweet.date)
		self.time2.setText(tweet2.date)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	gui = Gui(None)
	gui.show()
	app.exec_()
