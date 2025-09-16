import numpy as np
import matplotlib.pyplot as plt

import Processing_wind_flow
import Normalize_data
import Appr_data
import Data_loader

#const_normal = 10

#name_of_files = [ "F27_data_arr.dat", "F30_data_arr.dat", "F32_data_arr.dat", "F35_data_arr.dat", "F37_data_arr.dat", "F40_data_arr.dat", "F42_data_arr.dat", "F45_data_arr.dat", "F47_data_arr.dat", "F50_data_arr.dat"]

#num_of_files = [27,30,32,35,37,40,42,45,47,50]

# def get_value(r_input):
#     data = {
#         5: 2.78, 6: 2.57, 7: 2.45, 8: 2.37, 9: 2.31, 10: 2.26,
#         11: 2.23, 12: 2.20, 13: 2.18, 14: 2.16, 15: 2.15,
#         16: 2.13, 17: 2.12, 18: 2.11, 19: 2.10, 20: 2.093,
#         25: 2.064, 30: 2.045, 35: 2.032, 40: 2.023, 45: 2.016,
#         50: 2.009, 60: 2.001, 70: 1.996, 80: 1.991, 90: 1.987,
#         100: 1.984, 120: 1.980
#     }
#
#     if r_input <= 20:
#         return data.get(r_input, 2.78)
#
#     keys = sorted(data.keys())
#     closest_key = min(keys, key=lambda x: abs(x - r_input))
#     return data[closest_key]


