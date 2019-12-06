import numpy as np
import pickle

class Predict():
    """ Hazırda eğitilmiş model üzerinden tahmin üreten sınıf """

    def make_prediction(self):
        """
        Modeli ve test edilmesi istenen parametreyi input olarak alan metod
        Pickle ile model yüklenir ve input üzerinde gerekli shape işlemleri yapılarak output üretilir
        """

        model_name = input("Hangi modeli kullanacaksınız: ") # my_model.pickle
        number_list = input("Test etmek istediğiniz diziyi araya boşluk koyarak giriniz: ") # 36.3 36.6 37.5 38.8 39.3
        predict_array = list(map(float, number_list.split()))

        model = pickle.load(open(model_name, 'rb'))

        Xnew = np.array([predict_array])
        ynew = model.make_prediction(Xnew)

        print("X=%s, Predicted=%s" % (Xnew[0], round(ynew[0][0], 2)))
        print()

        del model