from tkinter import *
from MyWindows.MyWidget.publicNumber import pn


class CustomButton(Button):
    """
    自定义按钮类
    """

    def __init__(self, master, image_path, command, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.image = pn.imageLoader(image_path, (20, 20))[2]
        self['image'] = self.image
        self['command'] = command


class OpenFileButton(CustomButton):
    """
    打开ASCII文件按钮
    """

    def __init__(self, master, frame10, **kw):
        super().__init__(master, 'MyImage/open.png', lambda: pn.openFile(frame10), **kw)


class AddVectorFileButton(CustomButton):
    """
    添加矢量数据按钮
    """

    def __init__(self, master, frame10, **kw):
        super().__init__(master, 'MyImage/addV.png', lambda: pn.addVectorFile(frame10), **kw)


class SaveFileButton(CustomButton):
    """
    保存文件按钮
    """

    def __init__(self, master, **kw):
        super().__init__(master, 'MyImage/save.png', pn.saveFile, **kw)


class StartButton(CustomButton):
    """
    开始分析按钮
    """

    def __init__(self, master, **kw):
        super().__init__(master, 'MyImage/start.png', lambda: pn.startAnaThread(master), **kw)


class ShowButton(CustomButton):
    """
    成图按钮
    """

    def __init__(self, master, **kw):
        super().__init__(master, 'MyImage/show.png', pn.show_image, **kw)
