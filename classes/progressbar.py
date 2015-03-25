from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
import sys

class myProgressBar(QtGui.QProgressBar):
	value = 0  

	@pyqtSlot()
	def increaseValue(self):
		self.setValue(self.value)
		self.value = self.value+1

def main():    
	app 	 = QtGui.QApplication(sys.argv)
	progressBar	 = myProgressBar()

	progressBar.resize(250,50)    
	progressBar.setWindowTitle('Loading Twitter Data... ')
	progressBar.setWindowTitle('initializing Database... ')
	progressBar.setWindowTitle('Loading rhyme database... ')
	progressBar.setWindowTitle('Matching tweets... ')
	
	
	timer = QtCore.QTimer()
	progressBar.connect(timer,SIGNAL("timeout()"),progressBar,SLOT("increaseValue()"))
	seconds = 10
	timer.start(seconds * 10)

	progressBar.show()
		
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
