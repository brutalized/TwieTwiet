import sys
import urllib.request
from PyQt4 import QtGui, QtCore, uic
from images_rc import *


# Load the UI
form_class = uic.loadUiType("classes/TwieTwiet.ui")[0]

class ClickableLabel(QtGui.QLabel):
	def __init__(self, clickFunction=None, *args):
		super().__init__(*args)
		self.clickFunction = clickFunction

	def mouseReleaseEvent(self, event):
		if self.clickFunction:
			self.clickFunction()


class Gui(QtGui.QMainWindow, form_class):
	"""  """
	
	def __init__(self, twieTwiets, parent=None):
		""" initializing widgets """
		QtGui.QMainWindow.__init__(self, parent)
		self.setStyle(QtGui.QStyleFactory.create('Cleanlooks')) # widget bugfix 
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)

		self.twieTwiets = twieTwiets
		self.currentIndex = -1

		self.header = self.tableWidget.horizontalHeader()
		self.header.setResizeMode(QtGui.QHeaderView.Stretch)
		self.header.setBackgroundRole(QtGui.QPalette.NoRole)

		#user image
		url = "https://pbs.twimg.com/profile_images/578876386607173633/x9KS4jzR_normal.jpeg"
		pixmap = self.getUserImage(url)

		#user image2
		url2 = "https://pbs.twimg.com/profile_images/578876386607173633/x9KS4jzR_normal.jpeg"    
		pixmap2 = self.getUserImage(url2)

		#tweet1
		self.profile_picture = QtGui.QTableWidgetItem()
		self.profile_picture.setBackground(QtGui.QBrush(pixmap))
		self.tweet = ClickableLabel(self.showDetails, self.styleTweet("Welcome to TwieTwiet Bot! Hit the generate button to generate a TwieTwiet!"))
		self.tweet.setTextFormat(QtCore.Qt.RichText)
		self.tweet.setFont(QtGui.QFont("arial", 14))
		self.tweet.setAlignment(QtCore.Qt.AlignCenter)
		self.tweet.setWordWrap(True)
		self.name = QtGui.QTableWidgetItem("@TwieTwietNL")
		self.name.setTextColor(QtGui.QColor(51,204,255))
		self.name.setTextAlignment(QtCore.Qt.AlignCenter)
		self.time = QtGui.QTableWidgetItem("11:44")
		self.time.setTextAlignment(QtCore.Qt.AlignCenter)

		#tweet2
		self.profile_picture2 = QtGui.QTableWidgetItem()
		self.profile_picture2.setBackground(QtGui.QBrush(pixmap2))
		self.tweet2 = ClickableLabel(self.showDetails, self.styleTweet("Click on a TwieTwiet for additional information!"))
		self.tweet2.setTextFormat(QtCore.Qt.RichText)
		self.tweet2.setFont(QtGui.QFont("arial", 14))
		self.tweet2.setAlignment(QtCore.Qt.AlignCenter)
		self.tweet2.setWordWrap(True)
		self.name2 = QtGui.QTableWidgetItem("@TwieTwietNL")
		self.name2.setTextColor(QtGui.QColor(51,204,255))
		self.name2.setTextAlignment(QtCore.Qt.AlignCenter)
		self.time2 = QtGui.QTableWidgetItem("12:00")
		self.time2.setTextAlignment(QtCore.Qt.AlignCenter)

		self.tableWidget.setCellWidget(0,0,self.tweet)
		self.tableWidget.setCellWidget(1,0,self.tweet2)

		# Columns for extra information about a TwieTwiet
		self.tableWidget.insertColumn(1)
		self.tableWidget.insertColumn(0)
		self.tableWidget.insertColumn(0)
		self.tableWidget.hideColumn(0)
		self.tableWidget.hideColumn(1)
		self.tableWidget.hideColumn(3)
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

		self.pushButton.clicked.connect(self.updateUI)
		self.toggle = True

	def showDetails(self):
		""" show extra tweet information """
		if self.toggle:
			self.toggle = False
			self.tableWidget.showColumn(0)
			self.tableWidget.showColumn(1)
			self.tableWidget.showColumn(3)
		else:
			self.tableWidget.hideColumn(0)
			self.tableWidget.hideColumn(1)
			self.tableWidget.hideColumn(3)
			self.toggle = True

	def getUserImage(self, url):
		data = urllib.request.urlopen(url).read()
		pixmap = QtGui.QPixmap()
		pixmap.loadFromData(data)
		return pixmap

	def updateUI(self):
		""" Update tweet data """
		self.currentIndex = (self.currentIndex + 1) % len(self.twieTwiets)
		tweet, tweet2 = self.twieTwiets[self.currentIndex]

		pixmap = self.getUserImage(tweet.userImage)
		self.profile_picture.setBackground(QtGui.QBrush(pixmap))
		pixmap2 = self.getUserImage(tweet2.userImage)
		self.profile_picture2.setBackground(QtGui.QBrush(pixmap2))

		self.name.setText(tweet.userName)
		self.name2.setText(tweet2.userName)

		self.tweet.setText(self.styleTweet(tweet.message))
		self.tweet2.setText(self.styleTweet(tweet2.message))

		self.time.setText(tweet.date)
		self.time2.setText(tweet2.date)

	def styleTweet(self, message):
		words = message.split()	
		for i in range(len(words)):
			if words[i][0] == "#":
				words[i] = '<b style="font-size: 14px;">{}</b>'.format(words[i])
			elif words[i][0] == "@":
				words[i] = '<span style="color:#33ccff; font-size: 12px;">{}</span>'.format(words[i])
			elif words[i][0:4] == "http":
				words[i] = '<span style="color:#89dee3; text-decoration: underline;">{}</span>'.format(words[i])
		styledString = " ".join(words)

		return styledString


class ProgressBar(QtGui.QProgressBar):
	def __init__(self):
		super().__init__()
		self.resize(300, 50)

	def update(self, title, value):
		self.setWindowTitle(title)
		self.setValue(value)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	gui = Gui(None)
	gui.show()
	app.exec_()
