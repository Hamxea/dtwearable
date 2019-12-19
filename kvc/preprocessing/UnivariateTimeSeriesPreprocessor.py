from datetime import timedelta

import pandas as pd

class UnivariateTimeSeriesPreprocessor():
    """ Tek feature üzerinden eğitim yapacak algoritmalar için veriyi istenen formata çeviren sınıf
        Verilerin önce işlem id'ye göre sonra da interval'e göre sıralanması metotlarını içerir
        Sonuç bir dataframe olarak döner
    """

    def __init__(self):
        print()

    def preprocess(self, sorted_dto_list, time_interval_in_hours=2):
        differentiated_dict = self.differentiate_by_islem_id(sorted_dto_list, time_interval_in_hours)
        windowed_df = self.windowing(differentiated_dict, feature_name='vucut_sicakligi', window_size=3, column_list=list("ABC"))
        return windowed_df

    def differentiate_by_islem_id(self, sorted_dto_list, time_interval_in_hours):
        """ Gönderilen dto listesini işlem_id ye göre gruplayıp bir dict'e çeviren metot
            Buraya gelen listenin, ölçüm tarihine göre sıralanmış olması gerekmektedir
        """

        differentiated_dict = {}
        for i in range(len(sorted_dto_list)):
            dto = sorted_dto_list[i]
            if dto.islem_id not in differentiated_dict:
                differentiated_dict[dto.islem_id] = []
            inner_list = differentiated_dict[dto.islem_id]

            if len(inner_list) < 1:
                inner_list.append([])

            last_windowed_element = inner_list[-1]

            if len(last_windowed_element) < 1:
                last_windowed_element.append(dto)
            else:
                last_hemsire_gozlem = last_windowed_element[-1]
                if dto.olcum_tarihi - last_hemsire_gozlem.olcum_tarihi < timedelta(hours=time_interval_in_hours):
                    last_windowed_element.append(dto)
                else:
                    new_windowed_element = [dto]
                    inner_list.append(new_windowed_element)

        return differentiated_dict

    def windowing(self, differentiated_dict, feature_name, window_size, column_list):
        """
        işlem id'ye göre gruplanmış olan dict'leri, window size ve feature name'e göre listelere çeviren
        ve dataframe'e kaydeden metot. window_size ile column_list'in uzunluğu aynı olmalıdır.
        Örnek: window_size:5, column_list=list("ABCDE") veya window_size:3, column_list=list("ABC")
        """

        windowed_dataframe = pd.DataFrame(columns=column_list)
        for key in differentiated_dict:

            if len(differentiated_dict[key][0]) > window_size-1:
                counter = 0
                for i in range(len(differentiated_dict[key][0])):
                    if counter + window_size > len(differentiated_dict[key][0]):
                        break
                    temp_list = []
                    for j in range(window_size):
                        temp_list.append(getattr(differentiated_dict[key][0][counter + j], feature_name))
                    counter += 1
                    print(temp_list)
                    windowed_dataframe.loc[len(windowed_dataframe)] = [temp_list][0]
        return windowed_dataframe




