import csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle

def write_csv_file(path, data_array,access_type):
    with open(path, access_type, newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in data_array:
            writer.writerow(row)

def RandomForest():
    tfidf_value_matrix = pd.read_csv('./csv/5_tfidf_for_corpus.csv')

    number_of_columns = len(tfidf_value_matrix.columns)

    #tfidf value matrix(independent variables)
    X = tfidf_value_matrix.iloc[:, 0:number_of_columns-2].values
    #get story point list (dependent variable)
    y = tfidf_value_matrix.iloc[:, number_of_columns-1].values

    #separate training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)


    regressorModel = RandomForestRegressor(n_estimators=20, random_state=0)
    regressorModel.fit(X_train, y_train)

    ##save the model
    pickle.dump(regressorModel, open('./Models/RandomForestModel.sav', 'wb'))

    #Evaluation
    y_pred = regressorModel.predict(X_test)

    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    accuracy={
        'Mean Absolute Error': metrics.mean_absolute_error(y_test, y_pred),
        'Mean Squared Error':metrics.mean_squared_error(y_test, y_pred),
        'Root Mean Squared Error': np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    }

    ###estimates story point for the dataset (used to train)

    ##read and estimate for new dataset
    dataset = pd.read_csv('./csv/5_tfidf_for_corpus.csv')

    Existing_text_features=sc.fit_transform(dataset.iloc[:, 0:number_of_columns-2].values)

    text_score = regressorModel.predict(Existing_text_features)

    #add new colums to write new values
    dataset["test_score"]=text_score
    dataset["test_score_round"]=np.rint(text_score)

    write_csv_file('./csv/6_estimated_new_text_score.csv',dataset.to_numpy(),'w')

    ##save resultant format
    resultant_text_score = dataset[['issue_key','story_point','test_score', 'test_score_round']]
    write_csv_file('./csv/7_resultant_new_text_score.csv',[['Issue key','previous_story_point','estimated_test_score', 'text_score_rounded']],'w')
    write_csv_file('./csv/7_resultant_new_text_score.csv',resultant_text_score.to_numpy(),'a')

    ###refactor dataset 2 for linear regressor####
    input_dataset= pd.read_csv("./csv/2_input_dataset.csv")
    estimated_text_score_data = pd.read_csv("./csv/7_resultant_new_text_score.csv")

    ##merge 2 dataset by issue key
    merged_dataset=pd.merge(input_dataset, estimated_text_score_data, on='Issue key')
    merged_dataset.to_csv('./csv/8_merged_datset.csv', encoding='utf-8', mode='w', header=True, index=False)
    input_dataset2=merged_dataset[['Issue key','previous_story_point','estimated_test_score','Number of developers','Number of comments']]
    input_dataset2.to_csv('./csv/9_input_datset2.csv', encoding='utf-8', mode='w', header=True, index=False)

    return accuracy


def e():
  return 4;
