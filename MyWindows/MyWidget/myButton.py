from tkinter import *
from tkinter.filedialog import *

from MyWindows.MyWidget.publicNumber import pn
from MyWindows.MyWidget.algorithmTopLevel import AlgorithmParaTop


class CustomButton(Button):
    """
    自定义按钮类
    """

    def __init__(self, master, image_path, command):
        super().__init__(master)
        self.master = master
        self.image = pn.imageLoader(image_path, (20, 20))[2]
        self['image'] = self.image
        self['command'] = command


class OpenFileButton(CustomButton):
    """
    打开ASCII文件按钮
    """

    def __init__(self, master, frame10):
        super().__init__(master, 'MyImage/open.png', lambda: pn.openFile(frame10))


class AddVectorFileButton(CustomButton):
    """
    添加矢量数据按钮
    """

    def __init__(self, master, frame10):
        super().__init__(master, 'MyImage/addV.png', lambda: pn.addVectorFile(frame10))


class SaveFileButton(CustomButton):
    """
    保存文件按钮
    """

    def __init__(self, master):
        super().__init__(master, 'MyImage/save.png', pn.saveFile)


class StartButton(CustomButton):
    """
    开始分析按钮
    """

    def __init__(self, master):
        super().__init__(master, 'MyImage/start.png',
                         lambda: AlgorithmParaTop({'搜索半径(点数)': 15, '幂': 2}, 'IDW', master, pn.startAnaThread))


class ShowButton(CustomButton):
    """
    成图按钮
    """

    def __init__(self, master):
        super().__init__(master, 'MyImage/show.png', pn.show_image)


class OpenFilesButton(CustomButton):
    """
    打开指定文件按钮
    """

    def __init__(self, master, fileType, suffix):
        super().__init__(master, 'MyImage/open.png', self.openFile)
        self.master = master
        self.fileType = fileType
        self.suffix = suffix
        self.open_file_name = None

    def openFile(self):
        try:
            with askopenfile(title=f'选择{self.fileType}文件',
                             filetypes=[(f'{self.fileType}文件', f'*.{self.suffix}')]) as f:
                self.open_file_name = f.name
                self.master.InputVar.set(self.open_file_name)
        except TypeError:
            pass

    def getOpenFileName(self):
        return self.open_file_name


class SaveFilesButton(CustomButton):
    """
    保存指定文件按钮
    """

    def __init__(self, master, fileType, suffix):
        super().__init__(master, 'MyImage/save.png', self.saveFile)
        self.master = master
        self.fileType = fileType
        self.suffix = suffix
        self.save_file_name = None

    def saveFile(self):
        try:
            with asksaveasfile(title='另存为', initialfile='新建文件', defaultextension='',
                               filetypes=[(f'{self.fileType}文件', f'*.{self.suffix}')]) as f:
                self.save_file_name = f.name
                self.master.OutputVar.set(self.save_file_name)
        except TypeError:
            pass

    def getSaveFileName(self):
        return self.save_file_name
