import pickle
import datetime
import numpy as np
import pandas as pd
from joblib import dump

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, mean_squared_error

### Training the SVR on UCLA Dataset ###
# # Load Data
# data = np.array(pd.read_csv('./../../app_data/admission.csv'))

# # Get training and testing features and labels from train and test data
# tau = 0.7
# X = data[:,[3,6]] # Features cols for UR and GPA
# X[:,0] = 12-(X[:,0]*11)//5 # Re scale UR to 11
# X[:,1] = X[:,1]*(0.4) # Re Scale GPA to 4.0
# y = data[:,-1]  # Last column contains labels
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Pre-process the data
# scaler = StandardScaler()
# scaler.fit_transform(X_train)
# scaler.fit_transform(X_test)

# # Classification Labels
# Yc_train = np.where(y_train >= tau, 1, 0)
# Yc_test = np.where(y_train >= tau, 1, 0)

# # Regression Labels
# Yr_train = y_train
# Yr_test = y_test

# # Parameters
# C_range = np.logspace(-2, 10, 13)
# gamma_range = np.logspace(-9, 3, 13)
# param_grid = dict(gamma=gamma_range, C=C_range)
# kernel = "rbf"
# gamma_regression = "auto"

# # Train SVM classification model with RBF kernel using cross validation
# # cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
# # svm_c = GridSearchCV(SVC(kernel=kernel), param_grid=param_grid, cv=cv)
# # svm_c.fit(X_train, Yc_train)

# # print("The best parameters are %s with a score of %0.2f"
# #       % (svm_c.best_params_, svm_c.best_score_))

# # Train SVM Regression model with rbf kernel
# svm_r = SVR(gamma=gamma_regression, C=1.0, epsilon=0.2)
# svm_r.fit(X_train, Yr_train)

# dump(svm_r, './models/svm.joblib')
# # Test trained models
# print(X_test)
# Yr_pred = svm_r.predict(X_test)
# print(mean_squared_error(Yr_test, Yr_pred))

### Training the SVR on any Dataset in the training data collection ###
def train_svr(db, collection, model_name):
    # Create np arrays from training database
    X_tr, Y_tr = db.get_train_data(collection)

    # Scale the dataset
    scaler = StandardScaler()
    scaler.fit_transform(X_tr)

    # train a regression model
    svm_r = SVR(gamma='auto', C=1.0, epsilon=0.2)
    svm_r.fit(X_tr, Y_tr)

    # compress the model into binary and save other necessary model info
    model = pickle.dumps(svm_r)
    model_info = {}
    model_info['model'] = model
    model_info['name'] = model_name
    model_info['date'] = datetime.datetime.utcnow()

    return model_info



