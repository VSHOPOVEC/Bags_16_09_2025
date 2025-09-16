import re
import os 

class Bags_array(object):
    #читает по отдельности каждый файл из папки, полученные данные сохраняет в массивы -> на выходе получаем массив бэгов
    #причем получаем в результате 3х мерный массив структура которого (массив бэгов(точка разрыва, линии))
    def read_path(self):
           paths = os.listdir(str(self.folder_path))
           self.bags_array = []
           for path in paths:
              l_dict = {} #содержит только линии
              rim_dict = {}  #содержит только рим
              x_p, y_p = None, None
              try:
                  with open(self.folder_path + "/" + path) as file:
                      time_min = 0
                      time_max = 1000
                      for line in file:
                          if re.search(self.regex_point, line):
                              data = re.findall(self.regex_point, line)[0]
                              time_min = int(data[2])/(self.fps)
                              x_p = float(data[3].replace(',', '.'))*self.dx
                              y_p = float(data[4].replace(',', '.'))*self.dx
                              break;
                      for line in file:
                           if re.search(self.regex_line, line):
                               data = re.findall(self.regex_line, line)[0]
                               name = data[1]
                               t_s = float(data[2])/(self.fps)
                               t_e = int(data[3])/(self.fps)
                               x_s = float(data[4].replace(',', '.'))*self.dx - x_p
                               y_s = float(data[5].replace(',', '.'))*self.dx - y_p
                               x_e = float(data[6].replace(',', '.'))*self.dx - x_p
                               y_e = float(data[7].replace(',', '.'))*self.dx - y_p
                               dy = y_e - y_s
                               dx = x_e - x_s
                               dt = t_e - t_s
                               x_p = (x_e + x_s)/2
                               y_p  = (y_e + y_s)/2 #ВОПРОС В ОПРЕДЕЛНИИ ТОЧЕК ДЛЯ РИМА. Также ли они определяются как для точек края разрыва
                               t_p = (t_e + t_s)/2
                               v_y = dy/dt
                               v_x = dx/dt
                               v_m = (v_x**2 + v_y**2)**(1/2)
                               if(re.match('rim(\d+)', name) and (time_min < t_p < time_max)):
                                   n_arr = int(re.findall('rim(\d)', name)[0])
                                   if (n_arr not in rim_dict): 
                                       rim_dict[n_arr] = []
                                       rim_dict[n_arr].append((n_arr, x_p, y_p, t_p, v_m, v_y, v_x))
                                   else:
                                       rim_dict[n_arr].append((n_arr, x_p, y_p, t_p, v_m, v_y, v_x))
                               elif(re.match('\d+', name)):
                                   n_arr = int(re.findall('\d+', name)[0])
                                   if (time_max < t_e): time_max = t_e
                                   if (n_arr not in rim_dict): 
                                       l_dict[n_arr] = []
                                       l_dict[n_arr].append((n_arr, x_p, y_p, t_p, v_m, v_y, v_x))
                                   else:
                                       l_dict[n_arr].append((n_arr, x_p, y_p, t_p, v_m, v_y, v_x))
                  self.bags_array.append([l_dict, rim_dict])
              except Exception as e:
                  print(e)

    def bag_processing(self):
        for bag in self.bags_array:
            l_dict, rim_dict = bag[0], bag[1]
            print(l_dict)
        
        
    
    
    def read_config_file(self):
        try:
            with open(self.сonfig_file_path) as file:
                data = [re.findall(self.regex_config_file_info, line) for line in file]
                self.dx = float(data[0][0][1])/1000#мм/кол-во пикселей
                self.fps = float(data[1][0][1])
                self.type_ = str(data[2][0][1])
        except Exception as e:
            print(e)
    
    def __init__(self, folder_path, сonfig_file_path):
        
        self.folder_path = folder_path
        self.сonfig_file_path = сonfig_file_path
        
        #регулярные выражения для сортировки файлов/бэгов внутри папок
        self.regex_line =  re.compile(r'^(line)\t(?:(rim\d+|\d+))\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)')
        self.regex_point = re.compile(r'^(point)\t+(\d+)*\t+(\d+,*\d*)\t+(\d+,*\d*)\t+(\d+,*\d*)')
        self.regex_config_file_info = re.compile(r'^(\w+)=(\d+.*\d*|\w+)')
        
        self.read_config_file()
        self.read_path()
        self.bag_processing()
        
        
    
            
            
F25 = Bags_array("C:/Users/mikhailm/Desktop/Bags/F25","C:/Users/mikhailm/Desktop/Bags/config_file.txt")
                        
                        
        