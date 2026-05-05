from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

NAME_EMPTY_ERROR=-20
SURNAME_EMPTY_ERROR=-21
LOGIN_EMPTY_ERROR=-22
NEW_USER_CONFIG=20
LOAD_USER_CONFIG=21
CHECK_DATA=22
SAVE_DATA=23

class LoadUser(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.newUser=args[0]
		self.userInfo=args[1]
		self.ret=False

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=Bridge.easyLoginManager.initValues()
		if self.newUser:
			self.ret=Bridge.easyLoginManager.generateUsername()
		else:
			self.ret=Bridge.easyLoginManager.loadUserConfig(self.userInfo)

	#def run

#class LoadBell

class CheckData(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.dataToCheck=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.checkData(self.dataToCheck)
		
	#def run

#class CheckData

class SaveData(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.dataToSave=args[0]
		self.ret=[]

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
		self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]
		self.newUser=LoadUser(True,"")
		self.newUser.start()
		self.newUser.finished.connect(self._addNewUserRet)

	#def addNewUser

	def _addNewUserRet(self):

		self.currentUserConfig=copy.deepcopy(Bridge.easyLoginManager.currentUserConfig)
		self._initializeVars()
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.currentStack=2
		self.userCurrentOption=1

	#def _addNewUserRet

	def _initializeVars(self):

		self.username=Bridge.easyLoginManager.currentUserConfig["username"]
		self.login=Bridge.easyLoginManager.currentUserConfig["login"]
		self.name=Bridge.easyLoginManager.currentUserConfig["name"]
		self.surname=Bridge.easyLoginManager.currentUserConfig["surname"]
		self.pwdImgPaths=Bridge.easyLoginManager.currentUserConfig["pwdImgPaths"]
		self.showUserFormMessage=[False,"","Ok"]
		self.changesInUser=False

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
		self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]
		self.actionType="edit"
		self.editUser=LoadUser(False,userToLoad)
		self.editUser.start()
		self.editUser.finished.connect(self._loadUserRet)

	#def loadUser

	def _loadUserRet(self):

		if editUser.ret:
			self.currentUserConfig=copy.deepcopy(Bridge.easyLoginManager.currentUserConfig)
			self._initializeVars()
			self.core.mainStack.closePopUp=[True,""]
			self.core.mainStack.currentStack=2
			self.userCurrentOption=1
		else:
			self.core.mainStack.closePopUp=[True,""]
			self.core.usersOptionsStack.showMainMessage=[True,"","Error"]

	#def _loadUserRet

	@Slot(str)
	def updateNameValue(self,value):

		if value!=self.name:
			self.name=value
			self.currentUserConfig["name"]=self.name
			if not self.enableLoginEdition:
				self.login=Bridge.easyLoginManager.getFormattedLogin(self.name,self.surname)
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
			if not self.enableLoginEdition:
				self.login=Bridge.easyLoginManager.getFormattedLogin(self.name,self.surname)
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

	def updateUsername(self):

		pass

	#def updateUsername

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
		self.checkData=CheckData(self.currentUserConfig)
		self.checkData.start()
		self.checkData.finished.connect(self._checkDataRet)

	#def _applyUserChanges

	def _checkDataRet(self):

		if self.checkData.ret[0]:
			self.saveDataChanges()
		else:
			self.core.mainStack.closePopUp=[True,""]
			self.showUserFormMessage=[True,self.checkData.ret[1],"Error"]

	#def _checkDataRet

	def saveDataChanges(self):

		self.core.mainStack.closePopUp=[False,SAVE_DATA]
		self.saveData=SaveData(self.currentUserConfig)
		self.saveData.start()
		self.saveData.finished.connect(self._saveDataRet)

	#def saveData

	def _saveDataRet(self):

		if self.saveData.ret[0]:
			self.core.usersOptionsStack._updateUsersModel()
			self.core.usersOptionsStack.showMainMessage=[True,self.saveData.ret[1],"Ok"]
		else:
			self.core.usersOptionsStack.showMainMessage=[True,self.saveData.ret[1],"Error"]	

		self.core.usersOptionsStack.enableGlobalOptions=Bridge.easyLoginManager.checkGlobalOptionStatus()
		self.changesInUser=False
		self.core.mainStack.closeGui=True
		self.core.mainStack.moveToStack=1
		self.core.mainStack.manageGoToStack()
		self.core.mainStack.closePopUp=[True,""]

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


