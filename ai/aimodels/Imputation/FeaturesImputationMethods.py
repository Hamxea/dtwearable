""" TODO: bu sinif eksik özeklikler yöntemlar kullancak için......veri gelince düzeltecek """

from fancyimpute import NuclearNormMinimization
from fancyimpute import KNN
from impyute.imputation.cs import fast_knn
from impyute.imputation.cs import mice
from fancyimpute import SoftImpute, BiScaler
from sklearn.preprocessing import Imputer
from sklearn.impute import SimpleImputer


import numpy as np

class FeaturesImputationMethods():
  """ Eksik özeklikler (Imputation) yöntemlar with Multi-Step Output """

  def fancy_imputation_nuclear__norm_minimization(self, dataset):
      """ basit bir şekilde uygulanması cvxpy kullanarak Eksik özeklikler yöntem (Exact Matrix Completion via Convex Optimization """

      dataset_filled_nnm = NuclearNormMinimization().fit_transform(dataset)
      return dataset_filled_nnm

  def fancy_impute_KNN(self, dataset):
      """ k-Nearest Neighbors imputation eksik veri içeren diziler için empoze edilmiştir. Yalnızca en fazla birkaç satır içeren yoğun dizilerde çalışır."""

      dataset_filled_knn = KNN(k=3).fit_transform(dataset)

      return dataset_filled_knn

  def fast_knn_impyute(self, dataset):
      """ En yakın komşular yaklaşımının bir çeşidini kullanarak Impute """

      dataset_filled_fast_knn = fast_knn(dataset, k=30)

      return dataset_filled_fast_knn

  def fancy_soft_impute(self, dataset):
      """" Büyük Eksik Matrisleri Öğrenmek İçin Spektral Düzenleme Algoritmaları
            Nükleer norm hedefini doğrudan çözmek yerine, tekil değer eşiklemesi kullanarak seyrekliği sağlar. """

      dataset_incomplete_normalized = BiScaler().fit_transform(dataset)
      dataset_filled_softimpute = SoftImpute().fit_transform(dataset_incomplete_normalized)

      return dataset_filled_softimpute

  def sklearn_mean_impute(self, dataset):
      """ eksik değerleri ortalama sütun değerleriyle doldur """

      imputer = Imputer()
      dataset_filled_sklearn_impute = imputer.fit_transform(dataset)

      return dataset_filled_sklearn_impute

  def multivariate_feature_imputation(self, dataset):
      """ sklearn.impute'den SimpleImputer """
      """ Parameter strategy:
                            string ('mean', 'median', most_frequent, constant ) """

      imp = SimpleImputer(add_indicator=False, copy=True, fill_value=None,
                          missing_values=np.nan, strategy='mean', verbose=0)
      imp_fit = imp.fit(dataset)
      dataset_multivariate_feature_imputation = np.round(imp_fit.transform(dataset))

      return dataset_multivariate_feature_imputation

  def multivariate_imputation_chained_equation(self, dataset):
      """ Çok Değişkenli KullanmaImputation by Chained Equation (MICE) """

      dataset_mice = mice(dataset)

      return dataset_mice
