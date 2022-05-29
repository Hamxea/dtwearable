from loguru import logger

from experiments import config
from experiments.models import *
from experiments.models.ConvolutionalNeuralNetwork import ConvolutionalNeuralNetwork
from experiments.models.GatedRecurrentNeuralNetwork import GatedRecurrentNeuralNetwork
from experiments.models.LongShortTermMemory import LongShortTermMemory
from experiments.models.MultilayerPerceptron import MultilayerPerceptron
from experiments.models.RecurrentNeuralNetwork import RecurrentNeuralNetwork
from experiments.models.TimeSeriesPlots import TimeSeriesPlots
from experiments.utils import forecast

dataset_parameters = config.dataset_parameters
hyper_parameters = config.hyperparameters


def runner():
    logger.debug("Experiment Started!\n")

    # LSTM
    long_short_term_memory = LongShortTermMemory()
    lstm_model = long_short_term_memory.train(dataset_parameters, hyper_parameters)
    lstm_model, lstm_model_accuracy, X_test, y_test = lstm_model[0], lstm_model[1], lstm_model[2], lstm_model[3]
    # logger.debug('LSTM Accuracy : {0}%'.format(str(lstm_model_accuracy)))
    logger.debug("LSTM Finished!\n")

    # CNN
    # convolutional_neural_network = ConvolutionalNeuralNetwork()
    # cnn_model = convolutional_neural_network.train(dataset_parameters, hyper_parameters)
    # cnn_model, cnn_model_accuracy = cnn_model[0], cnn_model[1]['accuracy']
    # logger.debug('CNN Accuracy : {0}%'.format(str(cnn_model_accuracy)))
    logger.debug("CNN Finished!\n")

    # RNN
    recurrent_neural_network = RecurrentNeuralNetwork()
    rnn_model = recurrent_neural_network.train(dataset_parameters, hyper_parameters)
    rnn_model, rnn_model_accuracy = rnn_model[0], rnn_model[1]['accuracy']
    logger.debug('RNN Accuracy : {0}%'.format(str(rnn_model_accuracy)))
    logger.debug("RNN Finished!\n")

    # GRU
    gated_recurrent_neural_network = GatedRecurrentNeuralNetwork()
    gru_model = gated_recurrent_neural_network.train(dataset_parameters, hyper_parameters)
    gru_model, gru_model_accuracy = gru_model[0], gru_model[1]['accuracy']
    logger.debug('GRU Accuracy : {0}%'.format(str(gru_model_accuracy)))
    logger.debug("GRU Finished!\n")

    # MLP
    multi_layer_perceptron = MultilayerPerceptron()
    mlp_model = multi_layer_perceptron.train(dataset_parameters, hyper_parameters)
    mlp_model, mlp_model_accuracy = mlp_model[0], mlp_model[1]['accuracy']
    logger.debug('MLP Accuracy : {0}%'.format(str(mlp_model_accuracy)))
    logger.debug("MLP Finished!")

    # Plot Data
    time_series_plots = TimeSeriesPlots()
    time_series_plots.run_plot(dataset_parameters, hyper_parameters)
    logger.debug("Time Series Data Plotting Finished!\n")

    # Plot forcast

    # Get testing data
    forecast(lstm_model=lstm_model, cnn_model='cnn_model', rnn_model=rnn_model, gru_model=gru_model, mlp_model=mlp_model,
             X_test=X_test, y_test=y_test)
    logger.debug("Forcast Plotting Finished!\n")


if __name__ == "__main__":
    runner()

logger.debug("Experiment Finished!")
