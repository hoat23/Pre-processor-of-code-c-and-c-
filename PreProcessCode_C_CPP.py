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
# Global vars
#------------------------------------------------------------------------------------
ini_file 		= ""
end_file 		= ""
flagDefine 		= False
listDefine 		= []
file2process 	= ""
file2output 	= ""
#------------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------------
def deleteParentheses(lineTxt):
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
def deleteCommit(lineTxt):
	ind_comentario = getIndex(lineTxt,"//")
	if ind_comentario>-1:
		return lineTxt[:ind_comentario]
	else:
		return lineTxt
#------------------------------------------------------------------------------------
def getDefine(lineTxt):
	listTxt = deleteCommit(lineTxt).split()
	m=0
	listDefine=[]
	if(len(listTxt)>2):
		for n in range(0,len(listTxt)):
			if(listTxt[n]=="defined") and ( n+1<len(listTxt) ):
				n=n+1
				listDefine.append(deleteParentheses(listTxt[n]))
	else:
		listDefine.append( deleteParentheses(listTxt[1]) )
	#print("listDefine : "+str(len(listDefine)))
	return listDefine[0]
#------------------------------------------------------------------------------------
def getIndex(cadena,subCad):
	try:
		idx = cadena.index(subCad)
		return idx
	except ValueError:
		return -1
#------------------------------------------------------------------------------------
def thereIs(lineTxt , cadena2compare):
	listTxt = lineTxt.split()
	if len(listTxt)>0:
		newLineTxt = listTxt[0]
	else:
		newLineTxt = lineTxt
	ind_find 			= getIndex(newLineTxt, cadena2compare)
	ind_comentario_01	= getIndex(newLineTxt, '//')
	if ind_find>=0 and (ind_find<ind_comentario_01 or ind_comentario_01==-1) :
		return True
	else:
		return False
#------------------------------------------------------------------------------------
def pre_processLineTxt(lineTxt, cadena):
	listTxt = lineTxt.split()
	idx 	= getIndex(listTxt[0][0:1],cadena)
	if idx==-1:
		return False
	else:
		return True
#------------------------------------------------------------------------------------
def defineIsON(nameDefine):
	for n in range(0,len(listDefine)) :
		if(nameDefine==listDefine[n]):
			return True
	return False
#------------------------------------------------------------------------------------
def processDefine(lineTxt,writeON):
	global ini_file
	global end_file

	nameDefine = getDefine(lineTxt)
	print("Process... ["+nameDefine+"]")
	flagDefine = defineIsON(nameDefine)
	flagElse   = False
	flagWrite  = False
	while True:
		lineTxt = ini_file.readline()
		
		if (flagDefine and not(flagElse)) or (not(flagDefine) and flagElse):
			flagWrite = True
		if (flagDefine and flagElse):
			flagWrite = False

		if thereIs(lineTxt,"#else"):
			flagWrite= False
			flagElse = True
		if thereIs(lineTxt,"#endif"):
			break
		if thereIs(lineTxt,"#if"):
			processDefine(lineTxt,flagWrite and writeON)
		else:
			if flagWrite and writeON:
				end_file.write(lineTxt)
	return
#------------------------------------------------------------------------------------
def converter_code(nameSourceCode):
	global ini_file
	global end_file
	ini_file = open(nameSourceCode,"r")
	end_file = open(file2output,"w")
	if path.exists(nameSourceCode):
		lineTxt = ini_file.readline()
		while lineTxt != "":
			if thereIs(lineTxt,"#if"):
				processDefine(lineTxt,True)
			else:
				end_file.write(lineTxt)
			lineTxt = ini_file.readline()

		ini_file.close()
		end_file.close()
	else:
		print("converter_code - NOT FOUND FILE ["+nameSourceCode+"]")
	return
#------------------------------------------------------------------------------------
def load_list_define(nameFile):
	try:
		file_defines = open(nameFile,"r")
		lineTxt = file_defines.readline()
		n=0
		while lineTxt != "":
			lineTxt = file_defines.readline()
			if thereIs(lineTxt,"#define"):
				nameDefine = getDefine(lineTxt)
				n=n+1
				print("\t"+str(n)+": "+nameDefine)
				listDefine.append(nameDefine)
	except IOError as e:
		print(str(e))
	return
#------------------------------------------------------------------------------------
def checkArg():
	global file2process
	global file2output

	if (len(sys.argv) < 2):
		printInfo2Use()
		quit()

	file2process 	= sys.argv[1]
	if (len(sys.argv) == 1):
		file2output = "output.c"
	else:
		file2output = sys.argv[2]
#------------------------------------------------------------------------------------
def printInfo2Use():
	print("-------------------------------------------------------------------------------")
	print("PreProcessCode [fileInput.c] [fileOutput.c]")
	print("\t fileInput.c   -> Name file to process.")
	print("\t fileOutput.c  -> Name file to save process.")
	print(" ")
####################################### Main #######################################
print("   Pre-procesador de codigo C/C++ ")
print("   Autor 		: Deiner Zapata Silva")
print("   Start Time 		: " + datetime.now().strftime('%H:%M:%S'))
print("-------------------------------------------------------------------------------")
checkArg()
print("   Processing <"+file2process+">")
print("-------------------------------------------------------------------------------")
print("   Reading <defines.h>:")
load_list_define("defines.h")
print("-------------------------------------------------------------------------------")
converter_code(file2process)
print("-------------------------------------------------------------------------------")
print("   End Time 		:" + datetime.now().strftime('%H:%M:%S'))
