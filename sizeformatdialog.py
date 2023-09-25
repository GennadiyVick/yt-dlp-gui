# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SizeFormatDialog(object):
    def setupUi(self, SizeFormatDialog, lang):
        SizeFormatDialog.setObjectName("SizeFormatDialog")
        SizeFormatDialog.resize(222, 245)
        self.verticalLayout = QtWidgets.QVBoxLayout(SizeFormatDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lv = QtWidgets.QListView(SizeFormatDialog)
        self.lv.setObjectName("lv")
        self.lv.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lv.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lv.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lv.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.verticalLayout.addWidget(self.lv)
        self.buttonBox = QtWidgets.QDialogButtonBox(SizeFormatDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SizeFormatDialog, lang)
        self.buttonBox.accepted.connect(SizeFormatDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(SizeFormatDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SizeFormatDialog)

    def retranslateUi(self, SizeFormatDialog, lang):
        if lang == None: lang = Lang()
        SizeFormatDialog.setWindowTitle(lang.tr("size_format_dlg_title"))

class SizeFormatDialog(QtWidgets.QDialog):
    def __init__(self, sizelist, parent):
        super(SizeFormatDialog,self).__init__(parent)
        self.ui = Ui_SizeFormatDialog()
        self.ui.setupUi(self, parent.lang)
        self.model = QtGui.QStandardItemModel(self)
        self.ui.lv.setModel(self.model)
        for s in sizelist:
            self.model.appendRow(QtGui.QStandardItem(f'{s[0]}X{s[1]}'))

def showSizeDialog(parent, sizelist):
    r = -1
    dlg = SizeFormatDialog(sizelist,  parent)
    if dlg.exec() == 1:
        i = dlg.ui.lv.currentIndex().row()
        if i >= 0:
            r = i
    return r
