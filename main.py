from ScrapperIndeed import ScrapperIndeed
import pymongo
from pymongo import MongoClient
from selenium import webdriver

# SCRAPPING
# client = MongoClient('localhost', 27017)
# db = client['Simplon_Indeed']
# collection=db['job_offers']
# city_to_scrap = ['Nantes', 'Lyon', 'Toulouse', 'Bordeaux', 'Paris']
# work_to_scrap = ['data scientist', 'data analyst', 'developpeur', 'business intelligence']
#
# scrapperIndeed=ScrapperIndeed(collection)
# scrapperIndeed.scrapp_searches(work_to_scrap, city_to_scrap)

from PreprocessIndeed import PreprocessIndeed
from MLIndeed import MLIndeed
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# countVec_titre = CountVectorizer(ngram_range=(1, 2), min_df=.005, max_df=0.8, max_features=10)
# countVec_description = CountVectorizer(ngram_range=(1, 2), min_df=.02, max_df=0.8, max_features=20)
countVec_titre = CountVectorizer(ngram_range=(1, 2), min_df=.005, max_df=0.8)
countVec_description = CountVectorizer(ngram_range=(1, 2), min_df=.02, max_df=0.8)
preprocess = PreprocessIndeed('data/BDD_14_10_2019.json')

preprocess.preprocess_df(countVec_titre, countVec_description, correlation_description=0.1, correlation_titre=0.1)
# preprocess.preprocess_df(countVec_titre, countVec_description)

X_train, X_test, y_train, y_test = \
    train_test_split(preprocess.df.drop(['Salaire'], axis=1),
                     preprocess.df['Salaire'],
                     test_size=0.25, random_state=0)
# print(X_train.columns)
# print(y_train)
params = {'Log Reg': {'C': [1, 10]},
          'SVM': {'kernel': ['rbf'], 'C': [1, 10, 50, 100, 500, 1000], 'gamma': [0.1, 1, 5, 10, 50]},
          'Random Forest': {'n_estimators': [10, 50, 100], 'criterion': ['entropy', 'gini'],
                            'max_depth': [2, 3, 5], 'max_features': ['auto', 5, 10, 20]},
          'Ada Boost': {'n_estimators': [10, 50, 100], 'learning_rate': [0.1, 1, 10]},
          'Gradient Boost': {'n_estimators': [10, 20, 30], 'learning_rate': [0.01, 0.1, 1],
                             'max_depth': [3, 5]},
          'X Gradient Boost': {'n_estimators': [10, 20, 30]}}

models = MLIndeed(X_train, X_test, y_train, y_test)
models.best_models(params, 'accuracy')
print(models.accuracy())
