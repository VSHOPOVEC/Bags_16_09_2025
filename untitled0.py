import matplotlib.pyplot as plt 
import numpy as np
from scipy import optimize
import regex as re
file = 'C:/Users/mikhailm/Desktop/0810_F025_5000_50k_dia03_high_1728x1096.dat'
file2 = 'C:/Users/mikhailm/Desktop/0828_F025_5000_50k_dia03_high_1728x1096.dat'
pattern = '^point\t(\d+)\t(\d+)\t(\d+,*\d*)\t(\d+,*\d*)'
result = {}
dx=0.00392156862/1000
l = []

def fit_circle_least_squares(x, y):
    """
    Аппроксимация окружности методом наименьших квадратов
    Возвращает (center_x, center_y, radius)
    """
    def calc_R(x, y, xc, yc):
        """Вычисляет расстояния от центра до точек"""
        return np.sqrt((x - xc)**2 + (y - yc)**2)
    
    def f_2(c):
        """Функция для минимизации"""
        Ri = calc_R(x, y, *c)
        return Ri - Ri.mean()
    
    # Начальное приближение центра
    x_m = np.mean(x)
    y_m = np.mean(y)
    center_estimate = x_m, y_m
    
    # Оптимизация
    center, ier = optimize.leastsq(f_2, center_estimate)
    
    # Вычисление радиуса
    Ri = calc_R(x, y, *center)
    R = Ri.mean()
    
    return center[0], center[1], R

def m(file):
    result = {}
    l = []
    with open(file) as file:
        for line in file:
            res = re.findall(pattern, line)[0]
            if(int(res[1]) not in result):
                result[int(res[1])] = ([],[])
                l.append(int(res[1]))
                result[int(res[1])][0].append(float(res[2].replace(',', '.'))*dx)
                result[int(res[1])][1].append(float(res[3].replace(',', '.'))*dx)
            else:
                result[int(res[1])][0].append(float(res[2].replace(',', '.'))*dx)
                result[int(res[1])][1].append(float(res[3].replace(',', '.'))*dx)
    s = [fit_circle_least_squares(np.array((result[l_])[0]),np.array((result[l_])[1])) for l_ in l]
    time = [l_/5000 for l_ in l]
    radius = [float(s_[2]) for s_ in s]
    print(time, radius)
    plt.scatter(time, radius)
    plt.show()
    
m(file)
m(file2)