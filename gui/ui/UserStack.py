from PySide6.QtCore import QObject,Signal,Slot,QThread,Property
import os 
import sys
import threading
import time
import copy

import Core

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

NEW_USER_CONFIG=24
LOAD_USER_CONFIG=25
CHECK_DATA=26
SAVE_DATA=27
NEW_PASSWORD=28

class LoadUser(QThread):

	userLoaded=Signal(dict)

	def __init__(self,manager,isNewUser,userInfo):

		super().__init__()
		self.easyManager=manager
		self.newUser=isNewUser
		self.userInfo=userInfo

	#def __init__

	def run(self,):

		time.sleep(0.5)
		ret=self.easyManager.initValues()
		retLoaded=self.easyManager.loadUserConfig(self.newUser,self.userInfo)
		self.userLoaded.emit(retLoaded)
	
	#def run

#class LoadBell

class CheckData(QThread):

	dataChecked=Signal(dict)

	def __init__(self,manager,dataToCheck):

		super().__init__()
		self.easyManager=manager
		self.dataToCheck=dataToCheck

	#def __init__

	def run(self):

		time.sleep(0.5)
		ret=self.easyManager.checkData(self.dataToCheck)
		self.dataChecked.emit(ret)
	
	#def run

#class CheckData

class GetNewPassword(QThread):

	newPasswordGetted=Signal(dict)

	def __init__(self,manager):

		super().__init__()
		self.easyManager=manager

	#def __init__

	def run(self):

		time.sleep(0.5)
		ret=self.easyManager.generateUsername()
		self.newPasswordGetted.emit(ret)

	#def run

#class GetNewPassword

class SaveData(QThread):

	dataSaved=Signal(dict)

	def __init__(self,manager,isNewUser,datoToSave):

		super().__init__()
		self.easyManager=manager
		self.newUser=isNewUser
		self.dataToSave=datoToSave

	#def __init__

	def run(self):

		time.sleep(0.5)
		if self.newUser:
			ret=self.easyManager.saveNewUser(self.dataToSave)
		else:
			ret=self.easyManager.saveEditData(self.dataToSave)
		self.dataSaved.emit(ret)

	#def run

#class SaveData

