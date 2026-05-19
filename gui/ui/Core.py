#!/usr/bin/env python3

import sys

import EasyLoginManager
import UserStack
import UsersOptionsStack
import MainStack

class Core:
	
	singleton=None
	DEBUG=False
	
	@classmethod
	def get_core(cls):
		
		if cls.singleton==None:
			cls.singleton=Core()
			cls.singleton.init()

		return cls.singleton
		
	
	def __init__(self,args=None):

		self.dprint("Init...")
		
	#def __init__
	
	def init(self):

		self.easyLoginManager=EasyLoginManager.EasyLoginManager()
		self.userStack=UserStack.Bridge()
		self.usersOptionsStack=UsersOptionsStack.Bridge()
		self.mainStack=MainStack.Bridge()
		
		self.mainStack.initBridge()
	
		
	#def init

	def dprint(self,msg):
		
		if Core.DEBUG:
			
			print("[CORE] %s"%msg)
	
	#def  dprint

#class Core
