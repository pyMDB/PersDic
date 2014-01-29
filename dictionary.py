#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SCRIPT: PERSDIC
# AUTHOR: Kasra Ahmadvand // kasra.ahmadvand@gmail.com
# DATE:   2013/7/20
# REV:    1.1.0.T (Valid are A, B, T and P)
#         (For Alpha, Beta, Test and Production)
#
# PLATFORM: (SPECIFY: all linux distros)
#
#
# PURPOSE: Make a offline persisan dictionary for linux   
#                 
#               
#
# REV LIST:
#       DATE: 
#       BY:
#       MODIFICATION: 
#
##########################################################
########### DEFINE FILES AND VARIABLES:###################
#Generic_English_Persian.m2 : a free word data base ! 
#
##########################################################
##########################################################
############### FUNCTIONS: ###################
#
##########################################################
##########################################################

import sqlite3 as lite
import sys,codecs
import string 
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QFrame, QPalette
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QColor, QPixmap
dic1={}
a=''
item=2

#import data from database

con = lite.connect('data/Generic_English_Persian.m2')
with con:    
    cur = con.cursor()    
    cur.execute("SELECT * FROM word")
    rows = cur.fetchall()
    for row in rows:
      for i in range(len(row)):
       if isinstance(row[i], unicode):
        if item>0:
         val=row[i].encode('utf8')
         item=-item
        else :
         dic1[val]=row[i].encode('utf8')
         item=-item

lito=dic1.keys()

#classes and other objects 

class InputDialog(QtGui.QWidget):
 def __init__(self, parent=None):
  QtGui.QWidget.__init__(self, parent)
  lbl3 = QtGui.QLabel('Enter yor word here !', self)
  lbl3.move(134,13)
  self.setGeometry(500,700,500,600)
  self.setWindowTitle('Tiny Dictionary')
  self.button = QtGui.QPushButton('Translate',self)
  self.button.setIconSize(QtCore.QSize(183,30))
  #self.button.setFocusPolicy(QtCore.Qt.NoFocus)
  self.button.move(135,80)
  self.connect(self.button, QtCore.SIGNAL('clicked()'), self.insert)
  self.button1= QtGui.QPushButton('Update Translete', self)
  self.button1.move(10,560)
  self.connect(self.button1, QtCore.SIGNAL('clicked()'), self.update)
  self.setFocus()
  #self.icon1 = QtGui.QIcon()
  #self.icon1.addPixmap(QtGui.QPixmap('unnamed.png'))
  self.label = QtGui.QLineEdit(self)
  self.label.setGeometry(130,40,260,30)
  self.ba = QtGui.QLabel(self)
  self.ba.setPixmap(QtGui.QPixmap('dic/png1.png'))
  self.msg= QtGui.QMessageBox()
  self.dialogbox=QtGui.QInputDialog()
  self.dialogbox1=QtGui.QInputDialog()
  self.lbl5 = QtGui.QTextEdit(self)
  self.lbl5.setReadOnly(True)
  self.lbl5.setGeometry(30,150,430,400)
  self.setStyleSheet("QWidget {border:inset;border-radius:3px;color :black;font-weight:500; font-size: 10pt}QPushButton{color:#099000;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em;padding: 6px;}QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}")
  
  with open('Words.txt','a+') as f:
   b= sum(1 for line in f)
   lbl4 = QtGui.QLabel('['+ str(b)+']'+	' word exist in your dict...!', self)
   lbl4.move(110,125)
   f.close()

#the insert function
 def insert(self):
    flag=True
    pox=2
    with open('Words.txt','a+') as f:
     inword=(self.label.text()).toLower()
     for line in f:
      if line==(inword+'\n'):
       self.msg.setText("you have this word \n%s"%dic1[str(inword)].decode('utf8'))
       self.msg.exec_()
       #self.label.clear()
       flag=False
       break
     for i in lito:
      if i==(inword):
       if pox>0:
        self.lbl5.clear()
        pox=-pox
       self.lbl5.append(dic1[i].decode('utf8'))
       f.write(inword)
       f.write('\n')
       flag=False
      else:
       continue
     if (flag):
      text,ok=self.dialogbox.getText(QtGui.QInputDialog(),'Create Persian meaning','Enter meaning here: ',QtGui.QLineEdit.Normal,'meaning')
      if ok :  
       dic1[str(inword)]=unicode(text)
       con = lite.connect('data/Generic_English_Persian.m2')
       with con:    
        cur = con.cursor()    
        cur.execute("SELECT * FROM word")
        rows = cur.fetchall()
        i=len(rows)+1
        cur.execute("insert into word (id,Wname,Wmean) values (?, ?, ?)",
            (i,str(inword),unicode(text))) 
        con.commit()
       #self.label.clear()
       f.write(inword)
       f.write('\n')
#update function for update meaning
 def update(self):

  inword=(self.label.text()).toLower()
  text,ok=self.dialogbox1.getText(QtGui.QInputDialog(),'Update meaning','Enter meaning here: ',QtGui.QLineEdit.Normal,'aaas')
  if ok :
   con = lite.connect('data/Generic_English_Persian.m2')
   with con:
    cur = con.cursor()     
    cur.execute("SELECT * FROM word")
    cur.execute("UPDATE word SET Wmean=? WHERE Wname=?",(unicode(text), str(inword)))        
    con.commit()
 

 def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.insert()


"""class HoverButton(QtGui.QToolButton):

    def __init__(self, parent=None):
        super(HoverButton, self).__init__(parent)
        self.setMouseTracking(True)
        #self.button= QtGui.QPushButton('Translete', self)

    def enterEvent(self,event):
        #print("Enter")
        self.setStyleSheet("background-color:#400045;")

    def leaveEvent(self,event):
        self.setStyleSheet("background-color:998002;")
        #print("Leave")"""


app = QtGui.QApplication(sys.argv)
icon = InputDialog()
icon.show()
app.exec_()

# End of script

