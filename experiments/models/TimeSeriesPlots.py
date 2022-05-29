import os
import pickle
import pandas as pd
from datetime import datetime
from pathlib import Path

from keras.distribute.distribute_strategy_test import get_dataset
from loguru import logger
from matplotlib import pyplot

from experiments.config import model_plots_path, data_path


class TimeSeriesPlots():
    """ Long Short TermMemory (lstm) with 1-Step Output """

    global lstm_model
    global graph
    global EPOCHS
    EPOCHS = 25

    # Path of ai_models folder under User home
    file_path = str(Path.home()) + model_plots_path
    ai_model_class = "timeseries.analysis.plot"

    def __init__(self):
        # If the file_path folder does not exist in the file system, create it
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

    def get_dataset(self, dataset_parameters):
        """ Method that returns the appropriate dataset according to the dataset parameters """

        dataset_start_time = dataset_parameters['dataset_start_time']
        dataset_end_time = dataset_parameters['dataset_end_time']
        dataset_window_size = dataset_parameters['window_size']
        dataset_column_names_list = []
        for i in range(dataset_window_size):
            dataset_column_names_list.append('F' + str(i))

        data = pd.read_csv(data_path, sep=',')
        # df_data = data[["ap_hi", "ap_lo"]]

        return data

    def time_series_plots(self, df):

        # import plotly.express as px
        import plotly.graph_objs as go
        fig = go.Figure(data=go.Scatter(x=df['time'].astype(dtype=str),
                                        y=df['ap_hi'],
                                        marker_color='indianred', text="counts"))
        fig.update_layout({"title": 'Tweets about Malioboro from Jan 2020 to Jan 2021',
                           "xaxis": {"title": "Months"},
                           "yaxis": {"title": "Total tweets"},
                           "showlegend": False})
        ai_model_file_name = self.file_path + "/" + self.ai_model_class + "_" + str(
            datetime.now().timestamp()) + ".png"
        fig.write_image(ai_model_file_name, format="png", width=1000, height=600, scale=3)
        fig.show()

        print("ai_model_file_name:", ai_model_file_name)
        logger.debug("ai_model_file_name:", ai_model_file_name)

    def time_series_plots_2(self, df):

        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker

        df = df.set_index('time')
        # df = df.loc['2021-12-19':'2022-01-19']
        df = df.loc['2021-11-19':'2022-01-19']
        fig = plt.figure(figsize=(15, 7))
        plt.plot(df[['ap_hi', 'ap_lo']], 'o--')
        _ = plt.xticks(rotation=90)
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.title('Blood Pressure')
        plt.xlabel("Time")
        plt.ylabel("pressure (systolic & diastolic) ")
        plt.gca().legend(['systolic pressure', ' diastolic pressure'])
        plt.show()
        self.save_model_plot(self.ai_model_class)

    def save_model_plot(self, ai_model_class):
        """ Save model file with pickle """

        ai_model_file_name = self.file_path + "/" + ai_model_class + "_" + str(
            datetime.now().timestamp()) + ".png"
        pyplot.savefig(ai_model_file_name, dpi='figure', format=None, metadata=None,
                       bbox_inches=None, pad_inches=0.1,
                       facecolor='auto', edgecolor='auto',
                       backend=None)
        print("ai_model_file_name:", ai_model_file_name)
        logger.debug("ai_model_file_name:", ai_model_file_name)
        return ai_model_file_name

    def run_plot(self, dataset_parameters, hyperparameters):
        df_data = self.get_dataset(dataset_parameters)
        self.time_series_plots_2(df=df_data)
