#!/usr/bin/env python3

import os
import subprocess
import n4d.client
import copy
import gettext
import random
import unicodedata
import re

gettext.textdomain("easy-login")
_ = gettext.gettext


class EasyLoginManager(object):

	
	LOAD_USERS_ERROR=-1
	ADD_USER_ERROR=-2
	EDIT_USER_ERROR=-3
	NAME_EMPTY_ERROR=-4
	SURNAME_EMPTY_ERROR=-5
	LOGIN_EMPTY_ERROR=-6

	ADD_USER_SUCCESSFULLY=0
	EDIT_USER_SUCCESSFULLY=1
	REMOVE_USER_SUCCESSFULLY=2
	
	def __init__(self):

		super(EasyLoginManager, self).__init__()

		self.dbg=0
		self.credentials=[]
		self.server='localhost'
		self.usersConfigData=[]
		self.easyLoginEnabled=False
		self.pwdImgFolder="/usr/share/easy-login/themes/animals"
		self.missingImgPath="file:///usr/share/easy-login/gui/rsc/missingImg.png"
		self._getSystemLocale()
		self.initValues()

	#def __init__	

	def createN4dClient(self,ticket):

		ticket=ticket.replace('##U+0020##',' ')
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk,timeout=120)

	#def createN4dClient

	def _debug(self,function,msg):

		if self.dbg==1:
			print("[EASYLOGIN]: "+ str(function) + str(msg))

	#def _debug	

	def _getSystemLocale(self):

		language=os.environ["LANGUAGE"]

		if language!="":
			tmpLang=language.split(":")
			self.systemLocale=tmpLang[0]
		else:
			self.systemLocale=os.environ["LANG"]

	#def _getSystemLocale

	def initValues(self):

		self.userToLoad=""
		self.currentUserConfig={}
		self.pwdImgFolders=[self.missingImgPath,self.missingImgPath,self.missingImgPath,self.missingImgPath]
		self.currentUserConfig["username"]=""
		self.currentUserConfig["login"]=""
		self.currentUserConfig["name"]=""
		self.currentUserConfig["surname"]=""
		self.currentUserConfig["pwdImgPaths"]=self.pwdImgFolders

	#def initValues	

	def loadConfig(self):
		
		try:
			getStatus=self.client.EasyLogin.get_status_service()
			if getStatus!="None":
				self.easyLoginEnabled=getStatus
	
			self.usersConfig=self.client.EasyLogin.get_user_list()
			self._getUsersData()
			return [True,""]
		except Exception as e:
			print(str(e))
			return [False,EasyLoginManager.LOAD_USERS_ERROR]
		
	#def readConf	

	def _getUsersData(self):

		self.usersConfigData=[]

		for username,info in self.usersConfig.items():
			tmpData={}
			tmpData["username"]=username
			tmpData["login"]=info["login"]
			tmpData["name"]=info["name"]
			tmpData["surname"]=info["surname"]
			tmpData["metaInfo"]=f"{tmpData["login"]} {tmpData["name"]} {tmpData["surname"]}"
			tmpData.update(self._getImgFromUsername(username))
			self.usersConfigData.append(tmpData)

	#def _getUsersData

	def _getImgFromUsername(self,username):

		tmpImgs=list(username)
		tmpImgData={}
		i=1
		for item in tmpImgs:
			tmpPath=os.path.join(self.pwdImgFolder,f"{item}.png")

			if not os.path.exists(tmpPath):
				tmpPath=self.missingImgPath
			tmpImgData[f"pwdImg{i}"]=f"file://{tmpPath}"
			i+=1

		return tmpImgData

	#def _getImgFromUsername

	def checkGlobalOptionStatus(self):

		if len(self.usersConfig)>0:
			return True
		else:
			return False

	#def checkGlobalOptionStatus

	def generateUsername(self):

		tmpUsername=random.randint(0,8888)
		username=f"{tmpUsername:04}"

		self.currentUserConfig["username"]=username
		tmpImgPath=self._getImgFromUsername(username)
		self.currentUserConfig["pwdImgPaths"][0]=tmpImgPath.get("pwdImg1",self.missingImgPath)
		self.currentUserConfig["pwdImgPaths"][1]=tmpImgPath.get("pwdImg2",self.missingImgPath)
		self.currentUserConfig["pwdImgPaths"][2]=tmpImgPath.get("pwdImg3",self.missingImgPath)
		self.currentUserConfig["pwdImgPaths"][3]=tmpImgPath.get("pwdImg4",self.missingImgPath)

		return True

	#def generateUsername

	def loadUserConfig(self,userToLoad):

		self.currentUserConfig=self.usersConfig.get(userToLoad,{})
		if len(self.currentUserConfig)>0:
			self.currentUserConfig["username"]=userToLoad
			self.currentUserConfig.update(self._getImgFromUsername(userToLoad))
			return True

		return False

	#def loadUserConfig

	def enableEasyLogin(self, enableLogin):

		try:
			ret=self.client.EasyLogin.set_status_service(enableLogin)
			self.easyLoginEnabled=enableLogin
			getStatus=self.client.EasyLogin.get_status_service()
			if getStatus:
				self.easyLoginEnabled:True
			else:
				self.easyLoginEnabled:False
			
			return True
		except Exception as e:
			print(str(e))
			return False

	#def enableEasyLogin

	def checkData(self,dataToCheck):

		name=dataToCheck.get("name","")
		surname=dataToCheck.get("surname","")
		login=dataToCheck.get("login","")

		if name!="" and surname!="" and login !="":
			return [True,""]

		if name=="":
			return [False,EasyLoginManager.NAME_EMPTY_ERROR]
		
		if surname=="":
			return [False,EasyLoginManager.SURNAME_EMPTY_ERROR]

		if login=="":
			return [False,EasyLoginManager.LOGIN_EMPTY_ERROR]

	#def checkData

	def saveData(self, dataToSave):

		username=dataToSave.get("username","")
		info={}
		info["name"]=dataToSave.get("name","")
		info["surname"]=dataToSave.get("surname","")
		info["login"]=dataToSave.get("login","")

		try:
			ret=self.client.EasyLogin.store_id_user(username,info)
			if ret:
				self.usersConfig=self.client.EasyLogin.get_user_list()
				self._getUsersData()
			return [True,EasyLoginManager.ADD_USER_SUCCESSFULLY]
		except Exception as e:
			print(str(e))
			return [False,EasyLoginManager.ADD_USER_ERROR]

	#def saveData

	def removeUser(self,allUsers,userToRemove):

		pass

	#def removeUser

	def getFormattedLogin(self,name,surname):

		tmpLogin=f"{name}{surname}"
		tmpLogin=tmpLogin.replace(" ","")
		tmpLogin=unicodedata.normalize('NFD',tmpLogin)

		normalizedLogin=re.sub(r'[^a-zA-Z0-9]','',tmpLogin).lower()

		return normalizedLogin

	#def getFormattedLogin

#class EasyLoginManager 		
