from keymind.ai_predictions.Predict import Predict

import tensorflow as tf

class PredictionService():
    """ Predict sınıfını kullanarak üretilen tahminlerin veri tabanına kaydının yapıldığı sınıf """

    predict = Predict()

    predict.make_prediction()

