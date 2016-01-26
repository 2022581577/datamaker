# -*- coding:utf-8 -*-
import sys
import os
import time
import xdrlib
import xlrd
reload(sys)
sys.setdefaultencoding('utf-8') 

TYPENO = 'NO'
BASETYPE = ['DOUBLE', 'SERVER', 'CLIENT']	#暂时没有判断是否需要导出
BASESERVERTYPE = ['DOUBLE', 'SERVER']
VALUEDOUBLETYPE = ['INT', 'STRING', 'TERM', 'NUMBER']
VALUESERVERTYPE = ['INT.S', 'STRING.S', 'TERM.S', 'NUMBER.S']
VALUECLIENTTYPE = ['INT.C', 'STRING.C', 'TERM.C', 'NUMBER.C']

#获取目录中指定的文件名 
#>>>FlagStr=['F','EMS','txt'] #要求文件名称中包含这些字符 
#>>>FileList=GetFileList(FindPath,FlagStr) # 
def get_file_list(path, flagStr = [], notFlagStr = []):
	import os 
	fileList=[] 
	fileNames = os.listdir(path) 
	if (len(fileNames)>0): 
		for fn in fileNames: 
			if (len(flagStr) > 0): 
				#返回指定类型的文件名 
				if is_sub_string(flagStr, fn) and not_sub_string(notFlagStr, fn): 
					fullfilename = os.path.join(path, fn) 
					fileList.append(fullfilename) 
			else: 
				#默认直接返回所有文件名 
				fullfilename=os.path.join(path,fn) 
				fileList.append(fullfilename)
	return fileList
	
#判断字符串Str是否包含序列SubStrList中的每一个子字符串 
#>>>SubStrList=['F','EMS','txt'] 
#>>>Str='F06925EMS91.txt' 
#>>>IsSubString(SubStrList,Str)#return True (or False) 
def is_sub_string(subStrList, str): 
	flag = True
	for substr in subStrList: 
		if not(substr in str): 
			flag = False
	return flag 
	
def not_sub_string(subStrList, str): 
	flag = True
	for substr in subStrList: 
		if (substr in str): 
			flag = False
	return flag 


