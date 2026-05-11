from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import Core
import UsersModel

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

CHANGE_SERVICE_WAITING=20
REMOVING_USER=21
REMOVING_ALL_USERS=22
GENERATING_PDF_WAITING=23

class EnableLogin(QThread):

	loginEnabled=Signal(dict)

	def __init__(self,manager,value):

		super().__init__()
		self.easyManager=manager
		self.enableLogin=value

	#def __init__

	def run(self):

		time.sleep(0.5)
		ret=self.easyManager.enableEasyLogin(self.enableLogin)
		self.loginEnabled.emit(ret)

	#def run

#class EnableLogin

class RemoveUser(QThread):

	userRemoved=Signal(dict)

	def __init__(self,manager,allUsers,userToRemove):

		super().__init__()
		self.easyManager=manager
		self.allUsers=allUsers
		self.userToRemove=userToRemove

	#def __init__

	def run(self):

		time.sleep(0.5)
		ret=self.easyManager.removeUser(self.allUsers,self.userToRemove)
		self.userRemoved.emit(ret)

	#def run

#class RemoveUser

class GeneratePdf(QThread):

	pdfGenerated=Signal(dict)

	def __init__(self,manager,pdfPath):

		super().__init__()
		self.easyManager=manager
		self.pdfPath=pdfPath

	#def __init__

	def run(self,):

		time.sleep(0.5)
		ret=self.easyManager.generatePdf(self.pdfPath)
		self.pdfGenerated.emit(ret)

	#def run

#class GeneratePdf

class Bridge(QObject):

	on_easyLoginEnabled=Signal()
	on_showMainMessage=Signal()
	on_showRemoveUserDialog=Signal()
	on_enableGlobalOptions=Signal()

	def __init__(self):

		super().__init__()
		self.core=Core.Core.get_core()
		self.easyManager=self.core.easyLoginManager
		self._usersModel=UsersModel.UsersModel()
		self._easyLoginEnabled=False
		self._showMainMessage=[False,"","Ok"]
		self._showRemoveUserDialog=[False,False]
		self._enableGlobalOptions=False

	#def __init__
	
	@Property(bool,notify=on_easyLoginEnabled)
	def easyLoginEnabled(self):

		return self._easyLoginEnabled

	#def easyLoginEnabled

	@easyLoginEnabled.setter
	def easyLoginEnabled(self,easyLoginEnabled):

		if self._easyLoginEnabled!=easyLoginEnabled:
			self._easyLoginEnabled=easyLoginEnabled
			self.on_easyLoginEnabled.emit()

	#def easyLoginEnabled

	@Property('QVariantList',notify=on_showMainMessage)
	def showMainMessage(self):

		return self._showMainMessage

	#def showMainMessage

	@showMainMessage.setter
	def showMainMessage(self,showMainMessage):

		if self._showMainMessage!=showMainMessage:
			self._showMainMessage=showMainMessage
			self.on_showMainMessage.emit()

	#def showMainMessage

	@Property('QVariantList',notify=on_showRemoveUserDialog)
	def showRemoveUserDialog(self):

		return self._showRemoveUserDialog

	#def showRemoveUserDialog

	@showRemoveUserDialog.setter
	def showRemoveUserDialog(self,showRemoveUserDialog):

		if self._showRemoveUserDialog!=showRemoveUserDialog:
			self._showRemoveUserDialog=showRemoveUserDialog
			self.on_showRemoveUserDialog.emit()

	#def showRemoveUserDialog

	@Property(bool,notify=on_enableGlobalOptions)
	def enableGlobalOptions(self):

		return self._enableGlobalOptions

	#def enableGlobalOptions

	@enableGlobalOptions.setter
	def enableGlobalOptions(self,enableGlobalOptions):

		if self._enableGlobalOptions!=enableGlobalOptions:
			self._enableGlobalOptions=enableGlobalOptions
			self.on_enableGlobalOptions.emit()

	#def enableGlobalOptions

	@Property(QObject,constant=True)
	def usersModel(self):

		return self._usersModel

	#def usersModel
	def loadConfig(self):

		self.easyLoginEnabled=self.easyManager.easyLoginEnabled
		self._updateUsersModel()
		self._manageOptions()
	
	#def loadConfig

	def _manageOptions(self):

		self.enableGlobalOptions=self.easyManager.checkGlobalOptionStatus()

	#def _manageOptions

	def _updateUsersModel(self):

		ret=self._usersModel.clear()
		userEntries=self.easyManager.usersConfigData
		for item in userEntries:
			if item["username"]!="":
				self._usersModel.appendRow(item["username"],item["login"],item["name"],item["surname"],item["pwdImgPaths"],item["metaInfo"])
	
	#def _updateUsersModel

	@Slot(bool)
	def enableEasyLogin(self,value):

		self.core.mainStack.closePopUp=[False,CHANGE_SERVICE_WAITING]
		self.core.mainStack.closeGui=False
		self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]
		self.enableLoginT=EnableLogin(self.easyManager,value)
		self.enableLoginT.loginEnabled.connect(self._enableLoginRet)
		self.enableLoginT.finished.connect(self._enableLoginRet.deleteLater)
		self.enableLoginT.start()

	#def enableEasyLogin

	@Slot(dict)
	def _enableLoginRet(self,ret):

		self.easyLoginEnabled=self.easyManager.easyLoginEnabled

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True
		self.showMainMessage=[True,ret.get("code"),ret.get("type")]

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
		self.generatePdfT=GeneratePdf(self.easyManager,exportPath)
		self.generatePdfT.pdfGenerated.connect(self._generatePdfRet)
		self.generatePdfT.finished.connect(self.generatePdfT.deleteLater)
		self.generatePdfT.start()

	#def generateList

	@Slot(dict)
	def _generatePdfRet(self,ret):

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

		if not ret.get("status"):
			self.showMainMessage=[True,ret.get("code"),ret.get("type")]
	
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

		self.removeUserT=RemoveUser(self.easyManager,self.removeAllUsers,self.userToRemove)
		self.removeUserT.userRemoved.connect(self._removeUserRet)
		self.removeUserT.finished.connect(self.removeUserT.deleteLater)
		self.removeUserT.start()

	#def _launchRemoveBellProcess

	@Slot(dict)
	def _removeUserRet(self,ret):

		self._updateUsersModel()
		self._manageOptions()
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True
		self.showMainMessage=[True,ret.get("code"),ret.get("type")]

	#def _removeUserRet

#class Bridge