class Pro_data(object):
   def __init__(self, object_data):
      self.sorted_points, self.sorted_times, self.unsorted_points, self.unsorted_times = object_data.get_data()
      self.check_wait = None
      self.dispersion = None
      self.curr_sorted_points = None
      self.curr_sorted_times = None
      self.average_times = None
      self.average_points = None
      self.nu = None
      self.sigma = None
      self.y_func_prob = None
      self.x_func_prob = None
      self.average_thik = None
      self.value_data = None
      self.processing_the_result(1,1,3,10)

   def average_thikness(self):
       self.average_thik = np.mean(np.array(self.unsorted_points))


   def calculate_average(self, amount = 3):
        self._funk_average_points(amount), self._funk_average_times(amount)
        return self.average_points, self.average_times

   def _funk_average_points(self, amount_of_arr):
       sorted_points = self.curr_sorted_points
       len_time_arr = len(sorted_points) - 1
       average_points = list(
            np.concatenate([sorted_points[index1] for index1 in range(index2, amount_of_arr + index2)]).tolist()
            for index2 in range(0, len_time_arr - amount_of_arr)
       )
       self.average_points = average_points

   def _funk_average_times(self, amount_of_arr):
       sorted_times = self.sorted_times
       len_time_arr = len(sorted_times) - 1
       temp_list_time = [np.mean(sorted_times[0 + index: amount_of_arr + index]) for index in
                           range(0, len_time_arr - amount_of_arr)]
       average_time = np.array([float(x) for x in temp_list_time])
       self.average_times = average_time


   def to_return_data(self):
       return (self.check_wait, self.dispersion), (self.curr_sorted_times, self.curr_sorted_times), (self.unsorted_times, self.unsorted_points), (self.nu, self.sigma), (self.sorted_points, self.sorted_times)

   def processing_the_result(self, limit_of_thikness, limit_of_time, amount, normalize_const):
       try:
          self.average_thikness()
          self._funk_average_times(amount)
          mask_sorted_times = np.array([limit_of_time > time for time in self.average_times])
          self.curr_sorted_times = (np.array(self.average_times)[mask_sorted_times])
          mask_sorted_points = [np.array([limit_of_thikness > item for item in sub_list_points]) for sub_list_points in self.sorted_points]
          self.curr_sorted_points = [np.array(arr)[mask_temp] for arr, mask_temp in zip(self.sorted_points, mask_sorted_points)]
          self._funk_average_points(amount)
          normalize_data, self.value_data = Normalize_data.to_normalize_list_data(normalize_const, self.average_points)  # нормируем lgyy
          y_funk_of_probability_list, x_funk_of_probability_list, check_wait_list, dispersion_list, sigma_list, nu_list = Appr_data.to_get_funk_of_prob_for_all(normalize_data)
          check_wait_list_correct = [Normalize_data.to_return_data(check_wait, value[0], value[1], normalize_const) for check_wait, value in zip(check_wait_list, value_data)]
          self.y_func_prob = y_funk_of_probability_list; self.x_func_prob = x_funk_of_probability_list
          self.check_wait = np.array(check_wait_list_correct)[mask_sorted_times]
          self.dispersion = np.array(dispersion_list)[mask_sorted_times]
          self.sigma = np.array(sigma_list)[mask_sorted_times]
          self.nu = np.array(nu_list)[mask_sorted_times]

       except Exception as e:
          print(e)

   def to_plot(self, name):
       plt.scatter(self.curr_sorted_times, self.check_wait)
       try:
          plt.title("plot of " + str(name) +f" thick(time) array of {len(self.unsorted_points)} points")
       except Exception as e:
           plt.title("plot of " + str(name) + f" thick(time)")
       plt.grid()
       plt.show()

   def to_plot_cloud(self, name):
       plt.scatter(self.unsorted_times, self.unsorted_points)
       plt.title(name)
       plt.grid()
       plt.show()

   def to_plot_cloud_without_max(self, name):
       un_time = self.unsorted_times; un_point = self.unsorted_points; max_data = max(un_point)
       plt.title(name)
       un_filt_points = [p for p in un_point if p != max_data]
       un_filt_times = [t for p, t in zip(un_point, un_time) if p != max_data]
       plt.scatter(un_filt_times, un_filt_points)
       plt.show()

   def to_plot_d_list(self, name): #dispertion_list
       plt.plot(self.curr_sorted_times, self.dispersion)
       plt.title(name)
       plt.yscale('log')
       plt.show()

   def to_plot_s_nu_list(self, name):
       plt.plot(self.curr_sorted_times, self.nu, label = "nu")
       plt.plot(self.curr_sorted_times, self.sigma, label = "sigma")
       plt.title(name)
       plt.legend()
       plt.show()

   def to_plot_sigma_list(self,name):
       plt.plot(self.curr_sorted_times, self.sigma, label="sigma")
       plt.title(name)
       plt.legend()
       plt.show()

   def to_plot_func_of_prob(self):
       for y_f, x_f, p, s, n in zip(self.y_func_prob, self.x_func_prob, self.average_points, self.sigma, self.nu):
           plt.plot(x_f, y_f); plt.grid(); plt.title(f"amount of points {len(p)}")
           x = np.arange(0, max(x_f), 0.01)
           y = np.array([Appr_data.erf_func(item, s, n) for item in x])
           plt.plot(x,y)
           plt.plot()
           plt.show()

   def to_plot_nu_list(self, name):
       plt.title(name)
       plt.plot(self.curr_sorted_times, self.nu); plt.show()

   def to_plot_appr(self,name = None, amount = 3):
       c = Appr_data.liner_func_fit_am(self, amount)
       try:
            ch, time = self.check_wait, self.curr_sorted_times
            t = Normalize_data.to_normalize_data(10, time)[0]
            ch_sort = ch.append(c)
            ch = Normalize_data.to_normalize_data(10, ch_sort)[0]
            a,b = Appr_data.funk_fit(Appr_data.funk, t, ch, c)[0]
            t_ = np.array(t)
            y = Appr_data.special_f(t_, a, b, c)
            if name is not None:
                plt.title(name)
                plt.plot(t_, y)
                plt.scatter(t_, ch)
                plt.grid()
                plt.show()
            return a, b, c
       except Exception as e:
            a, b = None, None
            return a, b, c


   def to_plot_appr_with_c(self,name = None, amount = 3):
       c = Appr_data.liner_func_fit_am(self, amount)
       try:
            ch, time = self.check_wait, self.curr_sorted_times
            t = Normalize_data.to_normalize_data(10, time)[0]
            ch = Normalize_data.to_normalize_data(10, ch)[0]
            a,b,c = Appr_data.funk_fit_with_c(Appr_data.funk_with_c, t, ch)[0]
            t_ = np.array(t)
            y = Appr_data.special_f(t_, a, b, c)
            if name is not None:
                plt.title(name)
                plt.plot(t_, y)
                plt.scatter(t_, ch)
                plt.grid()
                plt.show()
            return a, b, c
       except Exception as e:
            print(e)
            a, b = None, None
            return a, b, c


class Pro_data_new(Pro_data):
    def __init__(self, path):
        self.set = Data_loader.DataSet(path)
        self.Pro_data = super().__init__(self.set)
