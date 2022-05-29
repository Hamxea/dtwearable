import datetime

from datetime import datetime
from pathlib import Path
from loguru import logger
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from experiments.config import data_path, model_plots_path
from matplotlib import pyplot

ai_model_forcast_class = "ai.aimodels.ForcastingAllAIModel.ForcastingAllAIModel"
# Path of ai_models folder under User home
file_path = str(Path.home()) + model_plots_path


def forecast(lstm_model, cnn_model, rnn_model, gru_model, mlp_model, X_test, y_test):
    # Comparison of the evaluation metrics

    y_pred_lstm = lstm_model.predict(X_test)
    # logger.debug(y_pred_lstm)
    # y_pred_cnn = cnn_model.predict(X_test)
    # logger.debug(y_pred_cnn)
    y_pred_rnn = rnn_model.predict(X_test)
    # logger.debug(y_pred_rnn)
    y_pred_gru = gru_model.predict(X_test)
    # logger.debug(y_pred_gru)
    # flatten input
    n_input = X_test.shape[1] * X_test.shape[2]
    X_test = X_test.reshape(X_test.shape[0], n_input)
    y_pred_mlp = mlp_model.predict(X_test)
    # logger.debug(y_pred_mlp)

    plot_forcasting(y_test, y_pred_lstm, 'y_pred_cnn', y_pred_rnn, y_pred_gru, y_pred_mlp)
    # return y_test, y_pred_lstm, y_pred_cnn, y_pred_rnn, y_pred_gru, y_pred_mlp


def plot_forcasting(y_test, y_pred_lstm, y_pred_cnn, y_pred_rnn, y_pred_gru, y_pred_mlp):
    pyplot.figure(figsize=(16, 8))

    num_samples = 40

    pyplot.plot(reverse_transform(y_test[0:num_samples]), '.--', label='Original Values')
    pyplot.plot(reverse_transform(y_pred_lstm[0:num_samples]), 'r--', label='LSTM Prediction')
    #pyplot.plot(reverse_transform(y_pred_cnn[0:num_samples]), 'm--', label='CNN Prediction')
    pyplot.plot(reverse_transform(y_pred_rnn[0:num_samples]), 'g--', label='RNN Predictions')
    pyplot.plot(reverse_transform(y_pred_gru[0:num_samples]), 'o--', label='GRU Predictions')
    pyplot.plot(reverse_transform(y_pred_mlp[0:num_samples]), 'b--', label='MLP Predictions')
    pyplot.title('Blood Pressure Forecast for ' + str(num_samples) + ' sample of days.')
    pyplot.xlabel("Time Series Samples")
    pyplot.ylabel("Blood Pressure (Systolic & Diastolic)")
    pyplot.legend(loc='best')
    pyplot.show()

    save_model_plot(ai_model_forcast_class)


# Function to rescale whatever transformations we have done,
# this will be used to retransform the values to original values after forecast.

def reverse_transform(arr):
    # Convert to numpy array
    arr = np.array(arr)

    # print(arr.shape)
    # arr = arr.reshape(-1, 1)

    # get the normalized scaler
    scaler, normalized_df = normalized()

    # First reverse the minmax scaling
    arr_inv_normal = scaler.inverse_transform(arr)
    # print(arr_inv_normal.shape)

    # Reverse the log transformation and subtract 1 ( Note, we had added 1 earlier)
    arr_reverse = np.exp(arr_inv_normal) - 1
    # print(arr_reverse.shape)
    return (arr_inv_normal)


def get_dataset(dataset_parameters):
    """ Method that returns the appropriate dataset according to the dataset parameters """

    # dataset_start_time = dataset_parameters['dataset_start_time']
    # dataset_end_time = dataset_parameters['dataset_end_time']
    # dataset_window_size = dataset_parameters['window_size']
    # dataset_column_names_list = []
    # for i in range(dataset_window_size):
    #    dataset_column_names_list.append('F' + str(i))

    data = pd.read_csv(data_path, sep=',')
    df_data = data[["ap_hi", "ap_lo"]]

    return df_data


def normalized_time_series(df):
    # prepare data for normalization
    df_values = df.values
    df_values = df_values.reshape(-1, 1)
    # train the normalization
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(df_values)
    print('Min: %f, Max: %f' % (scaler.data_min_, scaler.data_max_))
    # normalize the dataset and print the first 5 rows
    normalized_df = scaler.transform(df_values)
    return scaler, normalized_df


def normalized():
    df = get_dataset('{param: }')
    return normalized_time_series(df)


def save_model_plot(ai_model_class):
    """ Save model file with pickle """

    ai_model_file_name = file_path + "/" + ai_model_class + "_" + str(
        datetime.now().timestamp()) + ".png"
    pyplot.savefig(ai_model_file_name, dpi='figure', format=None, metadata=None,
                   bbox_inches=None, pad_inches=0.1,
                   facecolor='auto', edgecolor='auto',
                   backend=None)
    print("ai_model_file_name:", ai_model_file_name)
    logger.debug("ai_model_file_name:", ai_model_file_name)
    return ai_model_file_name
