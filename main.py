import os
import matplotlib
import MyWindows.mainWindow as mWin
from tkinter import *
from tkinter.messagebox import *


def StopAll():
    if askyesno('CscsGIS', '确定要退出吗？'):
        root.quit()
        root.destroy()
        exit()


if __name__ == '__main__':
    matplotlib.use('TkAgg')
    root = Tk()
    root.iconbitmap('MyImage/earth.ico')
    root.protocol('WM_DELETE_WINDOW', StopAll)
    a = mWin.MainWindow(root)
    a.mainloop()  # 不断刷新主窗口
