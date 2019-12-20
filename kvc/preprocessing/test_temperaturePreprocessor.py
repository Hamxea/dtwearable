from datetime import datetime, timedelta
from unittest import TestCase

from kvc.preprocessing.UnivariateTimeSeriesPreprocessor import UnivariateTimeSeriesPreprocessor
from kvc.restful.models.HemsireGozlemDTO import HemsireGozlemDTO


class TestTemperaturePreprocessor(TestCase):

    def test_differentiate_by_islem_no(self):
        li = []
        date = datetime.today()
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=3), 36, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=1), 38, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=0), 38, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 2, date - timedelta(hours=5), 36, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=2), 37, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 3, date - timedelta(hours=4), 37, None, None, None, None, None, None, None, None))

        temperature_preprocessor = UnivariateTimeSeriesPreprocessor()
        my_dict = temperature_preprocessor.differentiate_by_islem_no(li)

        islem_no = 1
        self.assertEqual(3, len(my_dict))
        self.assertTrue(islem_no in my_dict)
        self.assertEqual(4, len(my_dict[islem_no][-1]))

        islem_no = 2
        self.assertTrue(islem_no in my_dict)
        self.assertEqual(1, len(my_dict[islem_no][-1]))

        islem_no = 4
        self.assertTrue(islem_no not in my_dict)

    def test_windowing(self):
        li = []
        date = datetime.today()
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=5), 36, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=4), 37, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=3), 38, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=2), 39, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 1, date - timedelta(hours=1), 40, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 2, date - timedelta(hours=5), 36, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 3, date - timedelta(hours=4), 37, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 3, date - timedelta(hours=3), 38, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 3, date - timedelta(hours=2), 39, None, None, None, None, None, None, None, None))
        li.append(HemsireGozlemDTO(1, 3, date - timedelta(hours=1), 40, None, None, None, None, None, None, None, None))
        li.sort(key=lambda x: x.olcum_tarihi)
        temperature_preprocessor = UnivariateTimeSeriesPreprocessor()
        my_dict = temperature_preprocessor.differentiate_by_islem_no(li, 2)

        df = temperature_preprocessor.windowing(my_dict, feature_name='vucut_sicakligi', window_size=3, column_list=list("ABC"))

        self.assertEqual(5, len(df))
        self.assertEqual(5, df.shape[0])
        self.assertEqual(3, df.shape[1])
        self.assertEqual(37, df['2'].iloc[0])
        self.assertEqual(40, df['3'].iloc[4])