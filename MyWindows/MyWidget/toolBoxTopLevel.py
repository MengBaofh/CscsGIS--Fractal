from tkinter import *
from tkinter.ttk import *
from Pmw import Balloon
from MyWindows.MyWidget.myButton import OpenFilesButton, SaveFilesButton


class ParaInputTop(Toplevel):
    """
    工具箱弹窗类
    """
    width = 350
    height = 350

    def __init__(self, parameters: dict, master, type1: str, type2: str, method, **kw):
        super().__init__(master, kw)
        self.master = master
        self.vars = {}
        self.balloon = Balloon(self.master)
        self.parameters = parameters
        self.type1 = type1.split(':')
        self.type2 = type2.split(':')
        self.method = method
        self.InputVar = StringVar()
        self.OutputVar = StringVar()
        self.openFileButton = None
        self.saveFileButton = None
        self.setVars()
        self.setParaInputTop()
        self.setInOu()
        self.setLabelEntry()
        self.setBind()

    def setVars(self):
        self.InputVar.set(f'{self.type1[0]}文件路径')
        self.OutputVar.set(f'{self.type2[0]}文件导出路径')
        for parameter, default in self.parameters.items():
            self.vars[parameter] = IntVar() if type(default) == int else StringVar()
            self.vars[parameter].set(default)

    def setParaInputTop(self):
        self.title(f'{self.type1[0]}转{self.type2[0]}')
        self.iconbitmap('MyImage/earth.ico')
        self.geometry(f'{self.width}x{self.height}+500+200')

    def setLabelEntry(self):
        n = len(self.vars)
        x, y = 0.2, 0.15
        for parameter, var in self.vars.items():
            Label(self, text=parameter, relief='groove', anchor='center') \
                .place(relx=x, rely=y, relheight=0.07, relwidth=0.25)
            Entry(self, textvariable=self.vars[parameter], justify='center') \
                .place(relx=x + 0.35, rely=y, relheight=0.07, relwidth=0.25)
            y += 0.6 / n
        Button(self, text='确定',
               command=lambda: self.method(self, self.openFileButton.getOpenFileName(),
                                           self.saveFileButton.getSaveFileName(), self.vars)) \
            .place(relx=0.3, rely=0.9, relheight=0.07, relwidth=0.4)

    def setInOu(self):
        Button(self, textvariable=self.InputVar).place(relx=0.2, rely=0.053, relheight=0.07,
                                                       relwidth=0.53)
        Button(self, textvariable=self.OutputVar).place(relx=0.2, rely=0.703, relheight=0.07,
                                                        relwidth=0.53)
        self.openFileButton = OpenFilesButton(self, self.type1[0], self.type1[1])
        self.saveFileButton = SaveFilesButton(self, self.type2[0], self.type2[1])
        self.openFileButton.place(relx=0.73, rely=0.05, relheight=0.07, relwidth=0.07)
        self.saveFileButton.place(relx=0.73, rely=0.7, relheight=0.07, relwidth=0.07)

    def setBind(self):
        self.balloon.bind(self.openFileButton, f'点击选择{self.type1[0]}文件路径')
        self.balloon.bind(self.saveFileButton, f'点击设置导出{self.type2[0]}文件路径')

    def getButton(self):
        return self.openFileButton, self.saveFileButton
