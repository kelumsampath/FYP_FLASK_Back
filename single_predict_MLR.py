import pandas as pd
import numpy as np
import pickle

def single_predict_MLR():
    dataset = pd.read_csv("./csv/SinglePrediction/9_input_datset2.csv")

    y= dataset['previous_story_point']
    x= dataset[['estimated_test_score','Number of developers','Number of comments']]

    ###load saved model
    linear_Regression_Model = pickle.load(open('./Models/MultipleLinearRegressorModel.sav', 'rb'))
    y_pred= linear_Regression_Model.predict(x)

    dataset['Predicted_sp']=y_pred

    dataset['Predicted_sp (rounded)']=np.rint(y_pred)

    dataset.to_csv('./csv/SinglePrediction/10_final_output.csv', encoding='utf-8', mode='w', header=True, index=False)
    
    sp= int(np.rint(y_pred[0]))
    return sp