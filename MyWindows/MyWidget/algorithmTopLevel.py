from tkinter import *
# from tkinter.ttk import *
from Pmw import Balloon


class AlgorithmParaTop(Toplevel):
    """
    算法参数弹窗类
    """
    width = 350
    height = 350

    def __init__(self, parameters: dict, algorithm: str, master, method, **kw):
        super().__init__(master, kw)
        self.master = master
        self.vars = {}
        self.parameters = parameters
        self.algorithm = algorithm
        self.method = method
        self.balloon = Balloon(self.master)
        self.setParaTop()
        self.setVars()
        self.setLabelEntry()

    def setVars(self):
        for parameter, default in self.parameters.items():
            self.vars[parameter] = IntVar() if type(default) == int else StringVar()
            self.vars[parameter].set(default)

    def setParaTop(self):
        self.title(f'{self.algorithm}参数设置')
        self.iconbitmap('MyImage/earth.ico')
        self.geometry(f'{self.width}x{self.height}')
        self.attributes('-topmost', 'true')  # 保持窗口最上

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
               command=lambda: self.method(self, self.master, self.vars)).place(relx=0.3, rely=0.9, relheight=0.07,
                                                                                relwidth=0.4)
