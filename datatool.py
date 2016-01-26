# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

#from PyQt4 import QtCore, QtGui
import sys
import os
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
import make_data
reload(sys)
sys.setdefaultencoding('utf-8') 

try:
	_fromUtf8 = QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QApplication.translate(context, text, disambig)

class StandardDialog(QDialog):  
	def __init__(self,parent=None):  
		super(StandardDialog,self).__init__(parent)
		
		self.path = os.getcwd()
		self.initUi()
		self.retranslateUi()
		self.connect(self.pushButton_excel, SIGNAL(_fromUtf8("clicked()")), self.excel_dir) #excel目录
		self.connect(self.pushButton_client, SIGNAL(_fromUtf8("clicked()")), self.client_dir)
		self.connect(self.pushButton_server, SIGNAL(_fromUtf8("clicked()")), self.server_dir)
		self.connect(self.pushButton_log, SIGNAL(_fromUtf8("clicked()")), self.log_dir)
		self.connect(self.pushButton_single, SIGNAL(_fromUtf8("clicked()")), self.single_make) #单个导出
		self.connect(self.pushButton_all, SIGNAL(_fromUtf8("clicked()")), self.all_make) #批量导出
		
	def initUi(self):
		self.setObjectName(_fromUtf8("Dialog"))
		self.resize(423, 219)
		self.label_excle = QLabel(self)
		self.label_excle.setGeometry(QRect(30, 30, 90, 20))
		self.label_excle.setObjectName(_fromUtf8("label_excle"))
		self.label_client = QLabel(self)
		self.label_client.setGeometry(QRect(30, 60, 90, 16))
		self.label_client.setObjectName(_fromUtf8("label_client"))
		self.label_server = QLabel(self)
		self.label_server.setGeometry(QRect(30, 90, 90, 16))
		self.label_server.setObjectName(_fromUtf8("label_server"))
		self.label_log = QLabel(self)
		self.label_log.setGeometry(QRect(30, 120, 90, 16))
		self.label_log.setObjectName(_fromUtf8("label_log"))
		self.textBrowser_excel = QTextBrowser(self)
		self.textBrowser_excel.setGeometry(QRect(120, 30, 191, 20))
		self.textBrowser_excel.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textBrowser_excel.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textBrowser_excel.setReadOnly(False)
		self.textBrowser_excel.setObjectName(_fromUtf8("textBrowser_excel"))
		self.textBrowser_client = QTextBrowser(self)
		self.textBrowser_client.setGeometry(QRect(120, 60, 191, 20))
		self.textBrowser_client.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textBrowser_client.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textBrowser_client.setReadOnly(False)
		self.textBrowser_client.setObjectName(_fromUtf8("textBrowser_client"))
		self.textBrowser_server = QTextBrowser(self)
		self.textBrowser_server.setGeometry(QRect(120, 90, 191, 20))
		self.textBrowser_server.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textBrowser_server.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textBrowser_server.setReadOnly(False)
		self.textBrowser_server.setObjectName(_fromUtf8("textBrowser_server"))
		self.textBrowser_log = QTextBrowser(self)
		self.textBrowser_log.setGeometry(QRect(120, 120, 191, 20))
		self.textBrowser_log.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textBrowser_log.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textBrowser_log.setReadOnly(False)
		self.textBrowser_log.setObjectName(_fromUtf8("textBrowser_log"))
		self.pushButton_excel = QPushButton(self)
		self.pushButton_excel.setGeometry(QRect(320, 30, 75, 20))
		self.pushButton_excel.setObjectName(_fromUtf8("pushButton_excel"))
		self.pushButton_all = QPushButton(self)
		self.pushButton_all.setGeometry(QRect(220, 160, 121, 30))
		self.pushButton_all.setObjectName(_fromUtf8("pushButton_all"))
		self.pushButton_single = QPushButton(self)
		self.pushButton_single.setGeometry(QRect(70, 160, 121, 30))
		self.pushButton_single.setObjectName(_fromUtf8("pushButton_single"))
		self.pushButton_log = QPushButton(self)
		self.pushButton_log.setGeometry(QRect(320, 120, 75, 20))
		self.pushButton_log.setObjectName(_fromUtf8("pushButton_log"))
		self.pushButton_server = QPushButton(self)
		self.pushButton_server.setGeometry(QRect(320, 90, 75, 20))
		self.pushButton_server.setObjectName(_fromUtf8("pushButton_server"))
		self.pushButton_client = QPushButton(self)
		self.pushButton_client.setGeometry(QRect(320, 60, 75, 20))
		self.pushButton_client.setObjectName(_fromUtf8("pushButton_client"))
		
	def retranslateUi(self):
		self.setWindowTitle(_translate("Dialog", "数据生成工具", None))
		self.label_excle.setText(_translate("Dialog", "excel文件路径：", None))
		self.label_client.setText(_translate("Dialog", "前端保存路径：", None))
		self.label_server.setText(_translate("Dialog", "后端保存路径：", None))
		self.label_log.setText(_translate("Dialog", "日志保存路径：", None))
		self.pushButton_excel.setText(_translate("Dialog", "选择", None))
		self.pushButton_log.setText(_translate("Dialog", "选择", None))
		self.pushButton_server.setText(_translate("Dialog", "选择", None))
		self.pushButton_client.setText(_translate("Dialog", "选择", None))
		self.pushButton_all.setText(_translate("Dialog", "批量导出", None))
		self.pushButton_single.setText(_translate("Dialog", "单个导出", None))
		self.textBrowser_excel.setText(_translate("Dialog", self.path, None))
		self.textBrowser_client.setText(_translate("Dialog", self.path, None))
		self.textBrowser_server.setText(_translate("Dialog", self.path, None))
		self.textBrowser_log.setText(_translate("Dialog", self.path, None))
		
	def excel_dir(self):
		dir = QFileDialog.getExistingDirectory(self, _translate("Dialog", "选择文件夹", None), self.path)
		self.textBrowser_excel.setText(_translate("Dialog", str(dir), None))
		print "text:", _translate("Dialog", str(self.textBrowser_excel.toPlainText()), None)
		
	def client_dir(self):
		dir = QFileDialog.getExistingDirectory(self, _translate("Dialog", "选择文件夹", None), self.path)
		self.textBrowser_client.setText(_translate("Dialog", str(dir), None))
		print "text:", _translate("Dialog", str(self.textBrowser_client.toPlainText()), None)
		
	def server_dir(self):
		dir = QFileDialog.getExistingDirectory(self, _translate("Dialog", "选择文件夹", None), self.path)
		self.textBrowser_server.setText(_translate("Dialog", str(dir), None))
		print "text:", _translate("Dialog", str(self.textBrowser_server.toPlainText()), None)
		
	def log_dir(self):
		dir = QFileDialog.getExistingDirectory(self, _translate("Dialog", "选择文件夹", None), self.path)
		self.textBrowser_log.setText(_translate("Dialog", str(dir), None))
		print "text:", _translate("Dialog", str(self.textBrowser_log.toPlainText()), None)
		
	def single_make(self):  
		excel_dir = str(self.textBrowser_excel.toPlainText())
		s = QFileDialog.getOpenFileName(self, _translate("Dialog", "选择需导出的文件", None), _translate("Dialog", excel_dir, None), "Excel files(*.xlsx)")
		if str(s) != '':
			server_dir = str(self.textBrowser_server.toPlainText())
			client_dir = str(self.textBrowser_client.toPlainText())
			log_dir = str(self.textBrowser_log.toPlainText())
			error_flag = make_data.main({'isPath':0, 'file':str(s)}, server_dir, client_dir, log_dir)
			print 'error_flag:', error_flag
			#弹完成提示框
			if error_flag:
				self.msg("数据有误，请检查错误日志")
			else:
				self.msg("导出完成")
	
	def all_make(self):
		excel_dir = str(self.textBrowser_excel.toPlainText())
		server_dir = str(self.textBrowser_server.toPlainText())
		client_dir = str(self.textBrowser_client.toPlainText())
		log_dir = str(self.textBrowser_log.toPlainText())
		print 'dir:', excel_dir, ';', server_dir, ';', client_dir, ';', log_dir
		error_flag = make_data.main({'isPath':1, 'file':str(excel_dir)}, server_dir, client_dir, log_dir)
		print 'error_flag:', error_flag
		#弹完成提示框
		if error_flag:
			self.msg("数据有误，请检查错误日志")
		else:
			self.msg("导出完成")
			
	def msg(self, msg):  
		QMessageBox.information(self, _translate("Dialog", "完成", None), _translate("Dialog", msg, None), QMessageBox.Ok)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	form=StandardDialog()
	form.show() 
	sys.exit(app.exec_())

