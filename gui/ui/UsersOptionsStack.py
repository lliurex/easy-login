from PySide6.QtCore import QObject,Signal,Slot,QThread,Property
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
		if self.allUsers:
			ret=self.easyManager.removeAllUsers()
		else:
			ret=self.easyManager.removeSingleUser(self.userToRemove)
			
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

	easyLoginEnabledChanged=Signal()
	showMainMessageChanged=Signal()
	showRemoveUserDialogChanged=Signal()
	enableGlobalOptionsChanged=Signal()

	def __init__(self):

		super().__init__()
		self.core=Core.Core.get_core()
		self.easyManager=self.core.easyLoginManager
		self._usersModel=UsersModel.UsersModel()
		self._easyLoginEnabled=False
		self._showMainMessage={"show":False,"msgCode":'',"type":""}
		self._showRemoveUserDialog={"show":False,"allUsers":False}
		self._enableGlobalOptions=False

	#def __init__
	
	@Property(bool,notify=easyLoginEnabledChanged)
	def easyLoginEnabled(self):

		return self._easyLoginEnabled

	#def easyLoginEnabled

	@easyLoginEnabled.setter
	def easyLoginEnabled(self,easyLoginEnabled):

		if self._easyLoginEnabled!=easyLoginEnabled:
			self._easyLoginEnabled=easyLoginEnabled
			self.easyLoginEnabledChanged.emit()

	#def easyLoginEnabled

	@Property(dict,notify=showMainMessageChanged)
	def showMainMessage(self):

		return self._showMainMessage

	#def showMainMessage

	@showMainMessage.setter
	def showMainMessage(self,showMainMessage):

		if self._showMainMessage!=showMainMessage:
			self._showMainMessage=showMainMessage
			self.showMainMessageChanged.emit()

	#def showMainMessage

	@Property(dict,notify=showRemoveUserDialogChanged)
	def showRemoveUserDialog(self):

		return self._showRemoveUserDialog

	#def showRemoveUserDialog

	@showRemoveUserDialog.setter
	def showRemoveUserDialog(self,showRemoveUserDialog):

		if self._showRemoveUserDialog!=showRemoveUserDialog:
			self._showRemoveUserDialog=showRemoveUserDialog
			self.showRemoveUserDialogChanged.emit()

	#def showRemoveUserDialog

	@Property(bool,notify=enableGlobalOptionsChanged)
	def enableGlobalOptions(self):

		return self._enableGlobalOptions

	#def enableGlobalOptions

	@enableGlobalOptions.setter
	def enableGlobalOptions(self,enableGlobalOptions):

		if self._enableGlobalOptions!=enableGlobalOptions:
			self._enableGlobalOptions=enableGlobalOptions
			self.enableGlobalOptionsChanged.emit()

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

		self.core.mainStack.showPopUp={"show":True,"msgCode":CHANGE_SERVICE_WAITING}
		self.core.mainStack.closeGui=False
		self.showMainMessage={"show":False,"msgCode":'',"type":''}
		self.enableLoginT=EnableLogin(self.easyManager,value)
		self.enableLoginT.loginEnabled.connect(self._enableLoginRet)
		self.enableLoginT.finished.connect(self.enableLoginT.deleteLater)
		self.enableLoginT.start()

	#def enableEasyLogin

	@Slot(dict)
	def _enableLoginRet(self,ret):

		self.easyLoginEnabled=self.easyManager.easyLoginEnabled

		self.core.mainStack.showPopUp={"show":False,"msgCode":''}
		self.core.mainStack.closeGui=True
		self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}

	#def _enableLoginRet

	@Slot('QVariantList')
	def removeUser(self,data):

		self.showMainMessage={"show":False,"msgCode":'',"type":''}
		self.removeAllUsers=data[0]
		
		if self.removeAllUsers:
			self.userToRemove=None
		else:
			self.userToRemove=data[1]

		self.showRemoveUserDialog={"show":True,"allUsers":self.removeAllUsers}

	#def removeUser

	@Slot(str)
	def generateList(self,exportPath):

		self.core.mainStack.showPopUp={"show":True,"msgCode":GENERATING_PDF_WAITING}
		self.core.mainStack.closeGui=False
		self.showMainMessage={"show":False,"msgCode":'',"type":''}
		self.generatePdfT=GeneratePdf(self.easyManager,exportPath)
		self.generatePdfT.pdfGenerated.connect(self._generatePdfRet)
		self.generatePdfT.finished.connect(self.generatePdfT.deleteLater)
		self.generatePdfT.start()

	#def generateList

	@Slot(dict)
	def _generatePdfRet(self,ret):

		self.core.mainStack.showPopUp={"show":False,"msgCode":''}
		self.core.mainStack.closeGui=True

		self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
	
	#def _generatePdfRet

	@Slot(str)
	def manageRemoveUserDialog(self,response):

		self.showRemoveUserDialog={"show":False,"allUsers":False}
		if response=="Accept":
			self._launchRemoveUserProcess()

	#def manageRemoveBellDialog

	def _launchRemoveUserProcess(self):

		self.core.mainStack.closeGui=False
		if self.removeAllUsers:
			self.core.mainStack.showPopUp={"show":True,"msgCode":REMOVING_ALL_USERS}
		else:
			self.core.mainStack.showPopUp={"show":True,"msgCode":REMOVING_USER}

		self.removeUserT=RemoveUser(self.easyManager,self.removeAllUsers,self.userToRemove)
		self.removeUserT.userRemoved.connect(self._removeUserRet)
		self.removeUserT.finished.connect(self.removeUserT.deleteLater)
		self.removeUserT.start()

	#def _launchRemoveBellProcess

	@Slot(dict)
	def _removeUserRet(self,ret):

		self._updateUsersModel()
		self._manageOptions()
		self.core.mainStack.showPopUp={"show":False,"msgCode":''}
		self.core.mainStack.closeGui=True
		self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}

	#def _removeUserRet

#class Bridge

