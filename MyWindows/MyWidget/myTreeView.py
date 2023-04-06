from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

import pandas as pd
from MyWindows.MyWidget.publicNumber import pn


class MainLeftTreeView(Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.frame11 = self.master.frame11
        self.eventBind()

    def eventBind(self):
        self.bind("<<TreeviewSelect>>", self.onSelect)

    def onSelect(self, event):
        """
        treeview选中回调函数
        :return:
        """
        for select in event.widget.selection():
            if select in pn.treeViewSelections:
                pn.treeViewSelections.remove(select)
                self.updateText()
                self.frame11.getTreeView().updateRightTreeView()
            else:
                if select.split('.')[-1] == 'txt':  # 若勾选txt文件
                    if pn.state != 0 and pn.state < 1:  # 不允许在分析中途更换
                        showwarning('CscsGIS', '请等待分析完成！')
                        return
                    for anotherSameSelect in pn.treeViewSelections:
                        suffix = anotherSameSelect.split('.')[-1]
                        if suffix == 'txt':  # txt文件只能勾选一个
                            pn.treeViewSelections.remove(anotherSameSelect)
                            pn.clearAll()
                pn.treeViewSelections.append(select)
                self.updateText()
                self.frame11.getTreeView().updateRightTreeView()

    def updateText(self):
        """
        更新选中节点对应的标签状态
        :return:
        """
        for label in self.master.getButtonFrame().winfo_children():
            label.destroy()
        for node in self.master.getTreeView().get_children():
            Label(self.master.getButtonFrame(), text='√' if node in pn.treeViewSelections else '□').pack(fill=X)


class MainRightTreeView(Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master

    def updateRightTreeView(self):
        """
        更新右侧treeview
        :return:
        """
        for treeView in self.master.winfo_children():
            treeView.destroy()
        for name in pn.treeViewSelections:
            data = pn.tvSelectData[name]
            index = pn.treeViewSelections.index(name)
            if isinstance(data, pd.DataFrame):
                self.master.setTreeView(list(data.columns), data, index)
