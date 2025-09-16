import numpy as np
from scipy.optimize import curve_fit
import math as mt
from scipy.special import erf

def erf_func(x, sigma, nu):
    eps = 0.00000000001
    return 1 / 2 + 1 / 2 * erf(np.log(x + eps) - nu) / (sigma * np.sqrt(2))

def liner_func(x, a, b):
    return a * x + b

def exp_func(x, a, b, c):
    return a * np.exp(b*x) + c

def exp_func_fit(data_x, data_y):
    try:
        params = curve_fit(exp_func, data_x, data_y)
        return params
    except Exception as e: print(e)

def special_f(x, a, b, c):
    return a * x**b + c


def funk(c):
    def f(x, a, b):
        return a * x ** b + c
    return f

def funk_with_c(x,a,b,c):
    return a * x ** b + c

def funk_exp(c):
    def f(x, a, b):
        return a * np.exp(b*x) + c
    return f

#Один из 3 параметров закреплен и передается как c
def funk_fit(funk_3_paramters, data_x, data_y, c):
    try:
        temp = funk_3_paramters(c)
        params = curve_fit(temp, data_x, data_y)
        return params
    except Exception as e: print(e)

def funk_fit_with_c(funk_3_paramters, data_x, data_y):
    try:
        params = curve_fit(funk_3_paramters, data_x, data_y)
        return params
    except Exception as e: print(e)

def fit(data_x, data_y):
    try:
        params = curve_fit(special_f, data_x, data_y)
        return params
    except Exception as e: print(e)


def liner_func_fit(data_x, data_y):
    try:
        params = curve_fit(liner_func, data_x, data_y)
        return params
    except Exception as e: print(e)

def liner_func_fit_am(pro_res, amount_of_points):
    try:
        data_y = pro_res.check_wait
        data_x = pro_res.curr_sorted_times
        data_y_sort = data_y[0: amount_of_points: ]
        data_x_sort = data_x[0: amount_of_points: ]
        params = curve_fit(liner_func, data_x_sort, data_y_sort)
        return params[0][1]
    except Exception as e: print(e)

def erf_func_fit(data_x, data_y):
    params = curve_fit(erf_func, data_x, data_y)
    sigma_fit, nu_fit = params[0]; sigma, nu = float(sigma_fit), float(nu_fit)
    try:
        check_wait = mt.exp(nu + (sigma ** 2) / 2); dispersion = (mt.exp(sigma ** 2) - 1) * mt.exp(2 * nu + sigma ** 2)
        return check_wait, dispersion, sigma, nu
    except Exception as e: print(e); return 0, 0, sigma, nu

def to_get_funk_of_prob_for_all(normalize_data_list):
    result = [to_get_funk_of_prob(sublist) for sublist in normalize_data_list]
    y_funk_of_probability_list = [item[0] for item in result]
    x_funk_of_probability_list = [item[1] for item in result]
    check_wait_list = [item[2] for item in result]
    dispersion_list = [item[3] for item in result]
    sigma_list = [item[4] for item in result]
    nu_list = [item[5] for item in result]
    return y_funk_of_probability_list, x_funk_of_probability_list, check_wait_list, dispersion_list, sigma_list, nu_list

def to_get_funk_of_prob(normalize_data): #IN ARGS HAVE TO BE NORMALIZE DATA
    bins = 100
    n_data = normalize_data
    max_value = max(normalize_data)
    edges = np.linspace(0, max_value, num=bins)
    num_points_into_interval = np.histogram(n_data, bins=edges)[0]
    total_sum_of_points = np.sum(num_points_into_interval)
    probability_to_be_in_interval = num_points_into_interval / total_sum_of_points
    y_funk_of_probability = np.cumsum(probability_to_be_in_interval); x_funk_of_probability = edges[:-1]
    check_wait, dispersion, sigma, nu = erf_func_fit(x_funk_of_probability, y_funk_of_probability)
    return y_funk_of_probability, x_funk_of_probability, check_wait, dispersion, sigma, nu