class Bridge(QObject):

	usernameChanged=Signal()
	nameChanged=Signal()
	surnameChanged=Signal()
	loginChanged=Signal()
	enableLoginEditionChanged=Signal()
	pwImgPathsChanged=Signal()
	showUserFormMessageChanged=Signal()
	userCurrentOptionChanged=Signal()
	showChangesInUserDialogChanged=Signal()
	changesInUserChanged=Signal()
	isNewUserChanged=Signal()
	
	def __init__(self):

		super().__init__()
		self.core=Core.Core.get_core()
		self.easyManager=self.core.easyLoginManager
		self._username=self.easyManager.currentUserConfig["username"]
		self._login=self.easyManager.currentUserConfig["login"]
		self._name=self.easyManager.currentUserConfig["name"]
		self._surname=self.easyManager.currentUserConfig["surname"]
		self._pwdImgPaths=self.easyManager.currentUserConfig["pwdImgPaths"]
		self._enableLoginEdition=False
		self._userCurrentOption=0
		self._showUserFormMessage={"show":False,"msgCode":'',"type":''}
		self._showChangesInUserDialog=False
		self._changesInUser=False
		self._isNewUser=True

	#def _init__

	@Property(str,notify=usernameChanged)
	def username(self):

		return self._username

	#def username

	@username.setter
	def username(self,username):

		if self._username!=username:
			self._username=username
			self.usernameChanged.emit()

	#def username

	@Property(str,notify=nameChanged)
	def name(self):

		return self._name

	#def name

	@name.setter
	def name(self,name):

		if self._name!=name:
			self._name=name
			self.nameChanged.emit()

	#def name

	@Property(str,notify=surnameChanged)
	def surname(self):

		return self._surname

	#def surname

	@surname.setter
	def surname(self,surname):

		if self._surname!=surname:
			self._surname=surname
			self.surnameChanged.emit()

	#def surname

	@Property(str,notify=loginChanged)
	def login(self):

		return self._login

	#def _login

	@login.setter
	def login(self,login):

		if self._login!=login:
			self._login=login
			self.loginChanged.emit()

	#def login

	@Property(bool,notify=enableLoginEditionChanged)
	def enableLoginEdition(self):

		return self._enableLoginEdition

	#def enableLoginEdition

	@enableLoginEdition.setter
	def enableLoginEdition(self, enableLoginEdition):

		if self._enableLoginEdition!=enableLoginEdition:
			self._enableLoginEdition=enableLoginEdition
			self.enableLoginEditionChanged.emit()

	#def enableLoginEdition

	@Property('QVariantList',notify=pwImgPathsChanged)
	def pwdImgPaths(self):

		return self._pwdImgPaths

	#def pwdImgPaths

	@pwdImgPaths.setter
	def pwdImgPaths(self,pwdImgPaths):

		if self._pwdImgPaths!=pwdImgPaths:
			self._pwdImgPaths=pwdImgPaths
			self.pwImgPathsChanged.emit()

	#def pwdImgPaths

	@Property(dict,notify=showUserFormMessageChanged)
	def showUserFormMessage(self):

		return self._showUserFormMessage

	#def showUserFormMessage

	@showUserFormMessage.setter
	def showUserFormMessage(self,showUserFormMessage):

		if self._showUserFormMessage!=showUserFormMessage:
			self._showUserFormMessage=showUserFormMessage
			self.showUserFormMessageChanged.emit()

	#def showUserFormMessage

	@Property(int,notify=userCurrentOptionChanged)
	def userCurrentOption(self):

		return self._userCurrentOption

	#def userCurrentOption	

	@userCurrentOption.setter
	def userCurrentOption(self,userCurrentOption):
		
		if self._userCurrentOption!=userCurrentOption:
			self._userCurrentOption=userCurrentOption
			self.userCurrentOptionChanged.emit()

	#def userCurrentOption

	@Property(bool,notify=showChangesInUserDialogChanged)
	def showChangesInUserDialog(self):

		return self._showChangesInUserDialog

	#def _showChangesInUserDialog

	@showChangesInUserDialog.setter
	def showChangesInUserDialog(self,showChangesInUserDialog):

		if self._showChangesInUserDialog!=showChangesInUserDialog:
			self._showChangesInUserDialog=showChangesInUserDialog
			self.showChangesInUserDialogChanged.emit()

	#def showChangesInUserDialog

	@Property(bool,notify=changesInUserChanged)
	def changesInUser(self):

		return self._changesInUser

	#def _changesInUser

	@changesInUser.setter
	def changesInUser(self,changesInUser):

		if self._changesInUser!=changesInUser:
			self._changesInUser=changesInUser
			self.changesInUserChanged.emit()

	#def changesInUser

	@Property(bool,notify=isNewUserChanged)
	def isNewUser(self):

		return self._isNewUser

	#def isNewUser

	@isNewUser.setter
	def isNewUser(self,isNewUser):

		if self._isNewUser!=isNewUser:
			self._isNewUser=isNewUser
			self.isNewUserChanged.emit()

	#def isNewUser

	@Slot()
	def addNewUser(self):

		self.isNewUser=True
		self.core.mainStack.showPopUp={"show":True,"msgCode":NEW_USER_CONFIG}
		self.core.mainStack.closeGui=False
		self.core.usersOptionsStack.showMainMessage={"show":False,"msgCode":'',"type":''}
		self.newUserT=LoadUser(self.easyManager,self.isNewUser,"")
		self.newUserT.userLoaded.connect(self._addNewUserRet)
		self.newUserT.finished.connect(self.newUserT.deleteLater)
		self.newUserT.start()

	#def addNewUser

	@Slot(dict)
	def _addNewUserRet(self,ret):

		if ret.get("status"):
			self.currentUserConfig=copy.deepcopy(self.easyManager.currentUserConfig)
			self._initializeVars()
			self.core.mainStack.currentStack=2
			self.userCurrentOption=1
		else:
			self.core.usersOptionsStack.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}

		self.core.mainStack.showPopUp={"show":False,"msgCode":''}
		self.core.mainStack.closeGui=True

	#def _addNewUserRet

	def _initializeVars(self):

		self.username=self.easyManager.currentUserConfig["username"]
		self.login=self.easyManager.currentUserConfig["login"]
		self.name=self.easyManager.currentUserConfig["name"]
		self.surname=self.easyManager.currentUserConfig["surname"]
		self.pwdImgPaths=self.easyManager.currentUserConfig["pwdImgPaths"]
		self.showUserFormMessage={"show":False,"msgCode":'',"type":''}
		self.changesInUser=False
		self.enableLoginEdition=self.easyManager.currentUserConfig["customLogin"]
		self.previousLogin=self.login

	#def _initializeVars

	@Slot()
	def goHome(self):

		if not self.changesInUser:
			self.core.mainStack.currentStack=1
			self.core.mainStack.mainCurrentOption=0
			self.userCurrentOption=0
			self.core.mainStack.moveToStack=0
		else:
			self.showChangesInUserDialog=True
			self.core.mainStack.moveToStack=1

	#def goHome

	@Slot('QVariantList')
	def loadUser(self,userToLoad):

		self.core.mainStack.showPopUp={"show":True,"msgCode":LOAD_USER_CONFIG}
		self.core.mainStack.closeGui=False
		self.core.usersOptionsStack.showMainMessage={"show":False,"msgCode":'',"type":''}
		self.isNewUser=False
		self.editUserT=LoadUser(self.easyManager,self.isNewUser,userToLoad)
		self.editUserT.userLoaded.connect(self._loadUserRet)
		self.editUserT.finished.connect(self.editUserT.deleteLater)
		self.editUserT.start()

	#def loadUser

	@Slot(dict)
	def _loadUserRet(self,ret):

		if ret.get("status"):
			self.currentUserConfig=copy.deepcopy(self.easyManager.currentUserConfig)
			self._initializeVars()
			self.core.mainStack.currentStack=2
			self.userCurrentOption=1
		else:
			self.core.usersOptionsStack.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}

		self.core.mainStack.showPopUp={"show":False,"msgCode":''}
		self.core.mainStack.closeGui=True

	#def _loadUserRet

	@Slot(str)
	def updateNameValue(self,value):

		if value!=self.name:
			self.name=value
			self.currentUserConfig["name"]=self.name
			self.previousLogin=self.easyManager.getFormattedLogin(self.name,self.surname)
			if not self.enableLoginEdition:
				self.login=self.previousLogin
				self.currentUserConfig["login"]=self.login

		self._checkIfChanged()

	#def updateBellNameValue

	@Slot(str)
	def updateSurnameValue(self,value):

		if value!=self.surname:
			self.surname=value
			self.currentUserConfig["surname"]=self.surname
			self.previousLogin=self.easyManager.getFormattedLogin(self.name,self.surname)
			if not self.enableLoginEdition:
				self.login=self.previousLogin
				self.currentUserConfig["login"]=self.login

		self._checkIfChanged()

	#def updateSurnameValue

	@Slot()
	def forceLoginEdition(self):

		self.enableLoginEdition=True

	#def forceLoginEdition

	@Slot()
	def restoreDefaultLogin(self):

		self.enableLoginEdition=False
		self.login=self.easyManager.getFormattedLogin(self.name,self.surname)
		self.currentUserConfig["login"]=self.login

		self._checkIfChanged()

	#def restoreDefaultLogin

	@Slot(str)
	def updateLoginValue(self,value):

		if value!=self.login:
			self.login=value
			self.currentUserConfig["login"]=self.login

		self._checkIfChanged()

	#def updateLoginValue

	@Slot()
	def generateUsername(self):

		self.core.mainStack.showPopUp={"show":True,"msgCode":NEW_PASSWORD}
		self.core.mainStack.closeGui=False
		self.getNewPasswordT=GetNewPassword(self.easyManager)
		self.getNewPasswordT.newPasswordGetted.connect(self._getNewPasswordRet)
		self.getNewPasswordT.finished.connect(self.getNewPasswordT.deleteLater)
		self.getNewPasswordT.start()

	#def generateUsername

	@Slot(dict)
	def _getNewPasswordRet(self,ret):

		if ret.get("status"):
			self.pwdImgPaths=ret.get("data").get("pwdImgPaths")
			self.username=ret.get("data").get("username")
			self.currentUserConfig["username"]=self.username
			self.currentUserConfig["pwdImgPaths"]=self.pwdImgPaths

		self._checkIfChanged()

		self.core.mainStack.showPopUp={"show":False,"msgCode":''}
		self.core.mainStack.closeGui=True

	#def _getNewPasswordRet

	def _checkIfChanged(self):

		if self.currentUserConfig!=self.easyManager.currentUserConfig:
			self.changesInUser=True
		else:
			self.changesInUser=False

	#def _checkIfChanged

	@Slot(str)
	def manageChangesDialog(self,action):

		self.showChangesInUserDialog=False

		if action=="Accept":
			self._applyUserChanges()
		elif action=="Discard":
			self._cancelUserChanges()
		elif action=="Cancel":
			pass

	#def manageChangesDialog

	@Slot()
	def applyUserChanges(self):

		self._applyUserChanges()

	#def applyBellChanges

	def _applyUserChanges(self):

		self.core.mainStack.showPopUp={"show":True,"msgCode":CHECK_DATA}
		self.core.mainStack.closeGui=False
		self.checkDataT=CheckData(self.easyManager,self.currentUserConfig)
		self.checkDataT.dataChecked.connect(self._checkDataRet)
		self.checkDataT.finished.connect(self.checkDataT.deleteLater)
		self.checkDataT.start()

	#def _applyUserChanges

	@Slot(dict)
	def _checkDataRet(self,ret):

		if ret.get("status"):
			self.saveDataChanges()
		else:
			self.core.mainStack.showPopUp={"show":False,"msgCode":''}
			self.showUserFormMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}

	#def _checkDataRet

	def saveDataChanges(self):

		self.core.mainStack.showPopUp={"show":True,"msgCode":SAVE_DATA}
		self.saveDataT=SaveData(self.easyManager,self.isNewUser,self.currentUserConfig)
		self.saveDataT.dataSaved.connect(self._saveDataRet)
		self.saveDataT.finished.connect(self.saveDataT.deleteLater)
		self.saveDataT.start()

	#def saveData

	@Slot(dict)
	def _saveDataRet(self,ret):

		self.core.usersOptionsStack._updateUsersModel()
		self.core.usersOptionsStack.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}

		self.core.usersOptionsStack.enableGlobalOptions=self.easyManager.checkGlobalOptionStatus()
		self.changesInUser=False
		self.core.mainStack.moveToStack=1
		self.core.mainStack.manageGoToStack()
		self.core.mainStack.showPopUp={"show":False,"msgCode":''}
		self.core.mainStack.closeGui=True

	#def _saveDataRet

	@Slot()
	def cancelUserChanges(self):

		self._cancelUserChanges()

	#def cancelUserChanges

	def _cancelUserChanges(self):

		self.changesInUser=False
		self.core.mainStack.closeGui=True
		self.core.mainStack.moveToStack=1
		self.core.mainStack.manageGoToStack()

	#def _cancelUserChanges

#class Bridge

