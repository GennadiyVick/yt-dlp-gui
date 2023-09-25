from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog, lang):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(330, 202)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SettingsDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.hl_yt_dlp = QtWidgets.QHBoxLayout()
        self.hl_yt_dlp.setObjectName("hl_yt_dlp")
        self.leYtdlp = QtWidgets.QLineEdit(SettingsDialog)
        self.leYtdlp.setObjectName("leYtdlp")
        self.hl_yt_dlp.addWidget(self.leYtdlp)
        self.bBrowse_1 = QtWidgets.QToolButton(SettingsDialog)
        self.bBrowse_1.setMinimumSize(QtCore.QSize(30, 30))
        self.bBrowse_1.setText("...")
        self.bBrowse_1.setObjectName("bBrowse_1")
        self.hl_yt_dlp.addWidget(self.bBrowse_1)
        self.verticalLayout.addLayout(self.hl_yt_dlp)
        self.label_2 = QtWidgets.QLabel(SettingsDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.hl_player = QtWidgets.QHBoxLayout()
        self.hl_player.setObjectName("hl_player")
        self.lePlayer = QtWidgets.QLineEdit(SettingsDialog)
        self.lePlayer.setObjectName("lePlayer")
        self.hl_player.addWidget(self.lePlayer)
        self.bBrowse_2 = QtWidgets.QToolButton(SettingsDialog)
        self.bBrowse_2.setMinimumSize(QtCore.QSize(30, 30))
        self.bBrowse_2.setText("...")
        self.bBrowse_2.setObjectName("bBrowse_2")
        self.hl_player.addWidget(self.bBrowse_2)
        self.verticalLayout.addLayout(self.hl_player)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog, lang)
        self.buttonBox.accepted.connect(SettingsDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(SettingsDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog, lang):
        SettingsDialog.setWindowTitle(lang.tr('settingsdialog'))
        self.label.setText(lang.tr("yt_dlp_file"))
        self.label_2.setText(lang.tr("player_file"))

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, files, parent):
        super(SettingsDialog,self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self, parent.lang)
        self.ui.leYtdlp.setText(files[0])
        self.ui.lePlayer.setText(files[1])

def showSettingsDialog(parent, files):
    dlg = SettingsDialog(files, parent)
    if dlg.exec() == 1:
        return (True, (self.ui.leYtdlp.text(), self.ui.lePlayer.text()))
    else:
        return (False, None)

