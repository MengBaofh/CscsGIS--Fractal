from tkinter import *
# from tkinter.ttk import *

from MyWindows.MyWidget.myFrame import Frame0, Frame10, Frame11, Frame2
from MyWindows.MyWidget.myMenu import MenuBar


class MainWindow(Frame):
    main_width = 1100  # 主窗口宽
    main_height = 700
    frame0 = None  # frame0
    buttonFrame = None
    panedWindow = None
    frame10 = None
    frame11 = None
    frame2 = None  # 状态栏
    menu_bar = None  # 菜单栏
    root = None

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setMainWindow()
        self.setFrame()
        self.setMenuBar()

    def setMainWindow(self):
        self.root.title("CscsGIS")  # 主窗口名称
        self.root.geometry(f"{self.main_width}x{self.main_height}")  # 主窗口大小
        self.root.resizable(width=True, height=True)  # 主窗口可变
        self.root.minsize(width=self.main_width // 2, height=self.main_height // 2)

    def setFrame(self):
        self.panedWindow = PanedWindow(self.root, sashrelief=SUNKEN, relief='groove')
        self.frame11 = Frame11(self.panedWindow)
        self.frame10 = Frame10(self.panedWindow, self.frame11)
        self.frame0 = Frame0(self.root, self.frame10)
        self.frame2 = Frame2(self.root)
        self.setPanedWindow()
        self.frame0.place(relx=0, rely=0, relheight=0.05, relwidth=1)
        self.frame2.place(relx=0, rely=0.95, relheight=0.05, relwidth=1)

    def setPanedWindow(self):
        self.panedWindow.add(self.frame10)
        self.panedWindow.add(self.frame11)
        self.panedWindow.paneconfigure(self.frame10, minsize=200)
        self.panedWindow.paneconfigure(self.frame11, minsize=700)
        self.panedWindow.place(relx=0, rely=0.05, relheight=0.9, relwidth=1)

    def setMenuBar(self):
        self.menu_bar = MenuBar(self.root, self.getFrame())
        self.root['menu'] = self.menu_bar

    def getFrame(self):
        """
        获取该窗口下的全部frame对象
        :return:
        """
        return self.frame0, self.frame10, self.frame11, self.frame2
