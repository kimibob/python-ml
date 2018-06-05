from sklearn.datasets import load_boston
import numpy as np
import pandas as pd
import time
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn import preprocessing

boston = load_boston()

#print(boston)

def knn_regression(train_x, train_y):
    from sklearn.neighbors import KNeighborsRegressor
    model = KNeighborsRegressor()
    model.fit(train_x, train_y)
    return model

def lasso_regression(train_x, train_y):
    from sklearn.linear_model import Lasso
    model = Lasso()
    model.fit(train_x, train_y)
    return model


def linear_regression(train_x, train_y):
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(train_x, train_y)
    return model


def sgd_regression(train_x, train_y):
    from sklearn.linear_model import SGDRegressor
    model = SGDRegressor(max_iter=10)
    model.fit(train_x, train_y)
    return model


def ridge_regression(train_x, train_y):
    from sklearn.linear_model import Ridge
    model = Ridge()
    model.fit(train_x, train_y)
    return model


def svm_regression(train_x, train_y):
    from sklearn.svm import SVR
    model = SVR(kernel='rbf', C=1e3, gamma=0.1)
    # model = SVR(kernel='poly', C=1e3, degree=4)
    # model = SVR(kernel='linear', C=1e3)
    model.fit(train_x, train_y)
    return model


def cart_regression(train_x, train_y):
    from sklearn.tree import DecisionTreeRegressor
    model = DecisionTreeRegressor()
    model.fit(train_x, train_y)
    return model


def elastic_regression(train_x, train_y):
    from sklearn.linear_model import ElasticNet
    model = ElasticNet()
    model.fit(train_x, train_y)
    return model


def gradient_boosting_regression(train_x, train_y):
    from sklearn.ensemble import GradientBoostingRegressor
    model = GradientBoostingRegressor()
    model.fit(train_x, train_y)
    return model

def read_data(data_file):
    data = pd.read_csv(data_file)
    train = data[:int(len(data)*0.9)]
    test = data[int(len(data)*0.9):]
    train_y = train.down
    train_x = train.drop('down', axis=1).drop('up', axis=1)
    test_y = test.down
    test_x = test.drop('down', axis=1).drop('up', axis=1)
    return train_x, train_y, test_x, test_y


def polynomial_regression(train_x, train_y):
    from sklearn.preprocessing import PolynomialFeatures
    # 需要同时对训练集和测试机进行多项式transform
    poly_reg = PolynomialFeatures(degree = 4)
    X_poly = poly_reg.fit_transform(train_x)
    X_ploly_df = pd.DataFrame(X_poly, columns=poly_reg.get_feature_names())
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X_poly, train_y)
    return model, poly_reg


def plot(x_axis, title, test_y, predict):
    fig,ax = plt.subplots()
    plt.title(title)
    plt.xlabel('hour of date (h)')
    plt.ylabel('downbytes (MB)')
    """set interval for y label"""
    #yticks = range(10,110,10)
    #ax.set_yticks(yticks)
    """set min and max value for axes"""
    #ax.set_ylim([10,110])
    #ax.set_xlim([58,42])
    plt.plot(x_axis, test_y,"x-", label="test_y")
    plt.plot(x_axis, predict,"o-", label="predict")
    # 坐标网格线
    plt.grid(True)
    # 右上角图例说明
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.show()


if __name__ == '__main__':
    data_file = "H:\\httpbytes.csv"
    thresh = 0.5
    model_save_file = None
    model_save = {}
    print('reading training and testing data...')
    train_x, train_y, test_x, test_y = read_data(data_file)
    # 横坐标的值
    x = test_x.hour
    regression = {
           #'LR':linear_regression
           #,'KNN':knn_regression
           #,'LASSO':lasso_regression
           #,'RIDGE':ridge_regression
           #'SVM':svm_regression
           #'GBDT':gradient_boosting_regression
            'SGD':sgd_regression
           #,'CART':cart_regression
           #,'ELASTIC':elastic_regression
           #,'POLY':polynomial_regression
    }
    for key in regression:
        print('******************* %s ********************' % key)
        start_time = time.time()
        print('training took %fs!' % (time.time() - start_time))
        # 多项式回归需要对数据进行特殊预处理
        if key == 'POLY':
            model, poly = regression[key](train_x, train_y)
            test_poly_x = poly.transform(test_x)
            predict = model.predict(test_poly_x)
        # 对于特征归一化(feature scaling)敏感的算法
        elif key == 'SVM' or key == 'SGD':
            scaler = preprocessing.StandardScaler().fit(train_x)
            train_x_scaled = scaler.transform(train_x)
            model = regression[key](train_x_scaled, train_y)
            test_x_scaled = scaler.transform(test_x)
            predict = model.predict(test_x_scaled)
        else:
            model = regression[key](train_x, train_y)
            predict = model.predict(test_x)

        #print('test_x: %s predict: %s test_y: %s' %(test_x,predict,test_y))
        r2 = metrics.r2_score(test_y, predict)
        print('r2: %.2f%%' % r2)
        plot(x, key+" r2:"+ str("%.2f" % r2), test_y,predict)

