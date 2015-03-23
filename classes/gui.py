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
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)

		self.twieTwiets = twieTwiets
		self.currentIndex = -1

		self.header = self.tableWidget.horizontalHeader()
		self.header.setResizeMode(QtGui.QHeaderView.Stretch)
		self.header.setBackgroundRole(QtGui.QPalette.NoRole)

		#user image
		self.url = "http://eaassets-a.akamaihd.net/battlelog/prod/emblem/219/323/256/2955058837069862971.png"
		pixmap = self.getUserImage(self.url)

		#user image2
		self.url2 = "http://eaassets-a.akamaihd.net/battlelog/prod/emblem/219/323/256/2955058837069862971.png"    
		pixmap2 = self.getUserImage(self.url2)

		#tweet1
		self.profile_picture = QtGui.QTableWidgetItem()
		self.profile_picture.setBackground(QtGui.QBrush(pixmap))
		self.tweet = ClickableLabel(self.showDetails, self.styleTweet(" "))
		self.tweet.setTextFormat(QtCore.Qt.RichText)
		self.tweet.setFont(QtGui.QFont("arial", 14))
		self.tweet.setAlignment(QtCore.Qt.AlignCenter)
		self.name = QtGui.QTableWidgetItem(" ")
		self.name.setTextColor(QtGui.QColor(51,204,255))
		self.name.setTextAlignment(QtCore.Qt.AlignCenter)
		self.time = QtGui.QTableWidgetItem(" ")
		self.time.setTextAlignment(QtCore.Qt.AlignCenter)

		#tweet2
		self.profile_picture2 = QtGui.QTableWidgetItem()
		self.profile_picture2.setBackground(QtGui.QBrush(pixmap2))
		self.tweet2 = ClickableLabel(self.showDetails, " ")
		self.tweet2.setTextFormat(QtCore.Qt.RichText)
		self.tweet2.setFont(QtGui.QFont("arial", 14))
		self.tweet2.setAlignment(QtCore.Qt.AlignCenter)
		self.name2 = QtGui.QTableWidgetItem(" ")
		self.name2.setTextColor(QtGui.QColor(51,204,255))
		self.name2.setTextAlignment(QtCore.Qt.AlignCenter)
		self.time2 = QtGui.QTableWidgetItem(" ")
		self.time2.setTextAlignment(QtCore.Qt.AlignCenter)

		self.tableWidget.setCellWidget(0,0,self.tweet)
		self.tableWidget.setCellWidget(1,0,self.tweet2)

		self.pushButton.clicked.connect(self.updateUI)
		self.clickable = True

		self.updateUI()

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
				words[i] = '<span style="color:#33ccff;">{}</span>'.format(words[i])
			elif words[i][0:4] == "http":
				words[i] = '<span style="color:#89dee3; text-decoration: underline;">{}</span>'.format(words[i])
		styledString = " ".join(words)


		return styledString


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	gui = Gui(None)
	gui.show()
	app.exec_()
