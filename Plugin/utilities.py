# Import
import sys
import subprocess
import time
import distutils
import datetime
from datetime import datetime
import os
import os.path as path

#------------------------------------------------------------------------------------
class Utilities:
	def __init__(self):
		self.ini_file 		= ""
		self.end_file 		= ""
		self.flagDefine 	= False
		self.listDefine 	= []
		self.file2process 	= ""
		self.file2output 	= ""
		self.cont 			= 0
	#------------------------------------------------------------------------------------
	def deleteParentheses(self,lineTxt):
		listTxt 		= lineTxt.split()
		firstCharacter 	= listTxt[0][0]
		lastCharacter 	= listTxt[len(listTxt)-1][ len(listTxt[len(listTxt) - 1])-1]
		
		if firstCharacter=="(" and lastCharacter==")":
			listTxt[0] 				= listTxt[0][1:]
			listTxt[len(listTxt)-1] = listTxt[len(listTxt)-1][:len(listTxt[len(listTxt)-1]) - 1] 
		#print("firstElement : "+str(listTxt[0]))
		#print("lastElemente : "+str(listTxt[len(listTxt)-1]))
		newLineTxt = " ".join(listTxt)	
		return newLineTxt
	#------------------------------------------------------------------------------------
