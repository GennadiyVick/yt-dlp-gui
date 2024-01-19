# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from extensionformatdialog import ExtensionFormatDialog

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
        self.bExt = QtWidgets.QPushButton(SizeFormatDialog)
        self.bExt.setObjectName("bExt")
        self.verticalLayout.addWidget(self.bExt)
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
        self.bExt.setText(lang.tr("extension_variant"))
        SizeFormatDialog.setWindowTitle(lang.tr("size_format_dlg_title"))

class SizeFormatDialog(QtWidgets.QDialog):
    def __init__(self, sizelist, parent):
        super(SizeFormatDialog,self).__init__(parent)
        self.ui = Ui_SizeFormatDialog()
        self.ui.setupUi(self, parent.lang)
        self.model = QtGui.QStandardItemModel(self)
        self.show_extension = False
        self.ui.lv.setModel(self.model)
        for s in sizelist:
            self.model.appendRow(QtGui.QStandardItem(f'{s[0]}X{s[1]}'))
        self.ui.bExt.clicked.connect(self.show_ext_formats)

    def show_ext_formats(self):
        self.show_extension = True
        self.reject()

def showSizeDialog(parent, sizelist, formats):
    r = -1
    extension = None
    dlg = SizeFormatDialog(sizelist, parent)
    if dlg.exec() == 1:
        i = dlg.ui.lv.currentIndex().row()
        if i >= 0:
            r = i
    else:
        if dlg.show_extension:
            edlg = ExtensionFormatDialog(parent, formats)
            if edlg.exec() == 1:
                extension = edlg.get_extension()
    return r, extension
