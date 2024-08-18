#!/usr/bin/python3
import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QFileDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from subprocess import Popen, PIPE
import mainwindow
from lang import Lang
from sizeformatdialog import showSizeDialog
from settingsdialog import showSettingsDialog
import signal

YT_DLP_FILE = 'yt-dlp'
PLAYER_FILE = 'mplayer'

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

    def __init__(self, thread, cmd):
        super(ThreadWorker,self).__init__()
        self.cmd = cmd
        self.thread = thread
        self.dokill = False

    def run(self):
        self.dokill = False
        try:
            with Popen(self.cmd, shell=True, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
                for line in p.stdout:
                    self.onLineRead.emit(line)
                    if self.dokill:
                        os.kill(p.pid, signal.SIGINT)
        except Exception as e:
            print(str(e))
        self.thread.quit()
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.proxy = ''
        self.proxy_enabled = "0"
        self.player_file = ''
        self.yt_dlp_file = ''
        self.ui = mainwindow.Ui_MainWindow()
        self.lang = Lang()
        self.ui.setupUi(self, self.lang)
        self.ui.bBrowse.clicked.connect(self.getFolder)
        self.ui.bPlay.clicked.connect(self.play)
        self.ui.bDownload.clicked.connect(self.download)
        self.ui.bSet.clicked.connect(self.showsettings)
        self.currenturls = []
        self.currenturlindex = 0
        self.updatesettings()
        self.loading_formats = False
        self.formats = []
        self.selected_format = 0
        lines = []
        if len(sys.argv)>1:
            for i in range(1, len(sys.argv)):
                lines.append(sys.argv[i])
        self.ui.peLink.setPlainText('\n'.join(lines))

    def updatesettings(self):
        sets = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, os.path.join('RoganovSoft', 'Yt-dlp-gui'), "config")
        w, h = int(sets.value("Main/Width", "-1")), int(sets.value("Main/Height","-1"))
        if w > 0 and h > 0:
            self.resize(w,h)
        x, y = int(sets.value("Main/Left", "-1")), int(sets.value("Main/Top","-1"))
        if x > 0 and y > 0:
            self.move(x,y)
        else:
            self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())
        self.yt_dlp_file = sets.value("Main/yt_dlp_file", YT_DLP_FILE)
        self.player_file = sets.value("Main/player_file", PLAYER_FILE)
        self.proxy = sets.value('Main/proxy', '')
        self.proxy_enabled = sets.value('Main/proxy_enabled','0')
        self.ui.peDir.setPlainText(sets.value("Main/savepath",""))
        v = int(strtoint(sets.value("Main/selectedsize")))
        if v == 0:
            self.ui.b720.setChecked(True)
        elif v == 1:
            self.ui.bMax.setChecked(True)
        else:
            self.ui.bFormats.setChecked(True)

    def showsettings(self):
        r = showSettingsDialog(self, {'yt-dlp': self.yt_dlp_file, 'player': self.player_file, 'proxy': self.proxy, 'proxy_enabled': self.proxy_enabled})
        if r[0]:
            self.yt_dlp_file, self.player_file, self.proxy, self.proxy_enabled = r[1]



    def savesettings(self):
        sets = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, os.path.join('RoganovSoft', 'Yt-dlp-gui'), "config")
        sets.setValue("Main/Left", self.pos().x())
        sets.setValue("Main/Top", self.pos().y())
        sets.setValue("Main/Width", self.width())
        sets.setValue("Main/Height", self.height())
        sets.setValue("Main/yt_dlp_file", self.yt_dlp_file)
        sets.setValue("Main/player_file", self.player_file)
        sets.setValue('Main/proxy', self.proxy)
        sets.setValue('Main/proxy_enabled', self.proxy_enabled)
        sets.setValue("Main/savepath", self.ui.peDir.toPlainText())
        if self.ui.b720.isChecked():
            sets.setValue("Main/selectedsize",0)
        elif self.ui.bFormats.isChecked():
            sets.setValue("Main/selectedsize",2)
        else:
            sets.setValue("Main/selectedsize",1)

    def getFolder(self):
        fldr = QFileDialog.getExistingDirectory(self, self.lang.tr("open_a_folder"), "", QFileDialog.ShowDirsOnly)
        self.ui.peDir.setPlainText(fldr)

    def play(self):
        dir = self.ui.peDir.toPlainText().split('\n')
        if len(dir) == 0 or len(dir[0]) < 2:
            return
        os.chdir(dir[0])
        self.ui.peLog.setPlainText("")
        urls = self.ui.peLink.toPlainText().split('\n')
        if len(urls) > 1:
            self.ui.peLog.appendPlainText("!!!Play only first url!")
        pr = f' --proxy {self.proxy}' if self.proxy_enabled and len(self.proxy) > 3 else ''
        self.currenturls = [urls[0]]
        self.currenturlindex = 0
        self.ui.peLog.appendPlainText("Downloadin format 1280X720")
        self.runcmd(f'{self.yt_dlp_file}{pr} -f 22 -q -o- {urls[0]} | {self.player_file} -af scaletempo -softvol -softvol-max 400 -cache 8192  -')
        #yt-dlp -f 22 -q -o- "$*" | /home/genius/apps/mplayer.ext -af scaletempo -softvol -softvol-max 400 -cache 8192  -


    def download(self):
        self.loading_formats = False
        self.selected_format = 0
        self.formats.clear()
        self.ui.peLog.setPlainText("")
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
        pr = f' --proxy {self.proxy}' if self.proxy_enabled and len(self.proxy) > 3 else ''
        for i in range(len(urls)):
            if len(urls[i]) > 7:
                self.currenturlindex = i
                self.runcmd(f'{self.yt_dlp_file}{pr} {vf} {urls[i]}')
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
        self.ui.peLog.appendPlainText('run command: '+cmd)
        self.ui.pb.setValue(0)
        self.thread.start()

    def parseformats(self):
        flist = []

        for i in range(2, len(self.formats)):
            line = self.formats[i]
            vs = line[14:24].replace(' ','')
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
            ext = None
            if vs == 0:
                i, ext = showSizeDialog(self, flist, self.formats)
                print('ext:', ext)
                if ext == None:
                    if i < 0 or i >= len(flist):
                        self.currenturls = []
                        self.started = False
                        self.ui.bPlay.setEnabled(True)
                        self.ui.bDownload.setEnabled(True)
                        return
                    vs = flist[i][1]
                    self.selected_format = vs
                else:
                   vf = f'-f {ext}'
                   self.selected_format == 0
            self.loading_formats = False
            self.formats.clear()
            pr = f' --proxy {self.proxy}' if self.proxy_enabled and len(self.proxy) > 3 else ''
            if ext == None:
                vf = f'-f "bestvideo[height<={vs}]+bestaudio[ext=m4a]"'
            self.runcmd(f'{self.yt_dlp_file}{pr} {vf} {self.currenturls[self.currenturlindex]}')
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
            pr = f' --proxy {self.proxy}' if self.proxy_enabled and len(self.proxy) > 3 else ''
            self.runcmd(f'{self.yt_dlp_file}{pr} {vf} {self.currenturls[self.currenturlindex]}')
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
app.setWindowIcon(QtGui.QIcon(":/yt-dlp.png"))
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
