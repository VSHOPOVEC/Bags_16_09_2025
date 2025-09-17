import re
import numpy as np
from sympy.logic.utilities import load_file
import Bags_array


class DataSet(object):
    def __init__(self, data_file_path = None, using_bags_arr = None, sorted_points = None, sorted_times = None, unsorted_points = None, unsorted_time = None):
        self.data_file_path = data_file_path
        self.sorted_points, self.sorted_times, self.unsorted_points, self.unsorted_times = sorted_points, sorted_times, unsorted_points, unsorted_time
        self.average_times, self.average_points = None, None
        if data_file_path is not None:
            self._load_file(data_file_path, using_bags_arr)

    def __add__(self, other):
        sorted_points, sorted_times, unsorted_points, unsorted_times = self.sorted_points, self.sorted_times, self.unsorted_points, self.unsorted_times
        sorted_points_1, sorted_times_1, unsorted_points_1, unsorted_times_1 = other.sorted_points, other.sorted_times, other.unsorted_points, other.unsorted_times
        gen_unsorted_time = unsorted_times + unsorted_times_1; gen_unsorted_points = unsorted_points_1 + unsorted_points
        gen_sorted_times, gen_sorted_points = zip(*(sorted(zip(sorted_times + sorted_times_1, sorted_points + sorted_points_1))))
        return DataSet([self.data_file_path, other.data_file_path], gen_sorted_points, gen_sorted_times, gen_unsorted_points, gen_unsorted_time)

    def return_paths(self):
        return self.data_file_path

    def get_data(self):
        return  self.sorted_points, self.sorted_times, self.unsorted_points, self.unsorted_times

    def _load_file(self, file_path, using_bag_arr):
        if self.sorted_points is None and  self.sorted_times is None and self.unsorted_points is None and self.unsorted_times is None:
            if(using_bag_arr == True):
                data = (Bags_array.Bags_array(file_path)).bags_array #Здесь вместо file_path должна стоять ссылка на папку
                unsorted_points = []; unsorted_times = []
                for line in data:
                    unsorted_points.append(data[0]); unsorted_times.append(data[1])
                    print(unsorted_points)
                    
            else:
                try:
                    with open(file_path) as file:
                        lines = file.readlines()
                        unsorted_times = []
                        unsorted_points = []
                        pattern = r'\s*?(?P<name>\b\d+\.\d+e[-,+]\d+\b|\bNaN\b)\s+'
                        for line in lines:
                            sub_list = re.findall(pattern, line)
                            if sub_list[0] != 'NaN' and sub_list[2] != 'NaN':
                                unsorted_times.append(sub_list[0])
                                unsorted_points.append(float(sub_list[2]))
                                temp_dict = {}
                                for time, point in zip(unsorted_times, unsorted_points):
                                    if time not in temp_dict:
                                        temp_result = []
                                        temp_dict[time] = temp_result
                                        temp_result.append(point)
                                    else:
                                        temp_dict[time].append(point)
                                times = list(temp_dict.keys())
                                unsorted_times = list(float(time) for time in unsorted_times)
                                sorted_points = list(temp_dict.values())
                                sorted_times = [float(time) for time in times]
                                sorted_times, sorted_points = zip(*(sorted(zip(sorted_times, sorted_points))))
                                self.sorted_points, self.sorted_times, self.unsorted_points, self.unsorted_times = sorted_points, sorted_times, unsorted_points, unsorted_times
                except Exception as e:
                    print(e)