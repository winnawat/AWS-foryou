"""
Downloads diabetes dataset and write them in data and target csvs
"""
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR


def get_diabetes(multiplier=1):
    x, y = datasets.load_diabetes(return_X_y=True)

    means = np.mean(x, axis=0)
    std = np.std(x)
    y_mean = np.mean(y)
    y_std = np.std(y)

    n, d = x.shape

    new_x = x
    new_y = y

    for i in range(0, multiplier):
        mock_x = x + np.random.normal(loc=0, scale=std, size=(n, d))
        mock_y = y + np.random.normal(loc=0, scale=y_std, size=(n, 1)).ravel()

        new_x = np.append(new_x, mock_x, axis=0)
        new_y = np.append(new_y, mock_y, axis=0)
    np.savetxt("./examples/x_diabetes.csv", new_x, delimiter=",")
    np.savetxt("./examples/y_diabetes.csv", new_y, delimiter=",")
    return new_x, new_y


def run_sklearn_diabetes(data_loc, target_loc):
    x = np.array(pd.read_csv(data_loc))
    y = np.array(pd.read_csv(target_loc))

    X_train, X_test, y_train, y_test = \
        train_test_split(x, y.ravel(), random_state=0)

    # Standardize the data
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # list to store models and their scores
    models = []
    scores = []

    # Fit regression model
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    linear_score = linreg.score(X_test, y_test)

    print("linear regression score = %f" % linear_score)

    models.append(linreg)
    scores.append(linear_score)

    # set grid search parameters
    parameters = \
        {
            'gamma': ('scale', 'auto'),
            'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
            'C': [0.0001, 0.001, 0.01, 0.1, 1, 2, 3, 5, 10, 20, 30, 40, 50],
            'degree': [3, 4, 5, 6, 7, 8],
        }

    svr = SVR()
    grid_svr = GridSearchCV(svr, parameters, cv=5, n_jobs=-1, iid=False)
    grid_svr.fit(X_train, y_train)

    best_estimator = grid_svr.best_estimator_
    print("best hyperparameters estimate from grid search = \n %s "
          % best_estimator)

    best_estimator_score = grid_svr.best_score_
    print("score from using best hyperparameters = %f"
          % best_estimator_score)

    models.append(best_estimator)
    scores.append(best_estimator_score)

    print("begining 6-components PCA decomposition")

    components = 6
    pca = PCA(n_components=components, svd_solver='full')
    pca.fit(X_train)
    varratio = np.sum(pca.explained_variance_ratio_)

    print("percentage of variance explained = %f" % varratio)

    pca_X_train = pca.transform(X_train)
    pca_X_test = pca.transform(X_test)

    print("repeat grid search with PCA-transformed data")

    # Fit svr model
    parameters = \
        {
            'gamma': ('scale', 'auto'),
            'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
            'C': [0.0001, 0.001, 0.01, 0.1, 1, 2, 3, 5, 10, 20, 30, 40, 50],
            'degree': [3, 4, 5, 6, 7, 8],
        }

    svr = SVR()
    grid_svr = GridSearchCV(svr, parameters, cv=5, n_jobs=-1, iid=False)
    grid_svr.fit(pca_X_train, y_train)

    best_estimator = grid_svr.best_estimator_
    print("best hyperparameters estimate from grid search = \n %s "
          % best_estimator)

    best_estimator_score = grid_svr.best_score_
    print("score from using best hyperparameters = %f"
          % best_estimator_score)

    models.append(best_estimator)
    scores.append(best_estimator_score)

    best_model = models[scores.index(max(scores))]

    return best_model
