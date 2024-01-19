# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extensionformatdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ExtensionFormatDialog(object):
    def setupUi(self, ExtensionFormatDialog, lang):
        ExtensionFormatDialog.setObjectName("ExtensionFormatDialog")
        ExtensionFormatDialog.resize(595, 499)
        self.verticalLayout = QtWidgets.QVBoxLayout(ExtensionFormatDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lAudioVideo = QtWidgets.QLabel(ExtensionFormatDialog)
        self.lAudioVideo.setObjectName("lAudioVideo")
        self.verticalLayout.addWidget(self.lAudioVideo)
        self.twAudioVideo = QtWidgets.QTableWidget(ExtensionFormatDialog)
        self.twAudioVideo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twAudioVideo.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.twAudioVideo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.twAudioVideo.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.twAudioVideo.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.twAudioVideo.setShowGrid(False)
        self.twAudioVideo.setWordWrap(False)
        self.twAudioVideo.setColumnCount(1)
        self.twAudioVideo.setObjectName("twAudioVideo")
        self.twAudioVideo.setRowCount(0)
        self.twAudioVideo.horizontalHeader().setStretchLastSection(True)
        self.twAudioVideo.verticalHeader().setVisible(False)
        self.twAudioVideo.horizontalHeader().setMinimumSectionSize(30)
        self.verticalLayout.addWidget(self.twAudioVideo)
        self.lAudio = QtWidgets.QLabel(ExtensionFormatDialog)
        self.lAudio.setObjectName("lAudio")
        self.verticalLayout.addWidget(self.lAudio)
        self.twAudio = QtWidgets.QTableWidget(ExtensionFormatDialog)
        self.twAudio.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twAudio.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.twAudio.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.twAudio.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.twAudio.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.twAudio.setShowGrid(False)
        self.twAudio.setWordWrap(False)
        self.twAudio.setColumnCount(1)
        self.twAudio.setObjectName("twAudio")
        self.twAudio.setRowCount(0)
        self.twAudio.horizontalHeader().setStretchLastSection(True)
        self.twAudio.verticalHeader().setVisible(False)
        self.twAudio.horizontalHeader().setMinimumSectionSize(30)
        self.verticalLayout.addWidget(self.twAudio)
        self.lVideo = QtWidgets.QLabel(ExtensionFormatDialog)
        self.lVideo.setObjectName("lVideo")
        self.verticalLayout.addWidget(self.lVideo)
        self.twVideo = QtWidgets.QTableWidget(ExtensionFormatDialog)
        self.twVideo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twVideo.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.twVideo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.twVideo.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.twVideo.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.twVideo.setShowGrid(False)
        self.twVideo.setWordWrap(False)
        self.twVideo.setColumnCount(1)
        self.twVideo.setObjectName("twVideo")
        self.twVideo.setRowCount(0)
        self.twVideo.horizontalHeader().setStretchLastSection(True)
        self.twVideo.verticalHeader().setVisible(False)
        self.twVideo.horizontalHeader().setMinimumSectionSize(30)
        self.verticalLayout.addWidget(self.twVideo)
        self.lInfo = QtWidgets.QLabel(ExtensionFormatDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.lInfo.setFont(font)
        self.lInfo.setObjectName("lInfo")
        self.verticalLayout.addWidget(self.lInfo)
        self.buttonBox = QtWidgets.QDialogButtonBox(ExtensionFormatDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ExtensionFormatDialog, lang)
        self.buttonBox.accepted.connect(ExtensionFormatDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(ExtensionFormatDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ExtensionFormatDialog)

    def retranslateUi(self, ExtensionFormatDialog, lang):
        ExtensionFormatDialog.setWindowTitle(lang.tr("advanced_format_selection"))
        self.lAudioVideo.setText(lang.tr("audio_video_formats"))
        self.lAudio.setText(lang.tr("audio_formats"))
        self.lVideo.setText(lang.tr("video_formats"))
        self.lInfo.setText(lang.tr("formats_info"))