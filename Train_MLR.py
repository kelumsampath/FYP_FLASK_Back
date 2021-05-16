import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pickle
from SharedFucntions import nearestFibo

def MLR():
    dataset = pd.read_csv("./csv/9_input_datset2.csv")

    y= dataset['previous_story_point']
    x= dataset[['estimated_test_score','Number of developers','Number of comments']]

    linear_regression = LinearRegression()
    linear_regression.fit(x,y)

    ##save the model
    pickle.dump(linear_regression, open('./Models/MultipleLinearRegressorModel.sav', 'wb'))

    y_pred= linear_regression.predict(x)
    # print(type(y_pred))
    for i,predSp in enumerate(y_pred):
        # print(temp)
        # print(i)
        y_pred[i]=nearestFibo(predSp)
    # dataset["Estimated_sp"]=np.round(y_pred)
    dataset["Estimated_sp"]=y_pred
    dataset.to_csv('./csv/9_final.csv', encoding='utf-8', mode='w', header=True, index=False)

    print('Mean Absolute Error:', metrics.mean_absolute_error(y, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y, y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y, y_pred)))

    accuracy={
        'Mean Absolute Error': metrics.mean_absolute_error(y, y_pred),
        'Mean Squared Error':metrics.mean_squared_error(y, y_pred),
        'Root Mean Squared Error': np.sqrt(metrics.mean_squared_error(y, y_pred))
    }
    return accuracy