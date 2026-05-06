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

	
	LOAD_USERS_ERROR=-1
	ADD_USER_ERROR=-2
	EDIT_USER_ERROR=-3
	NAME_EMPTY_ERROR=-4
	SURNAME_EMPTY_ERROR=-5
	LOGIN_EMPTY_ERROR=-6
	REMOVE_USER_ERROR=-7
	REMOVE_ALL_USERS_ERROR=-8

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
			return self._getUsersInfo()
		except Exception as e:
			return [False,EasyLoginManager.LOAD_USERS_ERROR]
		
	#def readConf

	def _getUsersInfo(self):

		try:
			tmpConfig=self.client.EasyLogin.get_user_list()
			self.usersConfig=dict(sorted(tmpConfig.items(), key=lambda item:item[1]['login']))
			self._getUsersData()
			return [True,""]
		except Exception as e:
			return [False,EasyLoginManager.LOAD_USERS_ERROR]

	#def _getUsersInfo	

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
			else:
				tmpPath=f"file://{tmpPath}"
			tmpImgData[f"pwdImg{i}"]=tmpPath
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
		tmpImgPath=self._getImgFromUsername(username)
		
		return [True,username,tmpImgPath]

	#def generateUsername

	def loadUserConfig(self,newUser,infoToLoad):

		if newUser:
			getUsername=self.generateUsername()
			if getUsername[0]:
				self.currentUserConfig["username"]=getUsername[1]
				self.currentUserConfig["pwdImgPaths"][0]=getUsername[2].get("pwdImg1",self.missingImgPath)
				self.currentUserConfig["pwdImgPaths"][1]=getUsername[2].get("pwdImg2",self.missingImgPath)
				self.currentUserConfig["pwdImgPaths"][2]=getUsername[2].get("pwdImg3",self.missingImgPath)
				self.currentUserConfig["pwdImgPaths"][3]=getUsername[2].get("pwdImg4",self.missingImgPath)
				return True
			else:
				return False
		else:
			username=infoToLoad[0]
			self.currentUserConfig=self.usersConfig.get(username,{})

			if len(self.currentUserConfig)>0:
				self.currentUserConfig["username"]=username
				self.currentUserConfig["pwdImgPaths"]=[]
				self.currentUserConfig["pwdImgPaths"]=infoToLoad[1]
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
				retInfo=self._getUsersInfo()
				if retInfo[0]:
					return [True,EasyLoginManager.ADD_USER_SUCCESSFULLY]
				else:
					return retInfo
		except Exception as e:
			print(str(e))
			return [False,EasyLoginManager.ADD_USER_ERROR]

	#def saveData

	def removeUser(self,allUsers,userToRemove):

		if allUsers:
			try:
				ret=self.client.EasyLogin.wipe_db()
			except n4d.client.CallFailedError as e:
				print(str(e))
				return [False,EasyLoginManager.REMOVE_ALL_USERS_ERROR]
		else:
			try:
				ret=self.client.EasyLogin.remove_entry(userToRemove)
			except n4d.client.CallFailedError as e:
				print(str(e))
				return [False,EasyLoginManager.REMOVE_USER_ERROR]
		
		retInfo=self._getUsersInfo()
		
		if retInfo[0]:
			if allUsers:
				return [True.EasyLoginManager.REMOVE_ALL_USERS_SUCCESSFULLY]
			else:
				return [True,EasyLoginManager.REMOVE_USER_SUCCESSFULLY]

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
		cell_style.aligment=0

		story = []

		pdfTitle = Paragraph("EASY-LOGIN", styles['Title'])
		story.append(pdfTitle)
		story.append(Spacer(1, 20))

		pdfData=[[_("NAME"),_("LOGIN"),_("PASSWORD")]]

		for item in self.usersConfigData:
			tmpName=Paragraph(f"{item.get("name")} {item.get("surname")}",cell_style)
			tmpLogin=Paragraph(f"{item.get("login")}",cell_style)
			imgPaths=[]
			imgPaths.append(f"{item.get("pwdImg1").replace("file://","")}")
			imgPaths.append(f"{item.get("pwdImg2").replace("file://","")}")
			imgPaths.append(f"{item.get("pwdImg3").replace("file://","")}")
			imgPaths.append(f"{item.get("pwdImg4").replace("file://","")}")

			imgObjects=[]
			for img in imgPaths:
				if os.path.exists(img):
					imgObjects.append(Image(img,width=32,height=32))
				else:
					imgObjects.append("N/A")

			imgTable = Table([imgObjects], colWidths=[35]*len(imgObjects)) 
			imgTable.setStyle(TableStyle([
				('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
				('ALIGN', (0,0), (-1,-1), 'CENTER'),
			]))
			pdfData.append([tmpName,tmpLogin,imgTable])

		tmpTable = Table(pdfData, colWidths=[150,150,180], repeatRows=1)
		pdfStyle = TableStyle([
			('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
			('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
			('FONTSIZE', (0, 0), (-1, 0), 12),
			
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
			('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
			('FONTSIZE', (0, 1), (-1, -1), 10),
			
			('BOTTOMPADDING', (0, 0), (-1, -1), 10),
			('TOPPADDING', (0, 0), (-1, -1), 10),
			
		])
		
		tmpTable.setStyle(pdfStyle)
		story.append(tmpTable)

		try:
			doc.build(story)
			subprocess.run(["xdg-open",pdfFile])
			return True
		except Exception as e:
			print(e)
			return False

	#def generatePdf

#class EasyLoginManager 		
