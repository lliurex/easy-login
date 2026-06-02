#!/usr/bin/env python3

import os
import subprocess
import n4d.client
import copy
import gettext
import random
import unicodedata
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

gettext.textdomain("easy-login")
_ = gettext.gettext


class EasyLoginManager(object):

	
	LOAD_CONFIG_ERROR=-1
	ADD_NEW_USER_ERROR=-2
	SAVE_NEW_USER_ERROR=-3
	NAME_EMPTY_ERROR=-4
	SURNAME_EMPTY_ERROR=-5
	LOGIN_EMPTY_ERROR=-6
	REMOVE_USER_ERROR=-7
	REMOVE_ALL_USERS_ERROR=-8
	CHANGE_SERVICE_ERROR=-9
	GENERATING_PDF_ERROR=-10
	LOAD_USER_ERROR=-11
	GENERATING_NEW_PWD_ERROR=-12
	EDIT_USER_ERROR=-13
	REMOVE_OLD_USERNAME_ERROR=-14
	ERROR_UPDATING_USER_DATA=-15

	ADD_USER_SUCCESSFULLY=0
	REMOVE_USER_SUCCESSFULLY=2
	CHANGE_SERVICE_SUCCESSFULLY=3
	REMOVE_ALL_USERS_SUCCESSFULLY=4
	GENERATE_PDF_SUCCESSFULLY=5
	EDIT_USER_SUCCESSFULLY=6

	KIRIGAMI_MSG_OK=0
	KIRIGAMI_MSG_ERROR=1
	KIRIGAMI_MSG_WARNING=2
	KIRIGAMI_MSG_INFO=3

	
	def __init__(self):

		super(EasyLoginManager, self).__init__()

		self.dbg=0
		self.credentials=[]
		self.server='localhost'
		self.usersConfigData=[]
		self.easyLoginEnabled=False
		self.missingImgPath="file:///usr/share/easy-login/gui/rsrc/missingImg.png"
		self.pdfName="Easy-Login_Report.pdf"
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
			print(f"[EASYLOGIN]: {function} - {msg}")

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
		self.pwdImgFolders=[self.missingImgPath,self.missingImgPath,self.missingImgPath,self.missingImgPath]
		self.currentUserConfig={
			"username":"",
			"login":"",
			"name":"",
			"surname":"",
			"pwdImgPaths":self.pwdImgFolders,
			"uid":"",
			"customLogin":False
		}
		
	#def initValues	

	def loadConfig(self):
		
		try:
			getStatus=self.client.EasyLogin.get_status_service()
			if getStatus!="None":
				self.easyLoginEnabled=getStatus
			
			configParams=self.client.EasyLogin.get_config()
			self.pwdImgFolder=configParams.get("theme").get("path")

			return self._getUsersInfo()
		except Exception as e:
			self._debug("loadConfig",f"Error loading config: {e}")
			return {"status":False,"code":EasyLoginManager.LOAD_CONFIG_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}
		
	#def readConf

	def _getUsersInfo(self):

		try:
			self.usersConfig=self.client.EasyLogin.get_user_list()
			self.usersConfigData=[]
			
			for username,info in self.usersConfig.items():
				self._setUsersData(username,info)
			
			self.usersConfigData.sort(key=lambda x: x['login'].lower())
			
			return {"status":True,"code":"","type":EasyLoginManager.KIRIGAMI_MSG_OK}

		except Exception as e:
			self._debug("_getUsersInfo",f"Error getting users info: {e}")
			return {"status":False,"code":EasyLoginManager.LOAD_CONFIG_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

	#def _getUsersInfo	

	def _setUsersData(self,username,info):

		tmpData={
			"username":username,
			"login":info["login"],
			"name":info["name"],
			"surname":info["surname"],
			"metaInfo":f"{info['login']} {info['name']} {info['surname']}",
			"pwdImgPaths":self._getImgFromUsername(username)
		}

		self.usersConfigData=[item for item in self.usersConfigData if item.get("username")!=username]
		self.usersConfigData.append(tmpData)

	#def _setUsersData

	def _getImgFromUsername(self,username):

		tmpImgs=list(username)
		tmpImgData=[]
		i=1
		for item in tmpImgs:
			tmpPath=os.path.join(self.pwdImgFolder,f"{item}.png")

			if not os.path.exists(tmpPath):
				tmpPath=self.missingImgPath
			else:
				tmpPath=f"file://{tmpPath}"
			tmpImgData.append(tmpPath)
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

		try:
			username=self.client.EasyLogin.get_valid_username()
			tmpImgPath=self._getImgFromUsername(username)
			
			return {"status":True,"code":"","type":EasyLoginManager.KIRIGAMI_MSG_OK,"data":{"username":username,"pwdImgPaths":tmpImgPath}}
		except:
			return {"status":False,"code":EasyLoginManager.GENERATING_NEW_PWD_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR,"data":{}}

	#def generateUsername

	def loadUserConfig(self,newUser,infoToLoad):

		if newUser:
			getUsername=self.generateUsername()
			if getUsername.get("status"):
				self.currentUserConfig["username"]=getUsername.get("data").get("username")
				self.currentUserConfig["pwdImgPaths"]=getUsername.get("data").get("pwdImgPaths")
				return {"status":True,"code":"","type":EasyLoginManager.KIRIGAMI_MSG_OK}
			else:
				return {"status":False,"code":EasyLoginManager.ADD_NEW_USER_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}
		else:
			username=infoToLoad.get("username")
			self.currentUserConfig=self.usersConfig.get(username,{})
			if len(self.currentUserConfig)>0:
				self.currentUserConfig["username"]=username
				self.currentUserConfig["pwdImgPaths"]=[]
				self.currentUserConfig["pwdImgPaths"]=infoToLoad.get("pwdImgPaths")
				self.currentUserConfig["customLogin"]=self._lookingForCustomLogin()
				return {"status":True,"code":"","type":EasyLoginManager.KIRIGAMI_MSG_OK}
		
			return {"status":False,"code":EasyLoginManager.LOAD_USER_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

	#def loadUserConfig

	def _lookingForCustomLogin(self):

		defaultLogin=self.getFormattedLogin(self.currentUserConfig["name"],self.currentUserConfig["surname"])
		login=self.currentUserConfig["login"].replace(".easy","")

		if defaultLogin!=login:
			return True

		return False

	#def _lookingForCustomLogin

	def enableEasyLogin(self, enableLogin):

		try:
			ret=self.client.EasyLogin.set_status_service(enableLogin)
			self.easyLoginEnabled=enableLogin
			return {"status":True,"code":EasyLoginManager.CHANGE_SERVICE_SUCCESSFULLY,"type":EasyLoginManager.KIRIGAMI_MSG_OK}
		except Exception as e:
			self._debug("enableEasyLogin",f"Error changing status: {e}")
			return {"status":False,"code":EasyLoginManager.CHANGE_SERVICE_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

	#def enableEasyLogin

	def checkData(self,dataToCheck):

		name=dataToCheck.get("name","")
		surname=dataToCheck.get("surname","")
		login=dataToCheck.get("login","")

		if name!="" and surname!="" and login !="":
			return {"status":True,"code":"","type":EasyLoginManager.KIRIGAMI_MSG_OK}

		if name=="":
			return {"status":False,"code":EasyLoginManager.NAME_EMPTY_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}
		
		if surname=="":
			return {"status":False,"code":EasyLoginManager.SURNAME_EMPTY_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

		if login=="":
			return {"status":False,"code":EasyLoginManager.LOGIN_EMPTY_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

	#def checkData

	def saveNewUser(self,dataToSave):

		username=dataToSave.get("username")
		info={}
		info["name"]=dataToSave.get("name")
		info["surname"]=dataToSave.get("surname")
		info["login"]=dataToSave.get("login").replace(".easy",'')
		info["uid"]=dataToSave.get("uid")

		try:
			ret=self.client.EasyLogin.store_id_user(username,info)
			if ret:
				retUpdateData=self._updateUserData(username)
				if retUpdateData.get("status"):				
					return {"status":True,"code":EasyLoginManager.ADD_USER_SUCCESSFULLY,"type":EasyLoginManager.KIRIGAMI_MSG_OK}
				else:
					return retUpdateData
		except Exception as e:
			self._debug("saveNewUser",f"Error saving data: {e}")
			return {"status":False,"code":EasyLoginManager.SAVE_NEW_USER_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}


	#def saveNewUser
	
	def saveEditData(self, dataToSave):

		username=dataToSave.get("username")
		usernameOrig=self.currentUserConfig.get("username")
		updateUsername=False
		info={}
		info["name"]=dataToSave.get("name")
		info["surname"]=dataToSave.get("surname")
		info["login"]=dataToSave.get("login").replace(".easy",'')
		info["uid"]=dataToSave.get("uid")

		if username!=usernameOrig:
			updateUsername=True

		try:
			ret=self.client.EasyLogin.store_id_user(username,info)
			if ret:
				retUpdateData=self._updateUserData(username)
				if retUpdateData.get("status"):	
					if updateUsername:			
						retRemove=self.removeSingleUser(usernameOrig)
					
						if not retRemove.get("status"):
							return {"status":False,"code":EasyLoginManager.REMOVE_OLD_USERNAME_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_OK}

					return {"status":True,"code":EasyLoginManager.EDIT_USER_SUCCESSFULLY,"type":EasyLoginManager.KIRIGAMI_MSG_OK}

				else:
					return retUpdateData
		except Exception as e:
			self._debug("saveEditData",f"Error saving data: {e}")
			return {"status":False,"code":EasyLoginManager.EDIT_USER_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

	#def saveEditData

	def _updateUserData(self,username):

		try:
			userData=self.client.EasyLogin.load_user(username)
			self.usersConfig[username]=userData
			self._setUsersData(username,userData)
			self.usersConfigData.sort(key=lambda x: x['login'].lower())

			return {"status":True,"code":'',"type":''}
		except Exception as e:
			self._debug("_updateUserData",f"Error updating user data:{e}")
			return {"status":False,"code":EasyLoginManager.ERROR_UPDATING_USER_DATA,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

	#def _updateUserData
	
	def removeSingleUser(self,userToRemove):

		msgOk=EasyLoginManager.REMOVE_USER_SUCCESSFULLY
		try:
			ret=self.client.EasyLogin.remove_entry(userToRemove)
			self._popUserFromData(userToRemove)
			return {"status":True,"code":msgOk,"type":EasyLoginManager.KIRIGAMI_MSG_OK}
		except n4d.client.CallFailedError as e:
			self._debug("removeUser",f"Error removing user: {e}")
			return {"status":False,"code":EasyLoginManager.REMOVE_USER_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}
	
	#def removeSingleUser

	def removeAllUsers(self):

		msgOk=EasyLoginManager.REMOVE_ALL_USERS_SUCCESSFULLY
		try:
			ret=self.client.EasyLogin.wipe_db()
			self.usersConfig={}
			self.usersConfigData=[]
			return {"status":True,"code":msgOk,"type":EasyLoginManager.KIRIGAMI_MSG_OK}
		except n4d.client.CallFailedError as e:
			self._debug("removeAllUsers",f"Error removing all users: {e}")
			return {"status":False,"code":EasyLoginManager.REMOVE_ALL_USERS_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

	#def removeAllUsers

	def _popUserFromData(self,username):

		self.usersConfig.pop(username)
		self.usersConfigData=[item for item in self.usersConfigData if item.get("username")!=username]

	#def _popUserFromData

	def getFormattedLogin(self,name,surname):

		tmpLogin=f"{name}{surname}"
		tmpLogin=tmpLogin.replace(" ","")
		tmpLogin=unicodedata.normalize('NFD',tmpLogin)

		normalizedLogin=re.sub(r'[^a-zA-Z0-9]','',tmpLogin).lower()

		return normalizedLogin

	#def getFormattedLogin

	def generatePdf(self,exportPath):

		pdfFile=exportPath
		doc = SimpleDocTemplate(
			pdfFile,
			pagesize=A4,
			rightMargin=40,
			leftMargin=40,
			topMargin=40,
			bottomMargin=40
		)

		styles = getSampleStyleSheet()
		cell_style=styles["Normal"]
		cell_style.alignment=0

		story = []

		pdfTitle = Paragraph("EASY-LOGIN", styles['Title'])
		story.append(pdfTitle)
		story.append(Spacer(1, 20))

		pdfData=[[_("LOGIN"),_("STUDENT"),_("PASSWORD")]]

		for item in self.usersConfigData:
			tmpLogin=Paragraph(f"{item.get('login')}",cell_style)
			tmpName=Paragraph(f"{item.get('name')} {item.get('surname')}",cell_style)
			imgObjects = []
			paths = item.get("pwdImgPaths", [])
			for p in paths:
				img_path = p.replace("file://", "")
				if os.path.exists(img_path):
					imgObjects.append(Image(img_path, width=32, height=32))
				else:
					imgObjects.append("N/A")

			if not imgObjects:
				imgObjects = ["N/A"]
				
			imgTable = Table([imgObjects], colWidths=[35]*len(imgObjects)) 
			
			imgTable.setStyle(TableStyle([
				('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
				('ALIGN', (0,0), (-1,-1), 'CENTER'),
			]))
			pdfData.append([tmpLogin,tmpName,imgTable])

		tmpTable = Table(pdfData, colWidths=[170,150,160], repeatRows=1)
		pdfStyle = TableStyle([
			('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
			('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
			('FONTSIZE', (0, 0), (-1, 0), 12),
			
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
			('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
			('FONTSIZE', (0, 1), (-1, -1), 10),
			('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ced3d7')]),		
			('BOTTOMPADDING', (0, 0), (-1, -1), 10),
			('TOPPADDING', (0, 0), (-1, -1), 10),
			
		])
		
		tmpTable.setStyle(pdfStyle)
		story.append(tmpTable)

		try:
			doc.build(story)
			subprocess.run(["xdg-open",pdfFile])
			return {"status":True,"code":EasyLoginManager.GENERATE_PDF_SUCCESSFULLY,"type":EasyLoginManager.KIRIGAMI_MSG_OK}
		except Exception as e:
			self._debug("generatePdf",f"Error generating pdf: {e}")
			return {"status":False,"code":EasyLoginManager.GENERATING_PDF_ERROR,"type":EasyLoginManager.KIRIGAMI_MSG_ERROR}

	#def generatePdf

#class EasyLoginManager 		
