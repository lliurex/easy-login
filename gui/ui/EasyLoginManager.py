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
	SAVE_USER_ERROR=-3
	NAME_EMPTY_ERROR=-4
	SURNAME_EMPTY_ERROR=-5
	LOGIN_EMPTY_ERROR=-6
	REMOVE_USER_ERROR=-7
	REMOVE_ALL_USERS_ERROR=-8
	CHANGE_SERVICE_ERROR=-9
	GENERATING_PDF_ERROR=-10
	LOAD_USER_ERROR=-11
	GENERATING_NEW_PWD_ERROR=-12

	ADD_USER_SUCCESSFULLY=0
	REMOVE_USER_SUCCESSFULLY=2
	CHANGE_SERVICE_SUCCESSFULLY=3
	REMOVE_ALL_USERS_SUCCESSFULLY=4
	GENERATE_PDF_SUCCESSFULLY=5

	
	def __init__(self):

		super(EasyLoginManager, self).__init__()

		self.dbg=0
		self.credentials=[]
		self.server='localhost'
		self.usersConfigData=[]
		self.easyLoginEnabled=False
		self.pwdImgFolder="/usr/share/easy-login/themes/animals"
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
			return self._getUsersInfo()
		except Exception as e:
			self._debug("loadConfig",f"Error loading config: {e}")
			return {"status":False,"code":EasyLoginManager.LOAD_CONFIG_ERROR,"type":"Error"}
		
	#def readConf

	def _getUsersInfo(self):

		try:
			tmpConfig=self.client.EasyLogin.get_user_list()
			self.usersConfig=dict(sorted(tmpConfig.items(), key=lambda item:item[1]['login']))
			self._getUsersData()
			return {"status":True,"code":"","type":"Ok"}

		except Exception as e:
			self._debug("_getUsersInfo",f"Error getting users info: {e}")
			return {"status":False,"code":EasyLoginManager.LOAD_CONFIG_ERROR,"type":"Error"}

	#def _getUsersInfo	

	def _getUsersData(self):

		self.usersConfigData=[]

		for username,info in self.usersConfig.items():
			tmpData={}
			tmpData["username"]=username
			tmpData["login"]=info["login"]
			tmpData["name"]=info["name"]
			tmpData["surname"]=info["surname"]
			tmpData["metaInfo"]=f"{tmpData['login']} {tmpData['name']} {tmpData['surname']}"
			tmpData["pwdImgPaths"]=self._getImgFromUsername(username)
			self.usersConfigData.append(tmpData)

	#def _getUsersData

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

		username="".join(str(random.randint(0,8)) for _ in range(0,4))
		tmpImgPath=self._getImgFromUsername(username)
	
		return {"status":True,"code":"","type":"Ok","data":{"username":username,"pwdImgPaths":tmpImgPath}}

	#def generateUsername

	def loadUserConfig(self,newUser,infoToLoad):

		if newUser:
			getUsername=self.generateUsername()
			if getUsername.get("status"):
				self.currentUserConfig["username"]=getUsername.get("data").get("username")
				self.currentUserConfig["pwdImgPaths"]=getUsername.get("data").get("pwdImgPaths")
				return {"status":True,"code":"","type":"Ok"}
			else:
				return {"status":False,"code":EasyLoginManager.ADD_NEW_USER_ERROR,"type":"Error"}
		else:
			username=infoToLoad[0]
			self.currentUserConfig=self.usersConfig.get(username,{})

			if len(self.currentUserConfig)>0:
				self.currentUserConfig["username"]=username
				self.currentUserConfig["pwdImgPaths"]=[]
				self.currentUserConfig["pwdImgPaths"]=infoToLoad[1]
				return {"status":True,"code":"","type":"Ok"}
		
			return {"status":False,"code":EasyLoginManager.LOAD_USER_ERROR,"type":"Error"}

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
			
			return {"status":True,"code":EasyLoginManager.CHANGE_SERVICE_SUCCESSFULLY,"type":"Ok"}
		except Exception as e:
			self._debug("enableEasyLogin",f"Error changing status: {e}")
			return {"status":False,"code":EasyLoginManager.CHANGE_SERVICE_ERROR,"type":"Error"}

	#def enableEasyLogin

	def checkData(self,dataToCheck):

		name=dataToCheck.get("name","")
		surname=dataToCheck.get("surname","")
		login=dataToCheck.get("login","")

		if name!="" and surname!="" and login !="":
			return {"status":True,"code":"","type":"Ok"}

		if name=="":
			return {"status":False,"code":EasyLoginManager.NAME_EMPTY_ERROR,"type":"Error"}
		
		if surname=="":
			return {"status":False,"code":EasyLoginManager.SURNAME_EMPTY_ERROR,"type":"Error"}

		if login=="":
			return {"status":False,"code":EasyLoginManager.LOGIN_EMPTY_ERROR,"type":"Error"}

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
				retInfo=self._getUsersInfo()
				if retInfo.get("status"):
					return {"status":True,"code":EasyLoginManager.ADD_USER_SUCCESSFULLY,"type":"Ok"}
				else:
					return retInfo
		except Exception as e:
			self._debug("saveData",f"Error saving data: {e}")
			return {"status":False,"code":EasyLoginManager.SAVE_USER_ERROR,"type":"Error"}

	#def saveData

	def removeUser(self,allUsers,userToRemove):

		if allUsers:
			msgOk=EasyLoginManager.REMOVE_ALL_USERS_SUCCESSFULLY
			try:
				ret=self.client.EasyLogin.wipe_db()
			except n4d.client.CallFailedError as e:
				self._debug("removeUser",f"Error removing all users: {e}")
				return {"status":False,"code":EasyLoginManager.REMOVE_ALL_USERS_ERROR,"type":"Error"}
		else:
			msgOk=EasyLoginManager.REMOVE_USER_SUCCESSFULLY
			try:
				ret=self.client.EasyLogin.remove_entry(userToRemove)
			except n4d.client.CallFailedError as e:
				self._debug("removeUser",f"Error removing user: {e}")
				return {"status":False,"code":EasyLoginManager.REMOVE_USER_ERROR,"type":"Error"}
		
		retInfo=self._getUsersInfo()
		
		if retInfo.get("status"):
			return {"status":True,"code":msgOk,"type":"Ok"}
	
		return retInfo


	#def removeUser

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
			return {"status":True,"code":EasyLoginManager.GENERATE_PDF_SUCCESSFULLY,"type":"Ok"}
		except Exception as e:
			self._debug("generatePdf",f"Error generating pdf: {e}")
			return {"status":False,"code":EasyLoginManager.GENERATING_PDF_ERROR,"type":"Error"}

	#def generatePdf

#class EasyLoginManager 		
