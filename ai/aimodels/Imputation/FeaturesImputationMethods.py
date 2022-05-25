""" TODO: this class will use missing attributes methods......fix it when data comes in """

from fancyimpute import NuclearNormMinimization
from fancyimpute import KNN
from impyute.imputation.cs import fast_knn
from impyute.imputation.cs import mice
from fancyimpute import SoftImpute, BiScaler
from sklearn.preprocessing import Imputer
from sklearn.impute import SimpleImputer

import numpy as np


class FeaturesImputationMethods():
    """ Imputation methods with Multi-Step Output """

    def fancy_imp_nuclear__norm_min(self, dataset):
        """
      A simple implementation of  using cvxpy Missing features method (Exact Matrix Completion via Convex Optimization """

        dataset_filled_nnm = NuclearNormMinimization().fit_transform(dataset)
        return dataset_filled_nnm

    def fancy_imp_KNN(self, dataset):
        """ The k-Nearest Neighbors imputation is imposed for arrays with missing data.
         It only works on dense arrays with at most a few rows."""

        dataset_filled_knn = KNN(k=3).fit_transform(dataset)

        return dataset_filled_knn

    def fast_knn_imp(self, dataset):
        """ Impute using a variation of the nearest neighbors approach """

        dataset_filled_fast_knn = fast_knn(dataset, k=30)

        return dataset_filled_fast_knn

    def fancy_soft_imp(self, dataset):
        """ Spectral Arrangement Algorithms for Learning Large Missing Matrices
            It provides sparsity using singular value thresholding, rather than directly solving the nuclear norm target. """

        dataset_incomplete_normalized = BiScaler().fit_transform(dataset)
        dataset_filled_softimpute = SoftImpute().fit_transform(dataset_incomplete_normalized)

        return dataset_filled_softimpute

    def sklearn_mean_imp(self, dataset):
        """ fill missing values ​​with average column values ​​"""

        imputer = Imputer()
        dataset_filled_sklearn_impute = imputer.fit_transform(dataset)

        return dataset_filled_sklearn_impute

    def multivariate_feature_imp(self, dataset):
        """ SimpleImputer from sklearn.impute """
        """ Parameter strategy:
                            string ('mean', 'median', most_frequent, constant ) """

        imp = SimpleImputer(add_indicator=False, copy=True, fill_value=None,
                            missing_values=np.nan, strategy='mean', verbose=0)
        imp_fit = imp.fit(dataset)
        dataset_multivariate_feature_imputation = np.round(imp_fit.transform(dataset))

        return dataset_multivariate_feature_imputation

    def multivariate_imp_chained_equa(self, dataset):
        """ Using MultivariableImputation by Chained Equation (MICE) """

        dataset_mice = mice(dataset)

        return dataset_mice
