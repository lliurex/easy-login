from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import UsersModel

CHANGE_SERVICE_WAITING=10
REMOVING_USER=11
REMOVING_ALL_USERS=12

CHANGE_SERVICE_SUCCESSFULLY=11
CHANGE_SERVICE_ERROR=-10


class EnableLogin(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.enableLogin=args[0]
		self.ret=False

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.enableEasyLogin(self.enableLogin)

	#def run

#class EnableLogin

class RemoveUser(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.allUses=args[0]
		self.userToRemove=args[1]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.easyLoginManager.removeUser(self.allUsers,self.userToRemove)

	#def run

#class RemoveUser


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
		self._filterStatusValue="all"

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

	def _getFilterStatusValue(self):

		return self._filterStatusValue

	#def _getFilterStatusValue

	def _setFilterStatusValue(self,filterStatusValue):

		if self._filterStatusValue!=filterStatusValue:
			self._filterStatusValue=filterStatusValue
			self.on_filterStatusValue.emit()

	#def _setFilterStatusValue

	def _updateUsersModel(self):

		ret=self._usersModel.clear()
		userEntries=Bridge.easyLoginManager.usersConfigData
		for item in userEntries:
			if item["username"]!="":
				self._usersModel.appendRow(item["username"],item["login"],item["name"],item["surname"],item["pwdImg1"],item["pwdImg2"],item["pwdImg3"],item["pwdImg4"],item["metaInfo"])
	
	#def _updateUsersModel

	def _updateUsersModelInfo(self,param):

		updatedInfo=Bridge.easyLoginManager.usersConfigData
		if len(updatedInfo)>0:
			for i in range(len(updatedInfo)):
				index=self._usersModel.index(i)
				self._usersModel.setData(index,param,updatedInfo[i][param])

	#def _updateBellsModelInfo

	@Slot(str)
	def manageStatusFilter(self,value):

		self.filterStatusValue=value

	#def manageStatusFilter

	@Slot(bool)
	def enableEasyLogin(self,value):

		self.core.mainStack.closePopUp=[False,CHANGE_SERVICE_WAITING]
		self.core.usersOptionsStack.showMainMessage=[False,"","Ok"]
		self.enableLogin=EnableLogin(value)
		self.enableLogin.start()
		self.enableLogin.finished.connect(self._enableLoginRet)

	#def enableEasyLogin

	def _enableLoginRet(self):

		self.core.mainStack.closePopUp=[True,""]
		self.easyLoginEnabled=Bridge.easyLoginManager.easyLoginEnabled
		
		if self.enableLogin.ret:
			self.showMainMessage=[True,CHANGE_SERVICE_SUCCESSFULLY,"Ok"]
		else:
			self.showMainMessage=[True,CHANGE_SERVICE_ERROR,"Error"]

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

	#def removeBell

	@Slot(str)
	def manageRemoveUserDialog(self,response):

		self.showRemoveUserDialog=[False,False]
		if response=="Accept":
			self._launchRemoveUserProcess()

	#def manageRemoveBellDialog

	def _launchRemoveUserProcess(self):

		self.core.mainStack.closeGui=False
		if self.removeUserBells:
			self.core.mainStack.closePopUp=[False,REMOVING_ALL_BELLS]
		else:
			self.core.mainStack.closePopUp=[False,REMOVING_BELL]

		self.removeUserProcess=RemoveUser(self.removeAllUsers,self.userToRemove)
		self.removeUserProcess.start()
		self.removeUserProcess.finished.connect(self._removeUserProcessRet)

	#def _launchRemoveBellProcess

	def _removeUserProcessRet(self):

		if self.removeUserProcess.ret[0]:
			self._updateUsesModel()
			self.showMainMessage=[True,self.removeUserProcess.ret[1],"Ok"]
		else:
			self.showMainMessage=[True,self.removeUserProcess.ret[1],"Error"]

		self._manageOptions()
		self.filterStatusValue="all"
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

	#def _removeUserProcessRet

	on_easyLoginEnabled=Signal()
	easyLoginEnabled=Property(bool,_getEasyLoginEnabled,_setEasyLoginEnabled, notify=on_easyLoginEnabled)
	
	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage, notify=on_showMainMessage)
	
	on_showRemoveUserDialog=Signal()
	showRemoveUserDialog=Property('QVariantList',_getShowRemoveUserDialog,_setShowRemoveUserDialog,notify=on_showRemoveUserDialog)

	on_enableGlobalOptions=Signal()
	enableGlobalOptions=Property(bool,_getEnableGlobalOptions,_setEnableGlobalOptions,notify=on_enableGlobalOptions)

	on_filterStatusValue=Signal()
	filterStatusValue=Property(str,_getFilterStatusValue,_setFilterStatusValue,notify=on_filterStatusValue)

	usersModel=Property(QObject,_getUsersModel,constant=True)

#class Bridge

import Core


