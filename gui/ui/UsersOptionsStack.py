from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import UsersModel

CHANGE_SERVICE_WAITING=20
REMOVING_USER=21
REMOVING_ALL_USERS=22
GENERATING_PDF_WAITING=23

class EnableLogin(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.enableLogin=args[0]
		self.ret={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.enableEasyLogin(self.enableLogin)

	#def run

#class EnableLogin

class RemoveUser(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.allUsers=args[0]
		self.userToRemove=args[1]
		self.ret={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.removeUser(self.allUsers,self.userToRemove)

	#def run

#class RemoveUser

class GeneratePdf(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.pdfPath=args[0]
		self.ret={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.generatePdf(self.pdfPath)

	#def run

#class GeneratePdf

class Bridge(QObject):

	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.easyLoginManager=self.core.easyLoginManager
		self._usersModel=UsersModel.UsersModel()
		self._easyLoginEnabled=False
		self._showMainMessage=[False,"","Ok"]
		self._showRemoveUserDialog=[False,False]
		self._enableGlobalOptions=False

	#def _init__
	
	def loadConfig(self):

		self.easyLoginEnabled=Bridge.easyLoginManager.easyLoginEnabled
		self._updateUsersModel()
		self._manageOptions()
	
	#def loadConfig

	def _getEasyLoginEnabled(self):

		return self._easyLoginEnabled

	#def _getEasyLoginEnabled

	def _setEasyLoginEnabled(self,easyLoginEnabled):

		if self._easyLoginEnabled!=easyLoginEnabled:
			self._easyLoginEnabled=easyLoginEnabled
			self.on_easyLoginEnabled.emit()

	#def _setEasyLoginEnabled

	def _manageOptions(self):

		self.enableGlobalOptions=Bridge.easyLoginManager.checkGlobalOptionStatus()

	#def _manageOptions

	def _getShowRemoveUserDialog(self):

		return self._showRemoveUserDialog

	#def _getShowRemoveUserDialog

	def _setShowRemoveUserDialog(self,showRemoveUserDialog):

		if self._showRemoveUserDialog!=showRemoveUserDialog:
			self._showRemoveUserDialog=showRemoveUserDialog
			self.on_showRemoveUserDialog.emit()

	#def _setShowRemoveUserDialog

	def _getUsersModel(self):

		return self._usersModel

	#def _getUsersModel

	def _getShowMainMessage(self):

		return self._showMainMessage

	#def _getShowMainMessage

	def _setShowMainMessage(self,showMainMessage):

		if self._showMainMessage!=showMainMessage:
			self._showMainMessage=showMainMessage
			self.on_showMainMessage.emit()

	#def _setShowMainMessage

	def _getEnableGlobalOptions(self):

		return self._enableGlobalOptions

	#def _getEnableGlobalOptions

	def _setEnableGlobalOptions(self,enableGlobalOptions):

		if self._enableGlobalOptions!=enableGlobalOptions:
			self._enableGlobalOptions=enableGlobalOptions
			self.on_enableGlobalOptions.emit()

	#def _setEnableGlobalOptions

	def _updateUsersModel(self):

		ret=self._usersModel.clear()
		userEntries=Bridge.easyLoginManager.usersConfigData
		for item in userEntries:
			if item["username"]!="":
				self._usersModel.appendRow(item["username"],item["login"],item["name"],item["surname"],item["pwdImg1"],item["pwdImg2"],item["pwdImg3"],item["pwdImg4"],item["metaInfo"])
	
	#def _updateUsersModel

	@Slot(bool)
	def enableEasyLogin(self,value):

		self.core.mainStack.closePopUp=[False,CHANGE_SERVICE_WAITING]
		self.core.mainStack.closeGui=False
		self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]
		self.enableLoginT=EnableLogin(value)
		self.enableLoginT.start()
		self.enableLoginT.finished.connect(self._enableLoginRet)

	#def enableEasyLogin

	def _enableLoginRet(self):

		self.easyLoginEnabled=Bridge.easyLoginManager.easyLoginEnabled

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=False
		self.showMainMessage=[True,self.enableLoginT.ret.get("code"),self.enableLoginT.ret.get("type")]

	#def _enableLoginRet

	@Slot('QVariantList')
	def removeUser(self,data):

		self.showMainMessage=[False,"","Ok"]
		self.removeAllUsers=data[0]
		
		if self.removeAllUsers:
			self.userToRemove=None
		else:
			self.userToRemove=data[1]

		self.showRemoveUserDialog=[True,self.removeAllUsers]

	#def removeUser

	@Slot(str)
	def generateList(self,exportPath):

		self.core.mainStack.closePopUp=[False,GENERATING_PDF_WAITING]
		self.core.mainStack.closeGui=False
		self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]
		self.generatePdfT=GeneratePdf(exportPath)
		self.generatePdfT.start()
		self.generatePdfT.finished.connect(self._generatePdfRet)

	#def generateList

	def _generatePdfRet(self):

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

		if not self.generatePdfT.ret.get("status"):
			self.showMainMessage=[True,self.generatePdfT.ret.get("code"),self.generatePdfT.ret.get("type")]
	
	#def _generatePdfRet

	@Slot(str)
	def manageRemoveUserDialog(self,response):

		self.showRemoveUserDialog=[False,False]
		if response=="Accept":
			self._launchRemoveUserProcess()

	#def manageRemoveBellDialog

	def _launchRemoveUserProcess(self):

		self.core.mainStack.closeGui=False
		if self.removeAllUsers:
			self.core.mainStack.closePopUp=[False,REMOVING_ALL_USERS]
		else:
			self.core.mainStack.closePopUp=[False,REMOVING_USER]

		self.removeUserT=RemoveUser(self.removeAllUsers,self.userToRemove)
		self.removeUserT.start()
		self.removeUserT.finished.connect(self._removeUserRet)

	#def _launchRemoveBellProcess

	def _removeUserRet(self):

		self._updateUsersModel()
		self._manageOptions()
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True
		self.showMainMessage=[True,self.removeUserT.ret.get("code"),self.removeUserT.ret.get("type")]

	#def _removeUserRet

	on_easyLoginEnabled=Signal()
	easyLoginEnabled=Property(bool,_getEasyLoginEnabled,_setEasyLoginEnabled, notify=on_easyLoginEnabled)
	
	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage, notify=on_showMainMessage)
	
	on_showRemoveUserDialog=Signal()
	showRemoveUserDialog=Property('QVariantList',_getShowRemoveUserDialog,_setShowRemoveUserDialog,notify=on_showRemoveUserDialog)

	on_enableGlobalOptions=Signal()
	enableGlobalOptions=Property(bool,_getEnableGlobalOptions,_setEnableGlobalOptions,notify=on_enableGlobalOptions)

	usersModel=Property(QObject,_getUsersModel,constant=True)

#class Bridge

import Core


