from tkinter import *
from MyWindows.MyWidget.publicMember import pm
from MyWindows.MyTool.ToolBox import *
from MyWindows.MyWidget.toolBoxTopLevel import ParaInputTop
from MyWindows.MyWidget.algorithmTopLevel import AlgorithmParaTop


class MenuBar(Menu):
    """
    主窗口菜单栏
    """

    def __init__(self, root, frames, cnf={}, **kw):
        super().__init__(root, cnf, **kw)
        self.root: Tk = root
        self.frame0: Frame = frames[0]
        self.frame10: Frame = frames[1]
        self.addMenu()

    def addMenu(self):
        file_menu = FileMenu(self, self.frame10, tearoff=False)
        analyse_menu = AnalyseMenu(self, self.frame0, tearoff=False)
        set_menu = SetMenu(self, tearoff=False)
        toolBox_menu = ToolBoxMenu(self)
        about_menu = AboutMenu(self, tearoff=False)
        self.add_cascade(label='文件', menu=file_menu)  # 添加到菜单条中
        self.add_cascade(label='分析', menu=analyse_menu)
        self.add_cascade(label='设置', menu=set_menu)
        self.add_cascade(label='工具箱', menu=toolBox_menu)
        self.add_cascade(label='关于', menu=about_menu)


class FileMenu(Menu):
    """
    '文件'菜单
    """

    def __init__(self, master, frame10, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master: MenuBar = master
        self.add_command(label='打开文件', command=lambda: pm.openFile(frame10))  # 绑定事件
        self.add_command(label='添加矢量数据', command=lambda: pm.addVectorFile(frame10))  # 绑定事件
        self.add_command(label='保存数据', command=pm.saveFile)  # 绑定事件


class AnalyseMenu(Menu):
    """
    '分析'菜单
    """

    def __init__(self, master, frame0, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master: MenuBar = master
        self.frame0: Frame = frame0
        self.add_command(label='开始分析',
                         command=lambda: AlgorithmParaTop({'搜索半径(点数)': 15, '幂': 2}, 'IDW', self.frame0,
                                                          pm.startAnaThread))  # 绑定事件
        self.add_command(label='绘制分形维数等值图', command=pm.show_image)  # 绑定事件


class ToolBoxMenu(Menu):
    """
    '工具箱'菜单
    """

    def __init__(self, master, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master: MenuBar = master
        self.add_command(label='矢量转栅格',
                         command=lambda: ParaInputTop({'栅格边长(m)': 800}, master, '矢量:shp', '栅格:tif',
                                                      vectorToRaster))
        self.add_command(label='栅格转ASCII',
                         command=lambda: ParaInputTop({}, master, '栅格:tif', 'ASCII:txt', rasterToAscii))


class SetMenu(Menu):
    """
    '设置'菜单
    """

    def __init__(self, master, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master: MenuBar = master
        color_menu = ColorMenu(self, tearoff=False)
        vector_color_menu = VectorColorMenu(self, tearoff=False)
        self.add_cascade(label='等值图填充颜色', menu=color_menu)  # 添加到设置菜单中
        self.add_cascade(label='矢量颜色', menu=vector_color_menu)


class ColorMenu(Menu):
    """
    '设置--颜色设置'菜单
    """

    def __init__(self, master, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master: SetMenu = master
        pm.createStringVar()
        pm.var.set(pm.myContColor)
        for labels, colors in pm.colors.items():
            self.add_radiobutton(label=labels, variable=pm.var, value=colors, command=pm.setMyContColor)  # 绑定字符串的值


class VectorColorMenu(Menu):
    """
    '设置--矢量颜色设置'菜单
    """

    def __init__(self, master, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master: SetMenu = master
        pm.createVectorStringVar()
        pm.vectorVar.set(pm.vectorColor)
        for labels, colors in pm.vColors.items():
            self.add_radiobutton(label=labels, variable=pm.vectorVar, value=colors, command=pm.setVectorColor)


class AboutMenu(Menu):
    """
    '关于'菜单
    """

    def __init__(self, master, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master: MenuBar = master
        self.add_command(label='软件信息', command=pm.show_about)  # 绑定事件
