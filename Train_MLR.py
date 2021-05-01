import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pickle

def MLR():
    dataset = pd.read_csv("./csv/9_input_datset2.csv")

    y= dataset['previous_story_point']
    x= dataset[['estimated_test_score','Number of developers','Number of comments']]

    linear_regression = LinearRegression()
    linear_regression.fit(x,y)

    ##save the model
    pickle.dump(linear_regression, open('./Models/MultipleLinearRegressorModel.sav', 'wb'))

    y_pred= linear_regression.predict(x)

    print('Mean Absolute Error:', metrics.mean_absolute_error(y, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y, y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y, y_pred)))

    accuracy={
        'Mean Absolute Error': metrics.mean_absolute_error(y, y_pred),
        'Mean Squared Error':metrics.mean_squared_error(y, y_pred),
        'Root Mean Squared Error': np.sqrt(metrics.mean_squared_error(y, y_pred))
    }
    return accuracy