from datetime import timedelta

import pandas as pd

class TemperaturePreprocessor():
    """ cvcxv """

    def __init__(self):
        print()

    def preprocess(self, my_list, time_interval_in_hours=2):
        pass

    def differentiate_by_islem_id(self, my_list, time_interval_in_hours=2):
        my_list.sort(key=lambda x: x.olcum_tarihi)
        my_dict = {}
        for i in range(len(my_list)):
            hemsire_gozlem_dto = my_list[i]
            if hemsire_gozlem_dto.islem_id not in my_dict:
                my_dict[hemsire_gozlem_dto.islem_id] = []
            inner_list = my_dict[hemsire_gozlem_dto.islem_id]

            if len(inner_list) < 1:
                inner_list.append([])

            last_windowed_element = inner_list[-1]

            if len(last_windowed_element) < 1:
                last_windowed_element.append(hemsire_gozlem_dto)
            else:
                last_hemsire_gozlem = last_windowed_element[-1]
                if hemsire_gozlem_dto.olcum_tarihi - last_hemsire_gozlem.olcum_tarihi < timedelta(hours=time_interval_in_hours):
                    last_windowed_element.append(hemsire_gozlem_dto)
                else:
                    new_windowed_element = [hemsire_gozlem_dto]
                    inner_list.append(new_windowed_element)

        return my_dict

    def windowing(self, my_dict, window_size = 3, column_list=list("ABC")):
        df = pd.DataFrame(columns=column_list)
        for key in my_dict:

            if len(my_dict[key][0]) > window_size-1:
                counter = 0
                for i in range(len(my_dict[key][0])):
                    if counter + window_size > len(my_dict[key][0]):
                        break
                    temp_list = []
                    for j in range(window_size):
                        temp_list.append(my_dict[key][0][counter+j].vucut_sicakligi)
                    counter += 1
                    print(temp_list)
                    df.loc[len(df)] = [temp_list][0]

        return  df




