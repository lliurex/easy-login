from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex,QUrl
from PySide6.QtGui import QDesktopServices
import os 
import sys
import threading
import time
import copy

import signal
import Core

signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	def __init__(self,manager):
		
		QThread.__init__(self)
		self.easyManager=manager
		self.ret={}

	#def __init__

	def run(self,*args):
		
		time.sleep(1)
		self.ret=self.easyManager.loadConfig()

	#def run

#class GatherInfo

class Bridge(QObject):

	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		self.easyManager=self.core.easyLoginManager
		self._currentStack=0
		self._mainCurrentOption=0
		self._closePopUp=[True,""]
		self.moveToStack=""
		self._closeGui=True
		self._showLoadErrorMessage=[False,""]
		self.easyManager.createN4dClient(sys.argv[1])

	#def __init__

	def initBridge(self):

		self.currentStack=0
		self.closeGui=False
		self.gatherInfoT=GatherInfo(self.easyManager)
		self.gatherInfoT.start()
		self.gatherInfoT.finished.connect(self._loadConfig)
	
	#def initBridge
	
	def _loadConfig(self):

		self.closeGui=True
		if self.gatherInfoT.ret.get("status"):
			self.core.usersOptionsStack.loadConfig()
			self._systemLocale=self.easyManager.systemLocale
			self.currentStack=1
		else:
			self.showLoadErrorMessage=[True,self.gatherInfoT.ret.get("code")]
	
	#def _loadConfig

	def _getSystemLocale(self):

		return self._systemLocale

	#def _getSystemLocale

	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack	

	def _setCurrentStack(self,currentStack):
		
		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.on_currentStack.emit()

	#def _setCurentStack

	def _getMainCurrentOption(self):

		return self._mainCurrentOption

	#def _getMainCurrentOption	

	def _setMainCurrentOption(self,mainCurrentOption):
		
		if self._mainCurrentOption!=mainCurrentOption:
			self._mainCurrentOption=mainCurrentOption
			self.on_mainCurrentOption.emit()

	#def _setMainCurrentOption

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp

	def _setClosePopUp(self,closePopUp):

		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp
			self.on_closePopUp.emit()

	#def _setClosePopUp

	def _getShowLoadErrorMessage(self):

		return self._showLoadErrorMessage

	#def _getShowLoadErrorMessage

	def _setShowLoadErrorMessage(self,showLoadErrorMessage):

		if self._showLoadErrorMessage!=showLoadErrorMessage:
			self._showLoadErrorMessage=showLoadErrorMessage
			self.on_showLoadErrorMessage.emit()

	#def _setShowLoadErrorMessage

	def _getCloseGui(self):

		return self._closeGui

	#def _getCloseGui	

	def _setCloseGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui
			self.on_closeGui.emit()

	#def _setCloseGui

	@Slot(int)
	def moveToMainOptions(self,stack):

		if self.mainCurrentOption!=stack:
			if stack==0:
				self.mainCurrentOption=stack
			else:
				self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]

	#def moveToMainOptions	

	def manageGoToStack(self):

		if self.moveToStack!="":
			self.currentStack=self.moveToStack
			self.mainCurrentOption=0
			self.moveToStack=""

	#def _manageGoToStack

	@Slot()
	def openHelp(self):
		
		if 'valencia' in self._systemLocale:
			helpUrl='https://wiki.edu.gva.es/lliurex/'
		else:
			helpUrl='https://wiki.edu.gva.es/lliurex/'

		QDesktopServices.openUrl(QUrl(helpUrl))

	#def openHelp

	@Slot()
	def closeEasyLogin(self):

		if self.core.userStack.changesInUser:
			self.closeGui=False
			self.core.userStack.showChangesInUserDialog=True

	#def closeEasyLogin
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_mainCurrentOption=Signal()
	mainCurrentOption=Property(int,_getMainCurrentOption,_setMainCurrentOption, notify=on_mainCurrentOption)

	on_showLoadErrorMessage=Signal()
	showLoadErrorMessage=Property('QVariantList',_getShowLoadErrorMessage,_setShowLoadErrorMessage, notify=on_showLoadErrorMessage)

	on_closePopUp=Signal()
	closePopUp=Property('QVariantList',_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	systemLocale=Property(str,_getSystemLocale,constant=True)

#class Bridge




