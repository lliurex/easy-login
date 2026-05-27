from PySide6.QtCore import QObject, Signal, Slot, QThread, Property, QUrl
from PySide6.QtGui import QDesktopServices
import sys
import time
import signal
import Core

signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	infoGathered=Signal(dict)

	def __init__(self,manager):
		
		super().__init__()
		self.easyManager=manager

	#def __init__

	def run(self,*args):
		
		time.sleep(1)
		ret=self.easyManager.loadConfig()
		self.infoGathered.emit(ret)

	#def run

#class GatherInfo

class Bridge(QObject):

	currentStackChanged=Signal()
	mainCurrentOptionChanged=Signal()
	showLoadErrorMessageChanged=Signal()
	systemLocaleChanged=Signal()
	showPopUpChanged=Signal()
	closeGuiChanged=Signal()

	def __init__(self):

		super().__init__()
		self.core=Core.Core.get_core()
		self.easyManager=self.core.easyLoginManager
		self._currentStack=0
		self._mainCurrentOption=0
		self._showPopUp={"show":False,"msgCode":''}
		self.moveToStack=0
		self._closeGui=True
		self._showLoadErrorMessage={"show":False,"msgCode":''}
		self._systemLocale="es"
		self.easyManager.createN4dClient(sys.argv[1])

	#def __init__

	@Property(int,notify=currentStackChanged)
	def currentStack(self):

		return self._currentStack

	#def _getCurrentStack	

	@currentStack.setter
	def currentStack(self,currentStack):
		
		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.currentStackChanged.emit()

	#def currentStack

	@Property(int,notify=mainCurrentOptionChanged)
	def mainCurrentOption(self):

		return self._mainCurrentOption

	#def _mainCurrentOption

	@mainCurrentOption.setter
	def mainCurrentOption(self,mainCurrentOption):
		
		if self._mainCurrentOption!=mainCurrentOption:
			self._mainCurrentOption=mainCurrentOption
			self.mainCurrentOptionChanged.emit()
	
	#def mainCurrentOption

	@Property(dict,notify=showLoadErrorMessageChanged)
	def showLoadErrorMessage(self):

		return self._showLoadErrorMessage

	#def showLoadErrorMessage

	@showLoadErrorMessage.setter
	def showLoadErrorMessage(self,showLoadErrorMessage):

		if self._showLoadErrorMessage!=showLoadErrorMessage:
			self._showLoadErrorMessage=showLoadErrorMessage
			self.showLoadErrorMessageChanged.emit()

	#def showLoadErrorMessage

	@Property(dict,notify=showPopUpChanged)
	def showPopUp(self):

		return self._showPopUp

	#def _showPopUp

	@showPopUp.setter
	def showPopUp(self,showPopUp):

		if self._showPopUp!=showPopUp:
			self._showPopUp=showPopUp
			self.showPopUpChanged.emit()

	#def showPopUp
	
	@Property(bool,notify=closeGuiChanged)
	def closeGui(self):

		return self._closeGui

	#def closeGui

	@closeGui.setter	
	def closeGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui
			self.closeGuiChanged.emit()

	#def closeGui

	@Property(str,notify=systemLocaleChanged)
	def systemLocale(self):

		return self._systemLocale

	#def systemLocale

	@systemLocale.setter
	def systemLocale(self,systemLocale):

		if self._systemLocale!=systemLocale:
			self._systemLocale=systemLocale
			self.systemLocaleChanged.emit()

	#def systemLocale

	def initBridge(self):

		self.currentStack=0
		self.closeGui=False
		self.gatherInfoT=GatherInfo(self.easyManager)
		self.gatherInfoT.infoGathered.connect(self._loadConfig)
		self.gatherInfoT.finished.connect(self.gatherInfoT.deleteLater)
		self.gatherInfoT.start()
	
	#def initBridge
	@Slot(dict)
	def _loadConfig(self,ret):

		self.closeGui=True
		if ret.get("status"):
			self.core.usersOptionsStack.loadConfig()
			self._systemLocale=self.easyManager.systemLocale
			self.currentStack=1
		else:
			self.showLoadErrorMessage={"show":True,"msgCode":ret.get("code")}
	
	#def _loadConfig

	@Slot(int)
	def moveToMainOptions(self,stack):

		if self.mainCurrentOption!=stack:
			if stack==0:
				self.mainCurrentOption=stack
			else:
				self.core.usersOptionsStack.showMainMessage={"show":False,"msgCode":'',"type":''}

	#def moveToMainOptions	

	def manageGoToStack(self):

		if self.moveToStack!=0:
			self.currentStack=self.moveToStack
			self.mainCurrentOption=0
			self.moveToStack=0

	#def _manageGoToStack

	@Slot()
	def openHelp(self):
		
		if 'valencia' in self._systemLocale:
			helpUrl='https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Easy-Login.'
		else:
			helpUrl='https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Easy-Login'

		QDesktopServices.openUrl(QUrl(helpUrl))

	#def openHelp

	@Slot()
	def closeEasyLogin(self):

		if self.core.userStack.changesInUser:
			self.closeGui=False
			self.core.userStack.showChangesInUserDialog=True

	#def closeEasyLogin
	
#class Bridge




