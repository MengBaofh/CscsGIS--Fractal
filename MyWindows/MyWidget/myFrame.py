import pandas as pd
from tkinter import *
# from tkinter import ttk
from tkinter.ttk import *
from Pmw import Balloon
from MyWindows.MyTool.AutoScrollBar import AutoScrollBar
from MyWindows.MyWidget.myButton import AddVectorFileButton, OpenFileButton, SaveFileButton, StartButton, ShowButton
from MyWindows.MyWidget.myTreeView import MainLeftTreeView, MainRightTreeView


class Frame0(Frame):
    root = None
    pBar = None
    balloon = None
    showButton = None
    startButton = None
    openFileButton = None
    saveFileButton = None
    addVectorFileButton = None

    def __init__(self, root, frame10, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.frame10 = frame10
        self.balloon = Balloon(self.root)  # 主窗口气泡提示信息
        self.setButton()
        self.setPBar()

    def setButton(self):
        self.openFileButton = OpenFileButton(self, self.frame10)
        self.saveFileButton = SaveFileButton(self)
        self.startButton = StartButton(self)
        self.showButton = ShowButton(self)
        self.addVectorFileButton = AddVectorFileButton(self, self.frame10)

        self.balloon.bind(self.openFileButton, '打开文件')
        self.balloon.bind(self.saveFileButton, '保存文件')
        self.balloon.bind(self.startButton, '点击开始分析')
        self.balloon.bind(self.showButton, '点击绘制分形维等值图')
        self.balloon.bind(self.addVectorFileButton, '添加矢量数据')

        self.openFileButton.place(relx=0, rely=0, relheight=1, relwidth=0.03)
        self.addVectorFileButton.place(relx=0.0305, rely=0, relheight=1, relwidth=0.03)
        self.saveFileButton.place(relx=0.061, rely=0, relheight=1, relwidth=0.03)
        self.startButton.place(relx=0.0915, rely=0, relheight=1, relwidth=0.03)
        self.showButton.place(relx=0.122, rely=0, relheight=1, relwidth=0.03)

    def setPBar(self):
        self.pBar = Progressbar(self)  # 进度条
        self.pBar.place(relx=0.152, rely=0, relheight=1, relwidth=0.8458)


class ButtonFrame(Frame):
    root = None

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.rowconfigure(0, weight=1)  # 组件横向充满
        self.columnconfigure(0, weight=1)


class Frame10(Frame):
    root = None
    buttonFrame = None
    leftTreeView = None

    def __init__(self, root, frame11, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.frame11 = frame11
        self.rowconfigure(0, weight=1)  # 组件横向充满
        self.columnconfigure(0, weight=1)
        self.setFrame()
        self.setTreeView()

    def setFrame(self):
        self.buttonFrame = ButtonFrame(self)  # 存放按钮的容器
        self.buttonFrame.place(relx=0, rely=0, relheight=1, relwidth=0.1)

    def setTreeView(self):
        self.leftTreeView = MainLeftTreeView(self, show="tree")
        Style().configure('Treeview', rowheight=21)  # 设置节点高度
        self.leftTreeView.place(relx=0.1, rely=0, relheight=1, relwidth=0.9)

    def getButtonFrame(self):
        return self.buttonFrame

    def getTreeView(self):
        return self.leftTreeView


class Frame11(Frame):
    root = None
    treeView = None
    sroll_11_x = None
    sroll_11_y = None
    totalRow = None

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.rowconfigure(0, weight=1)  # 组件横向充满
        self.columnconfigure(0, weight=1)
        self.setTreeView(["None", "..."], pd.DataFrame(), 0)

    def setTreeView(self, columns: list, data: pd.DataFrame, num: int):
        """
        生成treeview
        :param columns: treeview的标题行
        :param data: 数据框
        :param num: treeview的号码
        :return:
        """
        self.totalRow = data.shape[0]  # 数据的总行数
        self.treeView = MainRightTreeView(self, show="headings", columns=columns)
        for column in columns:
            self.treeView.heading(column, text=column, anchor=CENTER)
        data_list = data.values.tolist()
        for index, rowData in enumerate(data_list):
            self.treeView.insert('', index, values=rowData)
        self.treeView.grid(row=num, column=0, sticky="nsew")
        self.setScrollBar(num)

    def setScrollBar(self, num):
        self.sroll_11_x = AutoScrollBar(self, orient=HORIZONTAL, command=self.treeView.xview)
        self.sroll_11_y = AutoScrollBar(self, orient=VERTICAL, command=self.treeView.yview)
        self.sroll_11_x.grid(row=self.totalRow, column=0, sticky=E + W)
        self.sroll_11_y.grid(row=num, column=1, sticky=N + S)
        self.treeView['xscrollcommand'] = self.sroll_11_x.set
        self.treeView['yscrollcommand'] = self.sroll_11_y.set

    def getTreeView(self):
        return self.treeView


class Frame2(Frame):

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.root = root
