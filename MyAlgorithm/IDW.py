import numpy as np


class IDW:
    def __init__(self, xGrid: tuple, yGrid: tuple, sample_point_X: tuple, sample_point_Y: tuple,
                 fractalDimension: list):
        """
        :param xGrid: 待拟合网格点群的x坐标群
        :param yGrid: 待拟合网格点群的y坐标群
        :param sample_point_X: 样本点群的x坐标群
        :param sample_point_Y: 样本点群的y坐标群
        :param fractalDimension: 样本点群对应的分形维数值列表
        """
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.sample_point_X = sample_point_X
        self.sample_point_Y = sample_point_Y
        self.fractalDimension = fractalDimension
        self.__vFractalDimension = []  # 拟合的分形维数列表
        self.start()

    def getVFractalDimension(self):
        """
        获取拟合的分形维数列表
        :return:
        """
        return self.__vFractalDimension

    @staticmethod
    def calDistance(xi: int, yi: int, x: int, y: int):
        """
        计算距离的平方
        :param xi: 网格点x
        :param yi: 网格点y
        :param x: 样本点x
        :param y: 样本点y
        :return:
        """
        return (x - xi) ** 2 + (y - yi) ** 2

    def cal_D_byWeight(self, weight: list):
        """
        返回每一个点的权重与分维值的乘积list
        :param weight:权重列表
        :return:list
        """
        return np.array(weight) * np.array(self.fractalDimension)

    def calculate_D(self, xi: int, yi: int):
        """
        计算一个网格点的预测分维值
        :param xi: 该点的x坐标
        :param yi: 该点的y坐标
        :return:
        """
        dSqrt_list = []  # 距离平方list
        dSqrt_list_append = dSqrt_list.append
        for sample_point_y in self.sample_point_Y:
            for sample_point_x in self.sample_point_X:
                dSqrt_list_append(self.calDistance(xi, yi, sample_point_x, sample_point_y))
        dRec_list = 1 / np.array(dSqrt_list)  # 距离平方的倒数list
        dSum = np.sum(dRec_list)  # 倒数平方的和
        weight_list = np.array(dRec_list) / dSum  # 权重list
        D = np.sum(self.cal_D_byWeight(weight_list))  # 计算的分维值
        return D

    def start(self):
        """
        启动算法
        :return:
        """
        vFractalDimension_append = self.__vFractalDimension.append
        for yi in self.yGrid:
            for xi in self.xGrid:
                IDW_D = self.calculate_D(xi, yi)
                vFractalDimension_append(IDW_D)
