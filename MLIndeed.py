from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


class MLIndeed():
    def __init__(self, X_train, X_test, y_train, y_test):
        '''
        Initializes the ML object
        :param X: X_train
        :param y: y_train
        '''

        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.bestModels = {}


    def accuracy(self):
        """
        accuracy of each model
        :return:
        """
        json = {}
        for clf in self.bestModels:
            model_accu = {
                'test_accuracy': accuracy_score(self.bestModels[clf].best_estimator_.predict(self.X_test), self.y_test),
                'train_accuracy': accuracy_score(self.bestModels[clf].best_estimator_.predict(self.X_train), self.y_train)}
            json[clf] = model_accu
        return json

    def confusion_matrix(self, y_test, y_predict):
        '''
        to be done
        :param y_test: ...
        :param y_predict: ...
        :return:
        '''
    def grid_search(self, model, params, scoring):
        '''
        Search the best parameters according to the scoring metric
        for the machine learning model
        :param model: machine learning object
        :param params: parameters to test
        :param scoring: metric
        :return: gridsearch object
        '''
        clf = GridSearchCV(model, params, scoring=scoring, n_jobs=-1)
        clf.fit(self.X_train, self.y_train)
        return clf


    def grid_search_svm(self, params, scoring):
        svm = SVC(random_state=0)
        return self.grid_search(svm, params, scoring)


    def grid_search_random_forest(self, params, scoring):
        randomForest = RandomForestClassifier(random_state=0, n_jobs=-1)
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



