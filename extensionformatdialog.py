from PyQt5 import QtCore, QtGui, QtWidgets

from extensionformatdialogui import Ui_ExtensionFormatDialog

class ExtensionFormatDialog(QtWidgets.QDialog):

    def __init__(self, parent, formats):
        super(ExtensionFormatDialog, self).__init__(parent)
        self.ui = Ui_ExtensionFormatDialog()
        self.ui.setupUi(self, parent.lang)

        for i in range(2,len(formats)):
            line = formats[i]
            size = line[10:20].strip()
            if 'x' in size and int(size[:size.index('x')]) < 400:
                continue
            if ' images ' in line:
                continue
            if ' audio only' in line:
                rc = self.ui.twAudio.rowCount()
                self.ui.twAudio.setRowCount(rc+1)
                self.ui.twAudio.setItem(rc,0,QtWidgets.QTableWidgetItem(line))
            elif ' video only' in line:
                rc = self.ui.twVideo.rowCount()
                self.ui.twVideo.setRowCount(rc+1)
                self.ui.twVideo.setItem(rc,0,QtWidgets.QTableWidgetItem(line))
            else:
                rc = self.ui.twAudioVideo.rowCount()
                self.ui.twAudioVideo.setRowCount(rc+1)
                self.ui.twAudioVideo.setItem(rc,0,QtWidgets.QTableWidgetItem(line))

        self.ui.twVideo.setHorizontalHeaderLabels([formats[0]])
        self.ui.twAudio.setHorizontalHeaderLabels([formats[0]])
        self.ui.twAudioVideo.setHorizontalHeaderLabels([formats[0]])
        self.ui.twVideo.itemSelectionChanged.connect(self.twvideo_itemchanged)
        self.ui.twAudio.itemSelectionChanged.connect(self.twvideo_itemchanged)
        self.ui.twAudioVideo.itemSelectionChanged.connect(self.twaudiovideo_itemchanged)

    def twvideo_itemchanged(self):
        self.ui.twAudioVideo.clearSelection()

    def twaudiovideo_itemchanged(self):
        self.ui.twVideo.clearSelection()
        self.ui.twAudio.clearSelection()

    def get_extension(self):
        result = None

        items1 = self.ui.twAudioVideo.selectedItems()
        items2 = self.ui.twVideo.selectedItems()
        items3 = self.ui.twAudio.selectedItems()

        if len(items1) > 0:
            result = items1[0].text()
            result = result[:result.index(' ')]
        elif len(items2) > 0 and len(items3) > 0:
            s1 = items2[0].text()
            s1 = s1[:s1.index(' ')]
            s2 = items3[0].text()
            s2 = s2[:s2.index(' ')]
            result=s1+'+'+s2
        elif len(items2) > 0:
            result = items2[0].text()
            result = result[:result.index(' ')]
        elif len(items3) > 0:
            result = items3[0].text()
            result = result[:result.index(' ')]
        return result



