#!/usr/bin/python3
import os
import sys
from PySide6 import QtCore, QtGui, QtQml

class UsersModel(QtCore.QAbstractListModel):

	UsernameRole= QtCore.Qt.UserRole + 1000
	LoginRole = QtCore.Qt.UserRole+1001
	NameRole= QtCore.Qt.UserRole + 1002
	SurnameRole = QtCore.Qt.UserRole+1003
	PwdImg1Role = QtCore.Qt.UserRole+1004
	PwdImg2Role = QtCore.Qt.UserRole+1005
	PwdImg3Role = QtCore.Qt.UserRole+1006
	PwdImg4Role = QtCore.Qt.UserRole+1007
	MetaInfoRole = QtCore.Qt.UserRole+1008
	
	def __init__(self,parent=None):
		
		super(UsersModel, self).__init__(parent)
		self._entries =[]
	
	#def __init__

	def rowCount(self, parent=QtCore.QModelIndex()):
		
		if parent.isValid():
			return 0
		return len(self._entries)

	#def rowCount

	def data(self, index, role=QtCore.Qt.DisplayRole):
		
		if 0 <= index.row() < self.rowCount() and index.isValid():
			item = self._entries[index.row()]
			if role == UsersModel.UsernameRole:
				return item["username"]
			elif role == UsersModel.LoginRole:
				return item["login"]
			elif role == UsersModel.NameRole:
				return item["name"]
			elif role == UsersModel.SurnameRole:
				return item["surname"]
			elif role == UsersModel.PwdImg1Role:
				return item["pwdImg1"]
			elif role == UsersModel.PwdImg2Role:
				return item["pwdImg2"]
			elif role == UsersModel.PwdImg3Role:
				return item["pwdImg3"]
			elif role == UsersModel.PwdImg4Role:
				return item["pwdImg4"]				
			elif role == UsersModel.MetaInfoRole:
				return item["metaInfo"]			
	#def data

	def roleNames(self):
		
		roles = dict()
		roles[UsersModel.UsernameRole] = b"username"
		roles[UsersModel.LoginRole]= b"login"
		roles[UsersModel.NameRole] = b"name"
		roles[UsersModel.SurnameRole] = b"surname"
		roles[UsersModel.PwdImg1Role] = b"pwdImg1"
		roles[UsersModel.PwdImg2Role] = b"pwdImg2"
		roles[UsersModel.PwdImg3Role] = b"pwdImg3"
		roles[UsersModel.PwdImg4Role] = b"pwdImg4"
		roles[UsersModel.MetaInfoRole]=b"metaInfo"


		return roles

	#def roleNames

	def appendRow(self,username,login,name,surname,pwdImg1,pwdImg2,pwdImg3,pwdImg4,metaInfo):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["username"])
		tmpN=username.strip()
		if username not in tmpId and username !="" and len(tmpN)>0:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(username=username,login=login,name=name,surname=surname,pwdImg1=pwdImg1,pwdImg2=pwdImg2,pwdImg3=pwdImg3,pwdImg4=pwdImg4,metaInfo=metaInfo))
			self.endInsertRows()

	#def appendRow

	def removeRow(self,index):
		self.beginRemoveRows(QtCore.QModelIndex(),index,index)
		self._entries.pop(index)
		self.endRemoveRows()
	
	#def removeRow

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class UsersModel
