from Train_Vecorize import get_word_root_format,create_document_term_matrix,read_csv_file,write_csv_file,filter_required_columns,refactor_dataset,get_dataset1
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np

def single_prefict_TS(data):
    #read data set from csv
    dataset = read_csv_file('./dataset/data.csv')
    #get only required fields from dataset
    filtered_dataset = filter_required_columns(dataset)
    #write filtered dataset into new csv
    write_csv_file('./csv/Prediction/1_filtered_dataser.csv',filtered_dataset,'w')
    #refactor input dataset as for different inputs
    preData = refactor_dataset(filtered_dataset)
    del preData[0]

    write_csv_file('./csv/SinglePrediction/2_input_dataset.csv', [["Summary", "Description" , "Number of developers","Number of comments","Issue key","Story point"]],'w')

    #refactor input dataset as for different inputs
    preData.insert(0,data)
    preData.insert(1,data)
    input_dataset = preData
    
    #write dataset in input format
    
    write_csv_file('./csv/SinglePrediction/2_input_dataset.csv', input_dataset,'a')

    #write title bar of input dataset1
    write_csv_file('./csv/SinglePrediction/3_input_dataset1.csv', [["Bug text", "issue key" , "Story point"]],'w')

    #delete title bar from input_dataset
    del input_dataset[0]

    word_stem_string=[["Bug text root form", "issue key", "Story point"]]

    #consider only one bug at once
    for bug in input_dataset:
        #get textual data from a bug-> bug set1=Bug text,Story point
        bug_set1 = get_dataset1(bug)
        #write bug set1 in 3_input_dataset1.csv
        write_csv_file('./csv/SinglePrediction/3_input_dataset1.csv', [bug_set1], 'a')

        #get word list in root format (stem)
        word_stem_string.append([get_word_root_format(bug_set1[0]),bug_set1[1],bug_set1[2]])

    #write title bar of input dataset1 root form
    write_csv_file('./csv/SinglePrediction/4_input_dataset1_rootform.csv', word_stem_string,'w')


    bug_text_list=[]
    issue_key_list=[]
    story_point_list=[]
    for bug in word_stem_string:
        bug_text_list.append(bug[0])
        issue_key_list.append(bug[1])
        story_point_list.append(bug[2])

    #genarate and write tfidf values to corpus
    term_matrix=create_document_term_matrix(bug_text_list)

    #adding issue kely, storypoint column to matrix
    term_matrix["issue_key"]=issue_key_list
    term_matrix["story_point"]=story_point_list

    #remove first row( title values) and save as csv
    term_matrix.drop(term_matrix.index[0]).to_csv (r'./csv/SinglePrediction/5_tfidf_for_corpus.csv', index = False, header=True)

    ####text score prediction
    sc = StandardScaler()

    ###read tf-idf value metrix from here
    tfidf_value_matrix = pd.read_csv('./csv/SinglePrediction/5_tfidf_for_corpus.csv')
    number_of_columns = len(tfidf_value_matrix.columns)

    ###input fit to the model
    Existing_text_features=sc.fit_transform(tfidf_value_matrix.iloc[:, 0:number_of_columns-2].values)

    ###load saved model
    regressorModel = pickle.load(open('./Models/RandomForestModel.sav', 'rb'))
    text_score = regressorModel.predict(Existing_text_features)

    #add new colums to write new values
    tfidf_value_matrix["test_score"]=text_score
    tfidf_value_matrix["test_score_round"]=np.rint(text_score)

    ##store predicted values
    write_csv_file('./csv/SinglePrediction/6_estimated_new_text_score.csv',tfidf_value_matrix.to_numpy(),'w')

    ##save resultant format
    resultant_text_score = tfidf_value_matrix[['issue_key','story_point','test_score', 'test_score_round']]
    write_csv_file('./csv/SinglePrediction/7_resultant_new_text_score.csv',[['Issue key','previous_story_point','estimated_test_score', 'text_score_rounded']],'w')
    write_csv_file('./csv/SinglePrediction/7_resultant_new_text_score.csv',resultant_text_score.to_numpy(),'a')

    ###refactor dataset 2 for linear regressor####
    input_dataset= pd.read_csv("./csv/SinglePrediction/2_input_dataset.csv")
    estimated_text_score_data = pd.read_csv("./csv/SinglePrediction/7_resultant_new_text_score.csv")

    ##merge 2 dataset by issue key
    merged_dataset=pd.merge(input_dataset, estimated_text_score_data, on='Issue key')
    merged_dataset.to_csv('./csv/SinglePrediction/8_merged_datset.csv', encoding='utf-8', mode='w', header=True, index=False)
    input_dataset2=merged_dataset[['Issue key','previous_story_point','estimated_test_score','Number of developers','Number of comments']]
    input_dataset2.to_csv('./csv/SinglePrediction/9_input_datset2.csv', encoding='utf-8', mode='w', header=True, index=False)
    
import Train_Vecorize