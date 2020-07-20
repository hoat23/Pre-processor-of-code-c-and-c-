#############################################################################################################
# OPCIONES DE COMPILADO
ADK_STATIC=1     # 1:Compilado con librerias estaticas  0:Compilado con librerias dinámicas
#############################################################################################################
# SETEANDO RUTAS
#############################################################################################################
# Setting vars from APP
strAppName = democlient
strPlatform = VOS2
# Setting vars for VOS2
strToolChainPath = C:/toolchains/windows/vos2
strSDKPath = C:/toolchains/vos2-sdk-winx86-release-30410400
strSDKLibPath = $(strSDKPath)/usr/local/lib
strSDKIncludes = $(strSDKPath)/usr/local/include
strADKPath = C:/toolchains/adk-full-ext-4.2.0-138/vos2
strCompilerPath = C:/toolchains/windows/vos2/gcc-linaro-arm-linux-gnueabihf-4.7-2013.03/bin/arm-linux-gnueabihf-g++.exe
strLinkerPath   = $(strCompilerPath)
strCompilerOptions = -c -Wno-write-strings -D__VOS_DEBUG -D__arm -pthread -DTIXML_USE_STL -Wall
strLinkerOptions = --sysroot=$(strSDKPath) -Wl,-rpath=$(strSDKPath)/usr/lib -Wl,-rpath=$(strSDKPath)/usr/local/lib -Wl,-rpath=$(strSDKPath)/lib -Wl,-rpath=$(strSDKPath)/usr/local/lib/svcmgr
# -fpermissive
#############################################################################################################
# Configuration file for using the XML library in GNOME applications : \usr\lib\xml2Conf.sh
XML2_SDK_LIB = $(strSDKPath)/usr/lib
XML2_SDK_INCL= $(strSDKPath)/usr/include/libxml2
#
XML2_LIBDIR=-L/usr/lib
XML2_LIBS=-lxml2 -lz   -lm 
XML2_INCLUDEDIR=-I/usr/include/libxml2
MODULE_VERSION=xml2-2.9.1
#
#############################################################################################################
#  SETEANDO VARIABLES DE ENTORNO
#############################################################################################################
APP_NAME = $(strAppName)
PLATFORM = $(strPlatform)				#No usado
SDK_PATH = $(strSDKPath)				#No usado
SDK_LIB_PATH = $(strSDKLibPath)
SDK_INCLUDES = $(strSDKIncludes)
EOS_INCLUDES = $(strEOSIncludes)
ADK_PATH = $(strADKPath)
COMPILER = $(strCompilerPath)
LINKER = $(strLinkerPath)
COPTIONS = $(strCompilerOptions)
LOPTIONS = $(strLinkerOptions)
#############################################################################################################
SOURCE_DIR=src
OBJ_DIR=obj
OUT_DIR=out

TARGET_FILE=$(APP_NAME)
TASKS_LIB = -ltestSO
EOS_INCLUDES =

ADK_LIB_PATH=$(ADK_PATH)/lib
ADK_INCLUDES= $(ADK_PATH)/include
ADK_LIBS= 	-lrt -lvfiplatforminfo -lsvc_utility -lvfibuzzer -lsvc_powermngt -lsvc_led -lvfisvc -lsvc_logmgr -lvfiipc -lsqlite -linf -linf_util -llog -llogapi -llogstream -lmsr

#LOG -dynamic library: -lsvc_logmgr -lvfiipc -llogapi         -llogstream
#LOG -static  library: -lsvc_logmgr -lvfiipc /liblog-static.a /liblogstream-static.a

#GUI -dynamic library: -lvfiguiprt     -lvfiipc
#GUI -static  library: /libvfiguiprt.a /libvfiipc.a 

#SQLITE BASIC -dynamic library: -lsqlite
#SQLITE BASIC -static  library: -libsqlite-static.a

#SQLITE XML -dynamic library: -linf -linf_util
#SQLITE XML -static  library: libibinf-static.a libibinf_util_sqlite-static.a lib_util_xmlfile-static.a

ADK_LIBS_STATIC =  $(ADK_LIB_PATH)\libvfisysinfo.a  $(ADK_LIB_PATH)\libvfiguiprt.a  $(ADK_LIB_PATH)\libvfiipc.a  $(ADK_LIB_PATH)\libfltkgui.a 

SOURCES := $(wildcard SRC/*.cpp) $(wildcard SRC/**/*.cpp)
APP_OBJECTS := $(patsubst %.cpp, %.o, ${SOURCES})
APP_OBJECTSX := $(addprefix $(OBJ_DIR)/, $(patsubst %.cpp, %.o, $(notdir ${SOURCES})))
CFLAGS := -DVFI_POSIX_IMPORT -DVFI_GUIPRT_IMPORT -DVFI_IPC_DLL_IMPORT -DVFI_PLATFORM_VOS2 -D_VOS2 -DLOGAPI_ENABLE_DEBUG 
# CFLAGS := -DVFI_PLATFORM_VOS -D_VOS -Wall <warnings visibles>

$(OUT_DIR)\$(TARGET_FILE) : $(APP_OBJECTS)
	@echo Linking... $(TARGET_FILE)
	@$(LINKER) -o $(OUT_DIR)\$(TARGET_FILE) $(LOPTIONS) $(APP_OBJECTSX) $(ADK_LIBS_STATIC) -pthread -lpthread -L$(SDK_LIB_PATH) -L$(SDK_LIB_PATH)\svcmgr $(SDK_LIBS) -L$(XML2_SDK_LIB) $(XML2_LIBS) -L$(ADK_LIB_PATH)  $(ADK_LIBS)

$(APP_OBJECTS) : %.o : %.cpp
	@echo Compiling $<
	@$(COMPILER) $(COPTIONS) $(CFLAGS) -I$(SDK_INCLUDES) -I$(XML2_SDK_INCL) -I$(ADK_INCLUDES)  -o $(OBJ_DIR)\$(notdir $@) $<
