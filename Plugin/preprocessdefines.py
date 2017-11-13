# Import
import sys
import subprocess
import time
import distutils
import datetime
from datetime import datetime
import os
import os.path as path
from User.utilities import Utilities

#------------------------------------------------------------------------------------
class PreProcessDefines:
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
	def deleteCommit(self,lineTxt):
		ind_comentario = self.getIndex(lineTxt,"//")
		if ind_comentario>-1:
			return lineTxt[:ind_comentario]
		else:
			return lineTxt
	#------------------------------------------------------------------------------------
	def evalSimpleConditional(self,lineTxt):
		listOperador = ["&&","||"]
		flagCond = False
		#print("evalSimpleConditional["+lineTxt+"]")
		for n_oper in range(0,len(listOperador)):
			operador = listOperador[n_oper]
			idx_oper = self.getIndex(lineTxt,operador)
			if (idx_oper!=-1) :
				def01 = lineTxt[0:idx_oper]
				def02 = lineTxt[idx_oper+len(operador):len(lineTxt)]
				flagCond=True
				#print("evalSimpleConditional - True ["+def01+"]"+"["+def02+"]")
				rpt1 = self.evalSimpleConditional(def01)
				rpt2 = self.evalSimpleConditional(def02)
				if(operador=="||"):
					rpt = rpt1 or rpt2 
					return rpt
				if(operador=="&&"):
					rpt = rpt1 and rpt2
					return rpt
		if (flagCond==False):
			#print("evalSimpleConditional["+lineTxt+"]")
			if(lineTxt=="True"):
				return True
			if(lineTxt=="False"):
				return False
			return self.defineIsON(lineTxt)
	#------------------------------------------------------------------------------------
	def evalConditional(self,milineTxt):
		flagCond = False
		idx_ini = -1
		idx_fin = -1
		lineTxt = milineTxt
		while(self.getIndex(lineTxt,")")!=-1 and self.cont<23):
			self.cont = self.cont + 1
			for n in range(0,len(lineTxt)):
				if lineTxt[n]=='(':
					idx_ini = n
				if lineTxt[n]==')':
					idx_fin = n
				if( idx_ini!=-1 and idx_fin!=-1 and flagCond==False):
					flagCond=True
					break
			if (flagCond==True):
				firstPart = lineTxt[0:idx_ini]
				mediumPart= lineTxt[idx_ini+1:idx_fin]
				secondPart= lineTxt[idx_fin+1:len(lineTxt)]
				#print("firstPart ["+firstPart+"]")
				#print("mediumPart["+mediumPart+"]")
				#print("secondPart["+secondPart+"]")
				rpt = self.defineIsON(mediumPart)
				lineTxt = firstPart+str(rpt)+secondPart
				#print("newLine["+lineTxt+"]")
				idx_ini = -1
				idx_fin = -1
				flagCond = False
		rpt = self.evalSimpleConditional(lineTxt)
		print("Process... ["+milineTxt+"] -> "+str(rpt))
		return rpt
	#------------------------------------------------------------------------------------
	def multiDefIsON(self,lineTxt):
		#Suponiendo camino feliz :-)
		lineTxt = self.deleteCommit(lineTxt)
		lineTxt = lineTxt.replace("\n","")
		idx_def = self.getIndex(lineTxt,"defined")
		rpt = False
		if(idx_def!=-1):
			lineTxt = lineTxt[idx_def+len("defined"):len(lineTxt)]
			lineTxt = lineTxt.replace(" ","") #deleting whitespaces
			#print("multiDefIsON["+lineTxt+"]")
			rpt = self.evalConditional(lineTxt)
		else:
			nameDefine = self.getDefine(lineTxt)
			rpt = self.defineIsON(nameDefine)
			print("Process... ["+nameDefine+"] --> "+str(rpt) )
		return rpt
	#------------------------------------------------------------------------------------
	def getDefine(self,lineTxt):
		listTxt = self.deleteCommit(lineTxt).split()
		#listTxt = self.multiDefIsON(lineTxt)
		m=0
		listDefineLocal=[]
		if(len(listTxt)>2):
			for n in range(0,len(listTxt)):
				if(listTxt[n]=="defined") and ( n+1<len(listTxt) ):
					n=n+1
					listDefineLocal.append(self.deleteParentheses(listTxt[n]))
		else:
			listDefineLocal.append( self.deleteParentheses(listTxt[1]) )
		#print("listDefine : "+str(len(listDefineLocal)))
		return listDefineLocal[0]
	#------------------------------------------------------------------------------------
	def getIndex(self,cadena,subCad):
		try:
			idx = cadena.index(subCad)
			return idx
		except ValueError:
			return -1
	#------------------------------------------------------------------------------------
	def thereIs(self,lineTxt , cadena2compare):
		listTxt = lineTxt.split()
		if len(listTxt)>0:
			newLineTxt = listTxt[0]
		else:
			newLineTxt = lineTxt
		ind_find 			= self.getIndex(newLineTxt, cadena2compare)
		ind_comentario_01	= self.getIndex(newLineTxt, '//')
		if ind_find>=0 and (ind_find<ind_comentario_01 or ind_comentario_01==-1) :
			return True
		else:
			return False
	#------------------------------------------------------------------------------------
	def pre_processLineTxt(self,lineTxt, cadena):
		listTxt = lineTxt.split()
		idx 	= self.getIndex(listTxt[0][0:1],cadena)
		if idx==-1:
			return False
		else:
			return True
	#------------------------------------------------------------------------------------
	def defineIsON(self,nameDefine):
		for n in range(0,len(self.listDefine)) :
			if(nameDefine==self.listDefine[n]):
				return True
		return False
	#------------------------------------------------------------------------------------
	def processDefine(self,lineTxt,writeON):
		flagDefine = self.multiDefIsON(lineTxt)
		flagElse   = False
		flagWrite  = False
		while True:
			lineTxt = self.ini_file.readline()
			
			if (flagDefine and not(flagElse)) or (not(flagDefine) and flagElse):
				flagWrite = True
			if (flagDefine and flagElse):
				flagWrite = False

			if self.thereIs(lineTxt,"#else"):
				flagWrite= False
				flagElse = True
			if self.thereIs(lineTxt,"#endif"):
				break
			if self.thereIs(lineTxt,"#if"):
				self.processDefine(lineTxt,flagWrite and writeON)
			else:
				if flagWrite and writeON:
					self.end_file.write(lineTxt)
		return
	#------------------------------------------------------------------------------------
	def converter_code(self,fullPathFile,dirFile):
		self.ini_file = open(fullPathFile,"r")
		self.end_file = open(dirFile+"/output.c","w")
		if path.exists(fullPathFile):
			lineTxt = self.ini_file.readline()
			while lineTxt != "":
				if self.thereIs(lineTxt,"#if"):
					self.processDefine(lineTxt,True)
				else:
					self.end_file.write(lineTxt)
				lineTxt = self.ini_file.readline()
			print("Closing files")
			self.ini_file.close()
			self.end_file.close()
		else:
			print("converter_code - NOT FOUND FILE ["+fullPathFile+"]")
		return
	#------------------------------------------------------------------------------------
	def load_list_defines(self,nameFile,dirFile):
		try:
			file_defines = open(dirFile+"\\"+nameFile,"r")
			lineTxt = file_defines.readline()
			n=0
			while lineTxt != "":
				lineTxt = file_defines.readline()
				if self.thereIs(lineTxt,"#define"):
					nameDefine = self.getDefine(lineTxt)
					n=n+1
					print("\t"+str(n)+": "+nameDefine)
					self.listDefine.append(nameDefine)

		except IOError as e:
			print(str(e))
		return
	#------------------------------------------------------------------------------------
	