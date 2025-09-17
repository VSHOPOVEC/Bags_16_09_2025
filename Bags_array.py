
import re
import os 
import numpy as np

class Bags_array(object):
    #читает по отдельности каждый файл из папки, полученные данные сохраняет в массивы -> на выходе получаем массив бэгов
    #причем получаем в результате 3х мерный массив структура которого (массив бэгов(точка разрыва, линии))
    def read_path(self):
           files_path = self.files_path
           self.bags_array = []
           for path in files_path:
              try:
                  with open(self.folder_path + "/" + path) as file:
                      for line in file:
                          if re.search(self.regex_point, line):
                              data = re.findall(self.regex_point, line)[0]
                              x_p = float(data[3].replace(',', '.'))*self.dx
                              y_p = float(data[4].replace(',', '.'))*self.dx
                              break;
                      rim_dict = {}
                      l_dict = {}
                      for line in file:
                          if re.search(self.regex_rim, line):
                              data = re.findall(self.regex_rim, line)[0]
                              n_rim = int(data[1])
                              t_s = float(data[2])*(1/self.fps)
                              t_e = float(data[3])*(1/self.fps)
                              x_s = float(data[4].replace(',', '.'))*self.dx #перевели в м
                              y_s = float(data[5].replace(',', '.'))*self.dx
                              x_e = float(data[6].replace(',', '.'))*self.dx
                              y_e = float(data[7].replace(',', '.'))*self.dx
                              dy = y_e - y_s; dx = x_e - x_s; dt = t_e - t_s; t_m = (t_e + t_s)/2
                              v_x = dx/dt; v_y = dy/dt
                              if (n_rim not in rim_dict): 
                                      rim_dict[n_rim] = []
                                      rim_dict[n_rim].append((v_y, v_x, t_m))
                              else:
                                      rim_dict[n_rim].append((v_y, v_x, t_m))
                          elif not re.search(self.regex_point, line):
                              data = re.findall(self.regex_line, line)[0]
                              n_list = int(data[0])
                              t_s = float(data[1])*(1/self.fps)
                              t_e = float(data[2])*(1/self.fps)
                              x_s = float(data[3].replace(',', '.'))*self.dx - x_p #перевели в систему отчета, связанную с подвижной точкой разрыва
                              y_s = float(data[4].replace(',', '.'))*self.dx - y_p
                              x_e = float(data[5].replace(',', '.'))*self.dx - x_p
                              y_e = float(data[6].replace(',', '.'))*self.dx - y_p
                              dy = y_e - y_s; dx = x_e - x_s; dt = t_e - t_s;  t_m = (t_e + t_s)/2
                              v_x = dx/dt; v_y = dy/dt
                              if (n_list not in l_dict): 
                                      l_dict[n_list] = []
                                      l_dict[n_list].append((v_y, v_x, t_m))
                              else:
                                      l_dict[n_list].append((v_y, v_x, t_m))
                                      
                                      
                                      
                      #Обработка рима 
                      keys_rim = rim_dict.keys()
                      temp_arr_rim = []
                      for key in keys_rim: 
                          temp_arr_rim.append(list(rim_dict[key]))
                      vel_dict = {}
                      for arr in temp_arr_rim: 
                          for line in arr:
                              if(line[2] not in vel_dict):
                                  vel_dict[line[2]] = []
                                  vel_dict[line[2]].append(line)
                              else:
                                  vel_dict[line[2]].append(line)
                      key_v = vel_dict.keys()
                      temp_arr_vel_rim = []
                      for key in key_v:
                          temp_arr_vel_rim.append(list(vel_dict[key]))
                      #velocity_list = []
                      for list_vel in temp_arr_vel_rim:
                          len_list = len(list_vel)
                          sum_v_x = 0; sum_v_y = 0
                          for sublist_vel in list_vel:
                              v_y = sublist_vel[0]; v_x = sublist_vel[1]; t_m = sublist_vel[2]
                              sum_v_x = sum_v_x + v_x; sum_v_y = sum_v_y + v_y
                          #velocity_list.append((sum_v_y/len_list, sum_v_x/len_list,  t_m))
                          vel_dict[t_m] = (sum_v_y/len_list, sum_v_x/len_list)
                          
                          
                      #Обработка линий
                      keys_line = l_dict.keys()
                      temp_arr_lines = []
                      for key in keys_line: 
                          temp_arr_lines.append(list(l_dict[key]))
                      vel_dict_line = {}
                      for arr in temp_arr_rim: 
                          for line in arr:
                              if(line[2] not in vel_dict_line):
                                  vel_dict_line[line[2]] = []
                                  vel_dict_line[line[2]].append(line)
                              else:
                                  vel_dict_line[line[2]].append(line)
                      keys_vel_line = vel_dict_line.keys()
                      for key in keys_vel_line:
                              for line in vel_dict_line[key]:
                                  v_y = float(line[0]); v_x = float(line[1])
                                  v_y_r = float(vel_dict[key][0]); v_x_r = float(vel_dict[key][1])
                                  v_y_m = v_y - v_y_r; v_x_m = v_x - v_x_r
                                  v_result = (v_y_m**2 + v_x_m**2)**(1/2)
                                  time = key
                                  if(v_result != 0):
                                      self.bags_array.append((self.calculate_thikness(v_result), time))
              except Exception as e:
                  print(e)
        
    def calculate_thikness(self, velocity):
        return 2*self.sigma/((velocity**2)*self.rho)
    
    def find_paths_to_files(self):
        files_path = os.listdir(str(self.folder_path))
        files_path_np = np.array(files_path)
        files_config_mask = np.array([ bool(re.match(self.regex_config_file, path)) for path in files_path])
        self.сonfig_file_path = str(list(files_path_np[files_config_mask])[0])
        files_path_mask = np.array([ bool(re.match(self.regex_file, path)) for path in files_path])
        self.files_path = list(files_path_np[files_path_mask])
    
    def read_config_file(self):
        try:
            with open(self.folder_path + '/' + self.сonfig_file_path) as file:
                data = [re.findall(self.regex_config_file_info, line) for line in file]
                self.dx = float(data[0][0][1])/100#м/кол-во пикселей
                self.fps = float(data[1][0][1])#кадров/секунду
                self.type_ = str(data[2][0][1])
                self.rho = float(data[4][0][1])
                self.sigma = float(data[3][0][1]) 
        except Exception as e:
            print(e)
    
    def __init__(self, folder_path):
        
        self.folder_path = folder_path
        
        #регулярные выражения для сортировки файлов/бэгов внутри папок
        self.regex_rim =  re.compile(r'^.+\t(rim(\d+))\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)')
        self.regex_line = re.compile(r'^.+\t(\d+)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)')
        self.regex_point = re.compile(r'^(point)\t+(\d+)*\t+(\d+,*\d*)\t+(\d+,*\d*)\t+(\d+,*\d*)')
        self.regex_config_file_info = re.compile(r'^(\w+)=(\d+.*\d*|\w+)')
        
        self.regex_config_file = re.compile(r'config_file')
        self.regex_file = re.compile(r'.*F\d+.*\.dat')
        
        self.find_paths_to_files()
        
        self.read_config_file()
        self.read_path()
        