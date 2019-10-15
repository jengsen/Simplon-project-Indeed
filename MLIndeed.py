from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


class MLIndeed():
    def __init__(self, X, y):
        '''
        Initializes the ML object
        :param X:
        :param y:
        '''

        self.X = X
        self.y = y
        self.bestModels = {}


    def metrics(self, y_test, y_pred):
        return accuracy_score(y_test, y_pred)

    def confusion_matrix(self, y_test, y_predict):
        '''
        to be done
        :param y_test:
        :param y_predict:
        :return:
        '''
    def grid_search(self, model, params, scoring):
        clf = GridSearchCV(model, params, scoring=scoring, n_jobs=-1)
        clf.fit(self.X, self.y)
        return clf.best_estimator_


    def grid_search_svm(self, params, scoring):
        svm = SVC(random_state=0)
        return self.grid_search(svm, params, scoring)


    def grid_search_random_forest(self, params, scoring):
        randomForest = RandomForestClassifier(random_state=0)
        return self.grid_search(randomForest, params, scoring)


    def grid_search_adaboost(self, params, scoring):
        ada = AdaBoostClassifier(random_state=0)
        return self.grid_search(ada, params, scoring)


    def grid_search_gboost(self, params, scoring):
        gboost = GradientBoostingClassifier(random_state=0)
        return self.grid_search(gboost, params, scoring)


    def best_models(self, params, scoring):
        self.bestModels['SVM'] = self.grid_search_svm(params['SVM'], scoring)
        self.bestModels['Random Forest'] = self.grid_search_random_forest(params['Random Forest'], scoring)
        self.bestModels['Ada Boost'] = self.grid_search_adaboost(params['Ada Boost'], scoring)
        self.bestModels['Gradient Boost'] = self.grid_search_gboost(params['Gradient Boost'], scoring)


params={'SVM': {'kernel': ['rbf'], 'C': [1, 10, 50, 100, 500, 1000], 'gamma': [0.1, 1, 5, 10, 50]},
        'Random Forest': {'n_estimators':  [10, 50, 100, 200], 'criterion': ['entropy', 'gini'], 'max_depth': [5, 10, 50, 100, None], 'max_features': ['auto', 5, 10, 20, None]},
        'Ada Boost': {'n_estimators':  [10, 50, 100, 200], 'learning_rate': [0.1, 1, 10]},
        'Gradient Boost': {'n_estimators':  [10, 50, 100, 200], 'learning_rate': [0.01, 0.1, 1], 'max_depth': [3, 5, 10, 50]}}
