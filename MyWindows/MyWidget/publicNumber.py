import sympy
import xlsxwriter
import numpy as np
import pandas as pd
import geopandas as gpd
from math import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from MyWindows.myThreading import AnalyseThread
from MyAlgorithm.IDW import IDW


class PublicNumber:
    # 所有PublicNumber类共享,仅在最初类创建时执行一次
    IOutPutDir = 'ImageOutPut'

    def __init__(self):
        self.gdf = pd.DataFrame()
        self.ana_thread = None
        self.image_open_origin = None
        self.image_load = None
        self.image_open = None
        self.plt = plt
        self.var = None
        self.vectorVar = None
        self.pBarMax = 0
        self.width = 0
        self.height = 0
        self.state = 0
        self.topPos = 0.0
        self.leftPos = 0.0
        self.cellSize = 0.0
        self.X0 = []
        self.Y0 = []
        self.Z0 = []
        self.s_list = []  # 读取的原始类二进制数据
        self.titleList = []
        self.treeViewSelections = []  # 选中的节点名列表
        self.ana_dict = {}
        self.tvSelectData = {}  # 导入的文件路径：文件数据(DataFrame)
        self.myContColor = 'hot_r'
        self.colors = {
            '黄-红(默认)': 'hot_r',
            '红-黄': 'hot',
            '白-蓝': 'YlGnBu',
            '蓝-白': 'YlGnBu_r',
            '黑-白': 'gray',
            '白-黑': 'gray_r'
        }
        self.vectorColor = 'black'
        self.vColors = {
            '黑(默认)': 'black',
            '红': 'red',
            '蓝': 'blue',
            '绿': 'green',
            '黄': 'yellow',
            '白': 'white'
        }

    def startAnaThread(self, frame0: Frame):
        self.ana_thread = AnalyseThread(target=self.ini, args=(frame0,))
        self.ana_thread.start()

    def createStringVar(self):
        self.var = StringVar()  # 初始化一个实时更新的字符串

    def createVectorStringVar(self):
        self.vectorVar = StringVar()  # 初始化一个实时更新的字符串

    def imageLoader(self, path: str, size: tuple):
        """
        图片加载器
        :param path: 路径
        :param size: 显示的大小
        :return:
        """
        self.image_open_origin = Image.open(path)  # 原始图片
        self.image_open = Image.open(path).resize(size)  # 裁剪后的图片
        self.image_load = ImageTk.PhotoImage(self.image_open)  # 加载后的已裁剪图片
        return self.image_open_origin, self.image_open, self.image_load

    def setMyContColor(self):
        """
        设置等值线填充颜色
        :return:
        """
        self.myContColor = self.var.get()

    def setVectorColor(self):
        """
        设置矢量颜色
        :return:
        """
        self.vectorColor = self.vectorVar.get()

    def clearAll(self):
        self.pBarMax = 0
        self.width = 0
        self.height = 0
        self.state = 0
        self.topPos = 0.0
        self.leftPos = 0.0
        self.cellSize = 0.0
        self.titleList.clear()
        self.s_list.clear()
        self.ana_dict.clear()

    def addVectorFile(self, frame10):
        with askopenfile(title='添加矢量数据', filetypes=[('Shapefile', '*.shp')]) as f:
            if f.name:
                try:
                    frame10.getTreeView().insert('', '0', f.name, text=f.name.split('/')[-1])
                except TclError:
                    showwarning('CscsGIS', f'<{f.name}>文件已导入！')
                else:
                    self.gdf = gpd.read_file(f.name)
                    self.tvSelectData[f.name] = self.gdf
                    frame10.getTreeView().updateText()
                    showinfo('CscsGIS', '成功导入矢量数据！')
            else:
                return

    def openFile(self, frame10):
        if self.state != 0 and self.state < 1:
            showwarning('CscsGIS', '请等待分析完成！')
            return
        with askopenfile(title='打开文件', filetypes=[('文本文件', '*.txt')]) as f:
            if f.name:
                try:
                    frame10.getTreeView().insert('', '0', f.name, text=f.name.split('/')[-1])
                except TclError:
                    showwarning('CscsGIS', f'<{f.name}>文件已导入！')
                else:
                    result = self.read(f.name)
                    (showinfo('CscsGIS', '成功导入数据！'), frame10.getTreeView().updateText()) if result else (
                        frame10.getTreeView().delete(f.name), showwarning('CscsGIS', '数据导入格式错误！'))
            else:
                return

    def read(self, file_name):
        if self.state != 0 and self.state < 1:
            showwarning('CscsGIS', '请等待分析完成！')
            return
        self.clearAll()
        titleRow = 0  # 标题行号
        title = ['ncols', 'nrows', 'xllcorner', 'yllcorner', 'cellsize', 'NODATA_value']
        file = open(file_name, mode='r', encoding=None)
        while True:
            content = file.readline()
            if content and titleRow < 6:
                if content.split()[0] != title[titleRow]:
                    return False
                self.titleList.append(content)
                titleRow += 1
            elif content:
                con_list = content.split()
                self.s_list.append(con_list)
            else:
                break
        self.width = int(self.titleList[0].split()[1])
        self.height = int(self.titleList[1].split()[1])
        self.cellSize = float(self.titleList[4].split()[1])
        self.leftPos = float(self.titleList[2].split()[1])
        self.topPos = float(self.titleList[3].split()[1]) + self.cellSize * self.height
        self.tvSelectData[file_name] = self.s_list
        return True

    def saveFile(self):
        if not self.ana_dict:
            showwarning('CscsGIS', '请先分析数据！')
            return
        if self.state != 0 and self.state < 1:
            showwarning('CscsGIS', '请等待分析完毕！')
            return
        with asksaveasfile(title='另存为', initialfile='新建文件', defaultextension='',
                           filetypes=[('Excel文件', '*.xlsx')]) as f:
            if f.name:
                self.print_in_excel(f.name)
            else:
                return

    def print_in_excel(self, file_name):
        """
        # 暂时弃用
        一键输出为Excel表
        :return:
        """
        cable_w_num = int(self.width / 8)  # 一行的格子数
        print('开始制作表格...')
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet('Sheet1')
        align_center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        worksheet.write(0, 0, '点号', align_center)
        worksheet.write(0, 1, '编码', align_center)
        worksheet.write(0, 2, 'E-W', align_center)
        worksheet.write(0, 3, 'N-S', align_center)
        worksheet.write(0, 4, '分维值', align_center)
        print('表格制作完毕，开始写入数据...')
        for cables, d in self.ana_dict.items():
            worksheet.write(int(cables) + 1, 0, int(cables) + 1, align_center)
            worksheet.write(int(cables) + 1, 2, (int(cables) % cable_w_num + 1) * 8, align_center)  # 列
            worksheet.write(int(cables) + 1, 3, (int(int(cables) / cable_w_num) + 1) * 8, align_center)  # 行
            worksheet.write(int(cables) + 1, 4, d, align_center)
        workbook.close()
        print('数据写入完毕!')

    def ini(self, frame0: Frame):
        """
        初始化数据栅格
        转换成 长宽均为8的倍数的栅格
        # 最多舍弃7行/列数据
        :return:
        """
        target_file_name = ''
        for file_name in self.treeViewSelections:
            suffix = file_name.split('.')[-1]
            target_file_name = file_name if suffix == 'txt' else ''
        if not target_file_name:
            showwarning('CscsGIS', '请先导入或选中数据！')
            return
        if self.state != 0 and self.state < 1:
            showwarning('CscsGIS', '请等待分析完成！')
            return
        if self.state == 1:
            if not askyesno("CscsGIS", '该数据已经分析过了，确定重新分析吗？'):
                return
        self.read(target_file_name)  # 读取目标文件数据
        el_height = self.height % 8
        el_width = self.width % 8
        # 循环删除第i行
        for i in range(-el_height, 0):
            self.s_list.pop(i)
        self.height -= el_height
        # 循环删除第j列
        for i in range(self.height):
            for j in range(-el_width, 0):
                self.s_list[i].pop(j)
        self.width -= el_width
        self.base_spl(frame0, self.s_list)

    def base_spl(self, frame0: Frame, raster_list: list):
        """
        分割成基础单元并对每一个进行操作spl
        :return:
        """
        final_dict = {}
        cable_w_num = int(self.width / 8)  # 一行的格子数
        cable_h_num = int(self.height / 8)  # 一列的格子数
        cable_count = cable_w_num * cable_h_num  # 基础单元格子数
        np_array = np.array
        for cables in range(cable_count):
            each_list = self.cable_content(raster_list, cables, cable_w_num, 8)
            each_list_two_dimension = np_array(each_list).reshape(8, 8)
            final_dict[cables] = self.spl(each_list_two_dimension)
        self.analyze(frame0, final_dict)

    def spl(self, each_cable_data_list: list):
        """
        分割并统计
        :param each_cable_data_list: 一个基础格子的数据
        :return:dict
        """
        count_dict = {}  # 对应关系字典（分割：含1的格子数）
        n = 1  # 一行的格子数
        length = len(each_cable_data_list)
        while int(length / n):
            count = 0
            cable_count = n * n  # 格子总数
            each_width = int(length / n)  # 一个格子的宽度（高度）
            for cables in range(cable_count):
                each_list = self.cable_content(each_cable_data_list, cables, n, each_width)
                if self.each_has(each_list):
                    count += 1
            count_dict[1 / n] = count
            n *= 2
        return count_dict

    @staticmethod
    def cable_content(data_list: list, cables: int, cable_w_num: int, each_width: int):
        """
        定出每个格子的内容
        :param data_list: 父数据
        :param cables: 格子标号
        :param cable_w_num: 一行的格子数
        :param each_width: 格子宽度（长度）
        :return: list
        """
        line = int(cables / cable_w_num)  # 该格子在第line行（从0开始的格子坐标）
        col = int(cables % cable_w_num)  # 该格子在第col列# （从0开始的格子坐标）
        startLine, endLine = each_width * line, each_width * (line + 1)  # 该格子起始行数和终止行数（栅格坐标）
        startCol, endCol = each_width * col, each_width * (col + 1)  # 起始列数和终止列数
        each_list = [data_list[i][j] for i in range(startLine, endLine) for j in range(startCol, endCol)]
        return each_list

    @staticmethod
    def each_has(content: list):
        """
        判断该格子是否有1
        :param content: 该格子内容
        :return:
        """
        for i in content:
            if int(i) == 1:
                return True
        return False

    def analyze(self, frame0: Frame, final_relation_dict: dict):
        """
        对final_dict进行最小二乘法拟合
        :param frame0:
        :param final_relation_dict: 每个基础格子的关系数据字典（格子序号：关系数据）
        :return:
        """
        self.ana_dict.clear()
        my_ana_dict = {}
        i = 0
        np_dot = np.dot
        sympy_diff = sympy.diff
        sympy_solve = sympy.solve
        sympy_symbols = sympy.symbols
        final_dict_len = len(final_relation_dict)  # 总格子数
        for cables, anas in final_relation_dict.items():
            Lab = []
            L_append = Lab.append
            L_anas = len(anas)
            count = 0  # 该格子各边长对应的1的数量=0的边长个数
            a, b = sympy_symbols('a b')
            for k, v in anas.items():
                i += 1
                self.pBarMax = final_dict_len * L_anas
                self.state = i / (final_dict_len * L_anas)
                if not v:
                    x, y = log(float(k), 10), 0
                    count += 1
                else:
                    y, x = log(float(v), 10), log(float(k), 10)
                L_append((y - a * x - b))
                frame0.pBar['maximum'] = final_dict_len * L_anas
                frame0.pBar['value'] = i
                frame0.update()
            if count == 4:  # 当边长全对应0个1时，说明该格子中无断裂构造，直接将其分形维数赋值为0，且跳过下面的最小二乘法分析
                my_ana_dict[cables] = 0
                continue
            # 最小二乘法求解a和b
            Lab_sum = np_dot(Lab, Lab)  # 求平方和
            pda = sympy_diff(Lab_sum, a)  # 对a求偏导
            pdb = sympy_diff(Lab_sum, b)
            sols = sympy_solve([pda, pdb], a, b)
            my_ana_dict[cables] = round(-sols.get(a), 5)  # 分维值保留5位小数
        self.ana_dict = my_ana_dict
        IDW_D_Len = self.image_init(my_ana_dict)
        showinfo('CscsGIS', f'分析完毕！\n计算得到{final_dict_len}个分维值\n通过IDW插值拟合了{IDW_D_Len}个分维值')

    def image_init(self, my_ana_dict: dict):
        """
        计算画图所需的X0,Y0,Z0
        :return: int
        """
        # plt.close()  # 清除原图
        cable_w_num = int(self.width / 8)  # 一行的基础格子数
        cable_h_num = int(self.height / 8)
        z = []
        # 数据点的x,y轴坐标尺,-4将分维值放到格子中间
        # x, y = np.linspace(8 - 4, self.width - 4, cable_w_num), np.linspace(8 - 4, self.height - 4, cable_h_num)
        x = np.linspace((8 - 4) * self.cellSize + self.leftPos, (self.width - 4) * self.cellSize + self.leftPos,
                        cable_w_num)
        y = np.linspace((8 - 4) * self.cellSize + self.topPos, self.topPos - (self.height - 4) * self.cellSize,
                        cable_h_num)
        z = [float(d) for d in my_ana_dict.values()]
        # 网格的坐标
        xGrid = np.linspace(self.leftPos, self.width * self.cellSize + self.leftPos, cable_w_num + 1)
        yGrid = np.linspace(self.topPos, self.topPos - self.height * self.cellSize, cable_w_num + 1)
        # idw算法分析
        idw = IDW(xGrid, yGrid, x, y, z)  # 实例化算法对象
        z0 = idw.getVFractalDimension()  # 网格的拟合分维值
        # 数据对齐
        self.X0, self.Y0 = np.meshgrid(xGrid, yGrid)
        self.Z0 = np.array(z0).reshape(len(self.Y0), len(self.X0[0]))
        return len(z0)

    def show_image(self):
        """
        绘制、保存、呈现分形维数等值图
        """
        if self.state != 1:
            showwarning('CscsGIS', '请先分析数据！')
            return
        self.plt.close()  # 清除原图
        self.plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
        self.plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
        self.plt.rcParams['toolbar'] = 'toolmanager'  # 设置工具栏为自定义
        fig, ax = self.plt.subplots()
        for index, fileName in enumerate(self.treeViewSelections):
            data = self.tvSelectData[fileName]
            if isinstance(data, pd.DataFrame):
                data.plot(color=self.vectorColor, ax=ax, zorder=index + 2, alpha=1)  # 234..(上)图层
        # 填充等值线
        C0 = self.plt.contourf(self.X0, self.Y0, self.Z0, 10, cmap=self.myContColor, zorder=1, alpha=1)  # 1(底)图层
        # 添加等值线
        C1 = self.plt.contour(self.X0, self.Y0, self.Z0, 10)
        self.plt.clabel(C1, inline=True, fontsize=7)  # 标注等值线
        self.plt.colorbar(C0, fraction=0.046, pad=0.04, shrink=1.0)  # 添加色带
        self.plt.xlabel('注意: 1e4 (m)= 1.0 x 10000 (m), 默认单位为米', fontsize=10)
        self.plt.xticks(rotation=30, fontsize=10)
        self.plt.yticks(fontsize=10)
        self.plt.title('分形维数等值图')
        # 显示图表
        self.plt.show()

    @staticmethod
    def show_about():
        """
        软件信息
        """
        showinfo('CscsGIS',
                 'Author：Hao Fang\n'
                 'Instructor：Yue Liu\n'
                 'Version：1.2.1\n'
                 'Name：ConstructSystemComplexitySimulation')


pn = PublicNumber()
