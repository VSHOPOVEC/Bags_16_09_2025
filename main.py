import numpy as np

import Data_loader
import Appr_data
import matplotlib.pyplot as plt

import Normalize_data
import Processing_data
from Normalize_data import to_normalize_data

Amount  = 3

if __name__ == '__main__':
    d_140_0 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F140_data_arr.dat")
    d_140_1 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F140_data_arr_old.dat")

    d_130_0 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F130_data_arr.dat")
    d_130_1 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F130_data_arr_new.dat")

    d_120_0 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F120_data_arr.dat")
    d_120_1 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F120_data_arr_new.dat")

    d_150_0 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F150_data_arr.dat")
    d_150_1 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F150_data_arr_new.dat")

    d_160_0 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F160_data_arr.dat")
    d_160_1 = Data_loader.DataSet("C:/Users/misha/Documents/Data/F160_data_arr_new.dat")

    d_140 = d_140_0 + d_140_1
    d_120 = d_120_1 + d_120_0
    d_130 = d_130_0 + d_130_1
    d_150 = d_150_0 + d_150_1
    d_160 = d_160_0 + d_160_1


    p_d_140 = Processing_data.Pro_data(d_140)
    p_d_120 = Processing_data.Pro_data(d_120)
    p_d_130 = Processing_data.Pro_data(d_130)
    p_d_150 = Processing_data.Pro_data(d_150)
    p_d_160 = Processing_data.Pro_data(d_160)

    p_d_160.processing_the_result(1, 1, Amount, 10)
    p_d_150.processing_the_result(1, 0.0012,Amount,10)
    p_d_140.processing_the_result(0.00008, 1, Amount,10)
    p_d_130.processing_the_result(1, 0.0015, Amount, 10)
    p_d_120.processing_the_result(1, 0.0014, Amount, 10)

    p_d_27 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F27_data_arr.dat")
    p_d_30 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F30_data_arr.dat")
    p_d_32 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F32_data_arr.dat")
    p_d_35 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F35_data_arr.dat")
    p_d_37 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F37_data_arr.dat")
    p_d_40 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F40_data_arr.dat")
    p_d_42 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F42_data_arr.dat")
    p_d_45 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F45_data_arr.dat")
    p_d_47 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F47_data_arr.dat")
    p_d_50 = Processing_data.Pro_data_new("C:/Users/misha/Documents/Data/Данные с большого канала/F50_data_arr.dat")

    p_d_27.processing_the_result(0.0002,1,Amount,10)
    p_d_30.processing_the_result(0.0001, 0.0030, Amount, 10)
    p_d_32.processing_the_result(0.0005, 0.00125, Amount, 10)
    p_d_35.processing_the_result(0.00005, 0.00125, Amount, 10)
    p_d_37.processing_the_result(0.00003,0.00127,Amount,10)
    p_d_40.processing_the_result(0.00004, 0.00125, Amount, 10)
    p_d_42.processing_the_result(1,1,Amount,10)
    p_d_45.processing_the_result(0.00004,0.001,Amount,10)
    p_d_50.processing_the_result(0.00015,1,Amount,10)


    #p_d_27.to_plot("27"); p_d_30.to_plot("30"); p_d_32.to_plot("32"); p_d_35.to_plot("35"); p_d_37.to_plot("37")
    #p_d_40.to_plot("40"); p_d_42.to_plot("42"); p_d_45.to_plot("45"); p_d_47.to_plot("47"); p_d_50.to_plot("50")
    #p_d = [p_d_27, p_d_30, p_d_32, p_d_35,p_d_37, p_d_40,p_d_45,p_d_47,p_d_50]
    #thick_zero = [item.to_plot_appr()[2] for item in p_d]
    #thick_zero_mask = [item is not None for item in thick_zero]
    #thick_zero = (np.array(thick_zero))[thick_zero_mask]
    #print(thick_zero)
    #p = [27,30,32,35,37,40, 45,47,50]
    #p = np.array(p)[thick_zero_mask]
    #plt.plot(p, thick_zero)
    #plt.show()







