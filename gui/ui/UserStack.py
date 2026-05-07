from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

NEW_USER_CONFIG=24
LOAD_USER_CONFIG=25
CHECK_DATA=26
SAVE_DATA=27
NEW_PASSWORD=28

class LoadUser(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.newUser=args[0]
		self.userInfo=args[1]
		self.ret={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=Bridge.easyLoginManager.initValues()
		self.ret=Bridge.easyLoginManager.loadUserConfig(self.newUser,self.userInfo)

	#def run

#class LoadBell

class CheckData(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.dataToCheck=args[0]
		self.ret={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.checkData(self.dataToCheck)
		
	#def run

#class CheckData

class GetNewPassword(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.ret={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.generateUsername()

	#def run

#class GetNewPassword

class SaveData(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.dataToSave=args[0]
		self.ret={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.saveData(self.dataToSave)

	#def run

#class SaveData

class Bridge(QObject):

	
	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.easyLoginManager=self.core.easyLoginManager
		self._username=Bridge.easyLoginManager.currentUserConfig["username"]
		self._login=Bridge.easyLoginManager.currentUserConfig["login"]
		self._name=Bridge.easyLoginManager.currentUserConfig["name"]
		self._surname=Bridge.easyLoginManager.currentUserConfig["surname"]
		self._pwdImgPaths=Bridge.easyLoginManager.currentUserConfig["pwdImgPaths"]
		self._enableLoginEdition=False
		self._userCurrentOption=0
		self._showUserFormMessage=[False,"","Ok"]
		self._showChangesInUserDialog=False
		self._changesInUser=False
		self._actionType="add"

	#def _init__

	def _getUsername(self):

		return self._username

	#def _getUsername

	def _setUsername(self,username):

		if self._username!=username:
			self._username=username
			self.on_username.emit()

	#def _setUsername

	def _getLogin(self):

		return self._login

	#def _getLogin

	def _setLogin(self,login):

		if self._login!=login:
			self._login=login
			self.on_login.emit()

	#def _setLogin

	def _getName(self):

		return self._name

	#def _getName

	def _setName(self,name):

		if self._name!=name:
			self._name=name
			self.on_name.emit()

	#def _setName

	def _getSurname(self):

		return self._surname

	#def _getSurname

	def _setSurname(self,surname):

		if self._surname!=surname:
			self._surname=surname
			self.on_surname.emit()

	#def _setBellValidityValue

	def _getEnableLoginEdition(self):

		return self._enableLoginEdition

	#def _getEnableLoginEdition

	def _setEnableLoginEdition(self, enableLoginEdition):

		if self._enableLoginEdition!=enableLoginEdition:
			self._enableLoginEdition=enableLoginEdition
			self.on_enableLoginEdition.emit()

	#def _setEnableLoginEdition

	def _getPwdImgPaths(self):

		return self._pwdImgPaths

	#def _getPwdImgPaths

	def _setPwdImgPaths(self,pwdImgPaths):

		if self._pwdImgPaths!=pwdImgPaths:
			self._pwdImgPaths=pwdImgPaths
			self.on_pwdImgPaths.emit()

	#def _setPwdImgPaths

	def _getUserCurrentOption(self):

		return self._userCurrentOption

	#def _getUserCurrentOption	

	def _setUserCurrentOption(self,userCurrentOption):
		
		if self._userCurrentOption!=userCurrentOption:
			self._userCurrentOption=userCurrentOption
			self.on_userCurrentOption.emit()

	#def _setUserCurrentOption

	def _getShowChangesInUserDialog(self):

		return self._showChangesInUserDialog

	#def _getShowChangesInUserDialog

	def _setShowChangesInUserDialog(self,showChangesInUserDialog):

		if self._showChangesInUserDialog!=showChangesInUserDialog:
			self._showChangesInUserDialog=showChangesInUserDialog
			self.on_showChangesInUserDialog.emit()

	#def _setShowChangesInUserDialog

	def _getChangesInUser(self):

		return self._changesInUser

	#def _getChangesInUser

	def _setChangesInUser(self,changesInUser):

		if self._changesInUser!=changesInUser:
			self._changesInUser=changesInUser
			self.on_changesInUser.emit()

	#def _setChangesInUser

	def _getShowUserFormMessage(self):

		return self._showUserFormMessage

	#def _getShowUserFormMessage

	def _setShowUserFormMessage(self,showUserFormMessage):

		if self._showUserFormMessage!=showUserFormMessage:
			self._showUserFormMessage=showUserFormMessage
			self.on_showUserFormMessage.emit()

	#def _setShowUserFormMessage

	def _getActionType(self):

		return self._actionType

	#def _getActionType

	def _setActionType(self,actionType):

		if self._actionType!=actionType:
			self._actionType=actionType
			self.on_actionType.emit()

	#def _setActionType

	@Slot()
	def addNewUser(self):

		actionType="add"
		self.core.mainStack.closePopUp=[False,NEW_USER_CONFIG]
		self.core.mainStack.closeGui=False
		self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]
		self.newUserT=LoadUser(True,"")
		self.newUserT.start()
		self.newUserT.finished.connect(self._addNewUserRet)

	#def addNewUser

	def _addNewUserRet(self):

		if self.newUserT.ret.get("status"):
			self.currentUserConfig=copy.deepcopy(Bridge.easyLoginManager.currentUserConfig)
			self._initializeVars()
			self.core.mainStack.currentStack=2
			self.userCurrentOption=1
		else:
			self.core.usersOptionsStack.showMainMessage=[True,self.newUserT.ret.get("code"),self.newUserT.ret.get("type")]

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

	#def _addNewUserRet

	def _initializeVars(self):

		self.username=Bridge.easyLoginManager.currentUserConfig["username"]
		self.login=Bridge.easyLoginManager.currentUserConfig["login"]
		self.name=Bridge.easyLoginManager.currentUserConfig["name"]
		self.surname=Bridge.easyLoginManager.currentUserConfig["surname"]
		self.pwdImgPaths=list(Bridge.easyLoginManager.currentUserConfig["pwdImgPaths"])
		self.showUserFormMessage=[False,"","Ok"]
		self.changesInUser=False
		self.enableLoginEdition=False
		self.previousLogin=self.login

	#def _initializeVars

	@Slot()
	def goHome(self):

		if not self.changesInUser:
			self.core.mainStack.currentStack=1
			self.core.mainStack.mainCurrentOption=0
			self.userCurrentOption=0
			self.core.mainStack.moveToStack=""
		else:
			self.showChangesInUserDialog=True
			self.core.mainStack.moveToStack=1

	#def goHome

	@Slot('QVariantList')
	def loadUser(self,userToLoad):

		self.core.mainStack.closePopUp=[False,LOAD_USER_CONFIG]
		self.core.mainStack.closeGui=False
		self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]
		self.actionType="edit"
		self.editUserT=LoadUser(False,userToLoad)
		self.editUserT.start()
		self.editUserT.finished.connect(self._loadUserRet)

	#def loadUser

	def _loadUserRet(self):

		if self.editUserT.ret.get("status"):
			self.currentUserConfig=copy.deepcopy(Bridge.easyLoginManager.currentUserConfig)
			self._initializeVars()
			self.core.mainStack.currentStack=2
			self.userCurrentOption=1
		else:
			self.core.usersOptionsStack.showMainMessage=[True,self.editUserT.ret.get("code"),self.editUserT.ret.get("type")]

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

	#def _loadUserRet

	@Slot(str)
	def updateNameValue(self,value):

		if value!=self.name:
			self.name=value
			self.currentUserConfig["name"]=self.name
			self.previousLogin=Bridge.easyLoginManager.getFormattedLogin(self.name,self.surname)
			if not self.enableLoginEdition:
				self.login=self.previousLogin
				self.currentUserConfig["login"]=self.login

		if self.currentUserConfig!=Bridge.easyLoginManager.currentUserConfig:
			self.changesInUser=True
		else:
			self.changesInUser=False

	#def updateBellNameValue

	@Slot(str)
	def updateSurnameValue(self,value):

		if value!=self.surname:
			self.surname=value
			self.currentUserConfig["surname"]=self.surname
			self.previousLogin=Bridge.easyLoginManager.getFormattedLogin(self.name,self.surname)
			if not self.enableLoginEdition:
				self.login=self.previousLogin
				self.currentUserConfig["login"]=self.login

		if self.currentUserConfig!=Bridge.easyLoginManager.currentUserConfig:
			self.changesInUser=True
		else:
			self.changesInUser=False

	#def updateSurnameValue

	@Slot()
	def forceLoginEdition(self):

		self.enableLoginEdition=True

	#def forceLoginEdition

	@Slot()
	def restoreDefaultLogin(self):

		self.enableLoginEdition=False
		self.login=self.previousLogin
		self.currentUserConfig["login"]=self.login

		if self.currentUserConfig!=Bridge.easyLoginManager.currentUserConfig:
			self.changesInUser=True
		else:
			self.changesInUser=False

	#def restoreDefaultLogin

	@Slot(str)
	def updateLoginValue(self,value):

		if value!=self.login:
			self.login=value
			self.currentUserConfig["login"]=self.login

		if self.currentUserConfig!=Bridge.easyLoginManager.currentUserConfig:
			self.changesInUser=True
		else:
			self.changesInUser=False

	#def updateLoginValue

	@Slot()
	def generateUsername(self):

		self.core.mainStack.closePopUp=[False,NEW_PASSWORD]
		self.core.mainStack.closeGui=False
		self.getNewPasswordT=GetNewPassword()
		self.getNewPasswordT.start()
		self.getNewPasswordT.finished.connect(self._getNewPasswordRet)

	#def generateUsername

	def _getNewPasswordRet(self):

		if self.getNewPasswordT.ret.get("status"):
			self.currentUserConfig["username"]=self.getNewPasswordT.ret.get("data").get("username")
			self.currentUserConfig["pwdImgPaths"][0]=self.getNewPasswordT.ret.get("data").get("imgPaths").get("pwdImg1")
			self.currentUserConfig["pwdImgPaths"][1]=self.getNewPasswordT.ret.get("data").get("imgPaths").get("pwdImg2")
			self.currentUserConfig["pwdImgPaths"][2]=self.getNewPasswordT.ret.get("data").get("imgPaths").get("pwdImg3")
			self.currentUserConfig["pwdImgPaths"][3]=self.getNewPasswordT.ret.get("data").get("imgPaths").get("pwdImg4")
			self.pwdImgPaths=list(self.currentUserConfig["pwdImgPaths"])
			self.username=self.currentUserConfig["username"]

		if self.currentUserConfig!=Bridge.easyLoginManager.currentUserConfig:
			self.changesInUser=True
		else:
			self.changesInUser=False

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

	#def _getNewPasswordRet

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

		self.core.mainStack.closePopUp=[False,CHECK_DATA]
		self.core.mainStack.closeGui=False
		self.checkDataT=CheckData(self.currentUserConfig)
		self.checkDataT.start()
		self.checkDataT.finished.connect(self._checkDataRet)

	#def _applyUserChanges

	def _checkDataRet(self):

		if self.checkDataT.ret.get("status"):
			self.saveDataChanges()
		else:
			self.core.mainStack.closePopUp=[True,""]
			self.showUserFormMessage=[True,self.checkDataT.ret.get("code"),self.checkDataT.ret.get("type")]

	#def _checkDataRet

	def saveDataChanges(self):

		self.core.mainStack.closePopUp=[False,SAVE_DATA]
		self.saveDataT=SaveData(self.currentUserConfig)
		self.saveDataT.start()
		self.saveDataT.finished.connect(self._saveDataRet)

	#def saveData

	def _saveDataRet(self):

		self.core.usersOptionsStack._updateUsersModel()
		self.core.usersOptionsStack.showMainMessage=[True,self.saveDataT.ret.get("code"),self.saveDataT.ret.get("type")]

		self.core.usersOptionsStack.enableGlobalOptions=Bridge.easyLoginManager.checkGlobalOptionStatus()
		self.changesInUser=False
		self.core.mainStack.moveToStack=1
		self.core.mainStack.manageGoToStack()
		self.core.mainStack.closePopUp=[True,""]
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

	on_username=Signal()
	username=Property(str,_getUsername,_setUsername, notify=on_username)

	on_name=Signal()
	name=Property(str,_getName,_setName, notify=on_name)

	on_surname=Signal()
	surname=Property(str,_getSurname,_setSurname,notify=on_surname)

	on_login=Signal()
	login=Property(str,_getLogin,_setLogin, notify=on_login)

	on_enableLoginEdition=Signal()
	enableLoginEdition=Property(bool,_getEnableLoginEdition,_setEnableLoginEdition, notify=on_enableLoginEdition)
	
	on_pwdImgPaths=Signal()
	pwdImgPaths=Property('QVariantList',_getPwdImgPaths,_setPwdImgPaths, notify=on_pwdImgPaths)

	on_showUserFormMessage=Signal()
	showUserFormMessage=Property('QVariantList',_getShowUserFormMessage,_setShowUserFormMessage, notify=on_showUserFormMessage)

	on_userCurrentOption=Signal()
	userCurrentOption=Property(int,_getUserCurrentOption,_setUserCurrentOption, notify=on_userCurrentOption)

	on_showChangesInUserDialog=Signal()
	showChangesInUserDialog=Property(bool,_getShowChangesInUserDialog,_setShowChangesInUserDialog,notify=on_showChangesInUserDialog)

	on_changesInUser=Signal()
	changesInUser=Property(bool,_getChangesInUser,_setChangesInUser,notify=on_changesInUser)

	on_actionType=Signal()
	actionType=Property(str,_getActionType,_setActionType,notify=on_actionType)

#class Bridge

import Core


