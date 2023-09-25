import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QFileDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from subprocess import Popen, PIPE
import mainwindow
from lang import Lang
from sizeformatdialog import showSizeDialog

def strtoint(v, default=0):
    try:
        a = eval(v)
    except:
        return default
    else:
        return a

class ThreadWorker(QObject):
    finished = pyqtSignal()
    onLineRead = pyqtSignal(str)
    #onDownloaded = pyqtSignal(feedparser.util.FeedParserDict)

    def __init__(self, thread, cmd):
        super(ThreadWorker,self).__init__()
        self.cmd = cmd
        self.thread = thread

    def run(self):
        try:
            with Popen(self.cmd, shell=True, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
                for line in p.stdout:
                    self.onLineRead.emit(line)
        except Exception as e:
            print(str(e))
        self.thread.quit()
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.lang = Lang()
        self.ui.setupUi(self, self.lang)
        self.ui.bBrowse.clicked.connect(self.getFolder)
        self.ui.bPlay.clicked.connect(self.play)
        self.ui.bDownload.clicked.connect(self.download)
        self.currenturls = []
        self.currenturlindex = 0
        self.updatesettings()
        self.yt_dlp_file = ''
        self.loading_formats = False
        self.formats = []
        self.selected_format = 0


    def updatesettings(self):
        sets = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, os.path.join('RoganovSoft', 'Yt-dlp-gui'), "config")
        w, h = int(sets.value("Main/Width","-1")), int(sets.value("Main/Height","-1"))
        if w > 0 and h > 0:
            self.resize(w,h)
        x, y = int(sets.value("Main/Left","-1")), int(sets.value("Main/Top","-1"))
        if x > 0 and y > 0:
            self.move(x,y)
        else:
            self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        self.yt_dlp_file = sets.value("Main/yt_dlp_file",'')
        self.ui.peDir.setPlainText(sets.value("Main/savepath",""))

    def savesettings(self):
        sets = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, os.path.join('RoganovSoft', 'Yt-dlp-gui'), "config")
        sets.setValue("Main/Left", self.pos().x())
        sets.setValue("Main/Top", self.pos().y())
        sets.setValue("Main/Width", self.width())
        sets.setValue("Main/Height", self.height())
        sets.setValue("Main/yt_dlp_file", self.yt_dlp_file)
        sets.setValue("Main/savepath",self.ui.peDir.toPlainText())

    def getFolder(self):
        self.ui.peDir.setPlainText(QFileDialog.getExistingDirectory (self, self.lang.tr("open_a_folder"), "", QFileDialog.ShowDirsOnly))

    def play(self):
        url = self.ui.peLink.toPlainText()
        self.runcmd('/home/genius/apps/yt-dlp-play '+url)

    def download(self):
        self.loading_formats = False
        self.selected_format = 0
        self.formats.clear()
        dir = self.ui.peDir.toPlainText().split('\n')
        if len(dir) == 0 or len(dir[0]) < 2:
            return
        os.chdir(dir[0])

        urls = self.ui.peLink.toPlainText().split('\n')
        self.currenturls = urls
        self.currenturlindex = 0
        if self.ui.b720.isChecked():
            vf = '-f 22'
        elif self.ui.bFormats.isChecked():
            vf = '-F'
        else:
            vf = ''

        for i in range(len(urls)):
            if len(urls[i]) > 7:
                self.currenturlindex = i
                self.runcmd(f'/home/genius/apps/yt-dlp {vf} {urls[i]}')
                break

    def runcmd(self, cmd):
        self.thread = QtCore.QThread()
        self.worker = ThreadWorker(self.thread, cmd)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.threadfinished)
        self.worker.onLineRead.connect(self.onLineRead)
        self.started = True
        self.ui.bPlay.setEnabled(False)
        self.ui.bDownload.setEnabled(False)
        self.ui.peLog.setPlainText('run command: '+cmd)
        self.ui.pb.setValue(0)
        self.thread.start()

    def parseformats(self):
        #https://www.youtube.com/watch?v=te17kB8RlS8
        flist = []
        for i in range(2, len(self.formats)):
            line = self.formats[i]
            vs = line[10:20].replace(' ','')
            if 'x' in vs:
                xi = vs.index('x')
                w = strtoint(vs[:xi])
                h = strtoint(vs[xi+1:])
                if w > 426 and not (w, h) in flist:
                    flist.append((w, h))
        if len(flist) > 0:
            vs = 0
            if self.selected_format > 0:
                for vsize in flist:
                    if vsize[1] == self.selected_format:
                        vs = self.selected_format
                        break
            if vs == 0:
                i = showSizeDialog(self, flist)
                if i < 0 or i >= len(flist): return
                vs = flist[i][1]
                self.selected_format = vs
            self.loading_formats = False
            self.formats.clear()
            vf = f'-f "bestvideo[height<={vs}]+bestaudio[ext=m4a]"'
            self.runcmd(f'/home/genius/apps/yt-dlp {vf} {self.currenturls[self.currenturlindex]}')
        else:
            self.ui.peLog.appendPlainText('error: !cannot parse formats')

    def threadfinished(self):
        if self.loading_formats:
            self.parseformats()
            return
        l = len(self.currenturls)
        if l > 0 and self.currenturlindex < l-1:
            self.currenturlindex += 1
            self.loading_formats = False
            self.formats.clear()
            if self.ui.b720.isChecked():
                vf = '-f 22'
            elif self.ui.bFormats.isChecked():
                vf = '-F'
            else:
                vf = ''
            self.runcmd(f'/home/genius/apps/yt-dlp {vf} {self.currenturls[self.currenturlindex]}')
            return
        self.currenturls = []
        self.started = False
        self.ui.bPlay.setEnabled(True)
        self.ui.bDownload.setEnabled(True)


    def onLineRead(self, line):
        if self.loading_formats:
            self.formats.append(line)
            return
        finfstr = '[info] Available formats'
        if not line.startswith('A:'):
            #[download] 100% of  272.53MiB in 00:01:01 at 4.45MiB/s
            if '[download] ' == line[:11]:
                if 'Destination:' in line:
                    self.ui.peLog.appendPlainText(line.rstrip())
                else:
                    try:
                        v = int(strtoint(line[11:line.index('%')]))
                        self.ui.pb.setValue(v)
                    except:
                        pass
            elif finfstr == line[:len(finfstr)]:
                self.loading_formats = True
            else:
                self.ui.peLog.appendPlainText(line.rstrip())

    def closeEvent(self,event):
        self.savesettings()
        super(MainWindow, self).closeEvent(event)


app = QtWidgets.QApplication(sys.argv)
themedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'darktheme')
fn = os.path.join(themedir,'theme.qrc')
if os.path.isfile(fn):
    with open(fn, 'r') as f:
        theme = f.read()
    theme = theme.replace('current_directory',themedir)
    app.setStyleSheet(theme)
my_mainWindow = MainWindow()
my_mainWindow.show()
sys.exit(app.exec_())
