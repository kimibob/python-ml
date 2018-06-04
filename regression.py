from sklearn.datasets import load_boston
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import ElasticNet

boston = load_boston()

#print(boston)

model = KNeighborsRegressor()
scoring = 'r2'
result = cross_val_score(model, boston.data, boston.target, cv=5, scoring=scoring)
print('KNeighbors Regression: %.3f' % result.mean())

model = Lasso()
result = cross_val_score(model, boston.data, boston.target, cv=5, scoring=scoring)
print('Lasso Regression: %.3f' % result.mean())

model = LinearRegression()
result = cross_val_score(model, boston.data, boston.target, cv=5, scoring=scoring)
print('Linear Regression: %.3f' % result.mean())

model = Ridge()
result = cross_val_score(model, boston.data, boston.target, cv=5, scoring=scoring)
print('Ridge Regression: %.3f' % result.mean())

model = SVR()
result = cross_val_score(model, boston.data, boston.target, cv=5, scoring=scoring)
print('SVM: %.3f' % result.mean())

model = DecisionTreeRegressor()
result = cross_val_score(model, boston.data, boston.target, cv=5, scoring=scoring)
print('CART: %.3f' % result.mean())

model = ElasticNet()
result = cross_val_score(model, boston.data, boston.target, cv=5, scoring=scoring)
print('ElasticNet Regression: %.3f' % result.mean())