class MakeData:
	def __init__(self, excel_file, server_path, client_path, log_path, time_str):
		self.excel_file = excel_file.decode('utf-8')
		self.server_path = (server_path + '\server\\').decode('utf-8')
		self.client_path = (client_path + '\client\\').decode('utf-8')
		self.log_path = (log_path + '\log\\').decode('utf-8')
		self.time_str = time_str
		self.excel = self.excel_analyze()	# 获取数据
		self.error_flag = False
	
	def error_flag(self):
		return self.error_flag
	
	def write_data(self):
		#写服务端文件
		if self.excel != None:
			self.write_server()
		else:
			print 'no excel!'
	
	#获取excel中的数据 mine
	#excel结构{'fileName':dataXXX, 'sheetList':sheet列表}
	#sheetList结构[sheet1, sheet2 ...](针对有数据的) 
	#sheet结构{'valueType':valueList, 'valueName':valueList, 'valueNotes':valueList, 'values':valueListList} valueList即为每行数据列表
	def excel_analyze(self):
		sheetList = []
		fileName = ""

		data = self.open_excel()
		if data != None:
			nsheets = data.nsheets
			for nsheet in range(0, nsheets):
				table = data.sheets()[nsheet]
				nrows = table.nrows #行数
				if nrows >= 3:	
				
					dictSheet = {'sheetNum':nsheet, 'valueType':[], 'valueName':[], 'valueNotes':[], 'values':[]}
					valueListList = []

					for nrow in range(0, nrows):
						valueList =  table.row_values(nrow) #某一行数据 
						if nrow == 0:	#第一行
							if valueList[0] not in BASETYPE:
								break
							else:
								dictSheet['valueType'] = valueList
						elif nrow == 1:	#第二行
							fileName = valueList[0]
							dictSheet['valueName'] = valueList
						elif nrow == 2:	#第三行
							dictSheet['valueNotes'] = valueList
						else:
							if valueList[0] == 'YES':
								valueListList.append(valueList)
					if valueListList != []:
						dictSheet['values'] = valueListList
						sheetList.append(dictSheet)
			excel = {'fileName':fileName, 'sheetList':sheetList}
			return excel
	
	#打开excel
	def open_excel(self):
		try:
			data = xlrd.open_workbook(self.excel_file)
			return data
		except Exception:	#可以记日志
			logStr = '打开excel有误,文件名:' + self.excel_file + '\n\n'
			self.server_log(logStr)
		
	#写服务端文件
	def write_server(self):
		sheetList = self.excel['sheetList']
		serverSheetList = []
		for sheet in sheetList:
			valueType = sheet['valueType']
			if valueType[0] in BASESERVERTYPE:
				serverSheetList.append(sheet)
		self.excel['sheetList'] = serverSheetList
		if len(self.excel['sheetList']) > 0:
			#写.hrl文件
			self.write_server_hrl()
			#写.erl文件
			self.write_server_erl()

	#写服务端头文件
	def write_server_hrl(self):
		fileName = self.excel['fileName']
		valueType = self.excel['sheetList'][0]['valueType']
		valueName = self.excel['sheetList'][0]['valueName']
		valueNotes = self.excel['sheetList'][0]['valueNotes']
		tplName = fileName.replace('data_', 'tpl_', 1)
		tplFileName = tplName+'.hrl'
		
		hrlHead = self.server_hrl_head(tplName, tplFileName)
		body = self.server_hrl_body(tplName, valueType, valueName, valueNotes)
		hrlTail = self.server_hrl_tail()
		writeStr = hrlHead + body + hrlTail
		
		server_path = self.server_path + 'tpl\\'
		if os.path.isdir(server_path):
			pass
		else:
			os.makedirs(server_path)
		fp = open(server_path + tplFileName, 'w')
		fp.write(writeStr)
		fp.close()

	#头文件头部
	def server_hrl_head(self, tplName, tplFileName):
		tplNameSuper = tplName.upper() + '_HRL'
		return '-ifndef('+ tplNameSuper + ').\n' + '-define(' + tplNameSuper + ', "' + tplFileName + '").\n\n'
		
	#头文件内容
	def server_hrl_body(self, tplName, valueType, valueName, valueNotes):
		bodyHead = '-record(' + tplName + ', {\n'
		boydMin = ''
		for i in range(1, len(valueType)):
			type = valueType[i]
			serverType = VALUEDOUBLETYPE + VALUESERVERTYPE
			if type in serverType:
				if i == 1:
					boydMin = boydMin + '				' + valueName[i] + '				%% ' + valueNotes[i] + '\n'
				else:
					boydMin = boydMin + '				,' + valueName[i] + '				%% ' + valueNotes[i] + '\n'
		bodyTail = '}).\n\n'
		body = bodyHead + boydMin + bodyTail
		return body

	#头文件尾部
	def server_hrl_tail(self):
		return '-endif.'
		
	#写服务端erl文件
	#excel结构{'fileName':dataXXX, 'sheetList':sheet列表}
	#sheetList结构[sheet1, sheet2 ...](针对有数据的) 
	#sheet结构{'valueType':valueList, 'valueName':valueList, 'valueNotes':valueList, 'values':valueListList} valueList即为每行数据列表
	def write_server_erl(self):
		fileName = self.excel['fileName']
		tplName = fileName.replace('data_', 'tpl_', 1)
		erlFileName = fileName+'.erl'
		
		erlHead = self.server_erl_head(fileName)
		body = self.server_erl_body(tplName)
		writeStr = erlHead + body
		server_path = self.server_path + 'erl\\'
		if os.path.isdir(server_path):
			pass
		else:
			os.makedirs(server_path)
		fp = open(server_path + erlFileName, 'w')
		fp.write(writeStr)
		fp.close()
		
	#erl文件头部
	def server_erl_head(self, fileName):
		module = '-module(' + fileName + ').\n\n'
		include = '-include("' + fileName + '.hrl").\n\n'
		compile = '-compile(export_all).\n\n'
		return module + include + compile

	#erl文件体
	def server_erl_body(self, tplName):
		sheetList = self.excel['sheetList']
		getKey = ''
		getKeyList = 'get_list() ->\n	['
		getKeyListBySheet = ''
		for i in range(0, len(sheetList)):
			valueType = self.excel['sheetList'][i]['valueType']
			valueName = self.excel['sheetList'][i]['valueName']
			sheet = sheetList[i]
			valueListList = sheet['values']
			keyOfSheet = str(i + 1)
			getKeyListBySheet = getKeyListBySheet + 'get_list(' + keyOfSheet + ') ->\n	['
			for j in range(0, len(valueListList)):
				valueList = valueListList[j]
				dictKeyFun = self.server_erl_fun_get(tplName, valueType, valueName, valueList)
				key = dictKeyFun['key']
				funGet = dictKeyFun['funGet']
				getKey = getKey + funGet
				if i == 0 and j == 0:
					getKeyList = getKeyList + key
				else:
					getKeyList = getKeyList + ', ' + key
				if j == 0:
					getKeyListBySheet = getKeyListBySheet + key
				else:
					getKeyListBySheet = getKeyListBySheet + ', ' + key
			getKeyListBySheet = getKeyListBySheet + '];\n'
		getTail = self.server_erl_get_tail()
		getKey = getKey + getTail
		getKeyList = getKeyList + '].\n\n'
		if len(sheetList) == 1:
			getKeyListBySheet = ''
		else:
			getKeyListBySheet = getKeyListBySheet + 'get_list(_) -> [].\n\n'
		return getKey + getKeyList + getKeyListBySheet

	#erl解析每行数据，返回Key和对应的get(Key)函数
	def server_erl_fun_get(self, tplName, valueType, valueName, ValueList):
		funGet = ''
		key = ''
		for i in range(1, len(valueType)):
			type = valueType[i]
			serverType = VALUEDOUBLETYPE + VALUESERVERTYPE
			if type in serverType:
				fromatValue = self.server_format_value(type, ValueList[i], key, valueName[i])
				if fromatValue != None:
					if funGet == '':
						key = fromatValue
						funGet = funGet + 'get(' + fromatValue + ') ->\n' + '	#' + tplName + '{\n' + '		' + valueName[i] + ' = ' + fromatValue + '\n'
					else:
						funGet = funGet + '		,' + valueName[i] + ' = ' + fromatValue + '\n'
		funGet = funGet + '		};\n'
		return {'key':key, 'funGet': funGet}

	# 后续需要加上判断值类型是否对应
	def server_format_value(self, type, value, key, name):
		try:
			if type.find('STRING') != -1:
				return '<<"' + str(value) + '">>'
			elif type.find('TERM') != -1:
				try:
					long(value)
				except:	#就是为term类型
					return str(value)
				else:	#值类型
					return str(long(value))
			elif type.find('INT') != -1:
				if value == '':
					return str(0)
				else:
					return str(long(value))
			elif type.find('NUMBER') != -1:
				if value == '':
					return str(0)
				else:
					return str(value)
			else:
				return str(value)
		except Exception:	#可以记日志
			logStr = '数值有误,文件名:' + self.excel_file + \
					', key:' + key + ', name:' + name + ', type:' + type + ', value:' + value + '\n\n'
			self.server_log(logStr)

	#erl文件get函数的尾部
	def server_erl_get_tail(self):
		return 'get(_) ->\n	false.\n\n'
		
	#写日志
	def server_log(self, str):
		self.error_flag = True
		if os.path.isdir(self.log_path):
			pass
		else:
			os.makedirs(self.log_path)
		server_log_file = self.log_path + 'log_server_' + self.time_str
		fp = open(server_log_file, 'a')
		fp.write(str)
		fp.close()

def main(file = {'isPath':0, 'file': '测试.xlsx'}, server_path='C:\Users\Administrator\Desktop\\', client_path='C:\Users\Administrator\Desktop\\', log_path='C:\Users\Administrator\Desktop\\'):
	time_str = time.strftime('%Y%m%d%H%M%S')
	error_flag = False
	if file['isPath'] == 0:
		_make_data = MakeData(file['file'], server_path, client_path, log_path, time_str)
		_make_data.write_data()
		error_flag = _make_data.error_flag
	else:
		excelPath = file['file'].decode('utf-8')
		excelList = get_file_list(excelPath, ['.xlsx'], ['~$'])
		for excel_file in excelList:
			_make_data = MakeData(excel_file, server_path, client_path, log_path, time_str)
			_make_data.write_data()
			if not error_flag:
				error_flag = _make_data.error_flag
	return error_flag

if __name__=="__main__":
	main()