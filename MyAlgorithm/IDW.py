import numpy as np


class IDW:
    def __init__(self, xGrid: tuple, yGrid: tuple, sample_point_X: tuple, sample_point_Y: tuple,
                 fractalDimension: list, radius: int, n: int, frame0):
        """
        :param xGrid: 待拟合网格点群的x坐标群
        :param yGrid: 待拟合网格点群的y坐标群
        :param sample_point_X: 样本点群的x坐标群
        :param sample_point_Y: 样本点群的y坐标群
        :param fractalDimension: 样本点群对应的分形维数值列表
        :param radius: 搜索半径
        :param n: 幂
        """
        self.frame0 = frame0
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.sample_point_X = sample_point_X
        self.sample_point_Y = sample_point_Y
        self.fractalDimension = fractalDimension
        self.radius = radius
        self.n = n
        self.__vFractalDimension = []  # 拟合的分形维数列表
        self.start()

    def getVFractalDimension(self):
        """
        获取拟合的分形维数列表
        :return:
        """
        return self.__vFractalDimension

    def calDistance(self, xi: int, yi: int, x: int, y: int):
        """
        计算距离的n次幂
        :param xi: 网格点x
        :param yi: 网格点y
        :param x: 样本点x
        :param y: 样本点y
        :return:
        """
        return abs(x - xi) ** self.n + abs(y - yi) ** self.n

    @staticmethod
    def cal_D_byWeight(weight: list, fractalList: list):
        """
        返回最近的点的权重与分维值的乘积list
        :param fractalList: 最近的分维值列表
        :param weight: 权重列表
        :return:list
        """
        return np.array(weight) * np.array(fractalList)

    def calculate_D(self, xi: int, yi: int):
        """
        计算一个网格点的预测分维值
        :param xi: 该点的x坐标
        :param yi: 该点的y坐标
        :return:
        """
        dSqrt_dict = {}  # 索引:距离平方
        dSqrt_list = []  # 最近点的距离平方列表
        D_list = []  # 最近点的分维值列表
        i = 0
        for spy in self.sample_point_Y:
            for spx in self.sample_point_X:
                dSqrt_dict[i] = self.calDistance(xi, yi, spx, spy)
                i += 1
        dSqrt_sort_list = sorted(dSqrt_dict.items(), key=lambda x: x[1])[:self.radius]  # 排序取最近的radius个点
        for i in dSqrt_sort_list:
            dSqrt_list.append(i[1])
            D_list.append(self.fractalDimension[i[0]])
        dRec_list = 1 / np.array(dSqrt_list)  # 距离平方的倒数list
        dSum = np.sum(dRec_list)  # 倒数平方的和
        weight_list = np.array(dRec_list) / dSum  # 权重list
        # 若插值点与样本点刚好一致（距离为0），则直接取样本点的分维值
        D = np.sum(self.cal_D_byWeight(weight_list, D_list)) if dSqrt_list[0] else D_list[0]
        return D

    def start(self):
        """
        启动算法
        :return:
        """
        i = 0
        self.frame0.pBar['maximum'] = len(self.sample_point_X) * len(self.sample_point_Y)
        for yi in self.yGrid:
            for xi in self.xGrid:
                self.__vFractalDimension.append(self.calculate_D(xi, yi))
                self.frame0.pBar['value'] = i
                self.frame0.pBar.update()
                i += 1
