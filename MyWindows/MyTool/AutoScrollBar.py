from tkinter import TclError, ttk


class AutoScrollBar(ttk.Scrollbar):
    """
    仅在需要时才显示的滚动条
    """
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError('该组件无法使用pack布局')

    def place(self, **kw):
        raise TclError('该组件无法使用place布局')
